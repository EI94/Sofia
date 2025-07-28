"""
Journey Analytics API per Sofia AI
API endpoints per monitoring completo del user journey e dashboard analytics
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
from app.tools.journey_analytics import (
    journey_analytics, track_journey_event, JourneyStage, EventType, 
    Channel, JourneyEvent, UserJourney, JourneyMetrics
)
from app.tools.error_handler import error_handler

logger = logging.getLogger(__name__)

router = APIRouter()

# ===== USER JOURNEY ENDPOINTS =====

@router.get("/journey/user/{user_id}")
async def get_user_journey(user_id: str):
    """
    Ottieni journey completo di un utente specifico
    
    Args:
        user_id: ID univoco dell'utente (es. numero telefono)
        
    Returns:
        dict: Journey completo con eventi e metriche
    """
    try:
        # Ottieni journey
        journey = await journey_analytics.get_user_journey(user_id)
        
        if not journey:
            raise HTTPException(status_code=404, detail=f"Journey not found for user {user_id}")
        
        # Ottieni eventi recenti
        recent_events = await journey_analytics.get_user_events(user_id, limit=50)
        
        # Converti eventi in dict per JSON
        events_data = [event.to_dict() for event in recent_events]
        
        # Calcola statistiche aggiuntive
        unique_channels = len(journey.channels_used)
        days_active = (journey.updated_at - journey.created_at).days + 1
        
        return {
            "status": "success",
            "user_id": user_id,
            "journey": {
                "created_at": journey.created_at.isoformat(),
                "updated_at": journey.updated_at.isoformat(),
                "current_stage": journey.current_stage.value,
                "channels_used": [ch.value for ch in journey.channels_used],
                "total_events": journey.total_events,
                "message_count": journey.message_count,
                "engagement_score": round(journey.engagement_score, 2),
                "converted": journey.converted,
                "conversion_date": journey.conversion_date.isoformat() if journey.conversion_date else None,
                "conversion_value": journey.conversion_value,
                "language": journey.language,
                "primary_intent": journey.primary_intent,
                "payment_status": journey.payment_status
            },
            "statistics": {
                "unique_channels": unique_channels,
                "days_active": days_active,
                "avg_events_per_day": round(journey.total_events / days_active, 2) if days_active > 0 else 0,
                "last_activity": journey.last_activity.isoformat() if journey.last_activity else None
            },
            "recent_events": events_data[:20],  # Top 20 più recenti
            "total_events_returned": len(events_data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting user journey: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user journey: {str(e)}")


@router.get("/journey/user/{user_id}/events")
async def get_user_events(
    user_id: str, 
    limit: int = Query(50, ge=1, le=500),
    event_type: Optional[str] = Query(None, description="Filter by event type")
):
    """
    Ottieni eventi specifici di un utente
    
    Args:
        user_id: ID utente
        limit: Numero massimo eventi da restituire
        event_type: Filtro per tipo evento (opzionale)
        
    Returns:
        dict: Lista eventi filtrati
    """
    try:
        events = await journey_analytics.get_user_events(user_id, limit)
        
        # Filtra per tipo evento se specificato
        if event_type:
            try:
                event_filter = EventType(event_type)
                events = [e for e in events if e.event_type == event_filter]
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid event_type: {event_type}")
        
        events_data = [event.to_dict() for event in events]
        
        return {
            "status": "success",
            "user_id": user_id,
            "filters": {
                "limit": limit,
                "event_type": event_type
            },
            "events": events_data,
            "total_events": len(events_data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting user events: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user events: {str(e)}")


# ===== FUNNEL ANALYTICS ENDPOINTS =====

@router.get("/journey/funnel")
async def get_funnel_metrics(
    period_days: int = Query(7, ge=1, le=90, description="Period in days for analysis")
):
    """
    Ottieni metriche funnel di conversione per periodo specificato
    
    Args:
        period_days: Numero di giorni da analizzare
        
    Returns:
        dict: Metriche complete del funnel
    """
    try:
        metrics = await journey_analytics.calculate_funnel_metrics(period_days)
        
        return {
            "status": "success",
            "period": {
                "days": period_days,
                "start": metrics.period_start.isoformat(),
                "end": metrics.period_end.isoformat()
            },
            "funnel": {
                "total_users": metrics.total_users,
                "stage_counts": metrics.stage_counts,
                "conversion_rates": {
                    stage: round(rate, 2) for stage, rate in metrics.conversion_rates.items()
                },
                "overall_conversion_rate": round(metrics.conversion_rate_overall, 2)
            },
            "channels": metrics.channel_metrics,
            "business_metrics": {
                "consultation_requests": metrics.total_consultation_requests,
                "payments_completed": metrics.total_payments_completed,
                "total_revenue": round(metrics.total_revenue, 2),
                "avg_revenue_per_user": round(
                    metrics.total_revenue / metrics.total_users, 2
                ) if metrics.total_users > 0 else 0
            },
            "quality_metrics": {
                "avg_engagement_score": round(metrics.avg_engagement_score, 2),
                "error_rate": round(metrics.error_rate, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting funnel metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get funnel metrics: {str(e)}")


@router.get("/journey/dropoffs")
async def get_drop_off_analysis(
    limit: int = Query(10, ge=1, le=20, description="Number of top drop-off points to return")
):
    """
    Analisi dei punti principali di abbandono nel funnel
    
    Args:
        limit: Numero massimo di drop-off points da restituire
        
    Returns:
        dict: Analisi drop-off con raccomandazioni
    """
    try:
        drop_offs = await journey_analytics.get_top_drop_off_points(limit)
        
        # Genera raccomandazioni basate sui drop-off
        recommendations = []
        for drop_off in drop_offs:
            if drop_off['drop_off_rate'] > 50:
                recommendations.append({
                    "stage": drop_off['from_stage'],
                    "issue": "High drop-off rate detected",
                    "recommendation": f"Review user experience at {drop_off['from_stage']} stage",
                    "priority": "high"
                })
            elif drop_off['drop_off_rate'] > 30:
                recommendations.append({
                    "stage": drop_off['from_stage'], 
                    "issue": "Moderate drop-off rate",
                    "recommendation": f"Optimize conversion flow from {drop_off['from_stage']}",
                    "priority": "medium"
                })
        
        return {
            "status": "success",
            "analysis": {
                "drop_off_points": drop_offs,
                "total_analyzed": len(drop_offs)
            },
            "recommendations": recommendations,
            "summary": {
                "highest_drop_off": drop_offs[0] if drop_offs else None,
                "avg_drop_off_rate": round(
                    sum(d['drop_off_rate'] for d in drop_offs) / len(drop_offs), 2
                ) if drop_offs else 0
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting drop-off analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get drop-off analysis: {str(e)}")


# ===== COHORT & RETENTION ENDPOINTS =====

@router.get("/journey/cohorts")
async def get_cohort_analysis(
    period_days: int = Query(30, ge=7, le=90, description="Period in days for cohort analysis")
):
    """
    Analisi coorte per retention e lifetime value
    
    Args:
        period_days: Periodo di analisi in giorni
        
    Returns:
        dict: Analisi completa delle coorti
    """
    try:
        cohort_data = await journey_analytics.get_cohort_analysis(period_days)
        
        # Calcola statistiche aggregate
        total_cohorts = len(cohort_data['cohorts'])
        if total_cohorts > 0:
            avg_conversion_rate = sum(
                cohort['conversion_rate'] for cohort in cohort_data['cohorts'].values()
            ) / total_cohorts
            
            total_users_all_cohorts = sum(
                cohort['total_users'] for cohort in cohort_data['cohorts'].values()
            )
            
            total_revenue_all_cohorts = sum(
                cohort['total_revenue'] for cohort in cohort_data['cohorts'].values()
            )
        else:
            avg_conversion_rate = 0
            total_users_all_cohorts = 0
            total_revenue_all_cohorts = 0
        
        return {
            "status": "success",
            "period": {
                "days": period_days,
                "start": cohort_data['period_start'],
                "end": cohort_data['period_end']
            },
            "cohorts": cohort_data['cohorts'],
            "summary": {
                "total_cohorts": total_cohorts,
                "avg_conversion_rate": round(avg_conversion_rate, 2),
                "total_users": total_users_all_cohorts,
                "total_revenue": round(total_revenue_all_cohorts, 2),
                "avg_revenue_per_cohort": round(
                    total_revenue_all_cohorts / total_cohorts, 2
                ) if total_cohorts > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting cohort analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cohort analysis: {str(e)}")


# ===== REAL-TIME DASHBOARD ENDPOINTS =====

@router.get("/journey/realtime")
async def get_realtime_metrics():
    """
    Metriche in tempo reale per dashboard live
    
    Returns:
        dict: Metriche real-time per dashboard
    """
    try:
        metrics = await journey_analytics.get_real_time_metrics()
        
        # Arricchisce con dati aggiuntivi per dashboard
        enhanced_metrics = metrics.copy()
        enhanced_metrics.update({
            "health_status": "healthy" if metrics['metrics']['active_users_1h'] > 0 else "idle",
            "trending": {
                "users": "up" if metrics['metrics']['active_users_1h'] > metrics['metrics']['active_users_24h'] / 24 else "down",
                "events": "up" if metrics['metrics']['events_1h'] > metrics['metrics']['events_24h'] / 24 else "down"
            },
            "alerts": _generate_real_time_alerts(metrics['metrics'])
        })
        
        return enhanced_metrics
        
    except Exception as e:
        logger.error(f"❌ Error getting real-time metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get real-time metrics: {str(e)}")


def _generate_real_time_alerts(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Genera alert basati sulle metriche real-time"""
    alerts = []
    
    # Alert per attività bassa
    if metrics['active_users_1h'] == 0 and metrics['events_1h'] == 0:
        alerts.append({
            "type": "warning",
            "message": "No user activity in the last hour",
            "severity": "medium"
        })
    
    # Alert per conversion rate bassa
    if metrics['conversion_rate_24h'] < 5.0:  # Sotto 5%
        alerts.append({
            "type": "info", 
            "message": f"Daily conversion rate is low: {metrics['conversion_rate_24h']:.1f}%",
            "severity": "low"
        })
    
    # Alert per engagement basso
    if metrics['avg_engagement_score'] < 30.0:
        alerts.append({
            "type": "warning",
            "message": f"Average engagement score is low: {metrics['avg_engagement_score']:.1f}",
            "severity": "medium"
        })
    
    return alerts


