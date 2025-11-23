FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código y el modelo
COPY . .

# EXPOSE es solo documentación, pero ayuda a Railway a veces a adivinar
EXPOSE 8000

# EL COMANDO MÁGICO:
# Usamos "sh -c" para que Linux pueda leer la variable ${PORT}
# Si Railway nos da un puerto, usa ese. Si no (local), usa el 8000.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
