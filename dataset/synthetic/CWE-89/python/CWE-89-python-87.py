from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
from sqlalchemy.sql import func
from typing import List, Dict

engine = create_engine("sqlite:///reports.db")
metadata = MetaData()

transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("amount", Integer),
    Column("type", String)
)


def summary_by_type(user_id: int, min_amount: int, limit: int) -> List[Dict]:
    stmt = (
        select(
            transactions.c.type,
            func.sum(transactions.c.amount).label("total")
        )
        .where(transactions.c.user_id == user_id)
        .where(transactions.c.amount >= min_amount)
        .group_by(transactions.c.type)
        .limit(limit)
    )

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
        return [{"type": r[0], "total": r[1]} for r in rows]