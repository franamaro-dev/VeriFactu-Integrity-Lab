# 💰 VeriFactu-SOC-Demo

### Inalterabilidad Fiscal y Monitorización de Integridad (MVP)

Este proyecto demuestra la implementación técnica de la **Ley Antifraude (VeriFactu)** en España, combinada con capacidades de un **Analista SOC L1** para detectar manipulaciones no autorizadas.

---

## 🛡️ Propósito del Proyecto

Demostrar cómo un desarrollador con enfoque en ciberseguridad puede:
1.  **Garantizar la inalterabilidad** de registros financieros mediante encadenamiento de hashes (SHA-256).
2.  **Implementar Trazabilidad** total mediante logs de auditoría detallados.
3.  **Configurar Alertas de Integridad** que simulan el comportamiento de un SIEM ante una brecha de datos.

---

## 🏗️ Arquitectura Técnica

- **Lenguaje**: Python 3.11
- **Base de Datos**: SQLite (Simulación de ledger persistente)
- **Seguridad**: Hashing criptográfico SHA-256 (Blockchain-style chaining)

### El "Caballo de Troya" SOC
Aunque el sistema gestiona facturas, incluye un `soc_monitor.py` que actúa como sensor de integridad:
- **Detección de Intrusos**: Verifica recursivamente que cada factura coincida con su hash y que la cadena no haya sido rota.
- **Respuesta ante Incidentes**: Genera logs de severidad `CRITICAL` ante discrepancias, listos para ser consumidos por un SIEM o automatizados vía Webhooks (n8n).

---

## 🚀 Guía de Uso

### 1. Generar Datos Iniciales
Ejecuta el núcleo del sistema para crear facturas válidas:
```bash
python app/core.py
```

### 2. Verificar Integridad (SOC Check)
Comprueba que los datos son íntegros:
```bash
python app/soc_monitor.py
```

### 3. Simular un Ataque (Bypassing Application Logic)
Simula a un atacante que modifica la base de datos saltándose la lógica de la aplicación:
```bash
python app/soc_monitor.py --attack
```

### 4. Detección del Incidente
Vuelve a ejecutar la verificación para ver cómo el monitor SOC detecta la intrusión:
```bash
python app/soc_monitor.py
```

---

## 📑 Ejemplo de Logs de Auditoría (Formato SOC)
| Timestamp | Acción | Detalles | Estado |
|-----------|---------|---------|--------|
| 2024-03-16T... | CREATE_INVOICE | ID: FAC-001, Hash: a3f2... | SUCCESS |
| 2024-03-16T... | INTEGRITY_CHECK | Full database verified | SUCCESS |
| 2024-03-16T... | INTEGRITY_ALERT | Tampering detected in invoice FAC-001 | **CRITICAL** |

---

## 👨‍💻 Perfil Analista
Este proyecto refleja conocimientos en:
- **Criptografía Aplicada**: Integridad de datos y funciones Hash.
- **Análisis Forense**: Reconstrucción de cadena de eventos.
- **Monitorización de Seguridad**: Diseño de checks de integridad proactivos.
