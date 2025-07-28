import json
import os
from typing import Dict, List

# Load exclusions from config file
def load_exclusions() -> Dict[str, List[str]]:
    """Load exclusions from config/exclusions.json"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'exclusions.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty exclusions if file not found
        return {}
    except json.JSONDecodeError:
        # Return empty exclusions if JSON is invalid
        return {}

# Cache exclusions
_EXCLUSIONS = load_exclusions()

def is_excluded(text: str, lang: str) -> bool:
    """Check if text is in exclusions for language"""
    if lang not in _EXCLUSIONS:
        return False
    
    text_lower = text.lower()
    exclusions = _EXCLUSIONS[lang]
    
    for exclusion in exclusions:
        if exclusion.lower() in text_lower:
            return True
    
    return False 