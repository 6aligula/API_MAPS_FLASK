#!/bin/bash
# wait-for.sh: espera a que un host:puerto esté disponible.
# Uso: ./wait-for.sh host:puerto [comando a ejecutar]

if [ "$#" -lt 1 ]; then
    echo "Uso: $0 host:puerto [comando a ejecutar]"
    exit 1
fi

hostport="$1"
host=$(echo "$hostport" | cut -d: -f1)
port=$(echo "$hostport" | cut -d: -f2)
shift

echo "Esperando a que $host en el puerto $port esté disponible..."

# Asegurarse de tener instalado netcat (nc)
while ! nc -z "$host" "$port"; do
    sleep 1
done

echo "$host:$port está disponible."

# Ejecutar el comando pasado como parámetro
exec "$@"