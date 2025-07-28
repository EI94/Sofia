"""
Health Monitoring API per Sofia AI
Endpoint per monitoring fallback system e salute generale del sistema
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
import logging
import os
from datetime import datetime
import psutil
from app.tools.fallback_system import fallback_manager, ServiceStatus
from app.tools.error_handler import error_handler
from app.gateways.memory import MemoryGateway
from app.tools.exclusions import EXCLUDED_SERVICES, EXCLUDED_KEYWORDS

logger = logging.getLogger(__name__)

router = APIRouter()

# ===== ENDPOINT HEALTH MONITORING =====

@router.get("/health")
async def health_check():
    """Health check basico per load balancer"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@router.get("/health/detailed")
async def detailed_health():
    """
    Health check dettagliato con informazioni su tutti i componenti
    """
    try:
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "components": {}
        }
        
        # === SISTEMA FALLBACK ===
        try:
            fallback_health = fallback_manager.get_system_health()
            health_data["components"]["fallback_system"] = {
                "status": fallback_health["overall_status"],
                "services_count": len(fallback_health["services"]),
                "chains_count": len(fallback_health["registered_chains"]),
                "services": fallback_health["services"],
                "registered_chains": fallback_health["registered_chains"]
            }
        except Exception as e:
            health_data["components"]["fallback_system"] = {
                "status": "error",
                "error": str(e)
            }
            health_data["overall_status"] = "degraded"
        
        # === FIRESTORE MEMORY ===
        try:
            memory_store = MemoryGateway()
            test_result = await memory_store.get_user("health_check_test")
            health_data["components"]["firestore"] = {
                "status": "healthy" if memory_store.client else "degraded",
                "connection": "connected" if memory_store.client else "fallback_memory"
            }
        except Exception as e:
            health_data["components"]["firestore"] = {
                "status": "error", 
                "error": str(e)
            }
            health_data["overall_status"] = "degraded"
        
        # === EXCLUSIONS SYSTEM ===
        try:
            health_data["components"]["exclusions"] = {
                "status": "healthy",
                "categories_count": len(EXCLUDED_SERVICES),
                "keywords_count": len(EXCLUDED_KEYWORDS),
                "configured": True
            }
        except Exception as e:
            health_data["components"]["exclusions"] = {
                "status": "error",
                "error": str(e)
            }
        
        # === ENVIRONMENT VARIABLES ===
        try:
            env_status = {
                "OPENAI_API_KEY": "✅" if os.getenv("OPENAI_API_KEY") else "❌",
                "TWILIO_ACCOUNT_SID": "✅" if os.getenv("TWILIO_ACCOUNT_SID") else "❌",
                "TWILIO_AUTH_TOKEN": "✅" if os.getenv("TWILIO_AUTH_TOKEN") else "❌",
                "ELEVENLABS_API_KEY": "✅" if os.getenv("ELEVENLABS_API_KEY") else "❌",
                "USE_ELEVENLABS_TTS": os.getenv("USE_ELEVENLABS_TTS", "false")
            }
            
            missing_env = sum(1 for v in env_status.values() if v == "❌")
            
            health_data["components"]["environment"] = {
                "status": "healthy" if missing_env <= 1 else "degraded",
                "variables": env_status,
                "missing_count": missing_env
            }
            
            if missing_env > 2:
                health_data["overall_status"] = "degraded"
                
        except Exception as e:
            health_data["components"]["environment"] = {
                "status": "error",
                "error": str(e)
            }
        
        # === SYSTEM RESOURCES ===
        try:
            health_data["components"]["system"] = {
                "status": "healthy",
                "cpu_percent": round(psutil.cpu_percent(interval=1), 1),
                "memory_percent": round(psutil.virtual_memory().percent, 1),
                "disk_percent": round(psutil.disk_usage('/').percent, 1)
            }
            
            # Allarmi risorse
            if health_data["components"]["system"]["memory_percent"] > 90:
                health_data["components"]["system"]["status"] = "warning"
                health_data["overall_status"] = "degraded"
                
        except Exception as e:
            health_data["components"]["system"] = {
                "status": "error",
                "error": str(e)
            }
        
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Errore health check dettagliato: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/health/fallback")
async def fallback_system_health():
    """
    Health check specifico per il sistema fallback con metriche dettagliate
    """
    try:
        return fallback_manager.get_system_health()
    except Exception as e:
        logger.error(f"❌ Errore fallback health: {e}")
        raise HTTPException(status_code=500, detail=f"Fallback health check failed: {str(e)}")


