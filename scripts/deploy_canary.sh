#!/bin/bash
"""
Sofia Lite - Canary Deployment Script
Deploys new version with 1% traffic for canary testing.
"""

set -e

PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"europe-west1"}
SERVICE_NAME=${3:-"sofia-lite"}

echo "🚀 Sofia Lite Canary Deployment"
echo "==============================="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo ""

# Get current git SHA
SHORT_SHA=$(git rev-parse --short HEAD)
FULL_SHA=$(git rev-parse HEAD)

echo "📋 Build Information:"
echo "  - Short SHA: $SHORT_SHA"
echo "  - Full SHA: $FULL_SHA"
echo "  - Branch: $(git branch --show-current)"
echo ""

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run: gcloud auth login"
    exit 1
fi

# Set project
echo "📋 Setting project..."
gcloud config set project $PROJECT_ID

# Build and push Docker image
echo "🐳 Building and pushing Docker image..."
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME:$SHORT_SHA"
docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME

echo "✅ Image pushed: $IMAGE_NAME"

# Deploy new revision with canary traffic
echo "🚀 Deploying new revision with canary traffic..."
gcloud run deploy $SERVICE_NAME \
    --image=$IMAGE_NAME \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --memory=4Gi \
    --cpu=2 \
    --max-instances=100 \
    --min-instances=1 \
    --concurrency=80 \
    --timeout=300 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
    --set-env-vars="REVISION=$SHORT_SHA" \
    --update-env-vars="DEPLOYMENT_TYPE=canary" \
    --update-secrets="OPENAI_API_KEY=openai-api-key:latest" \
    --update-secrets="ELEVENLABS_API_KEY=elevenlabs-api-key:latest" \
    --update-secrets="TWILIO_ACCOUNT_SID=twilio-account-sid:latest" \
    --update-secrets="TWILIO_AUTH_TOKEN=twilio-auth-token:latest" \
    --set-cloudsql-instances="" \
    --port=8000

# Get the new revision name
NEW_REVISION=$(gcloud run revisions list --service=$SERVICE_NAME --region=$REGION --limit=1 --format="value(metadata.name)")

echo "✅ New revision deployed: $NEW_REVISION"

# Update traffic split: 99% stable, 1% canary
echo "📊 Updating traffic split..."
gcloud run services update-traffic $SERVICE_NAME \
    --region=$REGION \
    --to-revisions="$NEW_REVISION=1,stable=99"

echo "✅ Traffic split updated: 1% canary, 99% stable"

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
sleep 30

# Run health checks
echo "🏥 Running health checks..."
HEALTH_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

# Test canary endpoint
CANARY_URL="$HEALTH_URL"
echo "🔍 Testing canary endpoint: $CANARY_URL"

# Send test request
TEST_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/test_response.txt "$CANARY_URL/health" || echo "000")
HTTP_CODE="${TEST_RESPONSE: -3}"

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Canary health check: PASSED"
else
    echo "❌ Canary health check: FAILED (HTTP $HTTP_CODE)"
    cat /tmp/test_response.txt
    exit 1
fi

# Test synthetic monitoring
echo "🧪 Testing synthetic monitoring..."
MONITOR_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/monitor_response.txt \
    -X POST "$CANARY_URL/webhook/whatsapp" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "From=whatsapp:+14155550123&Body=Ping" || echo "000")
MONITOR_CODE="${MONITOR_RESPONSE: -3}"

if [ "$MONITOR_CODE" = "200" ]; then
    echo "✅ Synthetic monitoring: PASSED"
else
    echo "❌ Synthetic monitoring: FAILED (HTTP $MONITOR_CODE)"
    cat /tmp/monitor_response.txt
fi

# Get current traffic split
echo "📊 Current traffic split:"
gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(spec.traffic[].percent,spec.traffic[].revisionName)" | paste -d'% ' - -

# Create monitoring alert for canary
echo "🚨 Setting up canary monitoring alerts..."
gcloud monitoring policies create \
    --policy-from-file=scripts/canary_alert_policy.json

echo ""
echo "🎉 Canary deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "  - Image: $IMAGE_NAME"
echo "  - Revision: $NEW_REVISION"
echo "  - Traffic: 1% canary, 99% stable"
echo "  - Health: ✅ PASSED"
echo "  - Monitoring: ✅ ACTIVE"
echo ""
echo "🔍 Monitor canary performance:"
echo "  gcloud run services describe $SERVICE_NAME --region=$REGION"
echo "  gcloud logging read 'resource.type=\"cloud_run_revision\" AND resource.labels.revision_name=\"$NEW_REVISION\"' --limit=10"
echo ""
echo "📈 View monitoring dashboard:"
echo "  https://console.cloud.google.com/monitoring/dashboards?project=$PROJECT_ID"
echo ""
echo "🔄 To promote canary to stable:"
echo "  ./scripts/promote_canary.sh $PROJECT_ID $REGION $SERVICE_NAME"
echo ""
echo "🔄 To rollback canary:"
echo "  ./scripts/rollback_canary.sh $PROJECT_ID $REGION $SERVICE_NAME" 