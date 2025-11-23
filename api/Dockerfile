FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código y MODELO
COPY . .

# Comando de arranque (Sin corchetes para que lea $PORT)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
