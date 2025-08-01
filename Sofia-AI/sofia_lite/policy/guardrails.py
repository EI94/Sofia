import re
from .language_support import T

# Simple abuse detection patterns
ABUSE_PATTERNS = [
    r'\b(fuck|shit|bitch|asshole|dick|pussy|cunt)\b',
    r'\b(merda|cazzo|stronzo|puttana|troia|vaffanculo)\b',
    r'\b(putain|merde|con|salope|enculé)\b',
    r'\b(mierda|puta|cabrón|gilipollas|joder)\b',
    r'\b(كسم|زبي|شرموطة|عرص|خول)\b',
    r'\b(चूत|मादरचोद|भेंस|गांड|लंड)\b',
    r'\b(چوت|مادرجنده|کیر|کص|گه)\b',
    r'\b(চুত|মাদারচোদ|ভেঁস|গাঁড়|লন্ড)\b',
    r'\b(ndey|yéex|dafa|dégg)\b'
]

def is_abusive(text: str) -> bool:
    """Check if text contains abusive language"""
    text_lower = text.lower()
    
    for pattern in ABUSE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    
    return False

def close_message(lang: str) -> str:
    """Return abuse close message in specified language"""
    return T("abuse_close", lang) 