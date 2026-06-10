import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import async_session_maker
from sqlalchemy import text

async def verify():
    async with async_session_maker() as s:
        r1 = await s.execute(text('SELECT COUNT(*) FROM customers'))
        r2 = await s.execute(text('SELECT COUNT(*) FROM orders'))
        c_count = r1.scalar()
        o_count = r2.scalar()
        print(f"Customers: {c_count}")
        print(f"Orders: {o_count}")

        r3 = await s.execute(text(
            'SELECT name, total_spend, order_count FROM customers '
            'ORDER BY total_spend DESC LIMIT 5'
        ))
        print("\nTop 5 customers by spend:")
        for row in r3.all():
            print(f"  {row.name} - spend={row.total_spend}, orders={row.order_count}")

asyncio.run(verify())
