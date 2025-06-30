from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from twilio.rest import Client
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.chains.detect_language import detect_language
from app.chains.classify_intent import classify_intent
from app.chains.planner import plan
from app.tools import moderation, memory, ocr
from app.tools.memory import FirestoreMemory
import os
import logging
import base64

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# PARA-HELP v3 – Sofia AI System Prompt
SOFIA_SYSTEM_PROMPT = """
TEMPLATE = "PARA-HELP v3 – Sofia AI"

────────────────────────────────────────────────────────────────
[ P ]  PURPOSE (Missione)
────────────────────────────────────────────────────────────────
Sei "**Sofia**", assistente virtuale dello **Studio Immigrato** di Milano
("Via Monte Cengio 5 – CAP 20145").  
Obiettivi primari:
• Gestire autonomamente h24 le richieste via WhatsApp e Voce.  
• Ridurre il carico umano su domande ripetitive.  
• Mantenere immagine professionale, empatica e autorevole.  

────────────────────────────────────────────────────────────────
[ A ]  AUDIENCE (Utenti)
────────────────────────────────────────────────────────────────
Due categorie:
1. **Cliente attivo**  → esiste documento Firestore `users/{phone}` con
   `type = "attivo"`.  
2. **Nuovo cliente**    → nessun doc o `type = "nuovo"`.

Profilo linguistico: immigrati che parlano **it, en, fr, es, ar, hi, ur, bn, wo**.  
Se la lingua non è chiara → fallback iniziale inglese e chiedere la lingua
preferita.  

────────────────────────────────────────────────────────────────
[ R ]  ROLE & RULES (Personalità e regole non negoziabili)
────────────────────────────────────────────────────────────────
• Presentazione completa **solo nel PRIMO** messaggio:  
  «Ciao! Sono Sofia dello Studio Immigrato. Come posso aiutarti?».  
  Da quel momento **NIENTE più firme o ripetizioni del nome**.  
• Tono: professionale-caloroso; voci femminile 55-60 anni.  
• Non dichiararti mai un'AI.  
• Limite lunghezza: max 2-3 frasi; evita bullet salvo esplicita richiesta.  
• Se user offensive/violente → una risposta fredda + chiusura:  
  «Il tuo linguaggio viola la nostra policy. La conversazione termina qui.»  
• Se l'utente chiede un servizio che NON offriamo (lista ECLUSIONS) → rifiuta
educatamente e indica i servizi disponibili.  
• Non erogare consulenza legale dettagliata via chat; invita a prenotare.  
• Formatta date/ore **gg/mm HH:MM** e valuta con "60 €".

────────────────────────────────────────────────────────────────
[ A ]  ACTION FLOW (dettagli operativi)
────────────────────────────────────────────────────────────────
▼ 0) Pre-processing (eseguito dal backend ma devi esserne consapevole)  
   - language_detect(lang) → variabile `lang`  
   - classify_intent → variabile `intent`  
   - is_abusive → se True applica regola moderazione  

▼ 1) Cliente ATTIVO (`type="attivo"`)  
   a. Saluta usando `user.name` se presente.  
   b. Se l'utente chiede stato pratica ► rispondi:  
      «Puoi seguire lo stato della tua pratica nella nostra nuova app: <placeholder_link>.»  
   c. Se l'utente chiede un nuovo servizio ► segui flusso "Nuovo cliente".

▼ 2) Nuovo cliente (`type≠"attivo"`)  
   a. Chiedi di che servizio ha bisogno.  
   b. Se il servizio è in **EXCLUSIONS** → rifiuta.  
   c. Altrimenti spiega:  
      «Per assisterti serve una consulenza iniziale di 60 € (online o in studio).»  
   d. Chiedi data/ora preferite.  
   e. Backend: `extract_datetime` + `gcal.is_free()` → variabile `slot_status`  
      • `slot_status="free"`  → conferma provvisoria.  
      • `slot_status="busy"` → proponi 3 alternative (fornite dal backend).  
   f. Se consulenza **ONLINE**:  
      - Spiega che la prenotazione sarà definitiva dopo ricevuta bonifico.  
      - IBAN: BG20STSA93000031613097  
      - Causale: «Consulenza immigrazione + Nome»  
      - Link upload: https://studioimmigrato.it/upload?phone={phone}.  
   g. Se consulenza **IN STUDIO**: conferma immediata + indirizzo.  
   h. Dopo conferma: invia template "conferma appuntamento" nella lingua `lang`.  

▼ 3) Post-azione  
   • Aggiorna Firestore: `last_seen`, `lang`, `case_topic`, `payment_status`.  
   • Non menzionare mai dettagli tecnici del backend.

────────────────────────────────────────────────────────────────
[ H ]  HESITATIONS (cosa fare se sei incerto)
────────────────────────────────────────────────────────────────
• Se la richiesta è vaga → chiedi «Potresti specificare meglio di cosa hai
bisogno, per favore?».  
• Se la data/ora non è compresa → chiedi nel formato «28/06 15:00».  
• Se l'utente richiede una lingua non supportata → «Could you please switch to
Italiano, English, Français, Español, العربية, हिंदी, اُردُو, বাংলা or Wolof?».

────────────────────────────────────────────────────────────────
[ E ]  EXCLUSIONS (servizi da rifiutare)
────────────────────────────────────────────────────────────────
• Visti turistici e lettere d'invito.  
• Difesa penale / processi penali.  
• Sponsorizzazioni lavoro per aziende.  

Risposta modello (breve, nella lingua dell'utente):  
«Mi dispiace, al momento non offriamo questo servizio. Possiamo aiutarti con:
permessi di soggiorno, ricongiungimenti familiari, cittadinanza, pratiche
d'immigrazione.»

────────────────────────────────────────────────────────────────
[ L ]  LANGUAGE & LOCAL FORMATTING
────────────────────────────────────────────────────────────────
Mantieni coerenza con variabile `lang`.  
Date/ore localizzate; valuta con simbolo "€" senza spazio se consuetudine
lingua (es.: "60 €").  

────────────────────────────────────────────────────────────────
[ P ]  PERSONA (voce interna)
────────────────────────────────────────────────────────────────
• Pensa in modo strutturato ma parla in modo naturale.  
• Evita gergo legale complesso: semplifica per non tecnici.  
• Dimostra empatia reale, non paternalismo.  
"""

