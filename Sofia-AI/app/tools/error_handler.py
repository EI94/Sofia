"""
Centralized Error Handling System per Sofia AI
Sistema enterprise per gestione errori standardizzata cross-channel
"""

import logging
import traceback
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Union, List, Callable
from enum import Enum
from dataclasses import dataclass, field
from functools import wraps
import asyncio
import json

logger = logging.getLogger(__name__)

# ===== ERROR TYPES E SEVERITÀ =====

class ErrorSeverity(Enum):
    """Livelli di severità degli errori"""
    LOW = "low"                    # Warning, non blocca funzionalità
    MEDIUM = "medium"              # Errore gestibile con fallback
    HIGH = "high"                  # Errore critico, fallback necessario
    CRITICAL = "critical"          # Sistema compromesso, alert immediato


class ErrorCategory(Enum):
    """Categorie di errori per classificazione"""
    NETWORK = "network"            # Errori di rete/connectivity
    API_EXTERNAL = "api_external"  # Errori API esterne (OpenAI, Twilio, etc.)
    API_INTERNAL = "api_internal"  # Errori API interne
    DATABASE = "database"          # Errori database/storage
    AUTHENTICATION = "auth"        # Errori autenticazione/autorizzazione
    VALIDATION = "validation"      # Errori validazione input
    BUSINESS_LOGIC = "business"    # Errori logica business
    SYSTEM = "system"             # Errori sistema/infrastruttura
    USER_INPUT = "user_input"     # Errori input utente
    TIMEOUT = "timeout"           # Errori timeout
    RATE_LIMIT = "rate_limit"     # Errori rate limiting
    UNKNOWN = "unknown"           # Errori non classificati


class Channel(Enum):
    """Canali di comunicazione supportati"""
    WHATSAPP = "whatsapp"
    VOICE = "voice"
    SMS = "sms"
    WEB = "web"
    API = "api"
    INTERNAL = "internal"


# ===== ERROR DATA CLASSES =====

