from fastapi import FastAPI
from pydantic import BaseModel
from agents import Runner, UserMessage
from agent_factory import make_intelligent_luna
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("luna-agent")

# FastAPI application creation
app = FastAPI(title="LUNA Smart Controller API")

# Intelligent agent creation
# For testing: use ip="127.0.0.1"
agent = make_intelligent_luna(ip="192.168.200.1", unit=0)

class Prompt(BaseModel):
    message: str

@app.post("/chat")
async def chat(p: Prompt):
    """
    Endpoint to send commands to the agent
    """
    logger.info(f"Received command: {p.message}")
    run = await Runner.run(agent, [UserMessage(p.message)])
    risposta = run.final_output
    logger.info(f"Response: {risposta}")
    return {"reply": risposta}

@app.get("/status")
async def status():
    """
    Endpoint to get the current system status
    """
    run = await Runner.run(agent, [UserMessage("Qual è lo stato attuale?")])
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "status": run.final_output
    }

# Scheduler for automatic execution
scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('cron', minute='*/5')
async def ai_decision_loop():
    """
    Performs an evaluation every 5 minutes
    """
    ora = datetime.datetime.now().strftime("%H:%M")
    logger.info(f"Automatic execution at {ora}")
    
    # The agent reasons and makes an autonomous decision
    run = await Runner.run(agent, [UserMessage(
        f"Sono le {ora}. Valuta i dati attuali e prendi la decisione ottimale."
    )])
    
    logger.info(f"Decision: {run.final_output}")

# Start the scheduler when the application starts
@app.on_event("startup")
async def startup_event():
    scheduler.start()
    logger.info("Scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    logger.info("Scheduler stopped") 