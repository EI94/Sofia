#!/bin/bash
# Sofia Lite - Monitoring Setup Script
# Configures Cloud Tasks scheduler for synthetic monitoring.

set -e

PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"europe-west1"}
SERVICE_URL=${3:-"https://sofia-lite-xxxxx-ew.a.run.app"}

echo "🚀 Setting up Sofia Lite Monitoring"
echo "=================================="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service URL: $SERVICE_URL"
echo ""

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run: gcloud auth login"
    exit 1
fi

# Set project
echo "📋 Setting project..."
gcloud config set project $PROJECT_ID

# Create Cloud Tasks queue for monitoring
echo "📋 Creating Cloud Tasks queue..."
gcloud tasks queues create sofia-monitoring \
    --location=$REGION \
    --max-concurrent-dispatches=10 \
    --max-attempts=3 \
    --min-backoff=10s \
    --max-backoff=300s \
    --max-doublings=5

# Create Cloud Scheduler job
echo "📋 Creating Cloud Scheduler job..."
gcloud scheduler jobs create http sofia-monitoring-job \
    --location=$REGION \
    --schedule="*/15 * * * *" \
    --uri="$SERVICE_URL/webhook/whatsapp" \
    --http-method=POST \
    --headers="Content-Type=application/x-www-form-urlencoded" \
    --message-body="From=whatsapp:+14155550123&Body=Ping" \
    --description="Sofia Lite synthetic monitoring - every 15 minutes"

echo ""
echo "✅ Monitoring setup completed!"
echo ""
echo "📊 Monitoring Components:"
echo "  - Cloud Tasks queue: sofia-monitoring"
echo "  - Scheduler job: sofia-monitoring-job"
echo ""
echo "🔍 To monitor:"
echo "  gcloud logging read 'resource.type=\"cloud_run_revision\"' --limit=10"
