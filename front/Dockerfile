FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8050
# Usamos Gunicorn para producción, tal como se ve en el PDF del taller
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]