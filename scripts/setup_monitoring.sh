#!/bin/bash
"""
Sofia Lite - Monitoring Setup Script
Configures Cloud Tasks scheduler for synthetic monitoring.
"""

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

# Create HTTP task for synthetic monitoring
echo "📋 Creating synthetic monitoring task..."
gcloud tasks create-http-task sofia-ping \
    --queue=sofia-monitoring \
    --location=$REGION \
    --url="$SERVICE_URL/webhook/whatsapp" \
    --method=POST \
    --header="Content-Type=application/x-www-form-urlencoded" \
    --body="From=whatsapp:+14155550123&Body=Ping" \
    --schedule="*/15 * * * *" \
    --description="Sofia Lite synthetic monitoring - every 15 minutes"

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

# Create log sink for monitoring
echo "📋 Creating log sink for monitoring..."
gcloud logging sinks create sofia-monitoring-sink \
    bigquery.googleapis.com/projects/$PROJECT_ID/datasets/sofia_monitoring \
    --log-filter='resource.type="cloud_run_revision" AND resource.labels.service_name="sofia-lite" AND (jsonPayload.last_reply_state!="ASK_SERVICE" OR severity>=ERROR)' \
    --location=$REGION

# Create BigQuery dataset for monitoring data
echo "📋 Creating BigQuery dataset..."
bq mk --location=$REGION sofia_monitoring

# Create monitoring table
echo "📋 Creating monitoring table..."
bq mk --table \
    --schema=scripts/monitoring_schema.json \
    sofia_monitoring:conversation_states

# Create Cloud Function for alerting
echo "📋 Creating Cloud Function for alerting..."
gcloud functions deploy sofia-alerting \
    --runtime=python311 \
    --trigger-topic=sofia-monitoring-alerts \
    --entry-point=process_alert \
    --source=scripts/alerting_function \
    --region=$REGION \
    --memory=256MB \
    --timeout=60s

# Create Pub/Sub topic for alerts
echo "📋 Creating Pub/Sub topic for alerts..."
gcloud pubsub topics create sofia-monitoring-alerts

# Create monitoring dashboard
echo "📋 Creating monitoring dashboard..."
gcloud monitoring dashboards create \
    --config=scripts/monitoring_dashboard.json

echo ""
echo "✅ Monitoring setup completed!"
echo ""
echo "📊 Monitoring Components:"
echo "  - Cloud Tasks queue: sofia-monitoring"
echo "  - Scheduler job: sofia-monitoring-job"
echo "  - Log sink: sofia-monitoring-sink"
echo "  - BigQuery dataset: sofia_monitoring"
echo "  - Alerting function: sofia-alerting"
echo "  - Pub/Sub topic: sofia-monitoring-alerts"
echo ""
echo "🔍 To monitor:"
echo "  gcloud logging read 'resource.type=\"cloud_run_revision\"' --limit=10"
echo "  bq query 'SELECT * FROM sofia_monitoring.conversation_states LIMIT 10'"
echo ""
echo "🚨 Alerts will be sent to: sofia-monitoring-alerts topic" 