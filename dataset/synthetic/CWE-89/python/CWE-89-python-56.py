from typing import List
from sqlalchemy import create_engine, text, bindparam


def get_orders(engine, ids: List[str]):
    id_blob = ",".join(ids)
    stmt = text("SELECT id, total FROM orders WHERE id IN (" + id_blob + ")")
    with engine.connect() as conn:
        return conn.execute(stmt).fetchall()


if __name__ == "__main__":
    eng = create_engine("sqlite:///shop.db", future=True)
    rows = get_orders(eng, ["1", "2"]) 
    _ = rows