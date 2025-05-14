# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los requisitos primero (mejor para cache)
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de tu proyecto
COPY . .

# Expone el puerto que Cloud Run usará
EXPOSE 8080

# Comando de arranque
CMD ["uvicorn", "main:fastapi_app", "--host", "0.0.0.0", "--port", "8080"]
