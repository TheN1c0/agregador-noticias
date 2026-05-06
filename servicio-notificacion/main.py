# main.py — Punto de entrada del servicio de notificación
import threading
from fastapi import FastAPI
from dotenv import load_dotenv

from pubsub_subscriber import escuchar

# Carga las variables de entorno desde .env
load_dotenv()

app = FastAPI(
    title="Servicio de Notificación - Agregador de Noticias Financieras",
    description="Escucha eventos de noticias clasificadas desde Pub/Sub y las notifica.",
    version="1.0.0",
)


@app.on_event("startup")
def iniciar_subscriber():
    """Al arrancar FastAPI, lanza el subscriber de Pub/Sub en un hilo separado."""
    hilo = threading.Thread(target=escuchar, daemon=True)
    hilo.start()
    print("[INFO] Subscriber de Pub/Sub iniciado en hilo separado.")


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que el servicio está corriendo."""
    return {"status": "ok"}
