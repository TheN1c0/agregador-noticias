import os
import json
from google.cloud import pubsub_v1

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = "noticias-financieras"

if not GCP_PROJECT_ID:
    raise EnvironmentError("La variable de entorno GCP_PROJECT_ID no está definida.")


def publicar_evento(noticia: dict) -> None:
    """Publica una noticia clasificada como mensaje JSON en un topic de Pub/Sub."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT_ID, TOPIC_ID)

    mensaje = json.dumps(noticia, ensure_ascii=False).encode("utf-8")
    future = publisher.publish(topic_path, data=mensaje)
    future.result()  # Espera confirmación de publicación
