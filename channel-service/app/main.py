from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from app.simulator import simulate_delivery

app = FastAPI(title="XENO Channel Service Stub")

class SendRequest(BaseModel):
    communications: list[dict]
    callback_url: str

@app.post("/channel/send")
async def send_communications(request: SendRequest, background_tasks: BackgroundTasks):
    """
    Accepts a batch of communications, responds immediately, 
    and simulates delivery/engagement asynchronously.
    """
    background_tasks.add_task(simulate_delivery, request.communications, request.callback_url)
    return {"status": "accepted", "message": f"Processing {len(request.communications)} communications."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
