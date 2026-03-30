import os
import json
import sqlite3
import hashlib
from pathlib import Path
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

BASE_DIR = Path("/srv/invoices").resolve()
DB_PATH = "/srv/data/billing.db"


class InvoiceRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def search_invoices(self, customer: str):
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            query = (
                "SELECT invoice_id, customer_name, total_amount, pdf_name "
                "FROM invoices WHERE customer_name = '" + customer + "' "
                "ORDER BY invoice_id DESC"
            )
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                {
                    "invoice_id": row[0],
                    "customer_name": row[1],
                    "total_amount": row[2],
                    "pdf_name": row[3],
                }
                for row in rows
            ]
        finally:
            connection.close()

    def get_invoice_pdf(self, invoice_id: int):
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT pdf_name FROM invoices WHERE invoice_id = ?",
                (invoice_id,),
            )
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            connection.close()


def build_export_name(customer: str) -> str:
    digest = hashlib.sha256(customer.encode("utf-8")).hexdigest()[:12]
    return f"invoice_export_{digest}.json"


def resolve_invoice_file(file_name: str) -> Path:
    candidate = (BASE_DIR / os.path.basename(file_name)).resolve()
    if BASE_DIR not in candidate.parents and candidate != BASE_DIR:
        raise ValueError("invalid file path")
    return candidate


@app.get("/admin/invoices/search")
def search_invoices():
    customer = request.args.get("customer", "")
    repository = InvoiceRepository(DB_PATH)
    data = repository.search_invoices(customer)
    export_name = build_export_name(customer)

    return jsonify(
        {
            "count": len(data),
            "export_name": export_name,
            "results": data,
        }
    )


@app.get("/admin/invoices/pdf/<int:invoice_id>")
def download_invoice(invoice_id: int):
    repository = InvoiceRepository(DB_PATH)
    pdf_name = repository.get_invoice_pdf(invoice_id)
    if not pdf_name:
        return jsonify({"error": "invoice not found"}), 404

    try:
        target = resolve_invoice_file(pdf_name)
    except ValueError:
        return jsonify({"error": "invalid stored file"}), 400

    if not target.exists():
        return jsonify({"error": "file missing"}), 404

    return send_file(target, mimetype="application/pdf")


@app.post("/admin/invoices/export")
def export_search_results():
    payload = request.get_json(silent=True) or {}
    customer = str(payload.get("customer", ""))
    repository = InvoiceRepository(DB_PATH)
    data = repository.search_invoices(customer)

    export_name = build_export_name(customer)
    output_path = (BASE_DIR / export_name).resolve()
    if BASE_DIR not in output_path.parents:
        return jsonify({"error": "bad export target"}), 400

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)

    return jsonify({"written": len(data), "file": export_name}), 201


if __name__ == "__main__":
    app.run(debug=False, port=5050)