"""
Customer ingestion and data management service.
"""
from datetime import datetime
from uuid import UUID
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.models import Customer, Order


# --- Datetime / UUID fields that need native Python types for asyncpg ---
_CUSTOMER_DATETIME_FIELDS = {"created_at", "updated_at", "last_order_date", "first_order_date"}
_CUSTOMER_UUID_FIELDS = {"id"}

_ORDER_DATETIME_FIELDS = {"created_at"}
_ORDER_UUID_FIELDS = {"id", "customer_id"}


def _coerce_types(record: dict, datetime_fields: set, uuid_fields: set) -> dict:
    """
    Convert ISO-format datetime strings → datetime objects and
    string UUIDs → uuid.UUID objects in-place.  asyncpg requires
    native Python types; it will not auto-cast from str.
    """
    for field in datetime_fields:
        val = record.get(field)
        if isinstance(val, str):
            record[field] = datetime.fromisoformat(val)

    for field in uuid_fields:
        val = record.get(field)
        if isinstance(val, str):
            record[field] = UUID(val)

    return record


async def ingest_customers(db: AsyncSession, customers_data: list[dict]) -> int:
    """
    Bulk upsert customers using Postgres INSERT ... ON CONFLICT DO UPDATE.
    """
    if not customers_data:
        return 0

    # Coerce str → datetime / UUID so asyncpg doesn't choke
    for rec in customers_data:
        _coerce_types(rec, _CUSTOMER_DATETIME_FIELDS, _CUSTOMER_UUID_FIELDS)

    stmt = pg_insert(Customer).values(customers_data)
    update_dict = {
        col.name: getattr(stmt.excluded, col.name)
        for col in Customer.__table__.columns
        if col.name not in ["id", "created_at"]
    }
    
    stmt = stmt.on_conflict_do_update(
        index_elements=["email"],
        set_=update_dict
    )
    
    await db.execute(stmt)
    await db.flush()
    return len(customers_data)


async def ingest_orders(db: AsyncSession, orders_data: list[dict]) -> int:
    """
    Bulk insert orders and update customer aggregates in batch.
    """
    if not orders_data:
        return 0

    # 1. Bulk resolve customer emails to IDs
    emails = list({o["customer_email"] for o in orders_data if o.get("customer_email")})
    email_to_id = {}
    if emails:
        stmt = select(Customer.email, Customer.id).where(Customer.email.in_(emails))
        result = await db.execute(stmt)
        for row in result.all():
            email_to_id[row.email] = row.id

    # 2. Prepare order dicts with resolved customer_ids
    valid_orders = []
    for o in orders_data:
        c_email = o.pop("customer_email", None)
        c_id = o.get("customer_id")
        if not c_id and c_email and c_email in email_to_id:
            c_id = email_to_id[c_email]
            
        if c_id:
            o["customer_id"] = c_id
            # Coerce str → datetime / UUID so asyncpg doesn't choke
            _coerce_types(o, _ORDER_DATETIME_FIELDS, _ORDER_UUID_FIELDS)
            valid_orders.append(o)
            
    if not valid_orders:
        return 0

    # 3. Bulk insert orders
    await db.execute(pg_insert(Order).values(valid_orders))
    await db.flush()

    # 4. Update aggregates in one go for ALL customers
    await _update_all_customer_aggregates(db)
    
    return len(valid_orders)


async def _update_all_customer_aggregates(db: AsyncSession):
    """Recalculate aggregates for all customers using a single bulk SQL update."""
    from sqlalchemy import text
    sql = """
    UPDATE customers
    SET 
        order_count = stats.order_count,
        total_spend = stats.total_spend,
        first_order_date = stats.first_order_date,
        last_order_date = stats.last_order_date,
        avg_order_value = CASE WHEN stats.order_count > 0 THEN stats.total_spend / stats.order_count ELSE 0 END,
        updated_at = NOW()
    FROM (
        SELECT 
            customer_id,
            COUNT(id) as order_count,
            COALESCE(SUM(amount), 0) as total_spend,
            MIN(created_at) as first_order_date,
            MAX(created_at) as last_order_date
        FROM orders
        GROUP BY customer_id
    ) AS stats
    WHERE customers.id = stats.customer_id;
    """
    await db.execute(text(sql))
