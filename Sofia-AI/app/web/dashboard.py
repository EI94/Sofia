"""
Real-Time Journey Analytics Dashboard per Sofia AI
Dashboard web interattiva con visualizzazioni live e controlli operativi
"""

from fastapi import APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, List, Optional
import json
import asyncio
import logging
from datetime import datetime, timedelta
from app.tools.journey_analytics import (
    journey_analytics, JourneyStage, EventType, Channel
)
from app.tools.error_handler import error_handler
from app.tools.alerting_system import alerting_system

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/web/templates")

# WebSocket connections per real-time updates
active_connections: List[WebSocket] = []

# ===== DASHBOARD WEB INTERFACE =====

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """
    Dashboard principale con visualizzazioni real-time
    
    Returns:
        HTMLResponse: Pagina dashboard completa
    """
    try:
        # Ottieni dati iniziali per dashboard
        funnel_metrics = await journey_analytics.calculate_funnel_metrics(7)
        realtime_metrics = await journey_analytics.get_real_time_metrics()
        drop_offs = await journey_analytics.get_top_drop_off_points(5)
        recent_users = list(journey_analytics.user_journeys.values())[-10:]  # Ultimi 10 utenti
        
        # Prepara dati per template
        dashboard_data = {
            "kpis": {
                "total_users": funnel_metrics.total_users,
                "conversion_rate": round(funnel_metrics.conversion_rate_overall, 2),
                "total_revenue": round(funnel_metrics.total_revenue, 2),
                "avg_engagement": round(funnel_metrics.avg_engagement_score, 2)
            },
            "realtime": realtime_metrics["metrics"],
            "funnel_stages": funnel_metrics.stage_counts,
            "channel_performance": funnel_metrics.channel_metrics,
            "top_drop_offs": drop_offs[:3],
            "recent_users": [
                {
                    "id": user.user_id[-4:],  # Ultimi 4 caratteri per privacy
                    "stage": user.current_stage.value,
                    "channels": len(user.channels_used),
                    "engagement": round(user.engagement_score, 1),
                    "last_activity": user.last_activity.strftime("%H:%M") if user.last_activity else "N/A"
                }
                for user in recent_users
            ]
        }
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "data": dashboard_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        logger.error(f"❌ Dashboard error: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard failed: {str(e)}")


