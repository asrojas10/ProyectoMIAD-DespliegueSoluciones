FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# No hardcodeamos el puerto en el CMD, usamos la variable $PORT
# Si $PORT no existe (en local), usa 8050 por defecto.
CMD gunicorn -b 0.0.0.0:${PORT:-8050} app:server
