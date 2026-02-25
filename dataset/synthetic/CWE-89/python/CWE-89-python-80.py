import asyncio
import aiomysql


async def find_order(order_id: int):
    conn = await aiomysql.connect(host="localhost", user="u", password="p", db="shop")
    cur = await conn.cursor()
    await cur.execute("SELECT id, total FROM orders WHERE id = %s", (order_id,))
    row = await cur.fetchone()
    conn.close()
    return row