"""
Order API routes — bulk ingest.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import OrderBulkIngest, MessageResponse
from app.services.ingestion import ingest_orders

router = APIRouter()


@router.post("/ingest", response_model=MessageResponse)
async def bulk_ingest(payload: OrderBulkIngest, db: AsyncSession = Depends(get_db)):
    """Bulk ingest orders. Auto-updates customer aggregates."""
    data = [o.model_dump() for o in payload.orders]
    count = await ingest_orders(db, data)
    return MessageResponse(message=f"Successfully ingested {count} orders", count=count)
