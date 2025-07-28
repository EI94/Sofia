#!/bin/bash

# SOFIA AI - ENTERPRISE PRODUCTION DEPLOYMENT
# Il miglior product tester del mondo!

echo "🚀 SOFIA AI - ENTERPRISE PRODUCTION DEPLOYMENT"
echo "================================================"

# Configurazione
PROJECT_ID="sofia-ai-464215"
SERVICE_NAME="sofia-ai"
REGION="europe-west1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🎯 Progetto: $PROJECT_ID"
echo "🔧 Servizio: $SERVICE_NAME"
echo "🌍 Regione: $REGION"
echo "📦 Immagine: $IMAGE_NAME"
echo ""

# Pre-deployment checks
echo "🔍 Pre-deployment checks..."

# Verifica autenticazione
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Errore: Non sei autenticato con gcloud"
    echo "   Esegui: gcloud auth login"
    exit 1
fi

# Verifica progetto
if ! gcloud config get-value project | grep -q "$PROJECT_ID"; then
    echo "❌ Errore: Progetto non configurato correttamente"
    echo "   Esegui: gcloud config set project $PROJECT_ID"
    exit 1
fi

# Verifica Dockerfile
if [ ! -f "Dockerfile.production" ]; then
    echo "❌ Errore: Dockerfile.production non trovato"
    exit 1
fi

echo "✅ Pre-deployment checks completati"
echo ""

# Build dell'immagine Docker
echo "🔨 Build immagine Docker..."
gcloud builds submit --tag $IMAGE_NAME .

if [ $? -ne 0 ]; then
    echo "❌ Errore durante il build dell'immagine"
    exit 1
fi

echo "✅ Immagine Docker buildata con successo"
echo ""

# Deploy su Cloud Run
echo "🚀 Deploy su Google Cloud Run..."

gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --min-instances 1 \
    --timeout 300 \
    --concurrency 80 \
    --set-env-vars ENVIRONMENT=production \
    --set-env-vars LOG_LEVEL=INFO

if [ $? -ne 0 ]; then
    echo "❌ Errore durante il deploy"
    exit 1
fi

echo "✅ Deploy completato con successo"
echo ""

# Ottieni URL del servizio
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "🎉 SOFIA AI DEPLOYATA CON SUCCESSO!"
echo "=================================="
echo "🌐 URL: $SERVICE_URL"
echo "📡 Webhook WhatsApp: $SERVICE_URL/webhook/whatsapp"
echo "📞 Webhook Voice: $SERVICE_URL/webhook/voice"
echo "🏥 Health Check: $SERVICE_URL/health"
echo ""

# Test rapido del servizio
echo "🧪 Test rapido del servizio..."
if curl -f "$SERVICE_URL/health" > /dev/null 2>&1; then
    echo "✅ Servizio risponde correttamente"
else
    echo "⚠️  Servizio potrebbe non essere ancora pronto"
fi

echo ""
echo "🚀 SOFIA AI È PRONTA PER IL CLIENTE!"
echo "📊 Controlla i log: gcloud logs tail --service=$SERVICE_NAME" 