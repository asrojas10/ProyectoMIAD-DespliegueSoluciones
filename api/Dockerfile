FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# USAMOS ESTA SINTAXIS ROBUSTA
# IMPORTANTE: Si tu archivo se llama 'api.py', cambia 'main:app' por 'api:app' abajo 👇
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
