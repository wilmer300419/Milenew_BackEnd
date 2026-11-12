-- Se ejecuta UNA sola vez (primer arranque, cuando el volumen esta vacio).
-- Corre dentro de psql conectado a la base por defecto ("postgres"),
-- por eso el script de esquema puede hacer DROP/CREATE DATABASE milenew_db.
-- El \c cambia la conexion a milenew_db para el resto de la sesion.
\i /sql/01_schema.sql
\c milenew_db
\i /sql/02_procedures.sql
