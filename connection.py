from aiopg import create_pool
import asyncpg

from config import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PORT
)

DB_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


async def log_event(user_id: int, username: str, event: str):
    conn = await asyncpg.connect(dsn=DB_DSN)
    try:
        exists = await conn.fetchval("""
            SELECT 1 FROM user_metrics
            WHERE user_id = $1 AND event = $2
        """, user_id, event)

        if not exists:
            await conn.execute("""
                INSERT INTO user_metrics (user_id, username, event)
                VALUES ($1, $2, $3)
            """, user_id, username, event)
    finally:
        await conn.close()


async def get_metrics_v1():
    conn = await asyncpg.connect(dsn=DB_DSN)
    try:
        rows = await conn.fetch("""
            SELECT event, COUNT(DISTINCT user_id) AS unique_users
            FROM user_metrics
            GROUP BY event
            ORDER BY event
        """)
        return rows
    finally:
        await conn.close()

async def get_metrics():
    conn = await asyncpg.connect(dsn=DB_DSN)
    try:
        rows = await conn.fetch("""
            SELECT event, array_agg(username) AS usernames
            FROM user_metrics
            GROUP BY event
        """)
        return {row["event"]: row["usernames"] for row in rows}
    finally:
        await conn.close()
