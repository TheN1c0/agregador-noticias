FROM python:3.11-slim

WORKDIR /app

# Instala dependencias primero para aprovechar caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Puerto del servicio de notificación
EXPOSE 8002

# Arranca el servidor con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
