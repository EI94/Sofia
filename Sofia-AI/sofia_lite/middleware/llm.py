import openai, os, json, functools
from typing import Tuple

# Initialize OpenAI client with error handling
_CLIENT = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        _CLIENT = openai.OpenAI(api_key=api_key)
    else:
        print("⚠️ OPENAI_API_KEY not set, LLM will return fallback responses")
except Exception as e:
    print(f"⚠️ OpenAI client initialization failed: {e}")

_SYS = ("Return ONLY JSON: "
        '{"intent":"<INTENT>","confidence":<0-1>}  '
        "INTENT=GREET,ASK_NAME,ASK_SERVICE,PROPOSE_CONSULT,"
        "ASK_CHANNEL,ASK_SLOT,ASK_PAYMENT,CONFIRM,ROUTE_ACTIVE,CLARIFY,ABUSE.")

@functools.lru_cache(maxsize=2048)
def classify(msg: str, lang="it") -> Tuple[str, float]:
    if not _CLIENT:
        return "CLARIFY", 0.0
    
    try:
        chat = _CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role":"user","content":f"{_SYS}\nUser({lang}): {msg}"}],
        )
        data = json.loads(chat.choices[0].message.content)
        return data["intent"], float(data["confidence"])
    except Exception:
        return "CLARIFY", 0.0

def chat(sys_prompt: str, user_prompt: str) -> str:
    """For skill replies (slow path, full ParaHelp)."""
    if not _CLIENT:
        return "Mi dispiace, il servizio non è disponibile al momento."
    
    try:
        rsp = _CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[{"role":"system","content":sys_prompt},
                      {"role":"user","content":user_prompt}],
        )
        return rsp.choices[0].message.content.strip()
    except Exception:
        return "Mi dispiace, c'è stato un errore tecnico." 