import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path

class VeriFactuCore:
    def __init__(self, db_path="data/verifactu.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    previous_hash TEXT,
                    current_hash TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    status TEXT NOT NULL
                )
            """)

    def _log_event(self, action, details, status="SUCCESS"):
        timestamp = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO audit_logs (timestamp, action, details, status) VALUES (?, ?, ?, ?)",
                (timestamp, action, details, status)
            )

    def get_last_hash(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT current_hash FROM invoices ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else "0" * 64

    def generate_invoice_hash(self, invoice_data, previous_hash):
        content = json.dumps(invoice_data, sort_keys=True) + previous_hash
        return hashlib.sha256(content.encode()).hexdigest()

    def add_invoice(self, invoice_id, amount):
        try:
            date = datetime.now().strftime("%Y-%m-%d")
            previous_hash = self.get_last_hash()
            
            invoice_data = {
                "invoice_id": invoice_id,
                "date": date,
                "amount": amount
            }
            
            current_hash = self.generate_invoice_hash(invoice_data, previous_hash)
            timestamp = datetime.now().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO invoices (invoice_id, date, amount, previous_hash, current_hash, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (invoice_id, date, amount, previous_hash, current_hash, timestamp)
                )
            
            self._log_event("CREATE_INVOICE", f"ID: {invoice_id}, Hash: {current_hash[:10]}...")
            return current_hash
        except Exception as e:
            self._log_event("CREATE_INVOICE", str(e), status="FAILED")
            raise

if __name__ == "__main__":
    vf = VeriFactuCore()
    h1 = vf.add_invoice("FAC-001", 150.50)
    print(f"Factura 1 añadida. Hash: {h1}")
    h2 = vf.add_invoice("FAC-002", 200.00)
    print(f"Factura 2 añadida. Hash: {h2}")