@dataclass
class ErrorContext:
    """Contesto dettagliato dell'errore per debugging e monitoring"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    channel: Optional[Channel] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    user_input: Optional[str] = None
    language: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SofiaError:
    """Errore standardizzato Sofia AI con tutte le informazioni necessarie"""
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    technical_message: str
    error_code: str
    context: ErrorContext
    original_exception: Optional[Exception] = None
    stack_trace: Optional[str] = None
    recovery_suggestions: List[str] = field(default_factory=list)
    should_retry: bool = False
    retry_after: Optional[int] = None
    should_alert: bool = False
    
    def __post_init__(self):
        """Post-init per aggiungere stack trace se presente exception"""
        if self.original_exception and not self.stack_trace:
            self.stack_trace = traceback.format_exc()


# ===== ERROR RESPONSE TEMPLATES =====

class ErrorResponseGenerator:
    """Genera risposte di errore appropriate per ogni canale"""
    
    # Template responses per lingua e canale
    ERROR_TEMPLATES = {
        "network": {
            "it": {
                "whatsapp": "🔌 Problema di connessione temporaneo. Riprovo tra poco...",
                "voice": "C'è un problema di connessione. Ti richiamo tra qualche minuto.",
                "sms": "Problema tecnico temporaneo. Riprova tra poco.",
                "web": "Connessione temporaneamente non disponibile. Ricarica la pagina.",
                "api": "Network connectivity issue"
            },
            "en": {
                "whatsapp": "🔌 Temporary connection issue. Trying again in a moment...",
                "voice": "There's a connection problem. I'll call you back in a few minutes.",
                "sms": "Temporary technical issue. Please try again.",
                "web": "Connection temporarily unavailable. Please refresh the page.",
                "api": "Network connectivity issue"
            }
        },
        "api_external": {
            "it": {
                "whatsapp": "⚙️ Servizio temporaneamente non disponibile. I nostri tecnici stanno risolvendo.",
                "voice": "Il servizio è temporaneamente non disponibile. Richiama tra poco.",
                "sms": "Servizio temporaneamente non disponibile. Riprova più tardi.",
                "web": "Servizio in manutenzione. Riprova tra qualche minuto.",
                "api": "External service unavailable"
            },
            "en": {
                "whatsapp": "⚙️ Service temporarily unavailable. Our technicians are working on it.",
                "voice": "The service is temporarily unavailable. Please call back in a moment.",
                "sms": "Service temporarily unavailable. Please try again later.",
                "web": "Service under maintenance. Please try again in a few minutes.",
                "api": "External service unavailable"
            }
        },
        "database": {
            "it": {
                "whatsapp": "📁 Problema temporaneo con i dati. Riprova tra qualche minuto.",
                "voice": "C'è un problema temporaneo. Ti ricontatto presto.",
                "sms": "Problema temporaneo. Riprova tra poco.",
                "web": "Database temporaneamente non disponibile.",
                "api": "Database connection error"
            },
            "en": {
                "whatsapp": "📁 Temporary data issue. Please try again in a few minutes.",
                "voice": "There's a temporary issue. I'll contact you again soon.",
                "sms": "Temporary issue. Please try again soon.",
                "web": "Database temporarily unavailable.",
                "api": "Database connection error"
            }
        },
        "validation": {
            "it": {
                "whatsapp": "❓ Non ho capito bene. Puoi riformulare la tua richiesta?",
                "voice": "Non ho capito bene. Puoi ripetere per favore?",
                "sms": "Messaggio non chiaro. Riprova con più dettagli.",
                "web": "Input non valido. Controlla i dati inseriti.",
                "api": "Invalid input data"
            },
            "en": {
                "whatsapp": "❓ I didn't understand well. Can you rephrase your request?",
                "voice": "I didn't understand well. Can you repeat please?",
                "sms": "Message unclear. Try again with more details.",
                "web": "Invalid input. Please check the data entered.",
                "api": "Invalid input data"
            }
        },
        "business": {
            "it": {
                "whatsapp": "🏢 Mi dispiace, non posso completare questa operazione. Contatta il supporto.",
                "voice": "Non posso completare l'operazione. Chiama il nostro ufficio per assistenza.",
                "sms": "Operazione non consentita. Contatta il supporto.",
                "web": "Operazione non autorizzata per il tuo account.",
                "api": "Business rule violation"
            },
            "en": {
                "whatsapp": "🏢 Sorry, I cannot complete this operation. Please contact support.",
                "voice": "I cannot complete the operation. Please call our office for assistance.",
                "sms": "Operation not allowed. Contact support.",
                "web": "Operation not authorized for your account.",
                "api": "Business rule violation"
            }
        },
        "system": {
            "it": {
                "whatsapp": "🔧 Problema tecnico temporaneo. I nostri tecnici sono al lavoro.",
                "voice": "Problema tecnico temporaneo. Ti richiameremo appena possibile.",
                "sms": "Problema tecnico. Il servizio sarà ripristinato presto.",
                "web": "Sistema in manutenzione. Riprova più tardi.",
                "api": "System maintenance in progress"
            },
            "en": {
                "whatsapp": "🔧 Temporary technical issue. Our technicians are working on it.",
                "voice": "Temporary technical issue. We'll call you back as soon as possible.",
                "sms": "Technical issue. Service will be restored soon.",
                "web": "System under maintenance. Please try again later.",
                "api": "System maintenance in progress"
            }
        },
        "timeout": {
            "it": {
                "whatsapp": "⏰ La richiesta sta impiegando troppo tempo. Riprova tra poco.",
                "voice": "La risposta sta tardando. Ti richiamo tra qualche minuto.",
                "sms": "Timeout. Riprova tra qualche minuto.",
                "web": "Richiesta scaduta. Riprova.",
                "api": "Request timeout"
            },
            "en": {
                "whatsapp": "⏰ The request is taking too long. Please try again in a moment.",
                "voice": "The response is delayed. I'll call you back in a few minutes.",
                "sms": "Timeout. Please try again in a few minutes.",
                "web": "Request timed out. Please try again.",
                "api": "Request timeout"
            }
        },
        "rate_limit": {
            "it": {
                "whatsapp": "🚦 Troppe richieste. Aspetta qualche secondo prima di riprovare.",
                "voice": "Stai chiamando troppo spesso. Riprova tra qualche minuto.",
                "sms": "Limite richieste superato. Aspetta prima di riprovare.",
                "web": "Troppe richieste. Attendi prima di riprovare.",
                "api": "Rate limit exceeded"
            },
            "en": {
                "whatsapp": "🚦 Too many requests. Wait a few seconds before trying again.",
                "voice": "You're calling too often. Please try again in a few minutes.",
                "sms": "Request limit exceeded. Wait before trying again.",
                "web": "Too many requests. Please wait before trying again.",
                "api": "Rate limit exceeded"
            }
        },
        "unknown": {
            "it": {
                "whatsapp": "😕 Qualcosa è andato storto. Riprova o contatta il supporto se il problema persiste.",
                "voice": "Si è verificato un errore. Richiama o contatta il nostro ufficio.",
                "sms": "Errore imprevisto. Riprova più tardi.",
                "web": "Errore imprevisto. Ricarica la pagina o contatta il supporto.",
                "api": "Unexpected error occurred"
            },
            "en": {
                "whatsapp": "😕 Something went wrong. Try again or contact support if the issue persists.",
                "voice": "An error occurred. Please call back or contact our office.",
                "sms": "Unexpected error. Please try again later.",
                "web": "Unexpected error. Refresh the page or contact support.",
                "api": "Unexpected error occurred"
            }
        }
    }
    
    @classmethod
    def generate_user_message(cls, error: SofiaError, language: str = "it") -> str:
        """
        Genera messaggio user-friendly per l'errore
        
        Args:
            error: SofiaError con dettagli errore
            language: Lingua per il messaggio
            
        Returns:
            str: Messaggio appropriato per l'utente
        """
        # Default values
        if language not in ["it", "en"]:
            language = "it"
        
        channel_key = error.context.channel.value if error.context.channel else "whatsapp"
        category_key = error.category.value
        
        # Trova template appropriato
        try:
            templates = cls.ERROR_TEMPLATES.get(category_key, cls.ERROR_TEMPLATES["unknown"])
            lang_templates = templates.get(language, templates["it"])
            message = lang_templates.get(channel_key, lang_templates["whatsapp"])
            
            return message
            
        except Exception as e:
            logger.error(f"❌ Errore generazione messaggio errore: {e}")
            # Fallback assoluto
            if language == "en":
                return "Sorry, something went wrong. Please try again later."
            else:
                return "Mi dispiace, si è verificato un errore. Riprova più tardi."

    def get_voice_error_response(self, language: str, error_type: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM) -> Dict[str, Any]:
        """
        Genera risposta di errore specifica per canale Voice con TwiML
        
        Args:
            language: Lingua del messaggio di errore
            error_type: Tipo di errore per personalizzazione
            severity: Severità dell'errore
            
        Returns:
            Dict con messaggio e istruzioni TwiML
        """
        
        # Messaggi base per livello di severità
        if severity == ErrorSeverity.LOW:
            base_messages = {
                "it": "C'è un piccolo problema tecnico, ma posso aiutarti comunque.",
                "en": "There's a small technical issue, but I can still help you.",
                "fr": "Il y a un petit problème technique, mais je peux quand même vous aider.",
                "es": "Hay un pequeño problema técnico, pero puedo ayudarte de todos modos."
            }
        elif severity == ErrorSeverity.MEDIUM:
            base_messages = {
                "it": "Mi dispiace, sto avendo difficoltà tecniche. Riprova tra qualche minuto.",
                "en": "I'm sorry, I'm having technical difficulties. Please try again in a few minutes.",
                "fr": "Je suis désolée, j'ai des difficultés techniques. Réessayez dans quelques minutes.",
                "es": "Lo siento, tengo dificultades técnicas. Inténtalo de nuevo en unos minutos."
            }
        elif severity == ErrorSeverity.HIGH:
            base_messages = {
                "it": "Si è verificato un errore grave. Richiama più tardi o contatta l'assistenza.",
                "en": "A serious error occurred. Please call back later or contact support.",
                "fr": "Une erreur grave s'est produite. Rappelez plus tard ou contactez le support.",
                "es": "Se produjo un error grave. Llama más tarde o contacta con el soporte."
            }
        else:  # CRITICAL
            base_messages = {
                "it": "Il sistema non è al momento disponibile. Riprova più tardi.",
                "en": "The system is currently unavailable. Please try again later.",
                "fr": "Le système n'est pas disponible actuellement. Réessayez plus tard.",
                "es": "El sistema no está disponible actualmente. Inténtalo más tarde."
            }
        
        message = base_messages.get(language, base_messages["it"])
        
        # Personalizzazioni per tipo di errore specifico
        if error_type == "llm_failure":
            if language == "en":
                message = "I'm having trouble understanding. Could you repeat that more clearly?"
            else:
                message = "Ho difficoltà a capire. Puoi ripetere più chiaramente?"
        elif error_type == "database_error":
            if language == "en":
                message = "I can't access your information right now. Please try again."
            else:
                message = "Non riesco ad accedere alle tue informazioni. Riprova per favore."
        elif error_type == "speech_recognition_error":
            if language == "en":
                message = "I didn't catch that. Could you speak a bit louder and clearer?"
            else:
                message = "Non ho sentito bene. Puoi parlare più forte e chiaramente?"
        elif error_type == "language_detection_error":
            message = "Could you please switch to Italian or English? // Puoi passare all'italiano o all'inglese per favore?"
        
        return {
            "message": message,
            "language": language,
            "severity": severity.value,
            "should_continue": severity in [ErrorSeverity.LOW, ErrorSeverity.MEDIUM],
            "should_hangup": severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
        }

    def create_voice_twiml_error_response(self, sofia_error: 'SofiaError') -> str:
        """
        Crea risposta TwiML completa per errori Voice
        
        Args:
            sofia_error: Errore Sofia standardizzato
            
        Returns:
            str: TwiML XML per risposta vocale di errore
        """
        # Rileva lingua dal contesto o usa default
        language = getattr(sofia_error.context, 'language', 'it') if sofia_error.context else 'it'
        
        # Determina tipo errore per messaggio personalizzato
        error_type = "general"
        if sofia_error.category == ErrorCategory.API_EXTERNAL:
            error_type = "llm_failure" if "openai" in sofia_error.technical_message.lower() else "external_api"
        elif sofia_error.category == ErrorCategory.DATABASE:
            error_type = "database_error"
        elif sofia_error.category == ErrorCategory.USER_INPUT:
            error_type = "speech_recognition_error"
        elif sofia_error.category == ErrorCategory.API_INTERNAL:
            if "language" in sofia_error.technical_message.lower():
                error_type = "language_detection_error"
        
        # Genera messaggio di errore appropriato
        error_response = self.get_voice_error_response(language, error_type, sofia_error.severity)
        
        # Costruisce TwiML response
        twiml_parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<Response>']
        
        # Determina lingua TTS
        tts_language = "it-IT"
        tts_voice = "alice"
        if language == "en":
            tts_language = "en-US"
            tts_voice = "alice"
        elif language == "fr":
            tts_language = "fr-FR"
            tts_voice = "alice"
        elif language == "es":
            tts_language = "es-ES"
            tts_voice = "alice"
        
        # Aggiunge messaggio TTS
        twiml_parts.append(f'    <Say language="{tts_language}" voice="{tts_voice}">{error_response["message"]}</Say>')
        
        # Gestisce continuazione conversazione o chiusura
        if error_response["should_continue"] and sofia_error.severity in [ErrorSeverity.LOW, ErrorSeverity.MEDIUM]:
            # Permette di continuare con un gather
            twiml_parts.extend([
                f'    <Gather input="speech" timeout="10" speechTimeout="auto" language="{tts_language}" action="/webhook/voice/process" method="POST">',
                f'        <Say language="{tts_language}" voice="{tts_voice}">Puoi riprovare.</Say>' if language == "it" else f'        <Say language="{tts_language}" voice="{tts_voice}">You can try again.</Say>',
                '    </Gather>'
            ])
            
            # Fallback se non sente nulla
            fallback_msg = "Ti richiameremo presto. Ciao!" if language == "it" else "We'll call you back soon. Goodbye!"
            twiml_parts.append(f'    <Say language="{tts_language}" voice="{tts_voice}">{fallback_msg}</Say>')
        else:
            # Termina chiamata per errori gravi
            goodbye_msg = "La chiamata termina qui. Ciao!" if language == "it" else "The call ends here. Goodbye!"
            twiml_parts.append(f'    <Say language="{tts_language}" voice="{tts_voice}">{goodbye_msg}</Say>')
        
        twiml_parts.append('</Response>')
        
        return '\n'.join(twiml_parts)


# ===== ERROR HANDLER PRINCIPALE =====

class SofiaErrorHandler:
    """Gestore centralizzato di tutti gli errori Sofia AI"""
    
    def __init__(self):
        self.error_stats: Dict[str, int] = {}
        self.error_history: List[SofiaError] = []
        self.max_history = 1000
        self.alert_callbacks: List[Callable] = []
        
        # Rate limiting per evitare spam di errori
        self.error_rate_limit: Dict[str, List[float]] = {}
        self.rate_limit_window = 300  # 5 minuti
        self.max_errors_per_window = 10
    
    def add_alert_callback(self, callback: Callable[[SofiaError], None]):
        """Aggiunge callback per alert su errori critici"""
        self.alert_callbacks.append(callback)
    
    async def handle_error(self, 
                          exception: Exception,
                          context: ErrorContext,
                          category: Optional[ErrorCategory] = None,
                          severity: Optional[ErrorSeverity] = None,
                          recovery_suggestions: Optional[List[str]] = None) -> SofiaError:
        """
        Gestisce un errore e genera SofiaError standardizzato
        
        Args:
            exception: Exception originale
            context: Contesto dell'errore
            category: Categoria errore (auto-detect se None)
            severity: Severità errore (auto-detect se None)
            recovery_suggestions: Suggerimenti per recovery
            
        Returns:
            SofiaError: Errore standardizzato
        """
        
        # Auto-detect categoria se non fornita
        if not category:
            category = self._detect_error_category(exception)
        
        # Auto-detect severità se non fornita
        if not severity:
            severity = self._detect_error_severity(exception, category)
        
        # Genera codice errore unico
        error_code = self._generate_error_code(category, severity, context)
        
        # Crea SofiaError
        sofia_error = SofiaError(
            category=category,
            severity=severity,
            message=self._extract_user_message(exception),
            technical_message=str(exception),
            error_code=error_code,
            context=context,
            original_exception=exception,
            recovery_suggestions=recovery_suggestions or [],
            should_retry=self._should_retry(exception, category),
            retry_after=self._get_retry_delay(exception, category),
            should_alert=severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
        )
        
        # Registra errore
        await self._log_error(sofia_error)
        
        # Aggiorna statistiche
        self._update_error_stats(sofia_error)
        
        # Aggiungi alla history
        self._add_to_history(sofia_error)
        
        # Controlla rate limiting
        if self._is_rate_limited(sofia_error):
            logger.warning(f"⚠️ Rate limiting attivo per errori {category.value}")
        
        # Invia alert se necessario
        if sofia_error.should_alert and not self._is_rate_limited(sofia_error):
            await self._send_alerts(sofia_error)
        
        return sofia_error
    
    def _detect_error_category(self, exception: Exception) -> ErrorCategory:
        """Auto-rileva categoria errore dall'exception"""
        
        exception_name = type(exception).__name__.lower()
        exception_message = str(exception).lower()
        
        # Network errors
        if any(term in exception_name for term in ["connection", "network", "timeout", "http"]):
            return ErrorCategory.NETWORK
        
        # Database errors
        if any(term in exception_name for term in ["database", "firestore", "sql", "connection"]):
            return ErrorCategory.DATABASE
        
        # API errors
        if any(term in exception_name for term in ["api", "request", "response", "http"]):
            return ErrorCategory.API_EXTERNAL
        
        # Authentication errors
        if any(term in exception_name for term in ["auth", "permission", "unauthorized", "forbidden"]):
            return ErrorCategory.AUTHENTICATION
        
        # Validation errors
        if any(term in exception_name for term in ["validation", "invalid", "format", "parse"]):
            return ErrorCategory.VALIDATION
        
        # Timeout errors
        if "timeout" in exception_name or "timeout" in exception_message:
            return ErrorCategory.TIMEOUT
        
        # Rate limit errors
        if any(term in exception_message for term in ["rate limit", "too many requests", "quota"]):
            return ErrorCategory.RATE_LIMIT
        
        return ErrorCategory.UNKNOWN
    
    def _detect_error_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Auto-rileva severità errore"""
        
        exception_message = str(exception).lower()
        
        # Critical keywords
        critical_keywords = ["critical", "fatal", "emergency", "system down", "database down"]
        if any(keyword in exception_message for keyword in critical_keywords):
            return ErrorSeverity.CRITICAL
        
        # High severity per certe categorie
        if category in [ErrorCategory.DATABASE, ErrorCategory.SYSTEM]:
            return ErrorSeverity.HIGH
        
        # Medium severity per API esterne
        if category in [ErrorCategory.API_EXTERNAL, ErrorCategory.NETWORK]:
            return ErrorSeverity.MEDIUM
        
        # Low severity per validation e user input
        if category in [ErrorCategory.VALIDATION, ErrorCategory.USER_INPUT]:
            return ErrorSeverity.LOW
        
        return ErrorSeverity.MEDIUM
    
    def _generate_error_code(self, category: ErrorCategory, severity: ErrorSeverity, context: ErrorContext) -> str:
        """Genera codice errore unico per tracking"""
        
        timestamp = int(time.time())
        category_code = category.value.upper()[:3]
        severity_code = severity.value.upper()[0]
        channel_code = context.channel.value.upper()[:2] if context.channel else "UN"
        
        return f"SOF_{category_code}_{severity_code}_{channel_code}_{timestamp}"
    
    def _extract_user_message(self, exception: Exception) -> str:
        """Estrae messaggio user-friendly dall'exception"""
        
        # Per alcune exception, usa messaggio specifico
        exception_name = type(exception).__name__
        
        user_friendly_messages = {
            "ConnectionError": "Problema di connessione",
            "TimeoutError": "Operazione scaduta",
            "ValidationError": "Dati non validi",
            "PermissionError": "Accesso non autorizzato",
            "FileNotFoundError": "Risorsa non trovata",
            "ValueError": "Valore non valido"
        }
        
        return user_friendly_messages.get(exception_name, "Errore imprevisto")
    
    def _should_retry(self, exception: Exception, category: ErrorCategory) -> bool:
        """Determina se l'operazione dovrebbe essere ripetuta"""
        
        # Retry per errori di rete e timeout
        if category in [ErrorCategory.NETWORK, ErrorCategory.TIMEOUT]:
            return True
        
        # Retry per alcuni errori API esterni
        if category == ErrorCategory.API_EXTERNAL and "rate limit" not in str(exception).lower():
            return True
        
        return False
    
    def _get_retry_delay(self, exception: Exception, category: ErrorCategory) -> Optional[int]:
        """Calcola delay per retry in secondi"""
        
        if category == ErrorCategory.RATE_LIMIT:
            return 60  # 1 minuto per rate limit
        
        if category in [ErrorCategory.NETWORK, ErrorCategory.TIMEOUT]:
            return 5  # 5 secondi per network
        
        if category == ErrorCategory.API_EXTERNAL:
            return 10  # 10 secondi per API esterne
        
        return None
    
    async def _log_error(self, error: SofiaError):
        """Registra errore nei log con livello appropriato"""
        
        log_data = {
            "error_code": error.error_code,
            "category": error.category.value,
            "severity": error.severity.value,
            "channel": error.context.channel.value if error.context.channel else None,
            "user_id": error.context.user_id,
            "endpoint": error.context.endpoint,
            "technical_message": error.technical_message
        }
        
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"🚨 CRITICAL ERROR: {error.error_code} - {error.message}", extra=log_data)
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(f"❌ HIGH ERROR: {error.error_code} - {error.message}", extra=log_data)
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(f"⚠️ MEDIUM ERROR: {error.error_code} - {error.message}", extra=log_data)
        else:
            logger.info(f"ℹ️ LOW ERROR: {error.error_code} - {error.message}", extra=log_data)
    
    def _update_error_stats(self, error: SofiaError):
        """Aggiorna statistiche errori"""
        
        key = f"{error.category.value}_{error.severity.value}"
        self.error_stats[key] = self.error_stats.get(key, 0) + 1
        
        # Mantieni stats per channel
        if error.context.channel:
            channel_key = f"channel_{error.context.channel.value}"
            self.error_stats[channel_key] = self.error_stats.get(channel_key, 0) + 1
    
    def _add_to_history(self, error: SofiaError):
        """Aggiunge errore alla history mantenendo limite"""
        
        self.error_history.append(error)
        
        # Mantieni solo gli ultimi N errori
        if len(self.error_history) > self.max_history:
            self.error_history = self.error_history[-self.max_history:]
    
    def _is_rate_limited(self, error: SofiaError) -> bool:
        """Controlla se questo tipo di errore è rate limited"""
        
        error_type = f"{error.category.value}_{error.severity.value}"
        now = time.time()
        
        # Pulisci vecchi timestamp
        if error_type in self.error_rate_limit:
            self.error_rate_limit[error_type] = [
                ts for ts in self.error_rate_limit[error_type] 
                if now - ts < self.rate_limit_window
            ]
        else:
            self.error_rate_limit[error_type] = []
        
        # Aggiungi timestamp corrente
        self.error_rate_limit[error_type].append(now)
        
        # Controlla limite
        return len(self.error_rate_limit[error_type]) > self.max_errors_per_window
    
    async def _send_alerts(self, error: SofiaError):
        """Invia alert per errori critici"""
        
        for callback in self.alert_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(error)
                else:
                    callback(error)
            except Exception as e:
                logger.error(f"❌ Errore invio alert: {e}")
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Ottieni statistiche errori per monitoring"""
        
        now = datetime.now(timezone.utc)
        recent_errors = [
            error for error in self.error_history 
            if (now - error.context.timestamp).total_seconds() < 3600  # Ultima ora
        ]
        
        return {
            "total_errors": len(self.error_history),
            "recent_errors_1h": len(recent_errors),
            "error_stats": self.error_stats.copy(),
            "rate_limited_types": list(self.error_rate_limit.keys()),
            "most_common_category": max(self.error_stats.items(), key=lambda x: x[1])[0] if self.error_stats else None
        }
    
    def get_recent_errors(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Ottieni errori recenti per debugging"""
        
        recent = self.error_history[-limit:] if len(self.error_history) > limit else self.error_history
        
        return [
            {
                "error_code": error.error_code,
                "category": error.category.value,
                "severity": error.severity.value,
                "message": error.message,
                "channel": error.context.channel.value if error.context.channel else None,
                "user_id": error.context.user_id,
                "timestamp": error.context.timestamp.isoformat(),
                "should_retry": error.should_retry,
                "retry_after": error.retry_after
            }
            for error in reversed(recent)
        ]

    def get_voice_error_response(self, language: str, error_type: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM) -> Dict[str, Any]:
        """
        Genera risposta di errore specifica per canale Voice con TwiML
        
        Args:
            language: Lingua del messaggio di errore
            error_type: Tipo di errore per personalizzazione
            severity: Severità dell'errore
            
        Returns:
            Dict con messaggio e istruzioni TwiML
        """
        
        # Messaggi base per livello di severità
        if severity == ErrorSeverity.LOW:
            base_messages = {
                "it": "C'è un piccolo problema tecnico, ma posso aiutarti comunque.",
                "en": "There's a small technical issue, but I can still help you.",
                "fr": "Il y a un petit problème technique, mais je peux quand même vous aider.",
                "es": "Hay un pequeño problema técnico, pero puedo ayudarte de todos modos."
            }
        elif severity == ErrorSeverity.MEDIUM:
            base_messages = {
                "it": "Mi dispiace, sto avendo difficoltà tecniche. Riprova tra qualche minuto.",
                "en": "I'm sorry, I'm having technical difficulties. Please try again in a few minutes.",
                "fr": "Je suis désolée, j'ai des difficultés techniques. Réessayez dans quelques minutes.",
                "es": "Lo siento, tengo dificultades técnicas. Inténtalo de nuevo en unos minutos."
            }
        elif severity == ErrorSeverity.HIGH:
            base_messages = {
                "it": "Si è verificato un errore grave. Richiama più tardi o contatta l'assistenza.",
                "en": "A serious error occurred. Please call back later or contact support.",
                "fr": "Une erreur grave s'est produite. Rappelez plus tard ou contactez le support.",
                "es": "Se produjo un error grave. Llama más tarde o contacta con el soporte."
            }
        else:  # CRITICAL
            base_messages = {
                "it": "Il sistema non è al momento disponibile. Riprova più tardi.",
                "en": "The system is currently unavailable. Please try again later.",
                "fr": "Le système n'est pas disponible actuellement. Réessayez plus tard.",
                "es": "El sistema no está disponible actualmente. Inténtalo más tarde."
            }
        
        message = base_messages.get(language, base_messages["it"])
        
        # Personalizzazioni per tipo di errore specifico
        if error_type == "llm_failure":
            if language == "en":
                message = "I'm having trouble understanding. Could you repeat that more clearly?"
            else:
                message = "Ho difficoltà a capire. Puoi ripetere più chiaramente?"
        elif error_type == "database_error":
            if language == "en":
                message = "I can't access your information right now. Please try again."
            else:
                message = "Non riesco ad accedere alle tue informazioni. Riprova per favore."
        elif error_type == "speech_recognition_error":
            if language == "en":
                message = "I didn't catch that. Could you speak a bit louder and clearer?"
            else:
                message = "Non ho sentito bene. Puoi parlare più forte e chiaramente?"
        elif error_type == "language_detection_error":
            message = "Could you please switch to Italian or English? // Puoi passare all'italiano o all'inglese per favore?"
        
        return {
            "message": message,
            "language": language,
            "severity": severity.value,
            "should_continue": severity in [ErrorSeverity.LOW, ErrorSeverity.MEDIUM],
            "should_hangup": severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
        }

    def create_voice_twiml_error_response(self, sofia_error: 'SofiaError') -> str:
        """
        Crea risposta TwiML completa per errori Voice
        
        Args:
            sofia_error: Errore Sofia standardizzato
            
        Returns:
            str: TwiML XML per risposta vocale di errore
        """
        # Rileva lingua dal contesto o usa default
        language = getattr(sofia_error.context, 'language', 'it') if sofia_error.context else 'it'
        
        # Determina tipo errore per messaggio personalizzato
        error_type = "general"
        if sofia_error.category == ErrorCategory.API_EXTERNAL:
            error_type = "llm_failure" if "openai" in sofia_error.technical_message.lower() else "external_api"
        elif sofia_error.category == ErrorCategory.DATABASE:
            error_type = "database_error"
        elif sofia_error.category == ErrorCategory.USER_INPUT:
            error_type = "speech_recognition_error"
        elif sofia_error.category == ErrorCategory.API_INTERNAL:
            if "language" in sofia_error.technical_message.lower():
                error_type = "language_detection_error"
        
        # Genera messaggio di errore appropriato
        error_response = self.get_voice_error_response(language, error_type, sofia_error.severity)
        
        # Costruisce TwiML response
        twiml_parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<Response>']
        
        # Determina lingua TTS
        tts_language = "it-IT"
        tts_voice = "alice"
        if language == "en":
            tts_language = "en-US"
            tts_voice = "alice"
        elif language == "fr":
            tts_language = "fr-FR"
            tts_voice = "alice"
        elif language == "es":
            tts_language = "es-ES"
            tts_voice = "alice"
        
        # Aggiunge messaggio TTS
        twiml_parts.append(f'    <Say language="{tts_language}" voice="{tts_voice}">{error_response["message"]}</Say>')
        
        # Gestisce continuazione conversazione o chiusura
        if error_response["should_continue"] and sofia_error.severity in [ErrorSeverity.LOW, ErrorSeverity.MEDIUM]:
            # Permette di continuare con un gather
            twiml_parts.extend([
                f'    <Gather input="speech" timeout="10" speechTimeout="auto" language="{tts_language}" action="/webhook/voice/process" method="POST">',
                f'        <Say language="{tts_language}" voice="{tts_voice}">Puoi riprovare.</Say>' if language == "it" else f'        <Say language="{tts_language}" voice="{tts_voice}">You can try again.</Say>',
                '    </Gather>'
            ])
            
            # Fallback se non sente nulla
            fallback_msg = "Ti richiameremo presto. Ciao!" if language == "it" else "We'll call you back soon. Goodbye!"
            twiml_parts.append(f'    <Say language="{tts_language}" voice="{tts_voice}">{fallback_msg}</Say>')
        else:
            # Termina chiamata per errori gravi
            goodbye_msg = "La chiamata termina qui. Ciao!" if language == "it" else "The call ends here. Goodbye!"
            twiml_parts.append(f'    <Say language="{tts_language}" voice="{tts_voice}">{goodbye_msg}</Say>')
        
        twiml_parts.append('</Response>')
        
        return '\n'.join(twiml_parts)


