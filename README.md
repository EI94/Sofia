# Sofia Lite - AI Assistant

Sofia Lite è un assistente AI per Studio Immigrato che gestisce prenotazioni di consulenze legali tramite WhatsApp e Voice.

## Deploy on Google Cloud Run

### Environment Variables & Secrets

Configura le seguenti variabili d'ambiente in Google Cloud Run:

#### Environment Variables
- `OPENAI_API_KEY`: Chiave API OpenAI per LLM
- `ELEVENLABS_API_KEY`: Chiave API ElevenLabs per TTS
- `TWILIO_ACCOUNT_SID`: Account SID Twilio
- `TWILIO_AUTH_TOKEN`: Token di autenticazione Twilio
- `GOOGLE_PROJECT_ID`: ID del progetto Google Cloud

#### Secret Manager
Configura i seguenti secrets in Google Secret Manager e mappali come variabili d'ambiente:
- `openai-api-key` → `OPENAI_API_KEY`
- `elevenlabs-api-key` → `ELEVENLABS_API_KEY`
- `twilio-account-sid` → `TWILIO_ACCOUNT_SID`
- `twilio-auth-token` → `TWILIO_AUTH_TOKEN`
- `google-project-id` → `GOOGLE_PROJECT_ID`

#### Volume Mount
Monta il file delle credenziali Google Cloud come volume:
- **Source**: Secret `gcp-service-account`
- **Mount Path**: `/secrets/gcp-sa.json`
- **Environment Variable**: `GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-sa.json`

### Deployment Steps

1. **Build the container**:
   ```bash
   docker build -t sofia-lite .
   ```

2. **Push to Container Registry**:
   ```bash
   docker tag sofia-lite gcr.io/YOUR_PROJECT/sofia-lite
   docker push gcr.io/YOUR_PROJECT/sofia-lite
   ```

3. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy sofia-lite \
     --image gcr.io/YOUR_PROJECT/sofia-lite \
     --platform managed \
     --region europe-west1 \
     --allow-unauthenticated
   ```

4. **Configure secrets and environment variables** in the Cloud Run console.

### Local Development

1. **Copy environment template**:
   ```bash
   cp sofia_lite/.env.example .env
   ```

2. **Fill in your actual values** in `.env`

3. **Run tests**:
   ```bash
   python -m pytest sofia_lite/tests/ -q
   python scripts/smoke_live.py
   ```

## Sofia Bulk API

Micro-servizio REST per test bulk conversazioni.

### Quick Start

```bash
curl -X POST https://sofia-bulk-api-ew1-xxxx.run.app/api/sofia/conversation \
  -H "Authorization: Bearer $BULK_API_KEY" \
  -H "Content-Type: application/json" \
  -d @sample_convo.json
```

### Environment Variables

- `BULK_API_KEY`: API key per autenticazione (32 caratteri random)
- `CORE_SOFIA_URL`: URL del core Sofia (https://sofia-lite-$(PROJECT_ID).run.app/api/prompt)

### Endpoints

- `POST /api/sofia/conversation` - Processa conversazione e completa messaggi assistant vuoti
- `GET /api/sofia/conversation/{cid}` - Recupera conversazione salvata
- `GET /health` - Health check
- `GET /docs` - Swagger documentation

### Rate Limiting

- 10 requests/second per API key
- Headers X-RateLimit automatici

## Architecture

- **Orchestrator**: Gestisce il flusso conversazionale
- **LLM Middleware**: Classificazione intent e generazione risposte
- **Memory**: Persistenza Firestore per contesto utente
- **Skills**: Moduli specializzati per ogni fase conversazionale
- **ParaHelp Template**: Template di sistema per risposte consistenti
- **Bulk API**: Micro-servizio per test bulk conversazioni

## Security

- ✅ Nessun secret hardcoded nel codice
- ✅ Gestione secrets tramite environment variables
- ✅ Integrazione con Google Secret Manager
- ✅ Fail-fast se secrets mancanti
- ✅ Rate limiting per API protection 