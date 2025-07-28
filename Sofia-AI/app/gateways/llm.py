"""
Gateway per LLM (OpenAI) - VERSIONE SEMPLIFICATA
"""

import asyncio
import logging
from typing import List, Dict, Any
from abc import ABC, abstractmethod
import os

logger = logging.getLogger(__name__)

class LLMGateway(ABC):
    """Gateway astratto per LLM"""
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Genera risposta dal LLM"""
        pass

class OpenAIGateway(LLMGateway):
    """Gateway per OpenAI - VERSIONE SEMPLIFICATA COME FUNZIONAVA PRIMA"""
    
    def __init__(self, client=None):
        if client is None:
            try:
                from openai import AsyncOpenAI
                # APPROCCIO SEMPLICE COME IN MODERATION.PY
                api_key = os.getenv("OPENAI_API_KEY")
                logger.info(f"🔍 API Key trovata: {'SÌ' if api_key else 'NO'}")
                if api_key:
                    # PULISCI L'API KEY DAL CARATTERE DI NEWLINE
                    api_key = api_key.strip()
                    logger.info(f"🔍 API Key lunghezza: {len(api_key)} caratteri")
                    logger.info(f"🔍 API Key inizia con: {api_key[:10]}...")
                
                if not api_key:
                    logger.error("❌ OPENAI_API_KEY non configurata")
                    self.client = None
                else:
                    self.client = AsyncOpenAI(
                        api_key=api_key,
                        timeout=120.0,  # Timeout di 2 minuti
                        max_retries=3
                    )
                    logger.info("✅ OpenAI client inizializzato con API key da environment")
            except ImportError:
                logger.error("❌ OpenAI non installato")
                self.client = None
            except Exception as e:
                logger.error(f"❌ Errore inizializzazione OpenAI: {e}")
                self.client = None
        else:
            self.client = client
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Genera risposta da OpenAI"""
        try:
            if not self.client:
                logger.warning("⚠️ Client OpenAI non disponibile, uso fallback")
                return self._generate_fallback_response(prompt)
            
            logger.info(f"📤 Invio richiesta a OpenAI: {prompt[:100]}...")
            
            # Timeout aggressivo per evitare blocchi
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.7,
                    **kwargs
                ),
                timeout=30.0  # Timeout di 30 secondi
            )
            
            reply = response.choices[0].message.content.strip()
            logger.info(f"✅ Risposta OpenAI ricevuta: {reply[:100]}...")
            return reply
            
        except asyncio.TimeoutError:
            logger.error("⏰ Timeout OpenAI (30s), uso fallback")
            return self._generate_fallback_response(prompt)
        except Exception as e:
            logger.error(f"❌ Errore OpenAI: {e}")
            logger.error(f"Tipo errore: {type(e)}")
            return self._generate_fallback_response(prompt)
    
    async def generate_response_with_system(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Genera risposta con system e user prompt separati"""
        try:
            if not self.client:
                logger.warning("⚠️ Client OpenAI non disponibile, uso fallback")
                return self._generate_fallback_response(user_prompt)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            logger.info(f"📤 Invio richiesta a OpenAI con system prompt: {system_prompt[:100]}...")
            
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7,
                    **kwargs
                ),
                timeout=30.0
            )
            
            reply = response.choices[0].message.content.strip()
            logger.info(f"✅ Risposta OpenAI ricevuta: {reply[:100]}...")
            return reply
            
        except asyncio.TimeoutError:
            logger.error("⏰ Timeout OpenAI (30s), uso fallback")
            return self._generate_fallback_response(user_prompt)
        except Exception as e:
            logger.error(f"❌ Errore OpenAI: {e}")
            return self._generate_fallback_response(user_prompt)
    
    def is_available(self) -> bool:
        """Verifica se il client OpenAI è disponibile"""
        return self.client is not None
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Risposta di fallback intelligente quando OpenAI non funziona"""
        prompt_lower = prompt.lower()
        
        # Risposte specifiche per domande comuni
        if "chi sei" in prompt_lower or "who are you" in prompt_lower:
            return "Ciao! Sono Sofia, l'assistente dello Studio Immigrato di Milano. Posso aiutarti con pratiche di immigrazione, consulenze legali e appuntamenti. Come posso esserti utile oggi?"
        
        if "ciao" in prompt_lower or "hello" in prompt_lower or "hi" in prompt_lower:
            return "Ciao! Sono Sofia dello Studio Immigrato. Come posso aiutarti oggi con le tue pratiche di immigrazione?"
        
        if "consulenza" in prompt_lower or "appuntamento" in prompt_lower:
            return "Perfetto! Per supportarti con le tue pratiche di immigrazione, abbiamo bisogno di vedere i documenti insieme e svolgere una consulenza. La consulenza ha un valore di 60 euro. Quando potrebbe andar bene?"
        
        if "servizi" in prompt_lower or "aiuto" in prompt_lower:
            return "Ti aiuto con pratiche di immigrazione, ricongiungimento familiare, permessi di soggiorno, cittadinanza italiana e molto altro. Per iniziare, ti serve una consulenza. Quando sei disponibile?"
        
        # Risposta generica
        return "Mi dispiace, c'è un problema tecnico temporaneo. Sono Sofia dello Studio Immigrato e posso aiutarti con pratiche di immigrazione. Riprova tra qualche minuto o chiamaci direttamente." 