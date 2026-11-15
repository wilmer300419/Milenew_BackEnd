#!/bin/bash
# Se ejecuta UNA sola vez (primer arranque, cuando el volumen esta vacio).
#
# El script de esquema del equipo de DB trae "DROP/CREATE DATABASE milenew_db"
# y el cambio de base solo como comentario ("-- psql: \c milenew_db"), asi que
# no se puede cargar tal cual: las tablas terminarian en la base "postgres".
# Por eso aqui: 1) se crea milenew_db, 2) se carga el esquema DENTRO de ella
# omitiendo las lineas DROP/CREATE DATABASE, 3) se cargan los stored procedures.
# Los archivos .sql originales no se modifican.
set -e

PSQL="psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER"

echo ">> Creando la base milenew_db"
$PSQL --dbname postgres -c "CREATE DATABASE milenew_db WITH ENCODING 'UTF8'"

echo ">> Cargando el esquema"
grep -viE '^[[:space:]]*(DROP|CREATE)[[:space:]]+DATABASE' /sql/01_schema.sql | $PSQL --dbname milenew_db

for f in /sql/02_procedures.sql /sql/03_procedures_final.sql /sql/04_procedures_hectordev.sql; do
  echo ">> Cargando $f"
  $PSQL --dbname milenew_db -f "$f"
done

echo ">> milenew_db lista"
