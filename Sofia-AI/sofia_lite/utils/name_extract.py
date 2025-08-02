"""
Sofia Lite - Multilingual Name Extraction
Extracts names from user messages in 9 languages using regex and LLM fallback.
"""

import re
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# Simple regex for names (letters, apostrophes, hyphens)
NAME_PATTERN = re.compile(r'[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ]', re.UNICODE)

# Language-specific patterns for name extraction
NAME_PATTERNS: Dict[str, List[str]] = {
    "it": [
        r"(?:mi chiamo|sono)\s+([a-zA-ZÀ-ÿ\s\'-]{2,})",
    ],
    "en": [
        r"(?:my name is|i'm|i am)\s+([a-zA-ZÀ-ÿ\s\'-]{2,})",
    ],
    "fr": [
        r"(?:je m'appelle|je suis)\s+([a-zA-ZÀ-ÿ\s\'-]{2,})",
    ],
    "es": [
        r"(?:me llamo|soy)\s+([a-zA-ZÀ-ÿ\s\'-]{2,})",
    ],
    "ar": [
        r"(?:اسمي|أنا)\s+([\u0600-\u06FF\s\'-]{2,})",  # Arabic Unicode range
    ],
    "hi": [
        r"(?:मेरा नाम|मैं)\s+([\u0900-\u097F\s\'-]{2,})",  # Hindi Unicode range
    ],
    "ur": [
        r"(?:میرا نام|میں)\s+([\u0600-\u06FF\s\'-]{2,})",  # Urdu uses Arabic script
    ],
    "bn": [
        r"(?:আমার নাম|আমি)\s+([\u0980-\u09FF\s\'-]{2,})",  # Bengali Unicode range
    ],
    "wo": [
        r"(?:sama bopp ma|man)\s+([a-zA-ZÀ-ÿ\s\'-]{2,})",
    ],
}

def extract_name_regex(text: str, lang: str = "it") -> Optional[str]:
    """Extract name using regex patterns for the specified language."""
    if lang not in NAME_PATTERNS:
        lang = "it"
    
    text_lower = text.lower().strip()
    
    for pattern in NAME_PATTERNS[lang]:
        match = re.search(pattern, text_lower, re.UNICODE | re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) >= 2 and NAME_PATTERN.match(name):
                logger.info(f"✅ Name extracted via regex: {name} (lang: {lang})")
                return name.title()
    
    return None

def extract_name(text: str, ctx) -> Optional[str]:
    """Extract name from text using regex first, then LLM fallback."""
    if not text or len(text.strip()) < 2:
        return None
    
    # Try regex first
    name = extract_name_regex(text, ctx.lang)
    if name:
        return name
    
    return None

def clean_name(name: str) -> str:
    """Clean and normalize extracted name."""
    if not name:
        return ""
    
    name = re.sub(r'\s+', ' ', name.strip())
    # Support Unicode characters for all languages
    name = re.sub(r'[^a-zA-ZÀ-ÿ\u0600-\u06FF\u0900-\u097F\u0980-\u09FF\s\'-]', '', name, flags=re.UNICODE)
    name = name.title()
    
    return name
