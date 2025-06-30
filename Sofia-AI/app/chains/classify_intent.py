from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import re
import asyncio

_prompt = PromptTemplate.from_template(
    "Classify the user message into one of these intents: prenotazione, richiesta informazioni, reclamo, saluto, spam, altro.\n"
    "Message: {text}\nIntent:"
)

_parser = StrOutputParser()

def classify_intent(text: str, llm: ChatOpenAI | None = None) -> str:
    """Versione sincrona per compatibilità"""
    llm = llm or ChatOpenAI(model='gpt-4o-mini')
    chain = _prompt | llm | _parser
    result = chain.invoke({"text": text})
    
    # Estrai l'intent usando regex
    match = re.search(r"(prenotazione|richiesta informazioni|reclamo|saluto|spam|altro)", result.lower())
    return match.group(1) if match else "altro"

async def aclassify_intent(text: str, llm: ChatOpenAI | None = None) -> str:
    """Versione asincrona"""
    llm = llm or ChatOpenAI(model='gpt-4o-mini')
    chain = _prompt | llm | _parser
    result = await chain.ainvoke({"text": text})
    
    # Estrai l'intent usando regex
    match = re.search(r"(prenotazione|richiesta informazioni|reclamo|saluto|spam|altro)", result.lower())
    return match.group(1) if match else "altro" 