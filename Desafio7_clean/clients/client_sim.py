# clients/client_sim.py
# ===========================================================
# "Baterista automático": genera logs y los envía por HTTP.
# - Usa un token por servicio (pulsera VIP).
# - Podés elegir servicio, tamaño del batch y repeticiones.
# - Envía en formato {"logs": [...]} (batch) o un solo objeto.
# ===========================================================

import json
import time
import random
import argparse
import requests
from datetime import datetime, timezone

# === Config básica (cambiar si tu server corre en otra IP/puerto) ===
SERVER_URL = "http://127.0.0.1:5000/logs"

# === Tokens deben MATCHEAR con tu server.py ===
TOKENS = {
    "billing":  "tok_bil_789",
    "users":    "tok_usr_456",
    "payments": "tok_pay_123",
}

SEVERITIES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
MESSAGES = [
    "inicio de ciclo de facturacion",
    "usuario facturado correctamente",
    "reintento de gateway",
    "timeout al conectar proveedor",
    "error al aplicar descuento",
    "confirmacion de pago",
    "validacion de datos",
    "actualizacion de perfil"
]

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def make_log(service: str) -> dict:
    """Crea un log válido para el servicio indicado."""
    return {
        "timestamp": now_utc_iso(),           # cuándo ocurrió en el cliente
        "service": service,                   # debe coincidir con el token
        "severity": random.choice(SEVERITIES),
        "message": random.choice(MESSAGES)
    }

def send_one(service: str) -> None:
    """Envía UN log (no batch)."""
    token = TOKENS[service]
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    payload = make_log(service)
    resp = requests.post(SERVER_URL, headers=headers, data=json.dumps(payload))
    print(f"[ONE] Status: {resp.status_code} -> {resp.text}")

def send_batch(service: str, n: int) -> None:
    """Envía n logs en un solo request como {'logs': [...]}."""
    token = TOKENS[service]
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    logs = [make_log(service) for _ in range(n)]
    payload = {"logs": logs}
    resp = requests.post(SERVER_URL, headers=headers, data=json.dumps(payload))
    print(f"[BATCH x{n}] Status: {resp.status_code} -> {resp.text}")

def main():
    parser = argparse.ArgumentParser(description="Cliente simulador de logs")
    parser.add_argument("--service", choices=TOKENS.keys(), default="billing",
                        help="Servicio que enviará los logs (debe coincidir con el token)")
    parser.add_argument("--mode", choices=["one", "batch"], default="batch",
                        help="Modo: 'one' envía 1 log; 'batch' envía varios por request")
    parser.add_argument("--batch-size", type=int, default=5,
                        help="Cantidad de logs por request en modo 'batch'")
    parser.add_argument("--repeat", type=int, default=3,
                        help="Cuántas veces repetir el envío")
    parser.add_argument("--sleep", type=float, default=1.0,
                        help="Segundos de espera entre repeticiones")
    args = parser.parse_args()

    print(f"Enviando logs del servicio '{args.service}' en modo '{args.mode}' "
          f"(batch_size={args.batch_size}, repeat={args.repeat})")

    for i in range(args.repeat):
        if args.mode == "one":
            send_one(args.service)
        else:
            send_batch(args.service, args.batch_size)
        time.sleep(args.sleep)

if __name__ == "__main__":
    main()
