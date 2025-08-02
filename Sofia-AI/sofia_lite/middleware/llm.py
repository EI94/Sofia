import openai, json, functools, asyncio
from typing import Tuple
from .. import get_config

# Initialize OpenAI client with error handling
_CLIENT = None
_SEMAPHORE = asyncio.Semaphore(5)  # Max 5 concurrent calls
_CACHE = {}  # Simple in-memory cache

def _get_client():
    global _CLIENT
    if _CLIENT is None:
        try:
            cfg = get_config()
            api_key = cfg["OPENAI_KEY"]
            if not api_key:
                raise RuntimeError("missing OPENAI_API_KEY")
            _CLIENT = openai.OpenAI(api_key=api_key)
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
def classify(msg: str, lang="it") -> Tuple[str, float]:
    # Check cache first
    cache_key = _cache_key("classify", msg, lang)
    cached_result = _get_cached(cache_key, ttl=30)
    if cached_result:
        return cached_result
    
    client = _get_client()
    
    try:
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role":"user","content":f"{_SYS}\nUser({lang}): {msg}"}],
            timeout=5.0  # 5 second timeout
        )
        data = json.loads(chat.choices[0].message.content)
        result = (data["intent"], float(data["confidence"]))
        
        # Cache the result
        _set_cached(cache_key, result)
        return result
        
    except Exception as e:
        raise RuntimeError(f"LLM classification failed: {e}")

def chat(sys_prompt: str, user_prompt: str) -> str:
    """For skill replies (slow path, full ParaHelp)."""
    # Check cache first
    cache_key = _cache_key("chat", sys_prompt, user_prompt)
    cached_result = _get_cached(cache_key, ttl=30)
    if cached_result:
        return cached_result
    
    client = _get_client()
    
    try:
        rsp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[{"role":"system","content":sys_prompt},
                      {"role":"user","content":user_prompt}],
            timeout=5.0  # 5 second timeout
        )
        result = rsp.choices[0].message.content.strip()
        
        # Cache the result
        _set_cached(cache_key, result)
        return result
        
    except Exception as e:
        raise RuntimeError(f"LLM chat failed: {e}") 