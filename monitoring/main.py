from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os
import asyncio

app = FastAPI(title="Sofia Monitoring Exporter")

# Sample counter metric
sofia_new_leads_total = Counter('sofia_new_leads_total', 'Total number of new leads')

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