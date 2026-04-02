from sqlalchemy import create_engine, text


class StockReport:
    def __init__(self, engine):
        self._engine = engine

    def low_stock(self, threshold: int, order_by: str):
        sql = (
            "SELECT sku, qty, updated_at "
            "FROM stock_items "
            "WHERE qty <= :threshold "
        )

        sql += "ORDER BY " + order_by + " ASC"

        stmt = text(sql)

        with self._engine.connect() as conn:
            return conn.execute(stmt, {"threshold": threshold}).fetchall()


engine = create_engine("sqlite:///warehouse.db", future=True)
report = StockReport(engine)