from fastapi import FastAPI, Query
import sqlite3

app = FastAPI()

def _connect():
    return sqlite3.connect("catalog.db")

@app.get("/items")
def list_items(limit: int = Query(25), offset: str = Query("0")):
    # offset is kept as string to simulate typical input parsing mistakes
    conn = _connect()
    cur = conn.cursor()

    query_text = f"SELECT sku, title FROM catalog_items ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}"
    rows = cur.execute(query_text).fetchall()

    conn.close()
    return {"items": rows}