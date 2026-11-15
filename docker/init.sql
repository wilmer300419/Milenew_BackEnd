-- Se ejecuta UNA sola vez (primer arranque, cuando el volumen esta vacio).
-- Corre dentro de psql conectado a la base por defecto ("postgres"),
-- por eso el script de esquema puede hacer DROP/CREATE DATABASE milenew_db.
-- El \c cambia la conexion a milenew_db para el resto de la sesion.
\i /sql/01_schema.sql
\c milenew_db
\i /sql/02_procedures.sql
-- SPs agregados por HectorDev (rol/permission, buses, tarjetas, route_bus;
-- estaciones, rutas, route_station, horarios, tipos de servicio y transaccion).
\i /sql/03_procedures_final.sql
\i /sql/04_procedures_hectordev.sql
