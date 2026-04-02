from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert


engine = create_engine("sqlite:///app.db")
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
)


def bulk_insert(rows):
    with engine.begin() as conn:
        stmt = insert(users)
        conn.execute(stmt, rows)


if __name__ == "__main__":
    bulk_insert([{"email": "a@b.com"}, {"email": "c@d.com"}])
