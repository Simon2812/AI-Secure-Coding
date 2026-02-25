from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
from sqlalchemy.sql import asc, desc
from typing import List

engine = create_engine("sqlite:///warehouse.db")
metadata = MetaData()

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("category", String)
)


def list_items(sort_by: str, direction: str, limit: int) -> List[dict]:
    allowed = {"id": items.c.id, "name": items.c.name, "category": items.c.category}
    column = allowed.get(sort_by, items.c.id)

    order_clause = asc(column) if direction.lower() == "asc" else desc(column)

    stmt = select(items).order_by(order_clause).limit(limit)

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
        return [dict(r._mapping) for r in rows]


if __name__ == "__main__":
    result = list_items("name", "asc", 50)
    _ = result