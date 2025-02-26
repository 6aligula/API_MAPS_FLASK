FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Actualiza el sistema e instala netcat y bash
RUN apt-get update && apt-get install -y netcat-openbsd bash

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

# Comando que lista el contenido de /usr/local/bin, espera a que MariaDB esté disponible
# y lanza la aplicación. Si falla, se mantiene el contenedor en ejecución.
CMD ["/bin/bash", "-c", "echo 'Contenido de /usr/local/bin:' && ls -l /usr/local/bin && /usr/local/bin/wait-for.sh mariadb:3306 && python app.py || tail -f /dev/null"]
