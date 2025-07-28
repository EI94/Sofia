#!/bin/bash

echo "🚀 DEPLOY STAGING - SOFIA AI REFACTORIZZATA"
echo "=========================================="

# Configurazione staging
PROJECT_ID="sofia-ai-staging"
SERVICE_NAME="sofia-ai-staging"
REGION="europe-west1"
IMAGE_NAME="gcr.io/$PROJECT_ID/sofia-ai-staging"

echo "📋 Configurazione:"
echo "   Project ID: $PROJECT_ID"
echo "   Service: $SERVICE_NAME"
echo "   Region: $REGION"
echo "   Image: $IMAGE_NAME"

# Build dell'immagine Docker
echo ""
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME .

# Push su Google Container Registry
echo ""
echo "📤 Pushing to Google Container Registry..."
docker push $IMAGE_NAME

# Deploy su Cloud Run
echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --timeout 300 \
  --concurrency 80 \
  --set-env-vars="ENVIRONMENT=staging" \
  --set-env-vars="LOG_LEVEL=DEBUG" \
  --set-env-vars="OPENAI_API_KEY=$(gcloud secrets versions access latest --secret=openai-api-key --project=$PROJECT_ID)" \
  --set-env-vars="TWILIO_ACCOUNT_SID=$(gcloud secrets versions access latest --secret=twilio-account-sid --project=$PROJECT_ID)" \
  --set-env-vars="TWILIO_AUTH_TOKEN=$(gcloud secrets versions access latest --secret=twilio-auth-token --project=$PROJECT_ID)" \
  --set-env-vars="GOOGLE_APPLICATION_CREDENTIALS=/secrets/google-credentials.json" \
  --set-env-vars="FIREBASE_PROJECT_ID=$PROJECT_ID"

# Verifica deploy
echo ""
echo "✅ Deploy completato!"
echo "🌐 URL: https://$SERVICE_NAME-$REGION.run.app"

# Test rapido
echo ""
echo "🧪 Test rapido del deploy..."
curl -X GET "https://$SERVICE_NAME-$REGION.run.app/health" || echo "⚠️ Health check non disponibile"

echo ""
echo "🎯 Sofia AI refactorizzata deployata su staging!"
echo "📊 Monitora i log: gcloud logging read 'resource.type=cloud_run_revision' --project=$PROJECT_ID --limit=50" 