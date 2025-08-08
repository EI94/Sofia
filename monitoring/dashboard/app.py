from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import json
from datetime import datetime, timedelta
import asyncio
import aiohttp

app = FastAPI(title="Sofia Dashboard", version="2.0")

# Static files e templates
app.mount("/static", StaticFiles(directory="monitoring/dashboard/static"), name="static")
templates = Jinja2Templates(directory="monitoring/dashboard/templates")

# Configurazione
SOFIA_MONITOR_URL = "https://sofia-monitor-1075574333382.europe-west1.run.app"
SOFIA_LITE_URL = "https://sofia-lite-1075574333382.us-central1.run.app"

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principale Sofia"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/metrics")
async def get_metrics():
    """API per ottenere le metriche in tempo reale"""
    try:
        # Ottieni metriche dal monitor
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SOFIA_MONITOR_URL}/metrics") as response:
                metrics_text = await response.text()
        
        # Parsing delle metriche Prometheus
        metrics = parse_prometheus_metrics(metrics_text)
        
        # Ottieni stato Sofia Lite
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SOFIA_LITE_URL}/status") as response:
                sofia_status = await response.json() if response.status == 200 else {"status": "offline"}
        
        return {
            "metrics": metrics,
            "sofia_status": sofia_status,
            "timestamp": datetime.now().isoformat(),
            "last_update": datetime.now().strftime("%H:%M:%S")
        }
    except Exception as e:
        return {
            "error": str(e),
            "metrics": {},
            "sofia_status": {"status": "error"},
            "timestamp": datetime.now().isoformat()
        }

def parse_prometheus_metrics(metrics_text):
    """Parsing delle metriche Prometheus"""
    metrics = {}
    for line in metrics_text.split('\n'):
        if line.startswith('sofia_') and not line.startswith('#'):
            try:
                # Esempio: sofia_new_leads_total 0.0
                parts = line.split(' ')
                if len(parts) >= 2:
                    metric_name = parts[0]
                    metric_value = float(parts[1])
                    metrics[metric_name] = metric_value
            except:
                continue
    return metrics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 