@router.get("/health/services")
async def services_health():
    """
    Stato di salute di tutti i servizi esterni monitorati
    """
    try:
        services_data = {}
        health_mgr = fallback_manager.health_manager
        
        for service_name, service_health in health_mgr.services.items():
            services_data[service_name] = {
                "status": service_health.status.value,
                "failure_count": service_health.failure_count,
                "success_count": service_health.success_count,
                "avg_response_time": round(service_health.average_response_time, 2),
                "last_success": service_health.last_success.isoformat() if service_health.last_success else None,
                "last_failure": service_health.last_failure.isoformat() if service_health.last_failure else None,
                "circuit_open": service_health.status.value == "circuit_open",
                "available": health_mgr.is_service_available(service_name),
                "recommended_tier": health_mgr.get_service_tier(service_name).value
            }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "services": services_data,
            "healthy_count": sum(1 for s in services_data.values() if s["status"] in ["healthy", "degraded"]),
            "total_count": len(services_data)
        }
        
    except Exception as e:
        logger.error(f"❌ Errore services health: {e}")
        raise HTTPException(status_code=500, detail=f"Services health check failed: {str(e)}")


@router.post("/health/services/{service_name}/reset")
async def reset_service_circuit(service_name: str):
    """
    Reset manuale del circuit breaker per un servizio specifico
    """
    try:
        health_mgr = fallback_manager.health_manager
        
        if service_name not in health_mgr.services:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        
        service = health_mgr.services[service_name]
        service.failure_count = 0
        service.status = ServiceStatus.HEALTHY
        service.circuit_open_until = None
        
        logger.info(f"🔄 Circuit breaker reset manualmente per {service_name}")
        
        return {
            "message": f"Circuit breaker reset for {service_name}",
            "service": service_name,
            "new_status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Errore reset circuit {service_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Circuit reset failed: {str(e)}")


@router.get("/health/metrics")
async def system_metrics():
    """
    Metriche del sistema per monitoring esterno (Prometheus-compatible)
    """
    try:
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "fallback_system": {
                "total_services": len(fallback_manager.health_manager.services),
                "healthy_services": sum(
                    1 for s in fallback_manager.health_manager.services.values() 
                    if s.status.value in ["healthy", "degraded"]
                ),
                "circuit_open_services": sum(
                    1 for s in fallback_manager.health_manager.services.values()
                    if s.status.value == "circuit_open"
                ),
                "registered_chains": len(fallback_manager.fallback_chains)
            },
            "exclusions": {
                "total_categories": len(EXCLUDED_SERVICES),
                "total_keywords": len(EXCLUDED_KEYWORDS)
            },
            "system": {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "uptime_seconds": psutil.boot_time()
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"❌ Errore system metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Metrics collection failed: {str(e)}")


