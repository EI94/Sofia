"""
Sistema di Alerting Avanzato per Sofia AI
Monitoring intelligente con soglie dinamiche, escalation e notifiche multi-channel
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from app.tools.journey_analytics import journey_analytics
from app.tools.error_handler import error_handler

logger = logging.getLogger(__name__)

# ===== ENUMS E TYPES =====

class AlertSeverity(Enum):
    """Livelli di severità degli alert"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(Enum):
    """Stati degli alert"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged" 
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

class AlertCategory(Enum):
    """Categorie di alert"""
    SYSTEM_HEALTH = "system_health"
    USER_EXPERIENCE = "user_experience"
    CONVERSION_METRICS = "conversion_metrics"
    ERROR_RATES = "error_rates"
    RESOURCE_USAGE = "resource_usage"
    SECURITY = "security"

class NotificationChannel(Enum):
    """Canali di notifica disponibili"""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    DISCORD = "discord"

# ===== DATA CLASSES =====

@dataclass
class AlertThreshold:
    """Soglia di alert con condizioni"""
    metric_name: str
    operator: str  # >, <, >=, <=, ==, !=
    value: float
    duration_minutes: int = 5  # Per quanto tempo deve persistere
    description: str = ""

@dataclass  
class AlertRule:
    """Regola di alerting"""
    rule_id: str
    name: str
    category: AlertCategory
    severity: AlertSeverity
    thresholds: List[AlertThreshold]
    enabled: bool = True
    cooldown_minutes: int = 15
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    escalation_minutes: int = 60  # Escalation dopo N minuti
    escalation_channels: List[NotificationChannel] = field(default_factory=list)
    description: str = ""

@dataclass
class Alert:
    """Alert attivo"""
    alert_id: str
    rule_id: str
    name: str
    category: AlertCategory
    severity: AlertSeverity
    status: AlertStatus
    triggered_at: datetime
    last_triggered: datetime
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    count: int = 1  # Quante volte è scattato
    current_value: Optional[float] = None
    threshold_value: Optional[float] = None
    context: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Converte alert in dict per serializzazione"""
        return {
            "alert_id": self.alert_id,
            "rule_id": self.rule_id,
            "name": self.name,
            "category": self.category.value,
            "severity": self.severity.value,
            "status": self.status.value,
            "triggered_at": self.triggered_at.isoformat(),
            "last_triggered": self.last_triggered.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "acknowledged_by": self.acknowledged_by,
            "count": self.count,
            "current_value": self.current_value,
            "threshold_value": self.threshold_value,
            "context": self.context,
            "notes": self.notes
        }

# ===== ALERTING SYSTEM MAIN CLASS =====

