"""
Utilità per rilevamento lingua usando LangChain LCEL.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

logger = logging.getLogger(__name__)


def detect_language(text: str, llm: ChatOpenAI = None) -> str:
    """
    Rileva la lingua del testo usando LangChain LCEL chain.
    
    Args:
        text: Testo da analizzare
        llm: Modello ChatOpenAI
    
    Returns:
        str: Codice ISO della lingua rilevata tra [it,en,fr,es,ar,hi,ur,bn,wo]
    """
    if not llm:
        return "it"  # Default italiano se modello non disponibile
    
    try:
        # Prompt per rilevamento lingua con lista specifica
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a language detection expert. Detect the language of the given text and return ONLY the ISO language code."),
            ("human", """Detect the language ISO code of this text. Choose ONLY from these options:
            [it, en, fr, es, ar, hi, ur, bn, wo]
            
            Text: {text}
            
            Return only the language code, nothing else.""")
        ])
        
        # Output parser per stringa
        output_parser = StrOutputParser()
        
        # LCEL Chain usando pipe operator
        chain = prompt | llm | output_parser
        
        # Esegui la chain
        response = chain.invoke({"text": text})
        
        # Valida il codice lingua
        valid_languages = ['it', 'en', 'fr', 'es', 'ar', 'hi', 'ur', 'bn', 'wo']
        lang_code = response.strip().lower()
        
        if lang_code in valid_languages:
            logger.info(f"Lingua rilevata: {lang_code} per testo: '{text[:50]}...'")
            return lang_code
        
        logger.warning(f"Codice lingua non valido: {lang_code}, uso default 'it'")
        return "it"  # Default se non riconosciuto
        
    except Exception as e:
        logger.error(f"Errore rilevamento lingua: {e}")
        return "it"


# Esempio di utilizzo
if __name__ == "__main__":
    from langchain_openai import ChatOpenAI
    import os
    
    # Test della funzione
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.1,
        model="gpt-3.5-turbo"
    )
    
    test_texts = [
        "Ciao, come stai?",  # Italiano
        "Hello, how are you?",  # Inglese
        "Bonjour, comment ça va?",  # Francese
        "Hola, ¿cómo estás?",  # Spagnolo
        "مرحبا، كيف حالك؟",  # Arabo
    ]
    
    for text in test_texts:
        detected = detect_language(text, llm)
        print(f"Testo: '{text}' -> Lingua: {detected}") 