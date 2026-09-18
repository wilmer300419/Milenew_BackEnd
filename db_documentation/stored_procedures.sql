-- =====================================================================
-- 3. STANDARD STORED PROCEDURES
--    PostgreSQL uses PROCEDURE + CALL. GET procedures use OUT refcursor
--    because PostgreSQL procedures do not directly return result sets.
-- =====================================================================

-- Helper procedure for state validation is intentionally not added;
-- each requested SP validates its own inputs.

-- ---------------------------------------------------------------------
-- Document_Type
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Document_Type(
    IN p_name_doc_type VARCHAR,
    IN p_acronym_doc_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO document_type(name_doc_type, acronym_doc_type)
    VALUES (p_name_doc_type, p_acronym_doc_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Document_Type(
    IN p_id_doc_type INT,
    IN p_name_doc_type VARCHAR,
    IN p_acronym_doc_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE document_type
    SET name_doc_type = p_name_doc_type,
        acronym_doc_type = p_acronym_doc_type
    WHERE id_doc_type = p_id_doc_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Document_Type % not found', p_id_doc_type;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Document_Type(INOUT p_cursor REFCURSOR DEFAULT 'cur_document_type')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM document_type
        WHERE state_doc_type = TRUE
        ORDER BY id_doc_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Document_Type(
    IN p_id_doc_type INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_document_type_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM document_type
        WHERE id_doc_type = p_id_doc_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Document_Type(
    IN p_id_doc_type INT,
    IN p_state_doc_type BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE document_type
    SET state_doc_type = p_state_doc_type
    WHERE id_doc_type = p_id_doc_type;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Document_Type % not found', p_id_doc_type;
    END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Person
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Person(
    IN p_id_doc_type_fk INT,
    IN p_num_doc_person VARCHAR,
    IN p_first_name_person VARCHAR,
    IN p_second_name_person VARCHAR,
    IN p_first_last_name_person VARCHAR,
    IN p_second_last_name_person VARCHAR,
    IN p_phone_number_person VARCHAR,
    IN p_birthdate_person DATE,
    IN p_email_person VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO person(
        id_doc_type_fk, num_doc_person, first_name_person, second_name_person,
        first_last_name_person, second_last_name_person, phone_number_person,
        birthdate_person, email_person
    )
    VALUES (
        p_id_doc_type_fk, p_num_doc_person, p_first_name_person, p_second_name_person,
        p_first_last_name_person, p_second_last_name_person, p_phone_number_person,
        p_birthdate_person, p_email_person
    );
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Person(
    IN p_id_person INT,
    IN p_id_doc_type_fk INT,
    IN p_num_doc_person VARCHAR,
    IN p_first_name_person VARCHAR,
    IN p_second_name_person VARCHAR,
    IN p_first_last_name_person VARCHAR,
    IN p_second_last_name_person VARCHAR,
    IN p_phone_number_person VARCHAR,
    IN p_birthdate_person DATE,
    IN p_email_person VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE person
    SET id_doc_type_fk = p_id_doc_type_fk,
        num_doc_person = p_num_doc_person,
        first_name_person = p_first_name_person,
        second_name_person = p_second_name_person,
        first_last_name_person = p_first_last_name_person,
        second_last_name_person = p_second_last_name_person,
        phone_number_person = p_phone_number_person,
        birthdate_person = p_birthdate_person,
        email_person = p_email_person
    WHERE id_person = p_id_person;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Person % not found', p_id_person;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Person(INOUT p_cursor REFCURSOR DEFAULT 'cur_person')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM person WHERE state_person = TRUE ORDER BY id_person;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Person(
    IN p_id_person INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_person_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM person WHERE id_person = p_id_person;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Person(IN p_id_person INT, IN p_state_person BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE person SET state_person = p_state_person WHERE id_person = p_id_person;
    IF NOT FOUND THEN RAISE EXCEPTION 'Person % not found', p_id_person; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- User (app_user)
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_User(
    IN p_id_person_fk INT,
    IN p_id_rol_fk INT,
    IN p_username VARCHAR,
    IN p_password VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO app_user(id_person_fk, id_rol_fk, username, password)
    VALUES (p_id_person_fk, p_id_rol_fk, p_username, p_password);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_User(
    IN p_id_user INT,
    IN p_id_person_fk INT,
    IN p_id_rol_fk INT,
    IN p_username VARCHAR,
    IN p_password VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE app_user
    SET id_person_fk = p_id_person_fk,
        id_rol_fk = p_id_rol_fk,
        username = p_username,
        password = p_password
    WHERE id_user = p_id_user;
    IF NOT FOUND THEN RAISE EXCEPTION 'User % not found', p_id_user; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_User(INOUT p_cursor REFCURSOR DEFAULT 'cur_user')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM app_user WHERE state_user = TRUE ORDER BY id_user;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_User(
    IN p_id_user INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_user_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM app_user WHERE id_user = p_id_user;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_User(IN p_id_user INT, IN p_state_user BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE app_user SET state_user = p_state_user WHERE id_user = p_id_user;
    IF NOT FOUND THEN RAISE EXCEPTION 'User % not found', p_id_user; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Token_Type
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Token_Type(IN p_name_token_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO token_type(name_token_type) VALUES (p_name_token_type);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Token_Type(IN p_id_token_type INT, IN p_name_token_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE token_type SET name_token_type = p_name_token_type
    WHERE id_token_type = p_id_token_type;
    IF NOT FOUND THEN RAISE EXCEPTION 'Token_Type % not found', p_id_token_type; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Token_Type(INOUT p_cursor REFCURSOR DEFAULT 'cur_token_type')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM token_type WHERE state_token_type = TRUE ORDER BY id_token_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Token_Type(
    IN p_id_token_type INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_token_type_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM token_type WHERE id_token_type = p_id_token_type;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Token_Type(IN p_id_token_type INT, IN p_state_token_type BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE token_type SET state_token_type = p_state_token_type
    WHERE id_token_type = p_id_token_type;
    IF NOT FOUND THEN RAISE EXCEPTION 'Token_Type % not found', p_id_token_type; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- User_Token
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_User_Token(
    IN p_id_token_type_fk INT,
    IN p_id_user_fk INT,
    IN p_start_time TIMESTAMP,
    IN p_end_time TIMESTAMP
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO user_token(id_token_type_fk, id_user_fk, start_time, end_time)
    VALUES (p_id_token_type_fk, p_id_user_fk, COALESCE(p_start_time, now()), p_end_time);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_User_Token(
    IN p_id_user_token INT,
    IN p_id_token_type_fk INT,
    IN p_id_user_fk INT,
    IN p_start_time TIMESTAMP,
    IN p_end_time TIMESTAMP
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE user_token
    SET id_token_type_fk = p_id_token_type_fk,
        id_user_fk = p_id_user_fk,
        start_time = p_start_time,
        end_time = p_end_time
    WHERE id_user_token = p_id_user_token;
    IF NOT FOUND THEN RAISE EXCEPTION 'User_Token % not found', p_id_user_token; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_User_Token(INOUT p_cursor REFCURSOR DEFAULT 'cur_user_token')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM user_token WHERE state_user_token = TRUE ORDER BY id_user_token;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_User_Token(
    IN p_id_user_token INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_user_token_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM user_token WHERE id_user_token = p_id_user_token;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_User_Token(IN p_id_user_token INT, IN p_state_user_token BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE user_token SET state_user_token = p_state_user_token
    WHERE id_user_token = p_id_user_token;
    IF NOT FOUND THEN RAISE EXCEPTION 'User_Token % not found', p_id_user_token; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Employee_Position
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Employee_Position(IN p_name_employee_position VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO employee_position(name_employee_position) VALUES (p_name_employee_position);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Employee_Position(
    IN p_id_employee_position INT,
    IN p_name_employee_position VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee_position SET name_employee_position = p_name_employee_position
    WHERE id_employee_position = p_id_employee_position;
    IF NOT FOUND THEN RAISE EXCEPTION 'Employee_Position % not found', p_id_employee_position; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Employee_Position(INOUT p_cursor REFCURSOR DEFAULT 'cur_employee_position')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM employee_position
    WHERE state_employee_position = TRUE ORDER BY id_employee_position;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Employee_Position(
    IN p_id_employee_position INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_employee_position_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM employee_position
    WHERE id_employee_position = p_id_employee_position;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Employee_Position(
    IN p_id_employee_position INT,
    IN p_state_employee_position BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee_position SET state_employee_position = p_state_employee_position
    WHERE id_employee_position = p_id_employee_position;
    IF NOT FOUND THEN RAISE EXCEPTION 'Employee_Position % not found', p_id_employee_position; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Employee_Area
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Employee_Area(
    IN p_name_employee_area VARCHAR,
    IN p_place_employee_area VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO employee_area(name_employee_area, place_employee_area)
    VALUES (p_name_employee_area, p_place_employee_area);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Employee_Area(
    IN p_id_employee_area INT,
    IN p_name_employee_area VARCHAR,
    IN p_place_employee_area VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee_area
    SET name_employee_area = p_name_employee_area,
        place_employee_area = p_place_employee_area
    WHERE id_employee_area = p_id_employee_area;
    IF NOT FOUND THEN RAISE EXCEPTION 'Employee_Area % not found', p_id_employee_area; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Employee_Area(INOUT p_cursor REFCURSOR DEFAULT 'cur_employee_area')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM employee_area
    WHERE state_employee_area = TRUE ORDER BY id_employee_area;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Employee_Area(
    IN p_id_employee_area INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_employee_area_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM employee_area
    WHERE id_employee_area = p_id_employee_area;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Employee_Area(
    IN p_id_employee_area INT,
    IN p_state_employee_area BOOLEAN
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee_area SET state_employee_area = p_state_employee_area
    WHERE id_employee_area = p_id_employee_area;
    IF NOT FOUND THEN RAISE EXCEPTION 'Employee_Area % not found', p_id_employee_area; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Employee
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Employee(
    IN p_id_employee_position_fk INT,
    IN p_id_employee_area_fk INT,
    IN p_id_user_fk INT,
    IN p_working_hours VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO employee(
        id_employee_position_fk, id_employee_area_fk, id_user_fk, working_hours
    )
    VALUES (
        p_id_employee_position_fk, p_id_employee_area_fk, p_id_user_fk, p_working_hours
    );
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Employee(
    IN p_id_employee INT,
    IN p_id_employee_position_fk INT,
    IN p_id_employee_area_fk INT,
    IN p_id_user_fk INT,
    IN p_working_hours VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee
    SET id_employee_position_fk = p_id_employee_position_fk,
        id_employee_area_fk = p_id_employee_area_fk,
        id_user_fk = p_id_user_fk,
        working_hours = p_working_hours
    WHERE id_employee = p_id_employee;
    IF NOT FOUND THEN RAISE EXCEPTION 'Employee % not found', p_id_employee; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Employee(INOUT p_cursor REFCURSOR DEFAULT 'cur_employee')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM employee WHERE state_employee = TRUE ORDER BY id_employee;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Employee(
    IN p_id_employee INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_employee_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM employee WHERE id_employee = p_id_employee;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Employee(IN p_id_employee INT, IN p_state_employee BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee SET state_employee = p_state_employee WHERE id_employee = p_id_employee;
    IF NOT FOUND THEN RAISE EXCEPTION 'Employee % not found', p_id_employee; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Passenger
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Passenger(IN p_id_user_fk INT)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO passenger(id_user_fk) VALUES (p_id_user_fk);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Passenger(IN p_id_passenger INT, IN p_id_user_fk INT)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE passenger SET id_user_fk = p_id_user_fk WHERE id_passenger = p_id_passenger;
    IF NOT FOUND THEN RAISE EXCEPTION 'Passenger % not found', p_id_passenger; END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Passenger(INOUT p_cursor REFCURSOR DEFAULT 'cur_passenger')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM passenger WHERE state_passenger = TRUE ORDER BY id_passenger;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Passenger(
    IN p_id_passenger INT,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_passenger_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR SELECT * FROM passenger WHERE id_passenger = p_id_passenger;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_UpdateState_Passenger(IN p_id_passenger INT, IN p_state_passenger BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE passenger SET state_passenger = p_state_passenger WHERE id_passenger = p_id_passenger;
    IF NOT FOUND THEN RAISE EXCEPTION 'Passenger % not found', p_id_passenger; END IF;
END;
$$;

-- ---------------------------------------------------------------------
-- Bus_Employee
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE sp_Insert_Bus_Employee(
    IN p_id_bus_fk INT,
    IN p_id_employee_fk INT,
    IN p_service_date DATE,
    IN p_start_time TIME,
    IN p_end_time TIME
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO bus_employee(
        id_bus_fk, id_employee_fk, service_date, start_time, end_time
    )
    VALUES (
        p_id_bus_fk, p_id_employee_fk, COALESCE(p_service_date, CURRENT_DATE),
        p_start_time, p_end_time
    );
END;
$$;

CREATE OR REPLACE PROCEDURE sp_Update_Bus_Employee(
    IN p_id_bus_fk INT,
    IN p_id_employee_fk INT,
    IN p_service_date DATE,
    IN p_start_time TIME,
    IN p_end_time TIME
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE bus_employee
    SET start_time = p_start_time,
        end_time = p_end_time
    WHERE id_bus_fk = p_id_bus_fk
      AND id_employee_fk = p_id_employee_fk
      AND service_date = p_service_date;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Bus_Employee assignment not found';
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetAll_Bus_Employee(INOUT p_cursor REFCURSOR DEFAULT 'cur_bus_employee')
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM bus_employee
        ORDER BY service_date DESC, start_time;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_GetById_Bus_Employee(
    IN p_id_bus_fk INT,
    IN p_id_employee_fk INT,
    IN p_service_date DATE,
    INOUT p_cursor REFCURSOR DEFAULT 'cur_bus_employee_by_id'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT * FROM bus_employee
        WHERE id_bus_fk = p_id_bus_fk
          AND id_employee_fk = p_id_employee_fk
          AND service_date = p_service_date;
END;
$$;

-- Bus_Employee has no state column in the supplied model.
-- Therefore the standard UpdateState SP is implemented as logical
-- activation through deletion/reinsertion only if a state column exists.
-- To keep the schema consistent, no state procedure is generated here.
-- If your teacher requires exactly five procedures for this table,
-- add state_bus_employee BOOLEAN and use the same pattern as the others.

-- =====================================================================
-- 4. DOCUMENTATION
-- =====================================================================

COMMENT ON TABLE route_schedule IS 'N:M relationship between routes and schedules.';
COMMENT ON TABLE route_station IS 'N:M relationship between routes and stations, including station order.';
COMMENT ON TABLE route_bus IS 'N:M relationship between routes and buses, including service date and time.';
COMMENT ON TABLE bus_employee IS 'N:M relationship between buses and employees, including service date and time.';
COMMENT ON COLUMN route_station.order_route_station IS 'Sequential order of the station within a route.';
COMMENT ON COLUMN card.id_passenger_fk IS 'Optional passenger association; NULL is allowed.';
COMMENT ON COLUMN route_bus.service_date IS 'Date on which the bus operates the route.';
COMMENT ON COLUMN route_bus.start_time IS 'Start time of the route-bus assignment.';
COMMENT ON COLUMN route_bus.end_time IS 'End time of the route-bus assignment.';
COMMENT ON COLUMN bus_employee.service_date IS 'Date on which the employee operates the bus.';
COMMENT ON COLUMN bus_employee.start_time IS 'Start time of the employee-bus assignment.';
COMMENT ON COLUMN bus_employee.end_time IS 'End time of the employee-bus assignment.';

-- =====================================================================
-- END
-- =====================================================================
