# server.py
# ======================== CAPA RÍTMICA (Base del sistema) ========================
# En esta sección levantamos el "metrónomo" (Flask) y armamos las "pistas" (SQLite).
# - Flask: framework web que nos deja definir endpoints como /health o /logs.
# - SQLite: base de datos liviana, archivo local "logs.db" donde guardamos eventos.

from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime, timezone
import os

app = Flask(__name__)
DB_PATH = os.environ.get("LOG_DB_PATH", "logs.db")  # Permite cambiar la ruta por variable de entorno

def get_conn():
    """
    Abre una conexión a SQLite y devuelve filas como dicts (sqlite3.Row).
    Esto es nuestra "cableado" hacia la mesa de mezcla (DB).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Crea la tabla 'logs' si no existe. Es como preparar las "pistas" del DAW.
    Campos:
      - timestamp: cuándo ocurrió el evento (enviado por el cliente)
      - service: quién tocó (servicio dueño del log)
      - severity: intensidad/criticidad (INFO, ERROR, etc.)
      - message: texto descriptivo
      - received_at: cuándo lo recibimos en el servidor (marca de tiempo del estudio)
      - token_used: con qué pase (token) entró
    """
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            service     TEXT NOT NULL,
            severity    TEXT NOT NULL,
            message     TEXT NOT NULL,
            received_at TEXT NOT NULL,
            token_used  TEXT NOT NULL
        );
        """)
        # Índices: como "buses" para encontrar rápido por tiempo o servicio.
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ts  ON logs(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_rcv ON logs(received_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_srv ON logs(service)")

def now_utc_iso():
    """ Devuelve tiempo actual en UTC ISO8601. Funciona como nuestro reloj maestro. """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Inicializamos la DB al cargar el módulo.
init_db()

@app.get("/health")
def health():
    """
    Endpoint simple para saber si el "estudio" está encendido y a tiempo.
    """
    return jsonify({"status": "ok", "time": now_utc_iso()})



# ======================== ACCESO AL ESTUDIO (Auth por token) =====================
# Pensalo como los "pases" para entrar a grabar. Cada token pertenece a un service.
VALID_TOKENS = {
    "tok_pay_123": "payments",
    "tok_usr_456": "users",
    "tok_bil_789": "billing",
}

# Niveles de severidad aceptados: definen la "intensidad" del evento.
ALLOWED_SEVERITIES = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

def get_token_and_owner():
    """
    Extrae el token del header Authorization: "Token <valor>".
    - Si el formato no es "Token ...", no hay acceso.
    - Si el token no está en VALID_TOKENS, tampoco.
    Devuelve (token, owner_service) o (None, None).
    """
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Token "):
        return None, None
    token = auth.split(" ", 1)[1].strip()
    owner = VALID_TOKENS.get(token)
    return token, owner

@app.post("/logs")
def receive_logs():
    """
    "Graba" logs que envían los clientes.
    Acepta 3 formatos:
      1) Un solo objeto: {timestamp, service, severity, message}
      2) Una lista de objetos: [ {...}, {...} ]
      3) Un objeto con clave "logs": {"logs": [ {...}, {...} ]}
    El flujo:
      - Chequeamos token (puerta del estudio).
      - Validamos Content-Type y JSON.
      - Normalizamos a una lista 'logs'.
      - Recorremos (for) cada log (ciclo de toma por toma):
          * chequear campos
          * chequear service dueño del token
          * chequear severity válida
          * acumular fila para insertar
      - Si hay filas válidas, INSERT masivo (executemany).
      - Devolvemos conteo de aceptados/fallidos y errores detallados.
    """
    token, owner_service = get_token_and_owner()
    if not token or not owner_service:
        return jsonify({"error": "Quién sos, bro?"}), 401  # Bloquea sin pase

    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "JSON inválido"}), 400

    # Normalización a lista: soportamos objeto, lista, o {"logs": [...]}
    if isinstance(payload, dict) and "logs" in payload:
        logs = payload["logs"]
    elif isinstance(payload, list):
        logs = payload
    elif isinstance(payload, dict):
        logs = [payload]
    else:
        return jsonify({"error": "Estructura JSON no soportada"}), 400

    accepted, failed = 0, 0
    errors = []
    rows = []

    # Recorremos (ciclo) cada "toma" y validamos
    for idx, item in enumerate(logs):
        if not isinstance(item, dict):
            failed += 1
            errors.append({"index": idx, "error": "cada log debe ser objeto JSON"})
            continue

        ts  = str(item.get("timestamp", "")).strip()
        srv = str(item.get("service", "")).strip()
        sev = str(item.get("severity", "")).strip().upper()
        msg = str(item.get("message", "")).strip()

        # Validaciones de presencia (condiciones tipo 'si no hay tal cosa, rechazar')
        if not ts or not srv or not sev or not msg:
            failed += 1
            errors.append({"index": idx, "error": "faltan campos requeridos"})
            continue

        # Coherencia de propietario: el pase (token) debe ser del mismo "service" que declara grabar
        if srv != owner_service:
            failed += 1
            errors.append({"index": idx, "error": f"token no coincide con service '{srv}'"})
            continue

        # Chequeo de severidad
        if sev not in ALLOWED_SEVERITIES:
            failed += 1
            errors.append({"index": idx, "error": f"severity inválida: {sev}"})
            continue

        # Si todo ok, preparamos fila para insertar (deferimos el INSERT para hacerlo por lote)
        rows.append((ts, srv, sev, msg, now_utc_iso(), token))
        accepted += 1

    # Inserción por lote si hay algo válido (optimiza I/O)
    if rows:
        with get_conn() as conn:
            conn.executemany("""
                INSERT INTO logs(timestamp, service, severity, message, received_at, token_used)
                VALUES (?, ?, ?, ?, ?, ?)
            """, rows)

    return jsonify({
        "accepted": accepted,
        "failed": failed,
        "errors": errors
    }), (200 if accepted else 400 if failed else 200)
@app.get("/logs")
def list_logs():
    """
    Consulta de logs con filtros opcionales:
      - timestamp_start, timestamp_end
      - received_at_start, received_at_end
      - service, severity
      - limit (default 100), offset (default 0)
    Devuelve ordenado por received_at DESC, id DESC.
    """
    qp = request.args

    timestamp_start   = qp.get("timestamp_start")
    timestamp_end     = qp.get("timestamp_end")
    received_at_start = qp.get("received_at_start")
    received_at_end   = qp.get("received_at_end")
    service           = qp.get("service")
    severity          = qp.get("severity")

    try:
        limit  = int(qp.get("limit", 100))
        offset = int(qp.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit/offset deben ser enteros"}), 400

    clauses, params = [], []

    if timestamp_start:
        clauses.append("timestamp >= ?")
        params.append(timestamp_start)
    if timestamp_end:
        clauses.append("timestamp <= ?")
        params.append(timestamp_end)
    if received_at_start:
        clauses.append("received_at >= ?")
        params.append(received_at_start)
    if received_at_end:
        clauses.append("received_at <= ?")
        params.append(received_at_end)
    if service:
        clauses.append("service = ?")
        params.append(service)
    if severity:
        clauses.append("severity = ?")
        params.append(severity)

    where_sql = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"""
        SELECT id, timestamp, service, severity, message, received_at, token_used
        FROM logs
        {where_sql}
        ORDER BY received_at DESC, id DESC
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])

    with get_conn() as conn:
        cur = conn.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]

    return jsonify({"count": len(rows), "results": rows})


if __name__ == "__main__":
    # host=0.0.0.0 expone el server a tu red local; port=5000 por convención.
    app.run(host="0.0.0.0", port=5000, debug=True)
