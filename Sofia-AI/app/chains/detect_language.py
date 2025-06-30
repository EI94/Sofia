"""
LangChain LCEL chain per rilevamento lingua con Regex output parser.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
import logging

logger = logging.getLogger(__name__)


def detect_language(text: str, llm: ChatOpenAI = None) -> str:
    """
    Rileva la lingua del testo usando LangChain LCEL chain con Regex output parser.
    
    Args:
        text: Testo da analizzare
        llm: Modello ChatOpenAI (opzionale)
    
    Returns:
        str: Codice ISO della lingua rilevata tra [it,en,fr,es,ar,hi,ur,bn,wo]
    """
    if not llm:
        return "en"  # Default inglese se modello non disponibile
    
    # Fix rapido per parole inglesi comuni
    english_words = ["hi", "hello", "how", "are", "you", "what", "where", "when", "why", "who"]
    if text.lower().strip() in english_words:
        return "en"
    
    try:
        # Prompt template per rilevamento lingua migliorato
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""Detect the language of this text and return ONLY the ISO code.

Available languages: it (Italian), en (English), fr (French), es (Spanish), ar (Arabic), hi (Hindi), ur (Urdu), bn (Bengali), wo (Wolof)

IMPORTANT: 
- "Hi" = English (en)
- "Ciao" = Italian (it) 
- "Hello" = English (en)

Text: {text}

ISO Code:"""
        )
        
        # String output parser
        output_parser = StrOutputParser()
        
        # LCEL Chain usando pipe operator
        chain = prompt | llm | output_parser
        
        # Esegui la chain
        result = chain.invoke({"text": text})
        
        # Estrai il codice lingua usando regex più preciso
        match = re.search(r"\b(it|en|fr|es|ar|hi|ur|bn|wo)\b", result.lower())
        lang_code = match.group(1) if match else "en"
        
        # Extra fix: se risulta "hi" ma il testo è "Hi", forza inglese
        if lang_code == "hi" and text.lower().strip() == "hi":
            lang_code = "en"
        
        logger.info(f"Lingua rilevata: {lang_code} per testo: '{text[:50]}...'")
        return lang_code
        
    except Exception as e:
        logger.error(f"Errore rilevamento lingua: {e}")
        return "en"  # Default inglese se errore 