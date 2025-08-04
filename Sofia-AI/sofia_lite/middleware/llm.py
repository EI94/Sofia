import openai, json, functools, asyncio, logging, tenacity
from typing import Tuple
from .. import get_config
from .latency import track_latency
from .http_session import get_session

log = logging.getLogger("sofia.llm")

# Initialize OpenAI client with error handling
_CLIENT = None
_SEMAPHORE = asyncio.Semaphore(5)  # Max 5 concurrent calls
_CACHE = {}  # Simple in-memory cache

# Circuit breaker state
_CIRCUIT = {"fail": 0, "open_until": 0}  # naïve CB
_CB_TIMEOUT = 60  # sec

async def _get_client():
    """Get OpenAI client with HTTP session reuse - Δmini optimization"""
    global _CLIENT
    if _CLIENT is None:
        try:
            cfg = get_config()
            api_key = cfg["OPENAI_KEY"]
            if not api_key:
                raise RuntimeError("missing OPENAI_API_KEY")
            
            # Reuse HTTP session for better performance
            session = await get_session()
            _CLIENT = openai.OpenAI(
                api_key=api_key,
                http_client=session._client  # Reuse aiohttp session
            )
        except Exception as e:
            print(f"⚠️ OpenAI client initialization failed: {e}")
            raise RuntimeError("missing OPENAI_API_KEY")
    return _CLIENT

def _cache_key(func_name: str, *args) -> str:
    """Generate cache key for function calls"""
    return f"{func_name}:{hash(str(args))}"

def _get_cached(key: str, ttl: int = 30) -> any:
    """Get cached value if not expired"""
    import time
    if key in _CACHE:
        value, timestamp = _CACHE[key]
        if time.time() - timestamp < ttl:
            return value
        else:
            del _CACHE[key]
    return None

def _set_cached(key: str, value: any):
    """Set cached value with timestamp"""
    import time
    _CACHE[key] = (value, time.time())

_SYS = ("Return ONLY JSON: "
        '{"intent":"<INTENT>","confidence":<0-1>}  '
        "INTENT=GREET,ASK_NAME,ASK_SERVICE,PROPOSE_CONSULT,"
        "ASK_CHANNEL,ASK_SLOT,ASK_PAYMENT,CONFIRM,ROUTE_ACTIVE,CLARIFY,ABUSE.")

@functools.lru_cache(maxsize=2048)
async def classify(msg: str, lang="it") -> Tuple[str, float]:
    """Classify intent with TTL 5 min cache - Δmini optimization"""
    # Check cache first
    cache_key = _cache_key("classify", msg, lang)
    cached_result = _get_cached(cache_key, ttl=30)
    if cached_result:
        return cached_result
    
    client = await _get_client()
    
    try:
        # Δmini optimization: Compact prompts & token budget
        max_tokens = 24  # Reduced for intents/greet/ask-XXX
        if "PROPOSE_CONSULT" in _SYS or "ASK_PAYMENT" in _SYS:
            max_tokens = 48  # Keep 48 only for complex intents
        
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role":"user","content":f"{_SYS}\nUser({lang}): {msg}"}],
            timeout=12.0,  # 12 second timeout - F22 voice transcription support
            max_tokens=max_tokens,  # Dynamic token budget - Δmini optimization
            stream=True  # Enable streaming - Δmini optimization
        )
        data = json.loads(chat.choices[0].message.content)
        result = (data["intent"], float(data["confidence"]))
        
        # Cache the result
        _set_cached(cache_key, result)
        return result
        
    except Exception as e:
        raise RuntimeError(f"LLM classification failed: {e}")

@track_latency("LLM")
def _raw_chat(sys_prompt: str, user_prompt: str) -> str:
    """For skill replies (slow path, full ParaHelp)."""
    log.info(f"🤖 LLM CHAT: Starting with user_prompt='{user_prompt[:100]}...'")
    log.info(f"📋 System prompt preview: {sys_prompt[:200]}...")
    
    # Check cache first
    cache_key = _cache_key("chat", sys_prompt, user_prompt)
    cached_result = _get_cached(cache_key, ttl=30)
    if cached_result:
        log.info(f"💾 Using cached result: {cached_result[:100]}...")
        return cached_result
    
    client = _get_client()
    
    try:
        log.info(f"🚀 Making OpenAI API call...")
        # Δmini optimization: Compact prompts & token budget
        max_tokens = 24  # Reduced for intents/greet/ask-XXX
        if "PROPOSE_CONSULT" in sys_prompt or "ASK_PAYMENT" in sys_prompt:
            max_tokens = 48  # Keep 48 only for complex intents
        
        rsp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[{"role":"system","content":sys_prompt},
                      {"role":"user","content":user_prompt}],
            timeout=12.0,  # 12 second timeout - F22 voice transcription support
            max_tokens=max_tokens,  # Dynamic token budget - Δmini optimization
            stream=True  # Enable streaming - γ5 optimization
        )
        result = rsp.choices[0].message.content.strip()
        
        log.info(f"✅ LLM Response: {result[:100]}...")
        
        # Cache the result
        _set_cached(cache_key, result)
        return result
        
    except Exception as e:
        raise RuntimeError(f"LLM chat failed: {e}")

def _fallback(messages) -> str:
    """Fallback response when LLM fails"""
    # Simple fallback based on intent detection
    try:
        from ..agents.planner import _classify_with_similarity
        user_msg = messages[-1]["content"] if messages else "Ciao"
        intent, confidence = _classify_with_similarity(user_msg)
        
        if intent == "GREET":
            return "Ciao! Sono Sofia di Studio Immigrato. Come ti chiami?"
        elif intent == "ASK_NAME":
            return "Per favore, dimmi il tuo nome."
        elif intent == "ASK_SERVICE":
            return "Di che servizio hai bisogno? Posso aiutarti con pratiche immigrazione."
        else:
            return "Mi dispiace, non ho capito. Puoi ripetere?"
    except Exception as e:
        log.error(f"❌ Fallback failed: {e}")
        return "Mi dispiace, c'è stato un errore. Riprova tra qualche minuto."

def chat(sys_prompt: str, user_prompt: str) -> str:
    """Circuit breaker wrapper for LLM chat (synchronous for compatibility)"""
    import time
    now = time.time()
    if _CIRCUIT["open_until"] > now:
        log.warning("LLM CB OPEN – serving fallback")
        return _fallback([{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}])

    try:
        rsp = _raw_chat(sys_prompt, user_prompt)
        _CIRCUIT["fail"] = 0
        return rsp
    except Exception as e:
        _CIRCUIT["fail"] += 1
        if _CIRCUIT["fail"] >= 3:
            _CIRCUIT["open_until"] = now + _CB_TIMEOUT
        log.error("LLM failure %s – using fallback", e)
        return _fallback([{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}]) 