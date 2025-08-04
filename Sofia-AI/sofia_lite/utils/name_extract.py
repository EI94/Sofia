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
        r"\b(?:sono|mi chiamo|il mio nome è)\s+([A-ZÀ-ÖØ-Ýa-zà-öø-ý\s\'-]+)",
        r"\b(?:mi chiamo|sono)\s+([A-ZÀ-ÖØ-Ýa-zà-öø-ý\s\'-]+)",
    ],
    "en": [
        r"\b(?:i'm called)\s+([A-Za-z\s\'-]+)",
        r"\b(?:my name is|i am)\s+([A-Za-z\s\'-]+)",
        r"\b(?:i'm)\s+([A-Za-z\s\'-]+)",
    ],
    "fr": [
        r"\b(?:je m'appelle|je suis|mon nom est)\s+([A-ZÂÊÎÔÛÄËÏÖÜŸÇa-zâêîôûäëïöüÿç\s\'-]+)",
        r"\b(?:je m'appelle|je suis)\s+([A-ZÂÊÎÔÛÄËÏÖÜŸÇa-zâêîôûäëïöüÿç\s\'-]+)",
    ],
    "es": [
        r"\b(?:soy|me llamo|mi nombre es)\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s\'-]+)",
        r"\b(?:me llamo|soy)\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s\'-]+)",
    ],
    "ar": [
        r"\b(?:اسمي|أنا)\s+([\u0600-\u06FF\s\'-]+)",  # Arabic Unicode range
    ],
    "hi": [
        r"\b(?:मेरा नाम|मैं)\s+([\u0900-\u097F\s\'-]+)",  # Hindi Unicode range
    ],
    "ur": [
        r"\b(?:میرا نام|میں)\s+([\u0600-\u06FF\s\'-]+)",  # Urdu uses Arabic script
    ],
    "bn": [
        r"\b(?:আমার নাম|আমি)\s+([\u0980-\u09FF\s\'-]+)",  # Bengali Unicode range
    ],
    "wo": [
        r"\b(?:sama bopp ma|man)\s+([A-Za-z\s\'-]+)",
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
            if len(name) >= 2:
                # Capitalize correctly
                name = clean_name(name)
                logger.info(f"✅ Name extracted via regex: {name} (lang: {lang})")
                return name
    
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
    
    # Remove numbers first
    name = re.sub(r'[0-9]', '', name)
    
    # Advanced cleaning: replace special characters with spaces to preserve word boundaries
    # This ensures "Mario@Rossi" becomes "Mario Rossi" instead of "Mariorossi"
    name = re.sub(r'[^a-zA-ZÀ-ÿ\u0600-\u06FF\u0900-\u097F\u0980-\u09FF\s\'-]', ' ', name, flags=re.UNICODE)
    
    # Normalize spaces (multiple spaces become single space)
    name = re.sub(r'\s+', ' ', name.strip())
    name = name.title()
    
    return name
