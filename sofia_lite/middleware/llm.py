import functools
import json
from typing import Tuple

import openai

from .. import get_config

# Lazy client initialization
_CLIENT = None


def _get_client():
    """Get or create OpenAI client"""
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


_SYS = (
    "Return ONLY JSON: "
    '{"intent":"<INTENT>","confidence":<0-1>}  '
    "INTENT=GREET,ASK_NAME,ASK_SERVICE,PROPOSE_CONSULT,"
    "ASK_CHANNEL,ASK_SLOT,ASK_PAYMENT,CONFIRM,ROUTE_ACTIVE,CLARIFY,ABUSE."
)


@functools.lru_cache(maxsize=2048)
def classify(msg: str, lang="it") -> Tuple[str, float]:
    client = _get_client()

    try:
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role": "user", "content": f"{_SYS}\nUser({lang}): {msg}"}],
        )
        data = json.loads(chat.choices[0].message.content)
        return data["intent"], float(data["confidence"])
    except Exception as e:
        raise RuntimeError(f"LLM classification failed: {e}")


def chat(sys_prompt: str, user_prompt: str) -> str:
    """For skill replies (slow path, full ParaHelp)."""
    client = _get_client()

    try:
        rsp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return rsp.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"LLM chat failed: {e}")