class SofiaAlertingSystem:
    """Sistema di alerting intelligente per Sofia AI"""
    
    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.notification_configs: Dict[NotificationChannel, Dict] = {}
        self.metric_cache: Dict[str, Any] = {}
        self.last_check: Optional[datetime] = None
        
        # Inizializza regole predefinite
        self._setup_default_rules()
        
        # Task asincroni
        self.monitoring_task: Optional[asyncio.Task] = None
        self.running = False
        
        logger.info("🚨 Sofia Alerting System initialized")

    def _setup_default_rules(self):
        """Configura regole di alerting predefinite"""
        
        # 1. Alert per conversion rate bassa
        self.add_rule(AlertRule(
            rule_id="low_conversion_rate", 
            name="Low Conversion Rate",
            category=AlertCategory.CONVERSION_METRICS,
            severity=AlertSeverity.MEDIUM,
            thresholds=[
                AlertThreshold(
                    metric_name="conversion_rate_24h",
                    operator="<",
                    value=3.0,
                    duration_minutes=10,
                    description="Conversion rate under 3% for 10 minutes"
                )
            ],
            cooldown_minutes=30,
            notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
            description="Monitors 24-hour conversion rate"
        ))
        
        # 2. Alert per alto tasso di errori
        self.add_rule(AlertRule(
            rule_id="high_error_rate",
            name="High Error Rate", 
            category=AlertCategory.ERROR_RATES,
            severity=AlertSeverity.HIGH,
            thresholds=[
                AlertThreshold(
                    metric_name="errors_per_hour",
                    operator=">",
                    value=10,
                    duration_minutes=5,
                    description="More than 10 errors per hour"
                )
            ],
            cooldown_minutes=15,
            notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
            escalation_minutes=30,
            escalation_channels=[NotificationChannel.SMS],
            description="Monitors system error rates"
        ))
        
        # 3. Alert per memoria alta
        self.add_rule(AlertRule(
            rule_id="high_memory_usage",
            name="High Memory Usage",
            category=AlertCategory.RESOURCE_USAGE,
            severity=AlertSeverity.MEDIUM,
            thresholds=[
                AlertThreshold(
                    metric_name="memory_usage_mb",
                    operator=">",
                    value=200,
                    duration_minutes=5,
                    description="Memory usage over 200MB"
                )
            ],
            cooldown_minutes=20,
            notification_channels=[NotificationChannel.EMAIL],
            description="Monitors system memory usage"
        ))
        
        # 4. Alert per nessuna attività utenti
        self.add_rule(AlertRule(
            rule_id="no_user_activity",
            name="No User Activity",
            category=AlertCategory.USER_EXPERIENCE,
            severity=AlertSeverity.LOW,
            thresholds=[
                AlertThreshold(
                    metric_name="active_users_1h",
                    operator="==",
                    value=0,
                    duration_minutes=60,
                    description="No active users for 1 hour"
                )
            ],
            cooldown_minutes=120,
            notification_channels=[NotificationChannel.EMAIL],
            description="Monitors user activity levels"
        ))
        
        # 5. Alert critico per sistema inattivo
        self.add_rule(AlertRule(
            rule_id="system_down",
            name="System Potentially Down",
            category=AlertCategory.SYSTEM_HEALTH,
            severity=AlertSeverity.CRITICAL,
            thresholds=[
                AlertThreshold(
                    metric_name="events_1h",
                    operator="==",
                    value=0,
                    duration_minutes=30,
                    description="No events processed in 30 minutes"
                )
            ],
            cooldown_minutes=10,
            notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.SMS],
            description="Critical system health check"
        ))

    # ===== RULE MANAGEMENT =====

    def add_rule(self, rule: AlertRule) -> bool:
        """
        Aggiunge una regola di alerting
        
        Args:
            rule: Regola da aggiungere
            
        Returns:
            bool: True se aggiunta con successo
        """
        try:
            self.rules[rule.rule_id] = rule
            logger.info(f"✅ Alert rule added: {rule.name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to add alert rule: {e}")
            return False

    def remove_rule(self, rule_id: str) -> bool:
        """Rimuove una regola di alerting"""
        try:
            if rule_id in self.rules:
                del self.rules[rule_id]
                logger.info(f"🗑️ Alert rule removed: {rule_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to remove alert rule: {e}")
            return False

    def enable_rule(self, rule_id: str) -> bool:
        """Attiva una regola"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            logger.info(f"✅ Alert rule enabled: {rule_id}")
            return True
        return False

    def disable_rule(self, rule_id: str) -> bool:
        """Disattiva una regola"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            logger.info(f"⏸️ Alert rule disabled: {rule_id}")
            return True
        return False

    # ===== MONITORING CORE =====

    async def start_monitoring(self):
        """Avvia il monitoring continuo"""
        if self.running:
            logger.warning("⚠️ Monitoring already running")
            return
            
        self.running = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("🚀 Alert monitoring started")

    async def stop_monitoring(self):
        """Ferma il monitoring"""
        self.running = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Alert monitoring stopped")

    async def _monitoring_loop(self):
        """Loop principale di monitoring"""
        while self.running:
            try:
                await self.check_all_rules()
                await asyncio.sleep(60)  # Check ogni minuto
            except Exception as e:
                logger.error(f"❌ Monitoring loop error: {e}")
                await asyncio.sleep(10)  # Attesa più breve in caso di errore

    async def check_all_rules(self):
        """Controlla tutte le regole di alerting"""
        current_time = datetime.now()
        
        try:
            # Ottieni metriche correnti
            await self._update_metrics()
            
            for rule_id, rule in self.rules.items():
                if not rule.enabled:
                    continue
                    
                try:
                    await self._check_rule(rule, current_time)
                except Exception as e:
                    logger.error(f"❌ Error checking rule {rule_id}: {e}")
            
            # Cleanup alert risolti automaticamente
            await self._cleanup_resolved_alerts()
            
            self.last_check = current_time
            
        except Exception as e:
            logger.error(f"❌ Error in check_all_rules: {e}")

    async def _update_metrics(self):
        """Aggiorna cache delle metriche"""
        try:
            # Metriche real-time
            realtime_metrics = await journey_analytics.get_real_time_metrics()
            self.metric_cache.update(realtime_metrics["metrics"])
            
            # Metriche di sistema
            system_stats = journey_analytics.get_system_stats()
            self.metric_cache.update(system_stats)
            
            # Metriche errori
            error_stats = error_handler.get_error_stats()
            self.metric_cache["errors_per_hour"] = error_stats["recent_errors_1h"]
            self.metric_cache["total_errors"] = error_stats["total_errors"]
            
        except Exception as e:
            logger.error(f"❌ Failed to update metrics: {e}")

    async def _check_rule(self, rule: AlertRule, current_time: datetime):
        """Controlla una singola regola"""
        
        # Controlla cooldown
        existing_alert = next(
            (alert for alert in self.active_alerts.values() 
             if alert.rule_id == rule.rule_id and alert.status == AlertStatus.ACTIVE),
            None
        )
        
        if existing_alert:
            cooldown_end = existing_alert.last_triggered + timedelta(minutes=rule.cooldown_minutes)
            if current_time < cooldown_end:
                return  # Ancora in cooldown
        
        # Valuta tutte le soglie
        triggered_thresholds = []
        for threshold in rule.thresholds:
            if self._evaluate_threshold(threshold):
                triggered_thresholds.append(threshold)
        
        # Se almeno una soglia è scattata
        if triggered_thresholds:
            await self._trigger_alert(rule, triggered_thresholds, current_time)
        elif existing_alert and existing_alert.status == AlertStatus.ACTIVE:
            # Nessuna soglia scattata ma alert attivo - potenziale risoluzione
            await self._check_auto_resolve(existing_alert, current_time)

    def _evaluate_threshold(self, threshold: AlertThreshold) -> bool:
        """Valuta se una soglia è stata superata"""
        metric_value = self.metric_cache.get(threshold.metric_name)
        if metric_value is None:
            return False
        
        try:
            # Valuta condizione
            if threshold.operator == ">":
                return metric_value > threshold.value
            elif threshold.operator == "<":
                return metric_value < threshold.value 
            elif threshold.operator == ">=":
                return metric_value >= threshold.value
            elif threshold.operator == "<=":
                return metric_value <= threshold.value
            elif threshold.operator == "==":
                return metric_value == threshold.value
            elif threshold.operator == "!=":
                return metric_value != threshold.value
            else:
                logger.error(f"❌ Unknown operator: {threshold.operator}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error evaluating threshold: {e}")
            return False

    async def _trigger_alert(self, rule: AlertRule, thresholds: List[AlertThreshold], current_time: datetime):
        """Scatena un alert"""
        
        # Controlla se esiste già
        existing_alert = next(
            (alert for alert in self.active_alerts.values()
             if alert.rule_id == rule.rule_id),
            None
        )
        
        if existing_alert:
            # Aggiorna alert esistente
            existing_alert.count += 1
            existing_alert.last_triggered = current_time
            existing_alert.current_value = self.metric_cache.get(thresholds[0].metric_name)
            
            logger.info(f"🔄 Alert updated: {rule.name} (count: {existing_alert.count})")
        else:
            # Crea nuovo alert
            alert = Alert(
                alert_id=f"alert_{rule.rule_id}_{int(current_time.timestamp())}",
                rule_id=rule.rule_id,
                name=rule.name,
                category=rule.category,
                severity=rule.severity,
                status=AlertStatus.ACTIVE,
                triggered_at=current_time,
                last_triggered=current_time,
                current_value=self.metric_cache.get(thresholds[0].metric_name),
                threshold_value=thresholds[0].value,
                context={
                    "triggered_thresholds": [
                        {
                            "metric": t.metric_name,
                            "operator": t.operator,
                            "threshold": t.value,
                            "current": self.metric_cache.get(t.metric_name)
                        }
                        for t in thresholds
                    ],
                    "all_metrics": dict(self.metric_cache)
                }
            )
            
            self.active_alerts[alert.alert_id] = alert
            self.alert_history.append(alert)
            
            logger.warning(f"🚨 New alert triggered: {rule.name}")
        
        # Invia notifiche
        await self._send_notifications(rule, existing_alert or alert)

    async def _check_auto_resolve(self, alert: Alert, current_time: datetime):
        """Controlla se un alert può essere risolto automaticamente"""
        rule = self.rules.get(alert.rule_id)
        if not rule:
            return
            
        # Se nessuna soglia è più scattata, risolvi
        any_threshold_triggered = any(
            self._evaluate_threshold(threshold) for threshold in rule.thresholds
        )
        
        if not any_threshold_triggered:
            await self.resolve_alert(alert.alert_id, "system", "Auto-resolved - thresholds no longer exceeded")

    # ===== ALERT MANAGEMENT =====

    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str, note: str = "") -> bool:
        """Riconosce un alert"""
        if alert_id not in self.active_alerts:
            return False
            
        alert = self.active_alerts[alert_id]
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = datetime.now()
        alert.acknowledged_by = acknowledged_by
        
        if note:
            alert.notes.append(f"[{datetime.now()}] Acknowledged by {acknowledged_by}: {note}")
        
        logger.info(f"✅ Alert acknowledged: {alert.name} by {acknowledged_by}")
        return True

    async def resolve_alert(self, alert_id: str, resolved_by: str, note: str = "") -> bool:
        """Risolve un alert"""
        if alert_id not in self.active_alerts:
            return False
            
        alert = self.active_alerts[alert_id]
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.now()
        
        if note:
            alert.notes.append(f"[{datetime.now()}] Resolved by {resolved_by}: {note}")
        
        # Rimuovi dagli alert attivi
        del self.active_alerts[alert_id]
        
        logger.info(f"✅ Alert resolved: {alert.name} by {resolved_by}")
        return True

    async def suppress_alert(self, alert_id: str, suppressed_by: str, duration_minutes: int = 60) -> bool:
        """Sopprime temporaneamente un alert"""
        if alert_id not in self.active_alerts:
            return False
            
        alert = self.active_alerts[alert_id]
        alert.status = AlertStatus.SUPPRESSED
        alert.notes.append(
            f"[{datetime.now()}] Suppressed by {suppressed_by} for {duration_minutes} minutes"
        )
        
        # Programma riattivazione automatica
        async def reactivate():
            await asyncio.sleep(duration_minutes * 60)
            if alert_id in self.active_alerts:
                self.active_alerts[alert_id].status = AlertStatus.ACTIVE
                logger.info(f"🔄 Alert reactivated after suppression: {alert.name}")
        
        asyncio.create_task(reactivate())
        
        logger.info(f"🔇 Alert suppressed: {alert.name} for {duration_minutes} minutes")
        return True

    async def _cleanup_resolved_alerts(self):
        """Pulisce alert risolti dalla storia (mantieni solo ultimi 100)"""
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]

    # ===== NOTIFICATIONS =====

    async def _send_notifications(self, rule: AlertRule, alert: Alert):
        """Invia notifiche per un alert"""
        try:
            # Determina canali di notifica
            channels = rule.notification_channels.copy()
            
            # Escalation se necessario
            if alert.count > 1 and rule.escalation_minutes:
                time_since_first = (alert.last_triggered - alert.triggered_at).total_seconds() / 60
                if time_since_first >= rule.escalation_minutes:
                    channels.extend(rule.escalation_channels)
            
            # Invia su ogni canale
            for channel in channels:
                try:
                    await self._send_notification_to_channel(channel, alert, rule)
                except Exception as e:
                    logger.error(f"❌ Failed to send notification to {channel.value}: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Error sending notifications: {e}")

    async def _send_notification_to_channel(self, channel: NotificationChannel, alert: Alert, rule: AlertRule):
        """Invia notifica su un canale specifico"""
        
        message = self._format_alert_message(alert, rule)
        
        if channel == NotificationChannel.EMAIL:
            await self._send_email_notification(alert, message)
        elif channel == NotificationChannel.SLACK:
            await self._send_slack_notification(alert, message)
        elif channel == NotificationChannel.WEBHOOK:
            await self._send_webhook_notification(alert, message)
        elif channel == NotificationChannel.SMS:
            await self._send_sms_notification(alert, message)
        else:
            logger.warning(f"⚠️ Unsupported notification channel: {channel.value}")

    def _format_alert_message(self, alert: Alert, rule: AlertRule) -> str:
        """Formatta messaggio di alert"""
        
        severity_emoji = {
            AlertSeverity.LOW: "ℹ️",
            AlertSeverity.MEDIUM: "⚠️", 
            AlertSeverity.HIGH: "🚨",
            AlertSeverity.CRITICAL: "🔥"
        }
        
        emoji = severity_emoji.get(alert.severity, "🔔")
        
        message = f"""
{emoji} SOFIA AI ALERT {emoji}

Alert: {alert.name}
Severity: {alert.severity.value.upper()}
Category: {alert.category.value.replace('_', ' ').title()}
Triggered: {alert.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}
Count: {alert.count}

Current Value: {alert.current_value}
Threshold: {alert.threshold_value}

Description: {rule.description}

Context:
{json.dumps(alert.context.get('triggered_thresholds', []), indent=2)}

Alert ID: {alert.alert_id}
        """.strip()
        
        return message

    async def _send_email_notification(self, alert: Alert, message: str):
        """Invia notifica email"""
        # Implementazione email placeholder
        logger.info(f"📧 Would send email notification: {alert.name}")

    async def _send_slack_notification(self, alert: Alert, message: str):
        """Invia notifica Slack"""  
        # Implementazione Slack placeholder
        logger.info(f"💬 Would send Slack notification: {alert.name}")

    async def _send_webhook_notification(self, alert: Alert, message: str):
        """Invia notifica webhook"""
        # Implementazione webhook placeholder
        logger.info(f"🔗 Would send webhook notification: {alert.name}")

    async def _send_sms_notification(self, alert: Alert, message: str):
        """Invia notifica SMS"""
        # Implementazione SMS placeholder
        logger.info(f"📱 Would send SMS notification: {alert.name}")

    # ===== API METHODS =====

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Ottieni tutti gli alert attivi"""
        return [alert.to_dict() for alert in self.active_alerts.values()]

    def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Ottieni cronologia alert"""
        recent_alerts = sorted(self.alert_history, key=lambda x: x.triggered_at, reverse=True)
        return [alert.to_dict() for alert in recent_alerts[:limit]]

    def get_alert_statistics(self) -> Dict[str, Any]:
        """Ottieni statistiche alert"""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        last_week = now - timedelta(days=7)
        
        recent_alerts = [a for a in self.alert_history if a.triggered_at >= last_24h]
        week_alerts = [a for a in self.alert_history if a.triggered_at >= last_week]
        
        return {
            "active_alerts": len(self.active_alerts),
            "alerts_24h": len(recent_alerts),
            "alerts_7d": len(week_alerts),
            "total_rules": len(self.rules),
            "enabled_rules": len([r for r in self.rules.values() if r.enabled]),
            "by_severity": {
                severity.value: len([a for a in self.active_alerts.values() if a.severity == severity])
                for severity in AlertSeverity
            },
            "by_category": {
                category.value: len([a for a in recent_alerts if a.category == category])
                for category in AlertCategory
            },
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "monitoring_active": self.running
        }

    def get_rules_summary(self) -> List[Dict[str, Any]]:
        """Ottieni riassunto delle regole"""
        return [
            {
                "rule_id": rule.rule_id,
                "name": rule.name,
                "category": rule.category.value,
                "severity": rule.severity.value,
                "enabled": rule.enabled,
                "thresholds_count": len(rule.thresholds),
                "notification_channels": [c.value for c in rule.notification_channels],
                "cooldown_minutes": rule.cooldown_minutes,
                "description": rule.description
            }
            for rule in self.rules.values()
        ]


# ===== GLOBAL INSTANCE =====

# Istanza globale del sistema di alerting
alerting_system = SofiaAlertingSystem()

# Export per compatibilità
__all__ = [
    'SofiaAlertingSystem',
    'AlertSeverity', 
    'AlertStatus',
    'AlertCategory',
    'NotificationChannel',
    'AlertRule',
    'AlertThreshold', 
    'Alert',
    'alerting_system'
] 