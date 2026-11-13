-- ---------------------------------------------------------------------
-- Rol
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Rol(
    IN p_name_rol VARCHAR,
    IN p_description_rol VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO rol(name_rol, description_rol)
    VALUES (p_name_rol, p_description_rol);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Rol(
    IN p_id_rol INT,
    IN p_name_rol VARCHAR,
    IN p_description_rol VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE rol
    SET name_rol = p_name_rol,
        description_rol = p_description_rol
    WHERE id_rol = p_id_rol;
    IF NOT FOUND THEN RAISE EXCEPTION 'Rol % not found', p_id_rol; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Rol(INOUT p_cursor REFCURSOR DEFAULT 'cur_rol')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM rol WHERE state_rol = TRUE ORDER BY id_rol;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Rol(
    IN p_id_rol INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_rol_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM rol WHERE id_rol = p_id_rol;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Rol(IN p_id_rol INT, IN p_state_rol BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE rol SET state_rol = p_state_rol WHERE id_rol = p_id_rol;
    IF NOT FOUND THEN RAISE EXCEPTION 'Rol % not found', p_id_rol; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Permission
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Permission(
    IN p_name_permission VARCHAR,
    IN p_description_permission VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO permission(name_permission, description_permission)
    VALUES (p_name_permission, p_description_permission);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Permission(
    IN p_id_permission INT,
    IN p_name_permission VARCHAR,
    IN p_description_permission VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE permission
    SET name_permission = p_name_permission,
        description_permission = p_description_permission
    WHERE id_permission = p_id_permission;
    IF NOT FOUND THEN RAISE EXCEPTION 'Permission % not found', p_id_permission; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Permission(INOUT p_cursor REFCURSOR DEFAULT 'cur_permission')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM permission WHERE state_permission = TRUE ORDER BY id_permission;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Permission(
    IN p_id_permission INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_permission_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM permission WHERE id_permission = p_id_permission;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Permission(IN p_id_permission INT, IN p_state_permission BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE permission SET state_permission = p_state_permission
    WHERE id_permission = p_id_permission;
    IF NOT FOUND THEN RAISE EXCEPTION 'Permission % not found', p_id_permission; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Rol_Permission
-- Tabla débil N:M sin atributos propios ni estado: Insert, Delete,
-- GetAll y GetById (mismo criterio que service_type_route).
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Rol_Permission(
    IN p_id_rol_fk INT,
    IN p_id_permission_fk INT
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO rol_permission(id_rol_fk, id_permission_fk)
    VALUES (p_id_rol_fk, p_id_permission_fk);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Delete_Rol_Permission(
    IN p_id_rol_fk INT,
    IN p_id_permission_fk INT
)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM rol_permission
    WHERE id_rol_fk = p_id_rol_fk
      AND id_permission_fk = p_id_permission_fk;
    IF NOT FOUND THEN RAISE EXCEPTION 'Rol_Permission association not found'; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Rol_Permission(INOUT p_cursor REFCURSOR DEFAULT 'cur_rol_permission')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM rol_permission
        ORDER BY id_rol_fk, id_permission_fk;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Rol_Permission(
    IN p_id_rol_fk INT,
    IN p_id_permission_fk INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_rol_permission_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM rol_permission
        WHERE id_rol_fk = p_id_rol_fk
          AND id_permission_fk = p_id_permission_fk;
END;
$$;

-- ---------------------------------------------------------------------
-- Card_Type
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Card_Type(IN p_name_card_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO card_type(name_card_type) VALUES (p_name_card_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Card_Type(IN p_id_card_type INT, IN p_name_card_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE card_type SET name_card_type = p_name_card_type
    WHERE id_card_type = p_id_card_type;
    IF NOT FOUND THEN RAISE EXCEPTION 'Card_Type % not found', p_id_card_type; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Card_Type(INOUT p_cursor REFCURSOR DEFAULT 'cur_card_type')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM card_type WHERE state_card_type = TRUE ORDER BY id_card_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Card_Type(
    IN p_id_card_type INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_card_type_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM card_type WHERE id_card_type = p_id_card_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Card_Type(IN p_id_card_type INT, IN p_state_card_type BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE card_type SET state_card_type = p_state_card_type
    WHERE id_card_type = p_id_card_type;
    IF NOT FOUND THEN RAISE EXCEPTION 'Card_Type % not found', p_id_card_type; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Card_State
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Card_State(IN p_name_card_state VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO card_state(name_card_state) VALUES (p_name_card_state);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Card_State(IN p_id_card_state INT, IN p_name_card_state VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE card_state SET name_card_state = p_name_card_state
    WHERE id_card_state = p_id_card_state;
    IF NOT FOUND THEN RAISE EXCEPTION 'Card_State % not found', p_id_card_state; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Card_State(INOUT p_cursor REFCURSOR DEFAULT 'cur_card_state')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM card_state WHERE state_card_state = TRUE ORDER BY id_card_state;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Card_State(
    IN p_id_card_state INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_card_state_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM card_state WHERE id_card_state = p_id_card_state;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Card_State(IN p_id_card_state INT, IN p_state_card_state BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE card_state SET state_card_state = p_state_card_state
    WHERE id_card_state = p_id_card_state;
    IF NOT FOUND THEN RAISE EXCEPTION 'Card_State % not found', p_id_card_state; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Card
-- id_passenger_fk es opcional (acepta NULL).
-- La tabla card no tiene columna de estado propia: el estado de la
-- tarjeta se maneja con id_card_state_fk, por eso sp_UpdateState_Card
-- cambia ese FK en lugar de un booleano.
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Card(
    IN p_id_passenger_fk INT,
    IN p_id_card_type_fk INT,
    IN p_id_card_state_fk INT,
    IN p_balance_card NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO card(id_passenger_fk, id_card_type_fk, id_card_state_fk, balance_card)
    VALUES (p_id_passenger_fk, p_id_card_type_fk, p_id_card_state_fk, COALESCE(p_balance_card, 0));
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Card(
    IN p_id_card INT,
    IN p_id_passenger_fk INT,
    IN p_id_card_type_fk INT,
    IN p_id_card_state_fk INT,
    IN p_balance_card NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE card
    SET id_passenger_fk = p_id_passenger_fk,
        id_card_type_fk = p_id_card_type_fk,
        id_card_state_fk = p_id_card_state_fk,
        balance_card = p_balance_card
    WHERE id_card = p_id_card;
    IF NOT FOUND THEN RAISE EXCEPTION 'Card % not found', p_id_card; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Card(INOUT p_cursor REFCURSOR DEFAULT 'cur_card')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM card ORDER BY id_card;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Card(
    IN p_id_card INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_card_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM card WHERE id_card = p_id_card;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Card(
    IN p_id_card INT,
    IN p_id_card_state_fk INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE card SET id_card_state_fk = p_id_card_state_fk WHERE id_card = p_id_card;
    IF NOT FOUND THEN RAISE EXCEPTION 'Card % not found', p_id_card; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Bus_Type
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Bus_Type(
    IN p_name_bus_type VARCHAR,
    IN p_capacity_bus_type INT
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO bus_type(name_bus_type, capacity_bus_type)
    VALUES (p_name_bus_type, p_capacity_bus_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Bus_Type(
    IN p_id_bus_type INT,
    IN p_name_bus_type VARCHAR,
    IN p_capacity_bus_type INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE bus_type
    SET name_bus_type = p_name_bus_type,
        capacity_bus_type = p_capacity_bus_type
    WHERE id_bus_type = p_id_bus_type;
    IF NOT FOUND THEN RAISE EXCEPTION 'Bus_Type % not found', p_id_bus_type; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Bus_Type(INOUT p_cursor REFCURSOR DEFAULT 'cur_bus_type')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM bus_type WHERE state_bus_type = TRUE ORDER BY id_bus_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Bus_Type(
    IN p_id_bus_type INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_bus_type_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM bus_type WHERE id_bus_type = p_id_bus_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Bus_Type(IN p_id_bus_type INT, IN p_state_bus_type BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE bus_type SET state_bus_type = p_state_bus_type
    WHERE id_bus_type = p_id_bus_type;
    IF NOT FOUND THEN RAISE EXCEPTION 'Bus_Type % not found', p_id_bus_type; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Bus
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Bus(
    IN p_id_bus_type_fk INT,
    IN p_code_bus VARCHAR,
    IN p_plate_bus VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO bus(id_bus_type_fk, code_bus, plate_bus)
    VALUES (p_id_bus_type_fk, p_code_bus, p_plate_bus);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Bus(
    IN p_id_bus INT,
    IN p_id_bus_type_fk INT,
    IN p_code_bus VARCHAR,
    IN p_plate_bus VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE bus
    SET id_bus_type_fk = p_id_bus_type_fk,
        code_bus = p_code_bus,
        plate_bus = p_plate_bus
    WHERE id_bus = p_id_bus;
    IF NOT FOUND THEN RAISE EXCEPTION 'Bus % not found', p_id_bus; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Bus(INOUT p_cursor REFCURSOR DEFAULT 'cur_bus')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM bus WHERE state_bus = TRUE ORDER BY id_bus;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Bus(
    IN p_id_bus INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_bus_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM bus WHERE id_bus = p_id_bus;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Bus(IN p_id_bus INT, IN p_state_bus BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE bus SET state_bus = p_state_bus WHERE id_bus = p_id_bus;
    IF NOT FOUND THEN RAISE EXCEPTION 'Bus % not found', p_id_bus; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Route_Schedule
-- Tabla débil N:M sin atributos propios ni estado: Insert, Delete,
-- GetAll y GetById.
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Route_Schedule(
    IN p_id_route_fk INT,
    IN p_id_schedule_fk INT
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO route_schedule(id_route_fk, id_schedule_fk)
    VALUES (p_id_route_fk, p_id_schedule_fk);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Delete_Route_Schedule(
    IN p_id_route_fk INT,
    IN p_id_schedule_fk INT
)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM route_schedule
    WHERE id_route_fk = p_id_route_fk
      AND id_schedule_fk = p_id_schedule_fk;
    IF NOT FOUND THEN RAISE EXCEPTION 'Route_Schedule association not found'; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Route_Schedule(INOUT p_cursor REFCURSOR DEFAULT 'cur_route_schedule')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route_schedule
        ORDER BY id_route_fk, id_schedule_fk;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Route_Schedule(
    IN p_id_route_fk INT,
    IN p_id_schedule_fk INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_route_schedule_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route_schedule
        WHERE id_route_fk = p_id_route_fk
          AND id_schedule_fk = p_id_schedule_fk;
END;
$$;

-- ---------------------------------------------------------------------
-- Route_Bus
-- PK compuesta (id_route_fk, id_bus_fk, service_date). Sin columna de
-- estado: mismo patrón que bus_employee, más Delete.
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Route_Bus(
    IN p_id_route_fk INT,
    IN p_id_bus_fk INT,
    IN p_service_date DATE,
    IN p_start_time TIME,
    IN p_end_time TIME
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO route_bus(id_route_fk, id_bus_fk, service_date, start_time, end_time)
    VALUES (p_id_route_fk, p_id_bus_fk, COALESCE(p_service_date, CURRENT_DATE),
            p_start_time, p_end_time);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Route_Bus(
    IN p_id_route_fk INT,
    IN p_id_bus_fk INT,
    IN p_service_date DATE,
    IN p_start_time TIME,
    IN p_end_time TIME
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE route_bus
    SET start_time = p_start_time,
        end_time = p_end_time
    WHERE id_route_fk = p_id_route_fk
      AND id_bus_fk = p_id_bus_fk
      AND service_date = p_service_date;
    IF NOT FOUND THEN RAISE EXCEPTION 'Route_Bus assignment not found'; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Delete_Route_Bus(
    IN p_id_route_fk INT,
    IN p_id_bus_fk INT,
    IN p_service_date DATE
)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM route_bus
    WHERE id_route_fk = p_id_route_fk
      AND id_bus_fk = p_id_bus_fk
      AND service_date = p_service_date;
    IF NOT FOUND THEN RAISE EXCEPTION 'Route_Bus assignment not found'; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Route_Bus(INOUT p_cursor REFCURSOR DEFAULT 'cur_route_bus')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route_bus
        ORDER BY service_date DESC, start_time;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Route_Bus(
    IN p_id_route_fk INT,
    IN p_id_bus_fk INT,
    IN p_service_date DATE,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_route_bus_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM route_bus
        WHERE id_route_fk = p_id_route_fk
          AND id_bus_fk = p_id_bus_fk
          AND service_date = p_service_date;
END;
$$;

-- ---------------------------------------------------------------------
-- Card_Transaction
-- Registro histórico: el Insert calcula balance_before / balance_after,
-- valida el saldo y actualiza card.balance_card en la misma operación.
-- Convención: el monto se suma al saldo (recarga: positivo,
-- pago de pasaje: negativo). No hay Update de montos; solo se anula
-- lógicamente con UpdateState.
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Card_Transaction(
    IN p_id_card_fk INT,
    IN p_id_transaction_type_fk INT,
    IN p_id_station_fk INT,
    IN p_amount_transaction NUMERIC
)
LANGUAGE plpgsql AS $$
DECLARE
    v_balance_before NUMERIC(10,2);
    v_balance_after  NUMERIC(10,2);
BEGIN
    SELECT balance_card INTO v_balance_before
    FROM card
    WHERE id_card = p_id_card_fk
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Card % not found', p_id_card_fk;
    END IF;

    v_balance_after := v_balance_before + p_amount_transaction;

    IF v_balance_after < 0 THEN
        RAISE EXCEPTION 'Insufficient balance on card %', p_id_card_fk;
    END IF;

    INSERT INTO card_transaction(
        id_card_fk, id_transaction_type_fk, id_station_fk,
        amount_transaction, balance_before, balance_after
    )
    VALUES (
        p_id_card_fk, p_id_transaction_type_fk, p_id_station_fk,
        p_amount_transaction, v_balance_before, v_balance_after
    );

    UPDATE card SET balance_card = v_balance_after WHERE id_card = p_id_card_fk;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Card_Transaction(INOUT p_cursor REFCURSOR DEFAULT 'cur_card_transaction')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM card_transaction
        WHERE state_transaction = TRUE
        ORDER BY transaction_date_hour DESC;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Card_Transaction(
    IN p_id_card_transaction INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_card_transaction_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM card_transaction
        WHERE id_card_transaction = p_id_card_transaction;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Card_Transaction(
    IN p_id_card_transaction INT,
    IN p_state_transaction BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE card_transaction SET state_transaction = p_state_transaction
    WHERE id_card_transaction = p_id_card_transaction;
    IF NOT FOUND THEN RAISE EXCEPTION 'Card_Transaction % not found', p_id_card_transaction; END IF;
END;
$$;