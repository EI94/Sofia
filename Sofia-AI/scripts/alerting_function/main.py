"""
Sofia Lite - Alerting Cloud Function
Processes alerts when conversations don't reach ASK_SERVICE state.
"""

import json
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_alert(event, context):
    """Process monitoring alerts for Sofia Lite."""
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
        
        # Check if this is a critical alert
        is_critical = (
            state != "ASK_SERVICE" or 
            error or 
            intent == "ERROR" or
            state == "CLOSED"
        )
        
        if is_critical:
            logger.warning(f"🚨 Critical alert for {phone}: state={state}, intent={intent}")
        
        logger.info(f"✅ Alert processed successfully")
        
    except Exception as e:
        logger.error(f"❌ Error processing alert: {e}")
        raise

def check_health(event, context):
    """Health check endpoint for the Cloud Function."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "function": "sofia-alerting"
    }
