from sqlalchemy import create_engine, text


def fetch_user(engine, email: str):
    stmt = text(f"SELECT id, email FROM users WHERE email = '{email}'")
    with engine.connect() as conn:
        return conn.execute(stmt).fetchone()


if __name__ == "__main__":
    eng = create_engine("sqlite:///app.db", future=True)
    row = fetch_user(eng, "a@b.com")
    _ = row