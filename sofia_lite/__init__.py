"""
Sofia Lite - AI Assistant for Studio Immigrato
"""

from functools import lru_cache
import os

@lru_cache
def get_config():
    """
    Centralized configuration loader for Sofia Lite.
    Returns a dictionary with all environment variables and secrets.
    """
    return {
        "OPENAI_KEY": os.getenv("OPENAI_API_KEY", ""),
        "ELEVEN_KEY": os.getenv("ELEVENLABS_API_KEY", ""),
        "GCLOUD_PROJECT": os.getenv("GOOGLE_PROJECT_ID", "local-dev"),
        "TWILIO_SID": os.getenv("TWILIO_ACCOUNT_SID", ""),
        "TWILIO_TOKEN": os.getenv("TWILIO_AUTH_TOKEN", ""),
        "GOOGLE_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    }

def validate_config():
    """
    Validate that all required configuration is present.
    Raises RuntimeError if any required secret is missing.
    """
    config = get_config()
    required_keys = ["OPENAI_KEY", "GCLOUD_PROJECT"]
    
    missing_keys = []
    for key in required_keys:
        if not config[key]:
            missing_keys.append(key)
    
    if missing_keys:
        missing_str = ", ".join(missing_keys)
        raise RuntimeError(f"Missing required configuration: {missing_str}")
    
    return config

# Don't validate config on import - only when explicitly called
# validate_config() 