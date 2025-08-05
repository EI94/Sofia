"""
Sofia Lite - Alerting Cloud Function
Processes alerts when conversations don't reach ASK_SERVICE state.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud import pubsub_v1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_alert(event, context):
    """
    Process monitoring alerts for Sofia Lite.
    
    Args:
        event: Pub/Sub event containing alert data
        context: Cloud Function context
    """
    try:
        # Parse Pub/Sub message
        pubsub_message = event['data']
        alert_data = json.loads(pubsub_message.decode('utf-8'))
        
        logger.info(f"🚨 Processing alert: {alert_data}")
        
        # Extract alert information
        phone = alert_data.get('phone', 'unknown')
        state = alert_data.get('state', 'unknown')
        intent = alert_data.get('intent', 'unknown')
        error = alert_data.get('error', '')
        revision = alert_data.get('revision', 'unknown')
        timestamp = alert_data.get('timestamp', datetime.now().isoformat())
        
        # Check if this is a critical alert
        is_critical = (
            state != "ASK_SERVICE" or 
            error or 
            intent == "ERROR" or
            state == "CLOSED"
        )
        
        if is_critical:
            # Send critical alert
            send_critical_alert(phone, state, intent, error, revision, timestamp)
        
        # Log to BigQuery for analysis
        log_alert_to_bigquery(alert_data)
        
        # Update monitoring metrics
        update_monitoring_metrics(alert_data)
        
        logger.info(f"✅ Alert processed successfully")
        
    except Exception as e:
        logger.error(f"❌ Error processing alert: {e}")
        raise

def send_critical_alert(phone, state, intent, error, revision, timestamp):
    """
    Send critical alert via multiple channels.
    """
    try:
        # Create alert message
        alert_message = f"""
🚨 Sofia Lite Critical Alert

📱 Phone: {phone}
🎯 State: {state}
🧠 Intent: {intent}
🔧 Revision: {revision}
⏰ Timestamp: {timestamp}
❌ Error: {error if error else 'None'}

🔍 Investigation needed!
        """.strip()
        
        # Send to Slack (if configured)
        slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        if slack_webhook:
            send_slack_alert(alert_message, slack_webhook)
        
        # Send to email (if configured)
        email_topic = os.getenv('EMAIL_ALERT_TOPIC')
        if email_topic:
            send_email_alert(alert_message, email_topic)
        
        # Send to PagerDuty (if configured)
        pagerduty_key = os.getenv('PAGERDUTY_API_KEY')
        if pagerduty_key:
            send_pagerduty_alert(alert_message, pagerduty_key)
        
        logger.info(f"📢 Critical alert sent for phone: {phone}")
        
    except Exception as e:
        logger.error(f"❌ Error sending critical alert: {e}")

def send_slack_alert(message, webhook_url):
    """Send alert to Slack."""
    import requests
    
    payload = {
        "text": message,
        "channel": "#sofia-alerts",
        "username": "Sofia Monitor",
        "icon_emoji": ":warning:"
    }
    
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

def send_email_alert(message, topic_name):
    """Send alert via email."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(os.getenv('GOOGLE_CLOUD_PROJECT'), topic_name)
    
    email_data = {
        "to": ["devops@studioimmigrato.it"],
        "subject": "Sofia Lite Critical Alert",
        "body": message
    }
    
    future = publisher.publish(topic_path, json.dumps(email_data).encode('utf-8'))
    future.result()

def send_pagerduty_alert(message, api_key):
    """Send alert to PagerDuty."""
    import requests
    
    headers = {
        "Authorization": f"Token token={api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "routing_key": os.getenv('PAGERDUTY_ROUTING_KEY'),
        "event_action": "trigger",
        "payload": {
            "summary": "Sofia Lite Critical Alert",
            "severity": "critical",
            "source": "sofia-lite-monitoring",
            "custom_details": message
        }
    }
    
    response = requests.post(
        "https://events.pagerduty.com/v2/enqueue",
        headers=headers,
        json=payload
    )
    response.raise_for_status()

def log_alert_to_bigquery(alert_data):
    """
    Log alert to BigQuery for analysis.
    """
    try:
        client = bigquery.Client()
        
        # Prepare data for BigQuery
        row = {
            "timestamp": datetime.now(),
            "phone": alert_data.get('phone', 'unknown'),
            "conversation_id": alert_data.get('conversation_id', 'unknown'),
            "message": alert_data.get('message', ''),
            "reply": alert_data.get('reply', ''),
            "intent": alert_data.get('intent', 'unknown'),
            "state": alert_data.get('state', 'unknown'),
            "lang": alert_data.get('lang', 'unknown'),
            "channel": alert_data.get('channel', 'unknown'),
            "response_time_ms": alert_data.get('response_time_ms'),
            "error": alert_data.get('error', ''),
            "revision": alert_data.get('revision', 'unknown'),
            "region": os.getenv('GOOGLE_CLOUD_REGION', 'unknown'),
            "user_type": alert_data.get('user_type', 'unknown'),
            "abuse_detected": alert_data.get('abuse_detected', False),
            "escalated": alert_data.get('escalated', False),
            "metadata": json.dumps(alert_data.get('metadata', {}))
        }
        
        # Insert into BigQuery
        dataset_id = "sofia_monitoring"
        table_id = "conversation_states"
        table_ref = client.dataset(dataset_id).table(table_id)
        
        errors = client.insert_rows_json(table_ref, [row])
        if errors:
            logger.error(f"❌ BigQuery insert errors: {errors}")
        else:
            logger.info(f"✅ Alert logged to BigQuery")
            
    except Exception as e:
        logger.error(f"❌ Error logging to BigQuery: {e}")

def update_monitoring_metrics(alert_data):
    """
    Update monitoring metrics for dashboards.
    """
    try:
        from google.cloud import monitoring_v3
        
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        
        # Create time series for alert metrics
        series = monitoring_v3.TimeSeries()
        series.metric.type = "custom.googleapis.com/sofia/alerts"
        series.resource.type = "global"
        series.resource.labels["project_id"] = os.getenv('GOOGLE_CLOUD_PROJECT')
        
        # Set metric labels
        series.metric.labels["state"] = alert_data.get('state', 'unknown')
        series.metric.labels["intent"] = alert_data.get('intent', 'unknown')
        series.metric.labels["revision"] = alert_data.get('revision', 'unknown')
        series.metric.labels["channel"] = alert_data.get('channel', 'unknown')
        
        # Set point value
        point = monitoring_v3.Point()
        point.value.int64_value = 1
        point.interval.end_time.seconds = int(datetime.now().timestamp())
        series.points = [point]
        
        # Write time series
        client.create_time_series(request={"name": project_name, "time_series": [series]})
        
        logger.info(f"✅ Monitoring metrics updated")
        
    except Exception as e:
        logger.error(f"❌ Error updating metrics: {e}")

def check_health(event, context):
    """
    Health check endpoint for the Cloud Function.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "function": "sofia-alerting"
    } 