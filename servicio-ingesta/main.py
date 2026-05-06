from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from clasificador import clasificar
from pubsub_publisher import publicar_evento

load_dotenv()

app = FastAPI(
    title="Servicio de Ingesta - Agregador de Noticias Financieras",
    description="Recibe noticias financieras, las clasifica con Gemini y publica eventos en Pub/Sub.",
    version="1.0.0",
)


class NoticiaInput(BaseModel):
    titulo: str
    url: str
    fecha: str
    fuente: str


class NoticiaOutput(BaseModel):
    titulo: str
    url: str
    fecha: str
    fuente: str
    categoria: str


@app.post("/noticias", response_model=NoticiaOutput)
async def recibir_noticia(noticia: NoticiaInput):
    """Recibe una noticia, la clasifica con Gemini y publica el evento en Pub/Sub."""
    try:
        categoria = clasificar(noticia.titulo)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al clasificar con Gemini: {e}")

    noticia_clasificada = {
        "titulo": noticia.titulo,
        "url": noticia.url,
        "fecha": noticia.fecha,
        "fuente": noticia.fuente,
        "categoria": categoria,
    }

    try:
        publicar_evento(noticia_clasificada)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al publicar en Pub/Sub: {e}")

    return noticia_clasificada
