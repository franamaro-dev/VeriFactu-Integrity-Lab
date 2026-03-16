# [SOC-L1] Incident Response Playbook: Unauthorized Data Modification

Este documento describe el procedimiento estándar (SOP) para responder a una alerta de integridad física en la base de datos de VeriFactu.

## 1. Detección (Fase L1)
- **Sensor**: `app/soc_monitor.py`.
- **Alert Type**: `INTEGRITY_ALERT (CRITICAL)`.
- **Trigger**: Discrepancia detectada entre el hash almacenado y el contenido real de una factura (Tampering).

## 2. Análisis y Triaje
- [ ] Verificar logs en `audit_logs` para identificar la ventana de tiempo de la modificación.
- [ ] Comparar el `current_hash` actual con el `previous_hash` de la siguiente factura para confirmar si la cadena se rompió.
- [ ] Identificar si el cambio fue por DB (bypass de lógica) o por el API (autorización comprometida).

## 3. Contención
- [ ] Aislar el servidor de base de datos de la red.
- [ ] Suspender credenciales de acceso administrativo temporalmente.
- [ ] Bloquear IPs sospechosas en el Firewall/WAF.

## 4. Erradicación y Recuperación
- [ ] Restaurar la base de datos desde el último backup íntegro verificado.
- [ ] Re-ejecutar el `soc_monitor.py` para asegurar que la integridad ha vuelto al 100%.

## 5. Lecciones Aprendidas (Post-Mortem)
- ¿Cómo se saltó el atacante la lógica de la aplicación?
- ¿Faltaba cifrado en reposo o permisos de sistema de archivos más restrictivos?
- Actualizar el motor de firmas en el Honeypot si el ataque fue vía Web.
