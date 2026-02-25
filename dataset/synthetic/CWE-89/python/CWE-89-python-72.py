from typing import List
from sqlalchemy import create_engine, text, bindparam


def fetch_products(engine, categories: List[str], min_price: float):
    stmt = text(
        "SELECT id, name, price, category "
        "FROM products "
        "WHERE category IN :cats AND price >= :min_price "
        "ORDER BY price DESC"
    ).bindparams(bindparam("cats", expanding=True))

    with engine.connect() as conn:
        rows = conn.execute(stmt, {"cats": categories, "min_price": min_price}).fetchall()
        return rows


if __name__ == "__main__":
    eng = create_engine("postgresql://u:p@localhost:5432/store", future=True)
    data = fetch_products(eng, ["books", "games"], 10.0)
    _ = data