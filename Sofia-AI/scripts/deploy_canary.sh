#!/bin/bash
# Sofia Lite - Canary Deployment Script
# Deploys new version with 1% traffic for canary testing.

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

echo "📋 Build Information:"
echo "  - Short SHA: $SHORT_SHA"
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

echo ""
echo "🎉 Canary deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "  - Image: $IMAGE_NAME"
echo "  - Revision: $NEW_REVISION"
echo "  - Traffic: 1% canary, 99% stable"
echo ""
echo "🔍 Monitor canary performance:"
echo "  gcloud run services describe $SERVICE_NAME --region=$REGION"
