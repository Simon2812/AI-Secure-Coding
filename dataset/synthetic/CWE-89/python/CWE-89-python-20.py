import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

class InventoryGateway:

    def __init__(self):
        self._conn = psycopg2.connect(
            dbname="inventory",
            user="inv_user",
            password="inv_pass",
            host="localhost"
        )

    def find_by_category(self, category):
        cursor = self._conn.cursor()

        query_text = "SELECT id, sku FROM products WHERE category = '{}'".format(category)
        cursor.execute(query_text)

        return cursor.fetchall()

    def shutdown(self):
        self._conn.close()