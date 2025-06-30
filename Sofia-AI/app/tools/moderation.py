from openai import OpenAI
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Solo categorie veramente problematiche, non semplice frustrazione
SERIOUS_ABUSE_CATEGORIES = {"hate", "violence"}

@lru_cache(maxsize=1024)
def _cached_moderation(text: str):
    return client.moderations.create(model="text-moderation-latest", input=text)

async def is_abusive(text: str) -> bool:
    """
    Moderazione meno aggressiva - blocca solo hate speech e violenza vera,
    permette frustrazione normale come "che cazzo dici"
    """
    try:
        resp = _cached_moderation(text)
        flags = {k for k, v in resp.results[0].categories.model_dump().items() if v}
        
        # Blocca solo categorie serie, ignora harassment semplice
        serious_flags = flags & SERIOUS_ABUSE_CATEGORIES
        
        # Se è solo harassment/sexual senza hate/violence, controllo ulteriormente
        if "harassment" in flags and not serious_flags:
            # Permetti espressioni di frustrazione comuni
            frustration_words = ["cazzo", "merda", "stronz", "fottut", "damn", "shit", "fuck"]
            if any(word in text.lower() for word in frustration_words):
                return False  # Non è abuso, è solo frustrazione
        
        return bool(serious_flags)
        
    except Exception as e:
        # Se c'è errore nell'API, permetti il messaggio (fail-safe)
        return False 