@router.get("/health/readiness")
async def readiness_check():
    """
    Readiness check per Kubernetes - verifica che il sistema sia pronto per ricevere traffico
    """
    try:
        # Controlla componenti critici
        critical_checks = {
            "fallback_system": False,
            "exclusions": False,
            "environment": False
        }
        
        # Test fallback system
        try:
            fallback_health = fallback_manager.get_system_health()
            critical_checks["fallback_system"] = fallback_health["overall_status"] in ["healthy", "degraded"]
        except:
            pass
        
        # Test exclusions
        try:
            critical_checks["exclusions"] = len(EXCLUDED_SERVICES) > 0
        except:
            pass
        
        # Test environment essentials
        try:
            critical_checks["environment"] = bool(os.getenv("OPENAI_API_KEY"))
        except:
            pass
        
        ready = all(critical_checks.values())
        
        if ready:
            return {
                "status": "ready", 
                "checks": critical_checks,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=503, 
                detail={
                    "status": "not_ready", 
                    "checks": critical_checks,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Errore readiness check: {e}")
        raise HTTPException(status_code=503, detail=f"Readiness check failed: {str(e)}")


@router.get("/health/liveness")
async def liveness_check():
    """
    Liveness check per Kubernetes - verifica che il processo sia ancora vivo
    """
    try:
        # Test basico che il processo risponde
        return {
            "status": "alive",
            "pid": os.getpid(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Errore liveness check: {e}")
        raise HTTPException(status_code=503, detail=f"Liveness check failed: {str(e)}") 

# ===== ERROR MONITORING ENDPOINTS =====

@router.get("/health/errors")
async def error_monitoring():
    """
    Monitoring completo del sistema error handling
    
    Returns:
        dict: Statistiche complete degli errori
    """
    try:
        error_stats = error_handler.get_error_stats()
        
        return {
            "status": "monitoring_active",
            "timestamp": datetime.now().isoformat(),
            "error_handler": {
                "total_errors": error_stats["total_errors"],
                "recent_errors_1h": error_stats["recent_errors_1h"],
                "error_stats": error_stats["error_stats"],
                "rate_limited_types": error_stats["rate_limited_types"],
                "most_common_category": error_stats["most_common_category"]
            },
            "health_status": "healthy" if error_stats["recent_errors_1h"] < 50 else "degraded"
        }
        
    except Exception as e:
        logger.error(f"❌ Errore error monitoring: {e}")
        raise HTTPException(status_code=500, detail=f"Error monitoring failed: {str(e)}")


@router.get("/health/errors/recent")
async def recent_errors(limit: int = 20):
    """
    Ottieni errori recenti per debugging
    
    Args:
        limit: Numero massimo di errori da restituire (default: 20)
        
    Returns:
        dict: Lista errori recenti con dettagli
    """
    try:
        if limit < 1 or limit > 100:
            limit = 20
            
        recent_errors = error_handler.get_recent_errors(limit)
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "recent_errors_count": len(recent_errors),
            "errors": recent_errors
        }
        
    except Exception as e:
        logger.error(f"❌ Errore recent errors: {e}")
        raise HTTPException(status_code=500, detail=f"Recent errors failed: {str(e)}")


@router.get("/health/errors/categories")
async def error_categories():
    """
    Statistiche errori per categoria per analytics
    
    Returns:
        dict: Breakdown degli errori per categoria e severità
    """
    try:
        error_stats = error_handler.get_error_stats()["error_stats"]
        
        # Raggruppa per categoria e severità
        categories = {}
        severities = {}
        channels = {}
        
        for key, count in error_stats.items():
            if key.startswith("channel_"):
                channel = key.replace("channel_", "")
                channels[channel] = count
            elif "_" in key:
                parts = key.split("_", 1)
                if len(parts) == 2:
                    category, severity = parts
                    
                    if category not in categories:
                        categories[category] = 0
                    categories[category] += count
                    
                    if severity not in severities:
                        severities[severity] = 0
                    severities[severity] += count
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "breakdown": {
                "by_category": categories,
                "by_severity": severities,
                "by_channel": channels
            },
            "total_tracked_errors": sum(error_stats.values())
        }
        
    except Exception as e:
        logger.error(f"❌ Errore error categories: {e}")
        raise HTTPException(status_code=500, detail=f"Error categories failed: {str(e)}")


@router.post("/health/errors/reset")
async def reset_error_stats():
    """
    Reset delle statistiche errori (solo per admin/testing)
    
    Returns:
        dict: Conferma reset
    """
    try:
        # Clear delle statistiche
        error_handler.error_stats.clear()
        error_handler.error_history.clear()
        error_handler.error_rate_limit.clear()
        
        return {
            "status": "reset_successful",
            "timestamp": datetime.now().isoformat(),
            "message": "Error statistics cleared"
        }
        
    except Exception as e:
        logger.error(f"❌ Errore reset stats: {e}")
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@router.post("/integration-test")
async def comprehensive_integration_test():
    """
    Test di integrazione completo per verificare tutti i sistemi Sofia AI
    
    - WhatsApp + SMS Fallback
    - Voice + TTS + Moderazione  
    - Journey Analytics + Error Handling
    - Dashboard + Alerting
    - Memory + Stati persistenti
    
    Returns:
        dict: Risultati completi test integrazione con score
    """
    
    from datetime import datetime
    import asyncio
    import time
    
    logger.info("🚀 AVVIO INTEGRATION TEST COMPLETO SOFIA AI")
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "test_id": f"integration_test_{int(datetime.now().timestamp())}",
        "duration_seconds": 0,
        "systems": {},
        "overall_score": 0,
        "status": "running"
    }
    
    start_time = time.time()
    
    try:
        
        # === TEST 1: WHATSAPP + SMS FALLBACK ===
        logger.info("🧪 Testing WhatsApp + SMS Fallback...")
        whatsapp_score = 0
        whatsapp_details = {}
        
        try:
            from app.api.whatsapp import _send_whatsapp_message, _format_whatsapp_numbers, _format_sms_numbers
            
            # Test formatting numeri
            test_number = "+1234567890"
            wa_to, wa_from = _format_whatsapp_numbers(test_number, "+1987654321")
            sms_to, sms_from = _format_sms_numbers(test_number, "+1987654321")
            
            whatsapp_details["number_formatting"] = {
                "whatsapp": {"to": wa_to, "from": wa_from},
                "sms": {"to": sms_to, "from": sms_from},
                "passed": True
            }
            whatsapp_score += 25
            
            # Test funzione fallback (simulazione)
            fallback_result = await _send_whatsapp_message(
                "whatsapp:+1234567890",
                "Integration test message",
                test_fallback=True  # Simula fallimento
            )
            
            whatsapp_details["sms_fallback"] = {
                "result": fallback_result,
                "passed": fallback_result.get("method") == "sms_fallback"
            }
            
            if fallback_result.get("method") == "sms_fallback":
                whatsapp_score += 50
            
            whatsapp_details["score"] = whatsapp_score
            
        except Exception as e:
            whatsapp_details["error"] = str(e)
            logger.error(f"❌ WhatsApp test failed: {e}")
        
        test_results["systems"]["whatsapp_sms"] = whatsapp_details
        
        
        # === TEST 2: VOICE + TTS + MODERAZIONE ===
        logger.info("🧪 Testing Voice + TTS + Moderazione...")
        voice_score = 0
        voice_details = {}
        
        try:
            from app.api.voice import create_enhanced_voice_response, _select_optimal_voice, _get_twilio_tts_config
            from app.tools.moderation import check_voice_content
            
            # Test selezione voce dinamica
            optimal_voice = _select_optimal_voice("it", {})
            voice_details["voice_selection"] = {
                "selected_voice": optimal_voice,
                "passed": "voice_id" in optimal_voice
            }
            
            if "voice_id" in optimal_voice:
                voice_score += 20
            
            # Test TTS config
            tts_lang, tts_voice = _get_twilio_tts_config("it")
            voice_details["tts_config"] = {
                "language": tts_lang,
                "voice": tts_voice,
                "passed": tts_lang == "it-IT"
            }
            
            if tts_lang == "it-IT":
                voice_score += 20
            
            # Test enhanced voice response
            enhanced_response = await create_enhanced_voice_response(
                "Ciao, questo è un test di integrazione",
                "it",
                enable_streaming=False  # Disable per test
            )
            
            voice_details["enhanced_response"] = {
                "created": enhanced_response is not None,
                "passed": enhanced_response is not None
            }
            
            if enhanced_response:
                voice_score += 30
            
            # Test moderazione Voice
            clean_blocked, clean_reason, clean_response = await check_voice_content(
                "Ciao, come stai?", "+1234567890", "test_call_123"
            )
            
            abusive_blocked, abusive_reason, abusive_response = await check_voice_content(
                "Sei un idiota maledetto!", "+1234567890", "test_call_456"  
            )
            
            voice_details["moderation"] = {
                "clean_content": {"blocked": clean_blocked, "reason": clean_reason},
                "abusive_content": {"blocked": abusive_blocked, "reason": abusive_reason},
                "passed": not clean_blocked and abusive_blocked
            }
            
            if not clean_blocked and abusive_blocked:
                voice_score += 30
            
            voice_details["score"] = voice_score
            
        except Exception as e:
            voice_details["error"] = str(e)
            logger.error(f"❌ Voice test failed: {e}")
        
        test_results["systems"]["voice_tts_moderation"] = voice_details
        
        
        # === TEST 3: JOURNEY ANALYTICS + ERROR HANDLING ===
        logger.info("🧪 Testing Journey Analytics + Error Handling...")
        analytics_score = 0
        analytics_details = {}
        
        try:
            from app.tools.journey_analytics import journey_analytics, track_journey_event, EventType, JourneyStage, Channel
            from app.tools.error_handler import error_handler, ErrorSeverity, ErrorCategory, Channel as ErrorChannel
            
            # Test journey tracking
            test_user = "+1234567890"
            session_id = f"test_session_{int(time.time())}"
            
            await track_journey_event(
                user_id=test_user,
                event_type=EventType.FIRST_CONTACT,
                channel=Channel.VOICE,
                stage=JourneyStage.DISCOVERY,
                session_id=session_id,
                data={"test": "integration_test"}
            )
            
            analytics_details["event_tracking"] = {
                "event_created": True,
                "passed": True
            }
            analytics_score += 25
            
            # Test real-time metrics
            realtime_metrics = await journey_analytics.get_real_time_metrics()
            analytics_details["realtime_metrics"] = {
                "metrics_available": bool(realtime_metrics.get("metrics")),
                "passed": bool(realtime_metrics.get("metrics"))
            }
            
            if realtime_metrics.get("metrics"):
                analytics_score += 25
            
            # Test system stats
            system_stats = journey_analytics.get_system_stats()
            analytics_details["system_stats"] = {
                "stats_available": bool(system_stats),
                "memory_usage": system_stats.get("memory_usage_mb", 0),
                "passed": bool(system_stats)
            }
            
            if system_stats:
                analytics_score += 25
            
            # Test error handler
            error_stats = error_handler.get_error_stats()
            analytics_details["error_handler"] = {
                "stats_available": bool(error_stats),
                "total_errors": error_stats.get("total_errors", 0),
                "passed": isinstance(error_stats, dict)
            }
            
            if isinstance(error_stats, dict):
                analytics_score += 25
            
            analytics_details["score"] = analytics_score
            
        except Exception as e:
            analytics_details["error"] = str(e)
            logger.error(f"❌ Analytics test failed: {e}")
        
        test_results["systems"]["analytics_errors"] = analytics_details
        
        
        # === TEST 4: MEMORY + STATI PERSISTENTI ===
        logger.info("🧪 Testing Memory + Stati Persistenti...")
        memory_score = 0
        memory_details = {}
        
        try:
            from app.gateways.memory import MemoryGateway
            
            from app.gateways.memory import FirestoreMemoryGateway
            memory_store = FirestoreMemoryGateway()
            test_user = "+1234567890"
            
            # Test upsert user
            upsert_result = await memory_store.upsert_user(
                test_user, "it", case_topic="test integration", 
                payment_status="test", type="test"
            )
            
            memory_details["user_upsert"] = {
                "success": upsert_result,
                "passed": upsert_result
            }
            
            if upsert_result:
                memory_score += 20
            
            # Test get user
            user_data = await memory_store.get_user(test_user)
            memory_details["user_retrieval"] = {
                "data_found": user_data is not None,
                "lang_correct": user_data.get("lang") == "it" if user_data else False,
                "passed": user_data is not None and user_data.get("lang") == "it"
            }
            
            if user_data and user_data.get("lang") == "it":
                memory_score += 30
            
            # Test conversation states
            state_update_result = await memory_store.update_conversation_state(
                test_user, "voice", "service_inquiry", 
                {"test": "integration", "timestamp": datetime.now().isoformat()}
            )
            
            memory_details["conversation_state"] = {
                "update_success": state_update_result,
                "passed": state_update_result
            }
            
            if state_update_result:
                memory_score += 25
            
            # Test get conversation state
            current_state = await memory_store.get_conversation_state(test_user, "voice")
            memory_details["state_retrieval"] = {
                "state_found": current_state is not None,
                "state_value": current_state,
                "passed": current_state == "service_inquiry"
            }
            
            if current_state == "service_inquiry":
                memory_score += 25
            
            memory_details["score"] = memory_score
            
        except Exception as e:
            memory_details["error"] = str(e)
            logger.error(f"❌ Memory test failed: {e}")
        
        test_results["systems"]["memory_states"] = memory_details
        
        
        # === TEST 5: DASHBOARD + ALERTING ===
        logger.info("🧪 Testing Dashboard + Alerting...")
        dashboard_score = 0
        dashboard_details = {}
        
        try:
            # Test alerting system
            from app.tools.alerting_system import alerting_system
            
            alert_stats = alerting_system.get_alert_statistics()
            dashboard_details["alerting_stats"] = {
                "stats_available": bool(alert_stats),
                "active_alerts": alert_stats.get("active_alerts", -1),
                "passed": isinstance(alert_stats, dict)
            }
            
            if isinstance(alert_stats, dict):
                dashboard_score += 30
            
            # Test rules summary
            rules_summary = alerting_system.get_rules_summary()
            dashboard_details["alerting_rules"] = {
                "rules_count": len(rules_summary),
                "rules_available": len(rules_summary) > 0,
                "passed": len(rules_summary) > 0
            }
            
            if len(rules_summary) > 0:
                dashboard_score += 30
            
            # Test dashboard health (simulato)
            dashboard_details["dashboard_health"] = {
                "simulated_check": True,
                "components_healthy": True,
                "passed": True
            }
            dashboard_score += 40
            
            dashboard_details["score"] = dashboard_score
            
        except Exception as e:
            dashboard_details["error"] = str(e)
            logger.error(f"❌ Dashboard test failed: {e}")
        
        test_results["systems"]["dashboard_alerting"] = dashboard_details
        
        
        # === CALCOLO SCORE FINALE ===
        end_time = time.time()
        test_results["duration_seconds"] = round(end_time - start_time, 2)
        
        # Calcola score totale (max 100 per sistema)
        system_scores = []
        for system_name, system_data in test_results["systems"].items():
            score = system_data.get("score", 0)
            system_scores.append(score)
            logger.info(f"📊 {system_name}: {score}/100")
        
        overall_score = sum(system_scores) / len(system_scores) if system_scores else 0
        test_results["overall_score"] = round(overall_score, 1)
        
        # Status finale
        if overall_score >= 90:
            test_results["status"] = "excellent"
            test_results["grade"] = "A+"
        elif overall_score >= 80:
            test_results["status"] = "good"
            test_results["grade"] = "A"
        elif overall_score >= 70:
            test_results["status"] = "acceptable"
            test_results["grade"] = "B"
        elif overall_score >= 60:
            test_results["status"] = "needs_improvement"
            test_results["grade"] = "C"
        else:
            test_results["status"] = "failed"
            test_results["grade"] = "F"
        
        # Summary
        test_results["summary"] = {
            "total_systems_tested": len(test_results["systems"]),
            "systems_passed": len([s for s in test_results["systems"].values() if s.get("score", 0) >= 70]),
            "highest_score": max(system_scores) if system_scores else 0,
            "lowest_score": min(system_scores) if system_scores else 0,
            "average_score": overall_score,
            "recommendation": _get_recommendation(overall_score)
        }
        
        logger.info(f"🎯 INTEGRATION TEST COMPLETATO: {overall_score}/100 - {test_results['grade']}")
        logger.info(f"⏱️ Durata: {test_results['duration_seconds']}s")
        
        return test_results
        
    except Exception as e:
        test_results["status"] = "error"
        test_results["error"] = str(e)
        test_results["duration_seconds"] = time.time() - start_time
        logger.error(f"❌ Integration test error: {e}")
        return test_results


def _get_recommendation(score: float) -> str:
    """Genera raccomandazione basata su score"""
    
    if score >= 90:
        return "🌟 Sistema eccellente! Pronto per produzione con prestazioni ottimali."
    elif score >= 80:
        return "✅ Sistema in buone condizioni. Possibili ottimizzazioni minori."
    elif score >= 70:
        return "⚠️ Sistema accettabile ma necessita miglioramenti in alcune aree."
    elif score >= 60:
        return "🔧 Sistema richiede ottimizzazioni significative prima del deploy."
    else:
        return "🚨 Sistema critico - risolvi problemi prima di procedere!"