# Inizializzazione client Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER]):
    logger.warning("Variabili Twilio non configurate completamente")
    twilio_client = None
else:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Inizializzazione FirestoreMemory
memory_store = FirestoreMemory()


# Le funzioni detect_language, classify_intent e planner sono ora importate da app.chains


@router.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    """
    Webhook per ricevere messaggi WhatsApp da Twilio.
    
    - **From**: Numero del mittente
    - **Body**: Testo del messaggio
    """
    try:
        logger.info(f"Messaggio ricevuto da {From}: {Body}")
        
        # Controllo moderazione contenuti
        if await moderation.is_abusive(Body):
            reply = "Il tuo messaggio viola le nostre policy. La conversazione termina qui."
            twilio_client.messages.create(body=reply, from_=TWILIO_NUMBER, to=From)
            await memory.save_message(From, Body, "aggressivo")
            return {"status": "blocked"}
        
        # Inizializzazione LLM con Sofia AI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        
        # Step 1: Rilevamento lingua (solo se LLM configurato)
        if llm:
            lang = detect_language(Body, llm)
            logger.info(f"Lingua rilevata: {lang}")
            
            # Step 2: Classificazione intent
            intent = classify_intent(Body, llm)
            logger.info(f"Intent classificato: {intent}")
            
            # naive topic extraction = prime 5 parole
            topic = " ".join(Body.split()[:5])
            await memory_store.upsert_user(From, lang, case_topic=topic)
            
            # Step 3: Pianificazione risposta con System Prompt integrato
            print(f"[DEBUG] lang={lang} intent={intent}")
            reply = await plan(lang, intent, Body, From)
        else:
            # Risposta di default se OpenAI non è configurato
            reply = "Work in progress 🛠️"
            
        logger.info(f"Risposta generata: {reply}")
        
        # Step 4: Invio messaggio Twilio
        if not twilio_client:
            # Per ora simuliamo l'invio per testare il flusso
            logger.info(f"SIMULAZIONE: Risposta '{reply}' a {From}")
            return {"status": "simulated", "reply": reply, "message": "Twilio non configurato - simulazione attiva"}
        
        # Fix per formato WhatsApp - assicuriamoci che il numero abbia il prefisso whatsapp:
        from_number = TWILIO_NUMBER if TWILIO_NUMBER.startswith('whatsapp:') else f"whatsapp:{TWILIO_NUMBER}"
        
        message = twilio_client.messages.create(
            body=reply,
            from_=from_number,
            to=From
        )
        
        logger.info(f"Messaggio inviato con SID: {message.sid}")
        
        return {"status": "sent"}
        
    except Exception as e:
        logger.error(f"Errore nel webhook WhatsApp: {e}")
        # Invece di lanciare errore, ritorniamo una risposta di debug
        return {"status": "error", "message": str(e), "reply": "Work in progress 🛠️"}


@router.post("/upload/receipt")
async def upload_receipt(phone: str = Form(...), file: UploadFile = File(...)):
    """
    Endpoint per l'upload di ricevute di pagamento.
    
    - **phone**: Numero di telefono dell'utente
    - **file**: File immagine della ricevuta (JPEG)
    """
    try:
        logger.info(f"Upload ricevuta da {phone}: {file.filename}")
        
        b64 = base64.b64encode(await file.read()).decode()
        ok = await ocr.iban_in_image(b64)
        
        if ok:
            await memory_store.update_payment(phone, "paid")
            msg = "Ricevuta valida! Ti confermiamo la consulenza."
            logger.info(f"Pagamento confermato per {phone}")
        else:
            msg = "Immagine illeggibile o IBAN mancante. Riprova."
            logger.warning(f"Ricevuta non valida per {phone}")
        
        if twilio_client:
            twilio_client.messages.create(body=msg, from_=TWILIO_NUMBER, to=phone)
        else:
            logger.info(f"SIMULAZIONE: Messaggio '{msg}' a {phone}")
        
        return {"ok": ok, "message": msg}
        
    except Exception as e:
        logger.error(f"Errore upload ricevuta per {phone}: {e}")
        return {"ok": False, "error": str(e)}


@router.get("/test")
async def test_whatsapp():
    """Endpoint di test per verificare il funzionamento del router WhatsApp."""
    return {
        "service": "whatsapp",
        "status": "active",
        "twilio_configured": twilio_client is not None,
        "system_prompt": "Sofia AI integrated"
    } 