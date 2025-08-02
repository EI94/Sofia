# Sofia Lite - AI Assistant

Sofia Lite è un assistente AI multilingue per servizi di immigrazione, progettato per gestire conversazioni su WhatsApp, SMS e Voice.

## Configurazione

### Variabili d'Ambiente

- `OPENAI_API_KEY`: Chiave API OpenAI
- `TWILIO_ACCOUNT_SID`: Account SID Twilio
- `TWILIO_AUTH_TOKEN`: Auth Token Twilio
- `TWILIO_WHATSAPP_NUMBER`: Numero WhatsApp Twilio (+18149149892)
- `FIREBASE_CRED_JSON`: Credenziali Firebase (JSON string)
- `GCP_PROJECT_ID`: ID progetto Google Cloud

### Test Webhook

Per abilitare i test diretti del webhook senza validazione Twilio:

```bash
export TEST_WEBHOOK=true
```

**Attenzione**: Questa variabile bypassa la validazione Twilio e dovrebbe essere usata solo per i test.

## Test

### Test Diretti Webhook

```bash
# Esegui test diretti del webhook
pytest tests/test_whatsapp_direct.py -v
```

### Test di Produzione

```bash
# Esegui test di produzione completi
make hammer-prod
```

## Deployment

```bash
# Deploy su Google Cloud Run
gcloud run deploy sofia-lite --source .
```

## Architettura

- **Intent Engine 2.0**: Classificazione intent con LLM + similarity
- **RAG Memory**: Memoria vettoriale per contesto persistente
- **Multilingua**: Supporto per 9 lingue
- **Webhook**: Endpoint per WhatsApp, SMS e Voice 