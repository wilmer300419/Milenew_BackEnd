-- =====================================================================
-- MILENEW - Procedimientos almacenados faltantes
-- Tablas: Schedule, Route, Service_Type, Service_Type_Route,
--         Route_Station, Station, Station_Type, Transaction_Type
-- =====================================================================

-- ---------------------------------------------------------------------
-- Schedule
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Schedule(
    IN p_start_time TIME,
    IN p_end_time TIME,
    IN p_day_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO schedule(start_time, end_time, day_type)
    VALUES (p_start_time, p_end_time, p_day_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Schedule(
    IN p_id_schedule INT,
    IN p_start_time TIME,
    IN p_end_time TIME,
    IN p_day_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE schedule
    SET start_time = p_start_time,
        end_time = p_end_time,
        day_type = p_day_type
    WHERE id_schedule = p_id_schedule;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Schedule % not found', p_id_schedule;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Schedule(INOUT p_cursor REFCURSOR DEFAULT 'cur_schedule')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM schedule
        WHERE state_schedule = TRUE
        ORDER BY id_schedule;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Schedule(
    IN p_id_schedule INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_schedule_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM schedule
        WHERE id_schedule = p_id_schedule;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Schedule(
    IN p_id_schedule INT,
    IN p_state_schedule BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE schedule
    SET state_schedule = p_state_schedule
    WHERE id_schedule = p_id_schedule;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Schedule % not found', p_id_schedule;
    END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Route
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Route(
    IN p_code_route VARCHAR,
    IN p_description_route VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO route(code_route, description_route)
    VALUES (p_code_route, p_description_route);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Route(
    IN p_id_route INT,
    IN p_code_route VARCHAR,
    IN p_description_route VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE route
    SET code_route = p_code_route,
        description_route = p_description_route
    WHERE id_route = p_id_route;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Route % not found', p_id_route;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Route(INOUT p_cursor REFCURSOR DEFAULT 'cur_route')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route
        WHERE state_route = TRUE
        ORDER BY id_route;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Route(
    IN p_id_route INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_route_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route
        WHERE id_route = p_id_route;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Route(
    IN p_id_route INT,
    IN p_state_route BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE route
    SET state_route = p_state_route
    WHERE id_route = p_id_route;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Route % not found', p_id_route;
    END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Service_Type
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Service_Type(IN p_name_service_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO service_type(name_service_type) VALUES (p_name_service_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Service_Type(
    IN p_id_service_type INT,
    IN p_name_service_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE service_type
    SET name_service_type = p_name_service_type
    WHERE id_service_type = p_id_service_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Service_Type % not found', p_id_service_type;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Service_Type(INOUT p_cursor REFCURSOR DEFAULT 'cur_service_type')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM service_type
        WHERE state_service_type = TRUE
        ORDER BY id_service_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Service_Type(
    IN p_id_service_type INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_service_type_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM service_type
        WHERE id_service_type = p_id_service_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Service_Type(
    IN p_id_service_type INT,
    IN p_state_service_type BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE service_type
    SET state_service_type = p_state_service_type
    WHERE id_service_type = p_id_service_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Service_Type % not found', p_id_service_type;
    END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Service_Type_Route
-- Tabla débil N:M (PK compuesta id_route_fk + id_service_type_fk).
-- No tiene columna de estado ni atributos propios, por lo que no aplica
-- Update ni UpdateState (mismo criterio usado en bus_employee): en su
-- lugar se agrega un Delete para romper la asociación.
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Service_Type_Route(
    IN p_id_route_fk INT,
    IN p_id_service_type_fk INT
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO service_type_route(id_route_fk, id_service_type_fk)
    VALUES (p_id_route_fk, p_id_service_type_fk);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Delete_Service_Type_Route(
    IN p_id_route_fk INT,
    IN p_id_service_type_fk INT
)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM service_type_route
    WHERE id_route_fk = p_id_route_fk
      AND id_service_type_fk = p_id_service_type_fk;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Service_Type_Route association not found';
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Service_Type_Route(INOUT p_cursor REFCURSOR DEFAULT 'cur_service_type_route')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM service_type_route
        ORDER BY id_route_fk, id_service_type_fk;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Service_Type_Route(
    IN p_id_route_fk INT,
    IN p_id_service_type_fk INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_service_type_route_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM service_type_route
        WHERE id_route_fk = p_id_route_fk
          AND id_service_type_fk = p_id_service_type_fk;
END;
$$;

-- ---------------------------------------------------------------------
-- Route_Station
-- Tabla débil N:M (PK compuesta id_route_fk + id_station_fk), pero SÍ
-- tiene atributo propio (order_route_station) y columna de estado,
-- por lo que sigue el patrón estándar completo de 5 procedimientos.
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Route_Station(
    IN p_id_route_fk INT,
    IN p_id_station_fk INT,
    IN p_order_route_station INT
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO route_station(id_route_fk, id_station_fk, order_route_station)
    VALUES (p_id_route_fk, p_id_station_fk, p_order_route_station);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Route_Station(
    IN p_id_route_fk INT,
    IN p_id_station_fk INT,
    IN p_order_route_station INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE route_station
    SET order_route_station = p_order_route_station
    WHERE id_route_fk = p_id_route_fk
      AND id_station_fk = p_id_station_fk;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Route_Station association not found';
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Route_Station(INOUT p_cursor REFCURSOR DEFAULT 'cur_route_station')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route_station
        WHERE state_route_station = TRUE
        ORDER BY id_route_fk, order_route_station;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Route_Station(
    IN p_id_route_fk INT,
    IN p_id_station_fk INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_route_station_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route_station
        WHERE id_route_fk = p_id_route_fk
          AND id_station_fk = p_id_station_fk;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Route_Station(
    IN p_id_route_fk INT,
    IN p_id_station_fk INT,
    IN p_state_route_station BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE route_station
    SET state_route_station = p_state_route_station
    WHERE id_route_fk = p_id_route_fk
      AND id_station_fk = p_id_station_fk;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Route_Station association not found';
    END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Station_Type
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Station_Type(IN p_name_station_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO station_type(name_station_type) VALUES (p_name_station_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Station_Type(
    IN p_id_station_type INT,
    IN p_name_station_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE station_type
    SET name_station_type = p_name_station_type
    WHERE id_station_type = p_id_station_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Station_Type % not found', p_id_station_type;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Station_Type(INOUT p_cursor REFCURSOR DEFAULT 'cur_station_type')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM station_type
        WHERE state_station_type = TRUE
        ORDER BY id_station_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Station_Type(
    IN p_id_station_type INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_station_type_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM station_type
        WHERE id_station_type = p_id_station_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Station_Type(
    IN p_id_station_type INT,
    IN p_state_station_type BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE station_type
    SET state_station_type = p_state_station_type
    WHERE id_station_type = p_id_station_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Station_Type % not found', p_id_station_type;
    END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Station
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Station(
    IN p_id_station_type_fk INT,
    IN p_name_station VARCHAR,
    IN p_address_station VARCHAR,
    IN p_latitude_station NUMERIC,
    IN p_longitude_station NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO station(
        id_station_type_fk, name_station, address_station,
        latitude_station, longitude_station
    )
    VALUES (
        p_id_station_type_fk, p_name_station, p_address_station,
        p_latitude_station, p_longitude_station
    );
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Station(
    IN p_id_station INT,
    IN p_id_station_type_fk INT,
    IN p_name_station VARCHAR,
    IN p_address_station VARCHAR,
    IN p_latitude_station NUMERIC,
    IN p_longitude_station NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE station
    SET id_station_type_fk = p_id_station_type_fk,
        name_station = p_name_station,
        address_station = p_address_station,
        latitude_station = p_latitude_station,
        longitude_station = p_longitude_station
    WHERE id_station = p_id_station;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Station % not found', p_id_station;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Station(INOUT p_cursor REFCURSOR DEFAULT 'cur_station')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM station
        WHERE state_station = TRUE
        ORDER BY id_station;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Station(
    IN p_id_station INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_station_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM station
        WHERE id_station = p_id_station;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Station(
    IN p_id_station INT,
    IN p_state_station BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE station
    SET state_station = p_state_station
    WHERE id_station = p_id_station;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Station % not found', p_id_station;
    END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Transaction_Type
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Transaction_Type(IN p_name_transaction_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO transaction_type(name_transaction_type) VALUES (p_name_transaction_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Transaction_Type(
    IN p_id_transaction_type INT,
    IN p_name_transaction_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE transaction_type
    SET name_transaction_type = p_name_transaction_type
    WHERE id_transaction_type = p_id_transaction_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Transaction_Type % not found', p_id_transaction_type;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Transaction_Type(INOUT p_cursor REFCURSOR DEFAULT 'cur_transaction_type')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM transaction_type
        WHERE state_transaction_type = TRUE
        ORDER BY id_transaction_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Transaction_Type(
    IN p_id_transaction_type INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_transaction_type_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM transaction_type
        WHERE id_transaction_type = p_id_transaction_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Transaction_Type(
    IN p_id_transaction_type INT,
    IN p_state_transaction_type BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE transaction_type
    SET state_transaction_type = p_state_transaction_type
    WHERE id_transaction_type = p_id_transaction_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Transaction_Type % not found', p_id_transaction_type;
    END IF;
END;
$$;

-- =====================================================================
-- END
-- =====================================================================
