FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# No hardcodeamos el puerto en el CMD, usamos la variable $PORT
# Si $PORT no existe (en local), usa 8050 por defecto.
# Forzamos puerto 8080 explícitamente
CMD gunicorn -b 0.0.0.0:8080 app:server