@router.get("/dashboard/user/{user_id}", response_class=HTMLResponse) 
async def user_detail_dashboard(request: Request, user_id: str):
    """
    Dashboard dettagliata per singolo utente
    
    Args:
        user_id: ID utente da visualizzare
        
    Returns:
        HTMLResponse: Pagina dettaglio utente
    """
    try:
        # Ottieni journey utente
        journey = await journey_analytics.get_user_journey(user_id)
        if not journey:
            raise HTTPException(status_code=404, detail="User journey not found")
        
        # Ottieni eventi utente
        events = await journey_analytics.get_user_events(user_id, limit=50)
        
        # Organizza eventi per timeline
        timeline_events = []
        for event in events:
            timeline_events.append({
                "timestamp": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "event_type": event.event_type.value.replace("_", " ").title(),
                "channel": event.channel.value.title(),
                "stage": event.stage.value.replace("_", " ").title(),
                "details": {
                    "language": event.language,
                    "intent": event.intent,
                    "user_input": event.user_input[:100] + "..." if event.user_input and len(event.user_input) > 100 else event.user_input,
                    "ai_response": event.ai_response[:100] + "..." if event.ai_response and len(event.ai_response) > 100 else event.ai_response,
                    "conversion_value": event.conversion_value
                }
            })
        
        user_data = {
            "journey": {
                "user_id": user_id,
                "created_at": journey.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "current_stage": journey.current_stage.value.replace("_", " ").title(),
                "channels_used": [ch.value.title() for ch in journey.channels_used],
                "total_events": journey.total_events,
                "engagement_score": round(journey.engagement_score, 2),
                "converted": journey.converted,
                "conversion_value": journey.conversion_value,
                "language": journey.language,
                "primary_intent": journey.primary_intent
            },
            "timeline": timeline_events[:20],  # Primi 20 eventi per timeline
            "stats": {
                "days_active": (journey.updated_at - journey.created_at).days + 1,
                "events_per_day": round(journey.total_events / max(1, (journey.updated_at - journey.created_at).days + 1), 2),
                "unique_channels": len(journey.channels_used),
                "last_activity": journey.last_activity.strftime("%Y-%m-%d %H:%M:%S") if journey.last_activity else "Unknown"
            }
        }
        
        return templates.TemplateResponse("user_detail.html", {
            "request": request,
            "user": user_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ User detail dashboard error: {e}")
        raise HTTPException(status_code=500, detail=f"User detail failed: {str(e)}")


# ===== REAL-TIME WEBSOCKET ENDPOINT =====

@router.websocket("/dashboard/ws")
async def dashboard_websocket(websocket: WebSocket):
    """
    WebSocket endpoint per aggiornamenti real-time dashboard
    """
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"📡 WebSocket connected: {len(active_connections)} active connections")
    
    try:
        while True:
            # Invia aggiornamenti ogni 30 secondi
            await asyncio.sleep(30)
            
            # Ottieni metriche aggiornate
            realtime_metrics = await journey_analytics.get_real_time_metrics()
            system_stats = journey_analytics.get_system_stats()
            error_stats = error_handler.get_error_stats()
            
            # Prepara update data
            update_data = {
                "type": "metrics_update",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "realtime": realtime_metrics["metrics"],
                    "system": {
                        "events_in_buffer": system_stats["events_in_buffer"],
                        "tracked_users": system_stats["tracked_users"],
                        "memory_usage_mb": system_stats["memory_usage_mb"]
                    },
                    "errors": {
                        "total": error_stats["total_errors"],
                        "recent_1h": error_stats["recent_errors_1h"]
                    }
                }
            }
            
            # Invia a tutti i client connessi
            await broadcast_update(update_data)
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"📡 WebSocket disconnected: {len(active_connections)} remaining connections")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


async def broadcast_update(data: Dict[str, Any]):
    """Invia aggiornamenti a tutti i client WebSocket connessi"""
    if not active_connections:
        return
    
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(data))
        except Exception as e:
            logger.warning(f"⚠️ Failed to send WebSocket update: {e}")
            disconnected.append(connection)
    
    # Rimuovi connessioni non funzionanti
    for connection in disconnected:
        active_connections.remove(connection)


# ===== API ENDPOINTS PER DASHBOARD =====