@router.get("/journey/dashboard")
async def get_dashboard_summary(
    period_days: int = Query(7, ge=1, le=30, description="Period for dashboard metrics")
):
    """
    Summary completo per dashboard principale
    
    Args:
        period_days: Periodo per le metriche del dashboard
        
    Returns:
        dict: Dati completi per dashboard
    """
    try:
        # Ottieni diverse metriche in parallelo
        funnel_metrics = await journey_analytics.calculate_funnel_metrics(period_days)
        realtime_metrics = await journey_analytics.get_real_time_metrics()
        drop_offs = await journey_analytics.get_top_drop_off_points(5)
        
        # Calcola KPI principali
        kpis = {
            "total_users": funnel_metrics.total_users,
            "conversion_rate": round(funnel_metrics.conversion_rate_overall, 2),
            "total_revenue": round(funnel_metrics.total_revenue, 2),
            "avg_revenue_per_user": round(
                funnel_metrics.total_revenue / funnel_metrics.total_users, 2
            ) if funnel_metrics.total_users > 0 else 0,
            "engagement_score": round(funnel_metrics.avg_engagement_score, 2)
        }
        
        # Top channels performance
        top_channels = sorted(
            funnel_metrics.channel_metrics.items(),
            key=lambda x: x[1]['conversion_rate'],
            reverse=True
        )[:3]
        
        return {
            "status": "success",
            "period": {
                "days": period_days,
                "end": datetime.now().isoformat()
            },
            "kpis": kpis,
            "realtime": realtime_metrics['metrics'],
            "funnel": {
                "stage_counts": funnel_metrics.stage_counts,
                "conversion_rates": funnel_metrics.conversion_rates
            },
            "channels": {
                "top_performing": [
                    {"channel": ch, "metrics": metrics} 
                    for ch, metrics in top_channels
                ],
                "all_channels": funnel_metrics.channel_metrics
            },
            "issues": {
                "top_drop_offs": drop_offs[:3],
                "alerts": _generate_real_time_alerts(realtime_metrics['metrics'])
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard summary: {str(e)}")


# ===== ADMIN & MANAGEMENT ENDPOINTS =====

@router.get("/journey/users")
async def get_users_list(
    limit: int = Query(20, ge=1, le=100),
    stage: Optional[str] = Query(None, description="Filter by current stage"),
    converted: Optional[bool] = Query(None, description="Filter by conversion status")
):
    """
    Lista utenti con filtri opzionali
    
    Args:
        limit: Numero massimo utenti da restituire
        stage: Filtro per stage corrente
        converted: Filtro per stato conversione
        
    Returns:
        dict: Lista utenti con metriche base
    """
    try:
        all_journeys = list(journey_analytics.user_journeys.values())
        
        # Applica filtri
        filtered_journeys = all_journeys
        
        if stage:
            try:
                stage_filter = JourneyStage(stage)
                filtered_journeys = [j for j in filtered_journeys if j.current_stage == stage_filter]
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid stage: {stage}")
        
        if converted is not None:
            filtered_journeys = [j for j in filtered_journeys if j.converted == converted]
        
        # Ordina per ultima attività
        filtered_journeys.sort(key=lambda x: x.updated_at, reverse=True)
        
        # Limita risultati
        limited_journeys = filtered_journeys[:limit]
        
        # Formatta risultati
        users_data = []
        for journey in limited_journeys:
            users_data.append({
                "user_id": journey.user_id,
                "current_stage": journey.current_stage.value,
                "channels_used": [ch.value for ch in journey.channels_used],
                "language": journey.language,
                "engagement_score": round(journey.engagement_score, 2),
                "converted": journey.converted,
                "conversion_value": journey.conversion_value,
                "created_at": journey.created_at.isoformat(),
                "last_activity": journey.last_activity.isoformat() if journey.last_activity else None,
                "total_events": journey.total_events,
                "message_count": journey.message_count
            })
        
        return {
            "status": "success",
            "filters": {
                "limit": limit,
                "stage": stage,
                "converted": converted
            },
            "users": users_data,
            "total_returned": len(users_data),
            "total_available": len(filtered_journeys)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting users list: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get users list: {str(e)}")


@router.get("/journey/system/stats")
async def get_system_stats():
    """
    Statistiche del sistema analytics per monitoring
    
    Returns:
        dict: Stats sistema journey analytics
    """
    try:
        stats = journey_analytics.get_system_stats()
        error_stats = error_handler.get_error_stats()
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "journey_analytics": stats,
            "error_handling": {
                "total_errors": error_stats["total_errors"],
                "recent_errors_1h": error_stats["recent_errors_1h"]
            },
            "health": {
                "system_healthy": stats['events_in_buffer'] < stats['buffer_max_size'] * 0.9,
                "memory_usage_mb": stats['memory_usage_mb'],
                "performance_status": "optimal" if stats['memory_usage_mb'] < 100 else "monitoring"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get system stats: {str(e)}")


# ===== EVENT TRACKING ENDPOINTS =====

@router.post("/journey/track")
async def track_custom_event(event_data: Dict[str, Any]):
    """
    Traccia evento custom (per integrations esterne)
    
    Args:
        event_data: Dati evento da tracciare
        
    Returns:
        dict: Conferma tracking
    """
    try:
        # Valida dati richiesti
        required_fields = ['user_id', 'event_type', 'channel', 'stage']
        missing_fields = [field for field in required_fields if field not in event_data]
        
        if missing_fields:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required fields: {missing_fields}"
            )
        
        # Converte stringhe in enums
        try:
            event_type = EventType(event_data['event_type'])
            channel = Channel(event_data['channel'])
            stage = JourneyStage(event_data['stage'])
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
        
        # Traccia evento
        from app.tools.journey_analytics import track_journey_event
        
        success = await track_journey_event(
            user_id=event_data['user_id'],
            event_type=event_type,
            channel=channel,
            stage=stage,
            session_id=event_data.get('session_id'),
            language=event_data.get('language'),
            intent=event_data.get('intent'),
            user_input=event_data.get('user_input'),
            ai_response=event_data.get('ai_response'),
            conversion_value=event_data.get('conversion_value', 0.0),
            data=event_data.get('data', {})
        )
        
        if success:
            return {
                "status": "success",
                "message": "Event tracked successfully",
                "user_id": event_data['user_id'],
                "event_type": event_data['event_type']
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to track event")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error tracking custom event: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to track event: {str(e)}")


@router.get("/journey/events/types")
async def get_available_event_types():
    """
    Ottieni tipi di eventi disponibili per tracking
    
    Returns:
        dict: Lista completa di event types, stages e channels
    """
    return {
        "status": "success",
        "available_types": {
            "event_types": [e.value for e in EventType],
            "journey_stages": [s.value for s in JourneyStage],
            "channels": [c.value for c in Channel]
        },
        "examples": {
            "discovery_event": {
                "user_id": "+391234567890",
                "event_type": "first_contact",
                "channel": "whatsapp",
                "stage": "discovery",
                "language": "it"
            },
            "conversion_event": {
                "user_id": "+391234567890",
                "event_type": "payment_verified",
                "channel": "whatsapp",
                "stage": "payment_completed",
                "conversion_value": 60.0
            }
        }
    } 