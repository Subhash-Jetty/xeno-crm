import asyncio
import random
import httpx
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def simulate_delivery(communications: list[dict], callback_url: str):
    """
    Simulate the lifecycle of a batch of communications.
    Sends receipts back to the CRM asynchronously.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Step 1: Initial "sent" / "failed" status
        receipts = []
        for comm in communications:
            # 10% chance of immediate failure
            if random.random() < 0.10:
                receipts.append({
                    "communication_id": comm["communication_id"],
                    "status": "failed",
                    "timestamp": datetime.utcnow().isoformat(),
                    "error_message": "Invalid recipient address or network failure"
                })
            else:
                receipts.append({
                    "communication_id": comm["communication_id"],
                    "status": "delivered",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        # Send first batch of receipts
        try:
            await client.post(callback_url, json={"receipts": receipts})
        except Exception as e:
            logger.error(f"Failed to send callback to {callback_url}: {e}")
            return

        # Keep track of delivered communications for further engagement
        delivered_comms = [r for r in receipts if r["status"] == "delivered"]
        
        # Simulate Opens (60% of delivered)
        await asyncio.sleep(random.uniform(2.0, 5.0))
        open_receipts = []
        opened_comms = []
        for r in delivered_comms:
            if random.random() < 0.60:
                opened_comms.append(r)
                open_receipts.append({
                    "communication_id": r["communication_id"],
                    "status": "opened",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        if open_receipts:
            try:
                await client.post(callback_url, json={"receipts": open_receipts})
            except Exception as e:
                logger.error(f"Failed to send open callbacks: {e}")

        # Simulate Reads (70% of opened)
        await asyncio.sleep(random.uniform(1.0, 3.0))
        read_receipts = []
        read_comms = []
        for r in opened_comms:
            if random.random() < 0.70:
                read_comms.append(r)
                read_receipts.append({
                    "communication_id": r["communication_id"],
                    "status": "read",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        if read_receipts:
            try:
                await client.post(callback_url, json={"receipts": read_receipts})
            except Exception as e:
                logger.error(f"Failed to send read callbacks: {e}")

        # Simulate Clicks (30% of read)
        await asyncio.sleep(random.uniform(1.0, 4.0))
        click_receipts = []
        for r in read_comms:
            if random.random() < 0.30:
                click_receipts.append({
                    "communication_id": r["communication_id"],
                    "status": "clicked",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        if click_receipts:
            try:
                await client.post(callback_url, json={"receipts": click_receipts})
            except Exception as e:
                logger.error(f"Failed to send click callbacks: {e}")
