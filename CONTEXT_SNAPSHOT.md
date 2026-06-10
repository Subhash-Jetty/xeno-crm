# XENO CRM - Project Context Snapshot

## Project Overview
This project is an AI-native customer engagement platform (a Mini CRM) built for a Forward Deployed Engineer (FDE) assignment at Xeno. The application acts as an autonomous AI agent for a coffee chain called "BeanBox", capable of creating segments, drafting personalized messages, and launching omnichannel marketing campaigns.

## Architecture & Tech Stack
1. **Frontend**: Next.js (App Router), Vanilla CSS (Custom Glassmorphism Dark Mode UI). Running on port 3000.
2. **Backend**: FastAPI, SQLAlchemy (Async), PostgreSQL (Supabase). Running on port 8000.
3. **Channel Service**: A separate FastAPI stub service simulating delivery, opens, reads, and clicks asynchronously. Running on port 8001.
4. **AI Agent**: 
   - Primary: **Groq (Llama 3.3 70B)** (Blazing fast for chat-first interactions).
   - Fallback: **Gemini 2.5 Flash** (Handles rate limits gracefully).

## Database Schema (Supabase)
- `customers`: id, name, email, phone, total_spend, order_count, last_order_date, tags.
- `orders`: id, customer_id, items, amount, channel, status.
- `segments`: id, rules, customer_count, natural_language_query, is_ai_generated.
- `segment_members`: Link table for materialized segment lists.
- `campaigns`: id, segment_id, message_template, channel, status, funnel stats.
- `communications`: Individual tracking records per user for campaign execution.
- `ai_conversations`: JSON storage for agent conversation history.

## What We Have Accomplished
1. **Full Scaffolding**: Both the Next.js frontend, FastAPI backend, and Channel Service have been completely coded.
2. **AI Tool Execution Loop**: We built a function-calling loop in `ai_agent.py` so the AI can execute querying, segmentation, messaging, and insights.
3. **Seed Data**: Wrote `generate_seed_data.py` (which created 1000 customers / 5000 orders) and an `ingest.py` script.
4. **Environment Setup**: The user created a Supabase project, executed `schema.sql`, and provided Groq and Gemini API keys stored in `backend/.env`.
5. **Python 3.12 Downgrade**: We downgraded from Python 3.14 to 3.12 and created a new `venv` to fix native compilation issues with `asyncpg` and `orjson`.
6. **Network Firewall Fix**: The university network blocks the PostgreSQL protocol via DPI. We installed and connected to **Cloudflare WARP** to successfully tunnel traffic to Supabase port 5432.
7. **Startup Script Fixes**: Refactored `start.ps1` to use absolute paths, ensuring the Channel Service and Backend start correctly in the background. We also added an `__init__.py` to `channel-service/app/`.
8. **Ingestion Optimization**: Completely rewrote the `ingestion.py` functions to use bulk SQLAlchemy `pg_insert` (ON CONFLICT DO UPDATE) and bulk raw SQL `UPDATE`s, reducing ingestion time from ~20 minutes to 2 seconds.
9. **UI Verification**: Successfully verified that the Next.js frontend (port 3000) and the AI Assistant chat interface are fully functional.

## The Current Error State (CRITICAL FOR NEXT AGENT)
The services (Frontend, Backend, Channel Service) are all successfully booting up via `start.ps1`, but the **seed data ingestion step still fails** with the following error during order ingestion:

```text
sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $8: '2026-04-28T08:40:38.782215' (expected a datetime.date or datetime.datetime instance, got 'str')
```

- **Why?** The `asyncpg` driver in SQLAlchemy strictly requires Python `datetime` objects for `TIMESTAMP` columns during bulk inserts. The `ingest.py` script currently loads the JSON string (e.g., `"created_at": "2026-04-28T..."`) and passes it directly to `pg_insert(Order).values(valid_orders)`.
- **What needs fixing?** In `backend/app/services/ingestion.py`, we need to parse the string dates into Python `datetime` objects for both `customers` and `orders` before passing them to the bulk insert operations. Also ensure the `items` JSON is correctly formatted as a python list/dict.

## Next Immediate Steps for the New Agent
1. **Fix Ingestion Date Parsing**: Update `ingest_customers` and `ingest_orders` in `backend/app/services/ingestion.py` to correctly parse `created_at` (and `updated_at` if present) from ISO strings to `datetime.fromisoformat()` objects.
2. **Re-run the Setup**: Execute `start.ps1` again to successfully populate the Supabase DB.
3. **Deployment Preparation**: After confirming local functionality and data, guide the user to deploy the Frontend to Vercel, the Backend to Koyeb, and the Channel Service to Render.

## Persona Directives
You are Antigravity (playing the role of an expert FDE). Maintain extreme technical competence, keep the UI beautiful, and ensure a magical demo experience for the evaluators. Avoid tedious manual work for the user whenever possible by leveraging local terminal execution.
