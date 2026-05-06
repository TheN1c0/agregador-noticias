# pubsub_subscriber.py — Escucha mensajes de noticias clasificadas desde Pub/Sub
import os
import json
from google.cloud import pubsub_v1

# Configuración del proyecto y subscription
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SUBSCRIPTION_ID = "notificaciones-sub"

if not GCP_PROJECT_ID:
    raise EnvironmentError("La variable de entorno GCP_PROJECT_ID no está definida.")


def callback(message):
    """Procesa cada mensaje recibido de Pub/Sub: lo imprime y hace acknowledge."""
    try:
        # Decodifica el mensaje JSON
        datos = json.loads(message.data.decode("utf-8"))

        categoria = datos.get("categoria", "desconocida")
        titulo = datos.get("titulo", "sin título")

        # Imprime la notificación en consola con formato legible
        print(f"[NOTIFICACIÓN] Categoría: {categoria} | Título: {titulo}")

        # Confirma que el mensaje fue procesado correctamente
        message.ack()

    except Exception as e:
        print(f"[ERROR] No se pudo procesar el mensaje: {e}")
        # No hace ack para que Pub/Sub reintente la entrega
        message.nack()


def escuchar():
    """Se suscribe al subscription de Pub/Sub y escucha mensajes indefinidamente."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, SUBSCRIPTION_ID)

    print(f"[INFO] Escuchando mensajes en {subscription_path}...")

    # Inicia la escucha. result() bloquea el hilo indefinidamente.
    streaming_pull = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull.result()
    except Exception as e:
        print(f"[ERROR] El subscriber se detuvo: {e}")
        streaming_pull.cancel()
        streaming_pull.result()
