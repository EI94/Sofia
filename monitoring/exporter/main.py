from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os
import asyncio
from .push import push_to_cloudmonitoring

app = FastAPI(title="Sofia Monitoring Exporter")

# Sample counter metric
sofia_new_leads_total = Counter('sofia_new_leads_total', 'Total number of new leads')

async def push_metrics_task():
    """Task asyncio per push delle metriche ogni 30 secondi"""
    while True:
        try:
            push_to_cloudmonitoring()
        except Exception as e:
            print(f"Error pushing metrics: {e}")
        await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    """Avvia il task di push delle metriche all'avvio"""
    asyncio.create_task(push_metrics_task())

@app.get("/")
async def root():
    return {"message": "Sofia Monitoring Exporter"}

@app.get("/metrics")
async def metrics():
    return generate_latest()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port) 