# ===== DECORATORI PER ERROR HANDLING =====

def handle_sofia_errors(category: Optional[ErrorCategory] = None,
                        severity: Optional[ErrorSeverity] = None,
                        channel: Optional[Channel] = None):
    """
    Decoratore per gestione automatica errori con SofiaErrorHandler
    
    Args:
        category: Categoria errore predefinita
        severity: Severità errore predefinita  
        channel: Canale di comunicazione
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Crea context dall'ambiente
                context = ErrorContext(
                    channel=channel,
                    endpoint=func.__name__,
                    method="async_function"
                )
                
                # Gestisce errore
                sofia_error = await error_handler.handle_error(
                    exception=e,
                    context=context,
                    category=category,
                    severity=severity
                )
                
                # Re-raise con SofiaError wrappato
                raise SofiaErrorException(sofia_error) from e
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Per funzioni sync, crea un loop per gestire l'errore
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                context = ErrorContext(
                    channel=channel,
                    endpoint=func.__name__,
                    method="sync_function"
                )
                
                if loop.is_running():
                    # Se loop già attivo, non possiamo usare handle_error asincrono
                    logger.error(f"❌ Sync error in {func.__name__}: {e}")
                    raise e
                else:
                    sofia_error = loop.run_until_complete(
                        error_handler.handle_error(e, context, category, severity)
                    )
                    raise SofiaErrorException(sofia_error) from e
        
        # Restituisce wrapper appropriato
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class SofiaErrorException(Exception):
    """Exception custom che contiene SofiaError"""
    
    def __init__(self, sofia_error: SofiaError):
        self.sofia_error = sofia_error
        super().__init__(sofia_error.message)


# ===== UTILITY FUNCTIONS =====

async def create_error_response(error: SofiaError, language: str = "it") -> Dict[str, Any]:
    """
    Crea response standardizzata per errore
    
    Args:
        error: SofiaError da processare
        language: Lingua per messaggio user
        
    Returns:
        dict: Response standardizzata
    """
    
    user_message = ErrorResponseGenerator.generate_user_message(error, language)
    
    response = {
        "success": False,
        "error": {
            "code": error.error_code,
            "message": user_message,
            "category": error.category.value,
            "severity": error.severity.value,
            "should_retry": error.should_retry,
            "retry_after": error.retry_after,
            "timestamp": error.context.timestamp.isoformat()
        }
    }
    
    # Aggiungi dati tecnici solo per canali API
    if error.context.channel in [Channel.API, Channel.INTERNAL]:
        response["error"]["technical_message"] = error.technical_message
        response["error"]["recovery_suggestions"] = error.recovery_suggestions
        response["error"]["context"] = {
            "endpoint": error.context.endpoint,
            "method": error.context.method,
            "user_id": error.context.user_id
        }
    
    return response


def extract_context_from_request(request, channel: Channel, user_id: str = None) -> ErrorContext:
    """
    Estrae ErrorContext da FastAPI request
    
    Args:
        request: FastAPI Request object
        channel: Canale di comunicazione
        user_id: ID utente se disponibile
        
    Returns:
        ErrorContext: Contesto dell'errore
    """
    
    return ErrorContext(
        user_id=user_id,
        channel=channel,
        endpoint=str(request.url.path) if hasattr(request, 'url') else None,
        method=request.method if hasattr(request, 'method') else None,
        user_agent=request.headers.get('User-Agent') if hasattr(request, 'headers') else None,
        ip_address=request.client.host if hasattr(request, 'client') else None
    )


def extract_voice_context_from_request(request: Any, user_id: str = "", additional_data: Optional[Dict[str, Any]] = None) -> ErrorContext:
    """
    Estrae contesto dettagliato da richiesta Voice per error tracking
    
    Args:
        request: FastAPI Request object
        user_id: ID utente (numero telefono)
        additional_data: Dati aggiuntivi (Call SID, etc.)
        
    Returns:
        ErrorContext: Contesto completo per error handling
    """
    if additional_data is None:
        additional_data = {}
    
    # Costruisce contesto ricco per Voice calls
    context = ErrorContext(
        user_id=user_id,
        channel=Channel.VOICE,
        endpoint=str(request.url.path) if hasattr(request, 'url') else None,
        method=request.method if hasattr(request, 'method') else "POST",
        timestamp=datetime.now(timezone.utc),
        additional_data={
            **additional_data,
            "user_agent": request.headers.get("User-Agent", "Twilio-Webhook") if hasattr(request, 'headers') else "Unknown",
            "content_type": request.headers.get("Content-Type", "application/x-www-form-urlencoded") if hasattr(request, 'headers') else "Unknown",
            "request_source": "twilio_voice_webhook"
        }
    )
    
    # Estrae informazioni specifiche Twilio se disponibili
    try:
        if hasattr(request, 'form'):
            # Async form extraction per context ricco
            form_keys = ["CallSid", "From", "To", "CallStatus", "Direction", "SpeechResult", "Confidence"]
            for key in form_keys:
                # Non possiamo fare await qui, ma possiamo tentare di ottenere valori
                context.additional_data[f"twilio_{key.lower()}"] = "pending_extraction"
    except Exception as e:
        logger.warning(f"⚠️ Impossibile estrarre form data Voice: {e}")
    
    return context


# ===== ISTANZA GLOBALE =====

# Gestore errori globale
error_handler = SofiaErrorHandler()

# Export per uso esterno
__all__ = [
    "error_handler",
    "SofiaError",
    "SofiaErrorException", 
    "ErrorCategory",
    "ErrorSeverity",
    "ErrorContext",
    "Channel",
    "ErrorResponseGenerator",
    "handle_sofia_errors",
    "create_error_response",
    "extract_context_from_request",
    "extract_voice_context_from_request"
] 