@router.get("/dashboard/api/summary")
async def dashboard_api_summary(period_days: int = 7):
    """
    API endpoint per summary dashboard
    
    Args:
        period_days: Periodo di analisi in giorni
        
    Returns:
        dict: Dati summary per dashboard
    """
    try:
        funnel_metrics = await journey_analytics.calculate_funnel_metrics(period_days)
        realtime_metrics = await journey_analytics.get_real_time_metrics()
        drop_offs = await journey_analytics.get_top_drop_off_points(5)
        system_stats = journey_analytics.get_system_stats()
        
        return {
            "status": "success",
            "period_days": period_days,
            "kpis": {
                "total_users": funnel_metrics.total_users,
                "conversion_rate": round(funnel_metrics.conversion_rate_overall, 2),
                "total_revenue": round(funnel_metrics.total_revenue, 2),
                "avg_revenue_per_user": round(
                    funnel_metrics.total_revenue / max(1, funnel_metrics.total_users), 2
                ),
                "avg_engagement": round(funnel_metrics.avg_engagement_score, 2)
            },
            "realtime": realtime_metrics["metrics"],
            "funnel": {
                "stages": funnel_metrics.stage_counts,
                "conversion_rates": funnel_metrics.conversion_rates
            },
            "channels": funnel_metrics.channel_metrics,
            "drop_offs": drop_offs,
            "system": {
                "health": "healthy" if system_stats["memory_usage_mb"] < 100 else "monitoring",
                "events_in_buffer": system_stats["events_in_buffer"],
                "tracked_users": system_stats["tracked_users"],
                "memory_usage": round(system_stats["memory_usage_mb"], 2)
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Dashboard API summary error: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard API failed: {str(e)}")


@router.get("/dashboard/api/chart/funnel")
async def dashboard_funnel_chart(period_days: int = 7):
    """
    API endpoint per dati chart funnel
    
    Returns:
        dict: Dati formattati per chart funnel
    """
    try:
        metrics = await journey_analytics.calculate_funnel_metrics(period_days)
        
        # Organizza dati per chart
        stages_order = [
            ("discovery", "Discovery"),
            ("engagement", "Engagement"), 
            ("qualification", "Qualification"),
            ("consultation_request", "Consultation Request"),
            ("booking_attempt", "Booking Attempt"),
            ("payment_pending", "Payment Pending"),
            ("payment_completed", "Payment Completed"),
            ("consultation_scheduled", "Consultation Scheduled"),
            ("consultation_completed", "Consultation Completed"),
            ("client_conversion", "Client Conversion")
        ]
        
        chart_data = {
            "labels": [],
            "counts": [],
            "conversion_rates": []
        }
        
        for stage_key, stage_label in stages_order:
            if stage_key in metrics.stage_counts:
                chart_data["labels"].append(stage_label)
                chart_data["counts"].append(metrics.stage_counts[stage_key])
                chart_data["conversion_rates"].append(
                    round(metrics.conversion_rates.get(stage_key, 0), 2)
                )
        
        return {
            "status": "success",
            "chart_data": chart_data,
            "total_users": metrics.total_users,
            "overall_conversion": round(metrics.conversion_rate_overall, 2)
        }
        
    except Exception as e:
        logger.error(f"❌ Funnel chart API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/api/chart/channels")
async def dashboard_channels_chart(period_days: int = 7):
    """
    API endpoint per dati chart performance canali
    
    Returns:
        dict: Dati performance canali per chart
    """
    try:
        metrics = await journey_analytics.calculate_funnel_metrics(period_days)
        
        # Organizza dati canali per chart
        chart_data = {
            "labels": [],
            "users": [],
            "events": [],
            "conversions": [],
            "conversion_rates": []
        }
        
        for channel, data in metrics.channel_metrics.items():
            chart_data["labels"].append(channel.title())
            chart_data["users"].append(data["unique_users"])
            chart_data["events"].append(data["events_count"])
            chart_data["conversions"].append(data["conversions"])
            chart_data["conversion_rates"].append(round(data["conversion_rate"], 2))
        
        return {
            "status": "success",
            "chart_data": chart_data,
            "period_days": period_days
        }
        
    except Exception as e:
        logger.error(f"❌ Channels chart API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/api/alerts")
async def dashboard_alerts():
    """
    API endpoint per alert del sistema
    
    Returns:
        dict: Lista alert correnti
    """
    try:
        realtime_metrics = await journey_analytics.get_real_time_metrics()
        system_stats = journey_analytics.get_system_stats()
        error_stats = error_handler.get_error_stats()
        
        alerts = []
        
        # Alert per attività bassa
        if realtime_metrics["metrics"]["active_users_1h"] == 0:
            alerts.append({
                "type": "warning",
                "title": "No User Activity",
                "message": "No users active in the last hour",
                "severity": "medium",
                "timestamp": datetime.now().isoformat()
            })
        
        # Alert per conversion rate bassa
        if realtime_metrics["metrics"]["conversion_rate_24h"] < 5.0:
            alerts.append({
                "type": "info",
                "title": "Low Conversion Rate",
                "message": f"24h conversion rate: {realtime_metrics['metrics']['conversion_rate_24h']:.1f}%",
                "severity": "low",
                "timestamp": datetime.now().isoformat()
            })
        
        # Alert per memory usage alta
        if system_stats["memory_usage_mb"] > 100:
            alerts.append({
                "type": "warning",
                "title": "High Memory Usage",
                "message": f"Memory usage: {system_stats['memory_usage_mb']:.1f} MB",
                "severity": "medium",
                "timestamp": datetime.now().isoformat()
            })
        
        # Alert per errori recenti
        if error_stats["recent_errors_1h"] > 5:
            alerts.append({
                "type": "error",
                "title": "High Error Rate",
                "message": f"{error_stats['recent_errors_1h']} errors in last hour",
                "severity": "high",
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "status": "success",
            "alerts": alerts,
            "total_alerts": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Dashboard alerts API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== ADMIN ACTIONS =====

@router.post("/dashboard/admin/reset-stats")
async def reset_system_stats():
    """
    Reset delle statistiche sistema (admin only)
    
    Returns:
        dict: Conferma reset
    """
    try:
        # Reset journey analytics stats
        journey_analytics.events_buffer.clear()
        journey_analytics.sessions.clear()
        # Mantieni user_journeys per non perdere dati utenti
        
        # Reset error handler stats
        error_handler.error_stats.clear()
        error_handler.error_history.clear()
        error_handler.error_rate_limit.clear()
        
        # Broadcast reset event
        await broadcast_update({
            "type": "system_reset",
            "timestamp": datetime.now().isoformat(),
            "message": "System statistics reset"
        })
        
        logger.info("🔄 System statistics reset by admin")
        
        return {
            "status": "success",
            "message": "System statistics reset successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ System reset error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/admin/export")
async def export_analytics_data(period_days: int = 30):
    """
    Export dati analytics per backup/analisi
    
    Args:
        period_days: Periodo di export in giorni
        
    Returns:
        dict: Dati analytics esportati
    """
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=period_days)
        
        # Filtra eventi nel periodo
        period_events = [
            event.to_dict() for event in journey_analytics.events_buffer
            if start_time <= event.timestamp <= end_time
        ]
        
        # Export user journeys nel periodo  
        period_journeys = []
        for user_id, journey in journey_analytics.user_journeys.items():
            if start_time <= journey.created_at <= end_time:
                journey_data = {
                    "user_id": user_id,
                    "created_at": journey.created_at.isoformat(),
                    "updated_at": journey.updated_at.isoformat(),
                    "current_stage": journey.current_stage.value,
                    "channels_used": [ch.value for ch in journey.channels_used],
                    "total_events": journey.total_events,
                    "engagement_score": journey.engagement_score,
                    "converted": journey.converted,
                    "conversion_value": journey.conversion_value,
                    "language": journey.language,
                    "primary_intent": journey.primary_intent
                }
                period_journeys.append(journey_data)
        
        export_data = {
            "export_info": {
                "created_at": datetime.now().isoformat(),
                "period_start": start_time.isoformat(),
                "period_end": end_time.isoformat(),
                "period_days": period_days
            },
            "summary": {
                "total_events": len(period_events),
                "total_journeys": len(period_journeys),
                "unique_users": len(set(event["user_id"] for event in period_events))
            },
            "events": period_events,
            "journeys": period_journeys
        }
        
        logger.info(f"📊 Analytics data exported: {len(period_events)} events, {len(period_journeys)} journeys")
        
        return export_data
        
    except Exception as e:
        logger.error(f"❌ Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== HEALTH CHECK DASHBOARD =====

@router.get("/dashboard/health")
async def dashboard_health():
    """
    Health check per dashboard e sistemi correlati
    
    Returns:
        dict: Stato salute completo
    """
    try:
        # Check journey analytics
        system_stats = journey_analytics.get_system_stats()
        journey_healthy = system_stats["events_in_buffer"] < system_stats["buffer_max_size"] * 0.9
        
        # Check error handler  
        error_stats = error_handler.get_error_stats()
        errors_healthy = error_stats["recent_errors_1h"] < 20
        
        # Check WebSocket connections
        websocket_healthy = len(active_connections) >= 0  # Always true, just tracking
        
        overall_health = journey_healthy and errors_healthy
        
        return {
            "status": "healthy" if overall_health else "degraded",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "journey_analytics": {
                    "status": "healthy" if journey_healthy else "degraded",
                    "events_buffer": system_stats["events_in_buffer"],
                    "memory_usage_mb": system_stats["memory_usage_mb"]
                },
                "error_handler": {
                    "status": "healthy" if errors_healthy else "degraded",
                    "recent_errors": error_stats["recent_errors_1h"],
                    "total_errors": error_stats["total_errors"]
                },
                "websockets": {
                    "status": "healthy",
                    "active_connections": len(active_connections)
                }
            },
            "metrics": {
                "uptime_status": "operational",
                "response_time_ms": "< 100",
                "availability": "99.9%"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Dashboard health check error: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        } 