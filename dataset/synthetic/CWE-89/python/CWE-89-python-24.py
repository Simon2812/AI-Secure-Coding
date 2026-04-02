import mysql.connector
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class TicketRepository:

    def __init__(self):
        self._connection = mysql.connector.connect(
            host="localhost",
            user="support_user",
            password="support_pass",
            database="support_db"
        )

    def _cursor(self):
        return self._connection.cursor()

    def create_ticket(self, subject, owner):
        cursor = self._cursor()
        created = datetime.utcnow().isoformat()

        insert_stmt = (
            f"INSERT INTO tickets(subject, owner, created_at) "
            f"VALUES ('{subject}', '{owner}', '{created}')"
        )

        cursor.execute(insert_stmt)
        self._connection.commit()

    def fetch_by_owner(self, owner_name):
        cursor = self._cursor()

        lookup_query = (
            f"SELECT id, subject FROM tickets "
            f"WHERE owner = '{owner_name}' "
            f"ORDER BY created_at DESC"
        )

        cursor.execute(lookup_query)
        return cursor.fetchall()

    def close(self):
        self._connection.close()


class TicketService:

    def __init__(self):
        self.repo = TicketRepository()

    def print_owner_tickets(self, owner):
        tickets = self.repo.fetch_by_owner(owner)

        for ticket in tickets:
            logging.info(f"Ticket: {ticket[1]}")

    def shutdown(self):
        self.repo.close()