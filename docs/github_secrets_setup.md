# Configurazione Secrets GitHub per Sofia Bulk API

## Secrets Richiesti

Per abilitare il deployment automatico del Sofia Bulk API tramite GitHub Actions, è necessario configurare i seguenti secrets nel repository GitHub:

### 1. GCP_SA_KEY
**Descrizione**: Chiave del Service Account Google Cloud per l'autenticazione
**Tipo**: File JSON
**Come ottenere**:
1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Seleziona il progetto `sofia-ai-464215`
3. Vai su "IAM & Admin" > "Service Accounts"
4. Crea un nuovo Service Account o usa quello esistente
5. Crea una nuova chiave JSON
6. Copia il contenuto del file JSON

### 2. GCP_PROJECT
**Descrizione**: ID del progetto Google Cloud
**Valore**: `sofia-ai-464215`

### 3. BULK_API_KEY
**Descrizione**: Chiave API per l'autenticazione del bulk API
**Valore**: `test-bulk-api-key-123` (per test) o una chiave sicura per produzione

### 4. CORE_SOFIA_URL
**Descrizione**: URL del servizio Sofia Lite core
**Valore**: `https://sofia-lite-sofia-ai-464215.run.app/api/prompt`

## Come Configurare i Secrets

1. Vai su GitHub repository: https://github.com/EI94/Sofia
2. Clicca su "Settings" (tab)
3. Nel menu laterale, clicca su "Secrets and variables" > "Actions"
4. Clicca su "New repository secret"
5. Aggiungi ogni secret con il nome e valore corrispondenti

## Test del Deployment

Dopo aver configurato i secrets, il deployment automatico si attiverà quando:
- Si fa push di un tag `bulk-api/v*`
- Si fa push sul branch `bulk-api-bootstrap`
- Si modificano i file del bulk API

## URL di Produzione

Il bulk API sarà disponibile su:
`https://sofia-bulk-api-ew1-1075574333382.europe-west1.run.app`

## Documentazione API

Swagger UI disponibile su:
`https://sofia-bulk-api-ew1-1075574333382.europe-west1.run.app/docs`
