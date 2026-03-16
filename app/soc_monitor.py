import sqlite3
from core import VeriFactuCore
import sys

def simulate_integrity_check():
    vf = VeriFactuCore()
    print("[SOC] Iniciando verificación de integridad de la cadena VeriFactu...")
    
    with sqlite3.connect(vf.db_path) as conn:
        cursor = conn.execute("SELECT id, invoice_id, date, amount, previous_hash, current_hash FROM invoices ORDER BY id ASC")
        rows = cursor.fetchall()
        
        expected_prev_hash = "0" * 64
        for row in rows:
            id_db, inv_id, date, amount, prev_h, curr_h = row
            
            # Re-calcular hash
            invoice_data = {"invoice_id": inv_id, "date": date, "amount": amount}
            calculated_hash = vf.generate_invoice_hash(invoice_data, prev_h)
            
            if calculated_hash != curr_h:
                print(f"\n[!!!] ALERTA DE SEGURIDAD: Brecha de integridad detectada en Factura ID {id_db} ({inv_id})")
                print(f"      Hash en DB: {curr_h}")
                print(f"      Hash calculado: {calculated_hash}")
                vf._log_event("INTEGRITY_ALERT", f"Tampering detected in invoice {inv_id}", status="CRITICAL")
                return False
            
            if prev_h != expected_prev_hash:
                 print(f"\n[!!!] ALERTA DE SEGURIDAD: Cadena rota en Factura ID {id_db} ({inv_id})")
                 vf._log_event("CHAIN_BROKEN_ALERT", f"Chain mismatch in invoice {inv_id}", status="CRITICAL")
                 return False
            
            expected_prev_hash = curr_h
            
    print("\n[OK] Integridad de datos verificada con éxito. No se detectaron manipulaciones.")
    vf._log_event("INTEGRITY_CHECK", "Full database verified", status="SUCCESS")
    return True

def simulate_tamper():
    print("[ATTACK] Simulando ataque de inyección directa en base de datos...")
    vf = VeriFactuCore()
    with sqlite3.connect(vf.db_path) as conn:
        conn.execute("UPDATE invoices SET amount = 99999.0 WHERE id = 1")
    print("[ATTACK] Modificación ilegal completada en Factura #1.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--attack":
        simulate_tamper()
    else:
        simulate_integrity_check()
