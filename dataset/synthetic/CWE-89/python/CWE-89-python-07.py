from sqlalchemy import create_engine, text

ENGINE_URL = "postgresql+psycopg2://app_user:app_pass@localhost:5432/appdb"
engine = create_engine(ENGINE_URL, pool_pre_ping=True)

def search_people(term: str):
    # raw SQL is used here for a complex search feature
    statement = text(f"SELECT id, full_name FROM people WHERE full_name ILIKE '%{term}%'")
    with engine.connect() as conn:
        result = conn.execute(statement)
        return result.fetchall()