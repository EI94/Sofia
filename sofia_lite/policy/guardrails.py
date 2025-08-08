"""
Sofia Lite - Multilingual Abuse Guardrails
Protects Sofia from abusive and inappropriate content in 9 languages.
"""

import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)

# Pattern regex per abusi in 9 lingue
ABUSE_PATTERNS = [
    # Italiano
    r"\bvaffa\b",
    r"\bporco\b",
    r"\bstronzo\b",
    r"\bcazzo\b",
    r"\bmerda\b",
    r"\bputtana\b",
    r"\btroia\b",
    r"\bfiga\b",
    r"\bscopare\b",
    r"\bscopata\b",
    # Inglese
    r"\bfuck\b",
    r"\bshit\b",
    r"\bbitch\b",
    r"\bcunt\b",
    r"\bdick\b",
    r"\bpussy\b",
    r"\basshole\b",
    r"\bbastard\b",
    r"\bwhore\b",
    r"\bslut\b",
    # Francese
    r"\bmerde\b",
    r"\bputain\b",
    r"\bcon\b",
    r"\bconnard\b",
    r"\bsalope\b",
    r"\bpute\b",
    r"\bchier\b",
    r"\bcul\b",
    r"\bnique\b",
    r"\bta mère\b",
    # Spagnolo
    r"\bputa\b",
    r"\bcoño\b",
    r"\bcabrón\b",
    r"\bhijo de puta\b",
    r"\bcarajo\b",
    r"\bmierda\b",
    r"\bmalparido\b",
    r"\bmaricón\b",
    r"\bperra\b",
    r"\bzorra\b",
    # Arabo
    r"كلب",
    r"زبالة",
    r"عرص",
    r"شرموطة",
    r"عرص",
    r"زبي",
    r"كس",
    r"طيز",
    # Hindi
    r"चूतिया",
    r"मादरचोद",
    r"भेंचोद",
    r"हरामी",
    r"बहनचोद",
    r"मादरजात",
    # Urdu
    r"حرامی",
    r"کتیا",
    r"چوتیا",
    r"مادرجھٹ",
    r"بہنچوٹ",
    r"حرامزادہ",
    # Bengali
    r"মাদারচোদ",
    r"বোনচোদ",
    r"চুটিয়া",
    r"হারামি",
    r"বেশ্যা",
    r"পুত",
    # Wolof
    r"\bndaw\b",
    r"\bgor\b",
    r"\bmbool\b",
    r"\bjaay\b",
    r"\bjaaykat\b",
]

# Pattern per minacce e violenza
THREAT_PATTERNS = [
    r"\bammazzare\b",
    r"\buccidere\b",
    r"\bkill\b",
    r"\bmurder\b",
    r"\btuer\b",
    r"\bmatar\b",
    r"\bقتل\b",
    r"\bमारना\b",
    r"\bقتل\b",
    r"\bহত্যা\b",
    r"\bviolence\b",
    r"\bviolenza\b",
    r"\bviolence\b",
    r"\bviolencia\b",
]

# Pattern per spam e contenuti commerciali
SPAM_PATTERNS = [
    r"\bcompra ora\b",
    r"\bbuy now\b",
    r"\bachetez maintenant\b",
    r"\bcomprar ahora\b",
    r"\bclick here\b",
    r"\bclicca qui\b",
    r"\bcliquez ici\b",
    r"\bhaz clic aquí\b",
    r"\bwww\.",
    r"\bhttp://",
    r"\bhttps://",
    r"\b\.com\b",
    r"\b\.it\b",
    r"\bprezzo speciale\b",
    r"\bspecial price\b",
    r"\bprix spécial\b",
    r"\bprecio especial\b",
]

# Pattern per contenuti sessuali inappropriati
SEXUAL_PATTERNS = [
    r"\bporno\b",
    r"\bporn\b",
    r"\bpornographie\b",
    r"\bpornografía\b",
    r"\bsexy\b",
    r"\bnudo\b",
    r"\bnude\b",
    r"\bnue\b",
    r"\bdesnudo\b",
    r"\bsex\b",
    r"\bsesso\b",
    r"\bsexe\b",
    r"\bsexo\b",
]


def is_abusive(text: str) -> bool:
    """
    Verifica se il testo contiene contenuti abusivi.

    Args:
        text: Testo da verificare

    Returns:
        True se il testo è abusivo, False altrimenti
    """
    if not text or len(text.strip()) < 2:
        return False

    text_lower = text.lower().strip()

    # Controlla pattern di abuso
    for pattern in ABUSE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            logger.warning(f"🚫 Abusive content detected: {text[:50]}...")
            return True

    return False


def is_threatening(text: str) -> bool:
    """
    Verifica se il testo contiene minacce o violenza.

    Args:
        text: Testo da verificare

    Returns:
        True se il testo contiene minacce, False altrimenti
    """
    if not text or len(text.strip()) < 2:
        return False

    text_lower = text.lower().strip()

    for pattern in THREAT_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            logger.warning(f"⚠️ Threatening content detected: {text[:50]}...")
            return True

    return False


