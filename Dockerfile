FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Actualiza el sistema e instala netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Copia requirements.txt e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Copia el script wait-for.sh y lo hace ejecutable
COPY wait-for.sh /usr/local/bin/wait-for.sh
RUN chmod +x /usr/local/bin/wait-for.sh

# Expone el puerto en el que se ejecuta Flask
EXPOSE 5000

# Comando para esperar a que MariaDB esté disponible y luego iniciar la aplicación
CMD ["/bin/sh", "-c", "/usr/local/bin/wait-for.sh mariadb:3306 && python app.py"]
