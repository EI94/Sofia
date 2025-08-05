"""
Sofia Lite - Multilingual Name Extraction
Extracts names from user messages in 9 languages using regex and LLM fallback.
"""

import re
import logging
from typing import Optional, Dict, List
from ..middleware.llm import chat
from ..agents.prompt_builder import build_system_prompt
from ..agents.context import Context

logger = logging.getLogger(__name__)

# Simple regex for names (letters, apostrophes, hyphens, spaces)
NAME_PATTERN = re.compile(r'[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ]', re.UNICODE)

# Language-specific patterns for name extraction
NAME_PATTERNS: Dict[str, List[str]] = {
    "it": [
        r"mi chiamo\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"sono\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
    ],
    "en": [
        r"my name is\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"i'm\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"i am\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"call me\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
    ],
    "fr": [
        r"je m'appelle\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"je suis\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"mon nom est\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
    ],
    "es": [
        r"me llamo\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"soy\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"mi nombre es\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
    ],
    "ar": [
        r"أنا\s+([\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+)",
        r"اسمي\s+([\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+)",
        r"أدعى\s+([\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+)",
    ],
    "hi": [
        r"मेरा नाम\s+([\u0900-\u097F]+)",
        r"मैं\s+([\u0900-\u097F]+)",
        r"मुझे\s+([\u0900-\u097F]+)\s+कहते हैं",
    ],
    "ur": [
        r"میرا نام\s+([\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+)",
        r"میں\s+([\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+)",
    ],
    "bn": [
        r"আমার নাম\s+([\u0980-\u09FF]+)",
        r"আমি\s+([\u0980-\u09FF]+)",
    ],
    "wo": [
        r"ma tudd\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
        r"ma\s+([a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s\'-]*[a-zA-ZÀ-ÿ])",
    ]
}

def extract_name_regex(text: str, lang: str = "it") -> Optional[str]:
    """
    Extract name using regex patterns for the specified language.
    
    Args:
        text: Input text to extract name from
        lang: Language code (it, en, fr, es, ar, hi, ur, bn, wo)
        
    Returns:
        Extracted name or None if not found
    """
    if lang not in NAME_PATTERNS:
        lang = "it"  # Fallback to Italian
    
    text_lower = text.lower().strip()
    
    for pattern in NAME_PATTERNS[lang]:
        match = re.search(pattern, text_lower, re.UNICODE | re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Validate that it looks like a name
            if len(name) >= 2 and NAME_PATTERN.match(name):
                logger.info(f"✅ Name extracted via regex: {name} (lang: {lang})")
                return name.title()  # Capitalize properly
    
    return None

def extract_name_llm(text: str, ctx: Context) -> Optional[str]:
    """
    Extract name using LLM when regex fails.
    
    Args:
        text: Input text to extract name from
        ctx: Conversation context
        
    Returns:
        Extracted name or None if not found
    """
    try:
        system_prompt = build_system_prompt(ctx)
        extraction_prompt = f"""
Extract ONLY the person's name from this text. Return ONLY the name, nothing else.
If no name is found, return "NONE".

Text: "{text}"
Name:"""

        response = chat(system_prompt, extraction_prompt)
        name = response.strip()
        
        # Validate response
        if name and name.lower() != "none" and len(name) >= 2:
            # Clean up the name
            name = re.sub(r'[^a-zA-ZÀ-ÿ\s\'-]', '', name, flags=re.UNICODE)
            if name:
                logger.info(f"✅ Name extracted via LLM: {name}")
                return name.title()
        
        logger.warning(f"❌ LLM extraction failed for: {text}")
        return None
        
    except Exception as e:
        logger.error(f"❌ LLM extraction error: {e}")
        return None

def extract_name(text: str, ctx: Context) -> Optional[str]:
    """
    Extract name from text using regex first, then LLM fallback.
    
    Args:
        text: Input text to extract name from
        ctx: Conversation context
        
    Returns:
        Extracted name or None if not found
    """
    if not text or len(text.strip()) < 2:
        return None
    
    # Try regex first (faster and more reliable)
    name = extract_name_regex(text, ctx.lang)
    if name:
        return name
    
    # Fallback to LLM
    name = extract_name_llm(text, ctx)
    return name

def clean_name(name: str) -> str:
    """
    Clean and normalize extracted name.
    
    Args:
        name: Raw extracted name
        
    Returns:
        Cleaned name
    """
    if not name:
        return ""
    
    # Remove extra whitespace and normalize
    name = re.sub(r'\s+', ' ', name.strip())
    
    # Remove non-name characters but keep letters, apostrophes, hyphens, spaces
    name = re.sub(r'[^a-zA-ZÀ-ÿ\s\'-]', '', name, flags=re.UNICODE)
    
    # Title case (first letter of each word capitalized)
    name = name.title()
    
    return name 