#!/usr/bin/env sh
set -e

# Esperar a que la DB responda en el puerto 5432
if [ "$DATABASE_HOST" != "" ]; then
  echo "Esperando a la base de datos en $DATABASE_HOST:$DATABASE_PORT..."
  until nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
    sleep 0.5
  done
fi

exec "$@"