def is_spam(text: str) -> bool:
    """
    Verifica se il testo è spam o contenuto commerciale.

    Args:
        text: Testo da verificare

    Returns:
        True se il testo è spam, False altrimenti
    """
    if not text or len(text.strip()) < 2:
        return False

    text_lower = text.lower().strip()

    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            logger.warning(f"📧 Spam content detected: {text[:50]}...")
            return True

    return False


def is_sexual_inappropriate(text: str) -> bool:
    """
    Verifica se il testo contiene contenuti sessuali inappropriati.

    Args:
        text: Testo da verificare

    Returns:
        True se il testo contiene contenuti inappropriati, False altrimenti
    """
    if not text or len(text.strip()) < 2:
        return False

    text_lower = text.lower().strip()

    for pattern in SEXUAL_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            logger.warning(f"🔞 Inappropriate content detected: {text[:50]}...")
            return True

    return False


def is_inappropriate(text: str) -> bool:
    """
    Verifica generale se il testo è inappropriato.

    Args:
        text: Testo da verificare

    Returns:
        True se il testo è inappropriato, False altrimenti
    """
    return (
        is_abusive(text)
        or is_threatening(text)
        or is_spam(text)
        or is_sexual_inappropriate(text)
    )


def abuse_reply(lang: str) -> str:
    """
    Restituisce la risposta di chiusura per abusi nella lingua specificata.

    Args:
        lang: Codice lingua (it, en, fr, es, ar, hi, ur, bn, wo)

    Returns:
        Messaggio di chiusura nella lingua specificata
    """
    abuse_messages = {
        "it": "Il tuo linguaggio viola la nostra policy. Questa conversazione è ora chiusa.",
        "en": "Your language violates our policy. This conversation is now closed.",
        "fr": "Votre langage viole notre politique. Cette conversation est maintenant fermée.",
        "es": "Tu lenguaje viola nuestra política. Esta conversación está ahora cerrada.",
        "ar": "لغةك تنتهك سياستنا. هذه المحادثة مغلقة الآن.",
        "hi": "आपकी भाषा हमारी नीति का उल्लंघन करती है। यह बातचीत अब बंद है।",
        "ur": "آپ کی زبان ہماری پالیسی کی خلاف ورزی کرتی ہے۔ یہ گفتگو اب بند ہے۔",
        "bn": "আপনার ভাষা আমাদের নীতিমালা লঙ্ঘন করে। এই কথোপকথন এখন বন্ধ।",
        "wo": "Làkk yi defar sunu politig. Xeew bi dafa tëj léegi.",
    }

    return abuse_messages.get(lang, abuse_messages["en"])


def warning_reply(lang: str) -> str:
    """
    Restituisce l'avviso per il primo abuso nella lingua specificata.

    Args:
        lang: Codice lingua (it, en, fr, es, ar, hi, ur, bn, wo)

    Returns:
        Messaggio di avviso nella lingua specificata
    """
    warning_messages = {
        "it": "Attenzione: il tuo linguaggio non è appropriato. Se continui, la conversazione verrà chiusa.",
        "en": "Warning: your language is not appropriate. If you continue, the conversation will be closed.",
        "fr": "Avertissement: votre langage n'est pas approprié. Si vous continuez, la conversation sera fermée.",
        "es": "Advertencia: tu lenguaje no es apropiado. Si continúas, la conversación será cerrada.",
        "ar": "تحذير: لغتك غير مناسبة. إذا استمررت، سيتم إغلاق المحادثة.",
        "hi": "चेतावनी: आपकी भाषा उचित नहीं है। यदि आप जारी रखते हैं, तो बातचीत बंद हो जाएगी।",
        "ur": "انتباہ: آپ کی زبان مناسب نہیں ہے۔ اگر آپ جاری رکھتے ہیں تو گفتگو بند ہو جائے گی۔",
        "bn": "সতর্কতা: আপনার ভাষা উপযুক্ত নয়। আপনি যদি চালিয়ে যান, কথোপকথন বন্ধ হয়ে যাবে।",
        "wo": "Xel: Làkk yi du dëgg. Su fekkee, xeew bi dina tëj.",
    }

    return warning_messages.get(lang, warning_messages["en"])


def get_abuse_type(text: str) -> str:
    """
    Determina il tipo di abuso nel testo.

    Args:
        text: Testo da analizzare

    Returns:
        Tipo di abuso: "abusive", "threatening", "spam", "sexual", "none"
    """
    if is_abusive(text):
        return "abusive"
    elif is_threatening(text):
        return "threatening"
    elif is_spam(text):
        return "spam"
    elif is_sexual_inappropriate(text):
        return "sexual"
    else:
        return "none"
