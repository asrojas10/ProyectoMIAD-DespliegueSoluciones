FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código y el modelo
COPY . .

# EL COMANDO MÁGICO:
# Usamos "sh -c" para que Linux pueda leer la variable ${PORT}
# Si Railway nos da un puerto, usa ese. Si no (local), usa el 8000.
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
