    -- =====================================================================
    -- PROJECT: Public Transportation System - MILENEW
    -- FILE:    milenew_db_modified.sql
    -- DESCRIPTION:
    --   Modified PostgreSQL schema according to the requested changes:
    --   1. passenger FK may be NULL where it is optional.
    --   2. N:M relationship between route and schedule.
    --   3. route_station_order added to route_station.
    --   4. Weak/N:M tables use composite primary keys made from FKs.
    --   5. route_bus and bus_employee include service date/time.
    --   6. Standard stored procedures for the requested tables.
    --
    -- IMPORTANT:
    --   The original model did not specify an exact table for the phrase
    --   "Null id pasajero fk". In this version, card.id_passenger_fk is
    --   optional (NULL), because a card can be registered before being
    --   associated with a passenger.
    -- =====================================================================

    DROP DATABASE IF EXISTS milenew_db;
    CREATE DATABASE milenew_db WITH ENCODING = 'UTF8';

    -- Connect to milenew_db before executing the rest of this file.
    -- psql: \c milenew_db


    -- =====================================================================
    -- 1. TABLE CREATION
    -- =====================================================================

    CREATE TABLE document_type (
        id_doc_type      SERIAL PRIMARY KEY,
        name_doc_type    VARCHAR(50) NOT NULL,
        acronym_doc_type VARCHAR(10) NOT NULL,
        state_doc_type   BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE person (
        id_person              SERIAL PRIMARY KEY,
        id_doc_type_fk         INT NOT NULL,
        num_doc_person         VARCHAR(20) NOT NULL UNIQUE,
        first_name_person      VARCHAR(50) NOT NULL,
        second_name_person     VARCHAR(50),
        first_last_name_person VARCHAR(50) NOT NULL,
        second_last_name_person VARCHAR(50),
        phone_number_person    VARCHAR(20),
        birthdate_person       DATE,
        email_person           VARCHAR(150) UNIQUE,
        state_person           BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE rol (
        id_rol          SERIAL PRIMARY KEY,
        name_rol        VARCHAR(50) NOT NULL,
        description_rol VARCHAR(200),
        state_rol       BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE permission (
        id_permission          SERIAL PRIMARY KEY,
        name_permission        VARCHAR(50) NOT NULL,
        description_permission VARCHAR(200),
        state_permission       BOOLEAN NOT NULL DEFAULT TRUE
    );

    -- Weak / N:M table: both FKs form the PK.
    CREATE TABLE rol_permission (
        id_rol_fk        INT NOT NULL,
        id_permission_fk INT NOT NULL,
        CONSTRAINT pk_rol_permission PRIMARY KEY (id_rol_fk, id_permission_fk)
    );

    CREATE TABLE app_user (
        id_user       SERIAL PRIMARY KEY,
        id_person_fk  INT NOT NULL,
        id_rol_fk     INT NOT NULL,
        username      VARCHAR(50) NOT NULL UNIQUE,
        password      VARCHAR(255) NOT NULL,
        state_user    BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE token_type (
        id_token_type    SERIAL PRIMARY KEY,
        name_token_type  VARCHAR(50) NOT NULL,
        state_token_type BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE user_token (
        id_user_token    SERIAL PRIMARY KEY,
        id_token_type_fk INT NOT NULL,
        id_user_fk       INT NOT NULL,
        start_time       TIMESTAMP NOT NULL DEFAULT now(),
        state_user_token BOOLEAN NOT NULL DEFAULT TRUE,
        end_time         TIMESTAMP
    );

    CREATE TABLE employee_position (
        id_employee_position    SERIAL PRIMARY KEY,
        name_employee_position  VARCHAR(50) NOT NULL,
        state_employee_position BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE employee_area (
        id_employee_area    SERIAL PRIMARY KEY,
        name_employee_area  VARCHAR(50) NOT NULL,
        place_employee_area VARCHAR(100),
        state_employee_area BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE employee (
        id_employee             SERIAL PRIMARY KEY,
        id_employee_position_fk INT NOT NULL,
        id_employee_area_fk     INT NOT NULL,
        id_user_fk              INT NOT NULL,
        working_hours           VARCHAR(50),
        state_employee          BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE passenger (
        id_passenger    SERIAL PRIMARY KEY,
        id_user_fk      INT NOT NULL,
        state_passenger BOOLEAN NOT NULL DEFAULT TRUE,
        latitude_passenger    NUMERIC(9,6),
        longitude_passenger   NUMERIC(9,6)
    );

    CREATE TABLE card_type (
        id_card_type    SERIAL PRIMARY KEY,
        name_card_type  VARCHAR(50) NOT NULL,
        state_card_type BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE card_state (
        id_card_state    SERIAL PRIMARY KEY,
        name_card_state  VARCHAR(50) NOT NULL,
        state_card_state BOOLEAN NOT NULL DEFAULT TRUE
    );

    -- id_passenger_fk is intentionally nullable as requested.
    CREATE TABLE card (
        id_card          SERIAL PRIMARY KEY,
        id_passenger_fk  INT,
        id_card_type_fk  INT NOT NULL,
        id_card_state_fk INT NOT NULL,
        balance_card     NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (balance_card >= 0)
    );

    CREATE TABLE transaction_type (
        id_transaction_type    SERIAL PRIMARY KEY,
        name_transaction_type  VARCHAR(50) NOT NULL,
        state_transaction_type BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE card_transaction (
        id_card_transaction    SERIAL PRIMARY KEY,
        id_card_fk             INT NOT NULL,
        id_transaction_type_fk INT NOT NULL,
        id_station_fk          INT NOT NULL,
        amount_transaction     NUMERIC(10,2) NOT NULL,
        balance_before         NUMERIC(10,2) NOT NULL,
        balance_after          NUMERIC(10,2) NOT NULL,
        transaction_date_hour  TIMESTAMP NOT NULL DEFAULT now(),
        state_transaction      BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE bus_type (
        id_bus_type       SERIAL PRIMARY KEY,
        name_bus_type     VARCHAR(50) NOT NULL,
        capacity_bus_type INT NOT NULL CHECK (capacity_bus_type > 0),
        state_bus_type    BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE bus (
        id_bus         SERIAL PRIMARY KEY,
        id_bus_type_fk INT NOT NULL,
        latitude_bus    NUMERIC(9,6),
        longitude_bus   NUMERIC(9,6),
        code_bus       VARCHAR(20) NOT NULL UNIQUE,
        plate_bus      VARCHAR(10) NOT NULL UNIQUE,
        state_bus      BOOLEAN NOT NULL DEFAULT TRUE
    );

    -- Weak / N:M table.
    -- Date/time attributes record when the bus-employee assignment/service occurs.
    CREATE TABLE bus_employee (
        id_bus_fk       INT NOT NULL,
        id_employee_fk  INT NOT NULL,
        service_date    DATE NOT NULL DEFAULT CURRENT_DATE,
        start_time      TIME NOT NULL,
        end_time        TIME,
        CONSTRAINT pk_bus_employee PRIMARY KEY (id_bus_fk, id_employee_fk, service_date),
        CONSTRAINT ck_bus_employee_time CHECK (end_time IS NULL OR end_time >= start_time)
    );

    CREATE TABLE schedule (
        id_schedule    SERIAL PRIMARY KEY,
        start_time     TIME NOT NULL,
        end_time       TIME NOT NULL,
        day_type       VARCHAR(20) NOT NULL,
        state_schedule BOOLEAN NOT NULL DEFAULT TRUE,
        CONSTRAINT ck_schedule_time CHECK (end_time >= start_time)
    );

    CREATE TABLE route (
        id_route          SERIAL PRIMARY KEY,
        code_route        VARCHAR(20) NOT NULL UNIQUE,
        description_route VARCHAR(200),
        state_route       BOOLEAN NOT NULL DEFAULT TRUE
    );

    -- New N:M relationship: route <-> schedule.
    CREATE TABLE route_schedule (
        id_route_fk    INT NOT NULL,
        id_schedule_fk INT NOT NULL,
        CONSTRAINT pk_route_schedule PRIMARY KEY (id_route_fk, id_schedule_fk)
    );

    -- Weak / N:M table.
    -- The order belongs to the route-station relationship, not to route itself.
    CREATE TABLE route_station (
        id_route_fk          INT NOT NULL,
        id_station_fk        INT NOT NULL,
        order_route_station  INT NOT NULL,
        state_route_station  BOOLEAN NOT NULL DEFAULT TRUE,
        CONSTRAINT pk_route_station PRIMARY KEY (id_route_fk, id_station_fk),
        CONSTRAINT uq_route_station_order UNIQUE (id_route_fk, order_route_station),
        CONSTRAINT ck_route_station_order CHECK (order_route_station > 0)
    );

    CREATE TABLE route_bus (
        id_route_fk  INT NOT NULL,
        id_bus_fk    INT NOT NULL,
        service_date DATE NOT NULL DEFAULT CURRENT_DATE,
        start_time   TIME NOT NULL,
        end_time     TIME,
        CONSTRAINT pk_route_bus PRIMARY KEY (id_route_fk, id_bus_fk, service_date),
        CONSTRAINT ck_route_bus_time CHECK (end_time IS NULL OR end_time >= start_time)
    );

    CREATE TABLE service_type (
        id_service_type    SERIAL PRIMARY KEY,
        name_service_type  VARCHAR(50) NOT NULL,
        state_service_type BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE service_type_route (
        id_route_fk        INT NOT NULL,
        id_service_type_fk INT NOT NULL,
        CONSTRAINT pk_service_type_route PRIMARY KEY (id_route_fk, id_service_type_fk)
    );

    CREATE TABLE station_type (
        id_station_type    SERIAL PRIMARY KEY,
        name_station_type  VARCHAR(50) NOT NULL,
        state_station_type BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE station (
        id_station          SERIAL PRIMARY KEY,
        id_station_type_fk  INT NOT NULL,
        name_station        VARCHAR(100) NOT NULL,
        address_station     VARCHAR(150),
        latitude_station    NUMERIC(9,6),
        longitude_station   NUMERIC(9,6),
        state_station       BOOLEAN NOT NULL DEFAULT TRUE
    );

    -- =====================================================================
    -- 2. FOREIGN KEYS
    -- =====================================================================

    ALTER TABLE person
        ADD CONSTRAINT fk_person_document_type
        FOREIGN KEY (id_doc_type_fk) REFERENCES document_type(id_doc_type);

    ALTER TABLE rol_permission
        ADD CONSTRAINT fk_rol_permission_rol
        FOREIGN KEY (id_rol_fk) REFERENCES rol(id_rol),
        ADD CONSTRAINT fk_rol_permission_permission
        FOREIGN KEY (id_permission_fk) REFERENCES permission(id_permission);

    ALTER TABLE app_user
        ADD CONSTRAINT fk_app_user_person
        FOREIGN KEY (id_person_fk) REFERENCES person(id_person),
        ADD CONSTRAINT fk_app_user_rol
        FOREIGN KEY (id_rol_fk) REFERENCES rol(id_rol);

    ALTER TABLE user_token
        ADD CONSTRAINT fk_user_token_token_type
        FOREIGN KEY (id_token_type_fk) REFERENCES token_type(id_token_type),
        ADD CONSTRAINT fk_user_token_app_user
        FOREIGN KEY (id_user_fk) REFERENCES app_user(id_user);

    ALTER TABLE employee
        ADD CONSTRAINT fk_employee_employee_position
        FOREIGN KEY (id_employee_position_fk) REFERENCES employee_position(id_employee_position),
        ADD CONSTRAINT fk_employee_employee_area
        FOREIGN KEY (id_employee_area_fk) REFERENCES employee_area(id_employee_area),
        ADD CONSTRAINT fk_employee_app_user
        FOREIGN KEY (id_user_fk) REFERENCES app_user(id_user);

    ALTER TABLE passenger
        ADD CONSTRAINT fk_passenger_app_user
        FOREIGN KEY (id_user_fk) REFERENCES app_user(id_user);

    ALTER TABLE bus
        ADD CONSTRAINT fk_bus_bus_type
        FOREIGN KEY (id_bus_type_fk) REFERENCES bus_type(id_bus_type);

    ALTER TABLE bus_employee
        ADD CONSTRAINT fk_bus_employee_bus
        FOREIGN KEY (id_bus_fk) REFERENCES bus(id_bus),
        ADD CONSTRAINT fk_bus_employee_employee
        FOREIGN KEY (id_employee_fk) REFERENCES employee(id_employee);

    ALTER TABLE route_schedule
        ADD CONSTRAINT fk_route_schedule_route
        FOREIGN KEY (id_route_fk) REFERENCES route(id_route),
        ADD CONSTRAINT fk_route_schedule_schedule
        FOREIGN KEY (id_schedule_fk) REFERENCES schedule(id_schedule);

    ALTER TABLE route_bus
        ADD CONSTRAINT fk_route_bus_route
        FOREIGN KEY (id_route_fk) REFERENCES route(id_route),
        ADD CONSTRAINT fk_route_bus_bus
        FOREIGN KEY (id_bus_fk) REFERENCES bus(id_bus);

    ALTER TABLE service_type_route
        ADD CONSTRAINT fk_service_type_route_route
        FOREIGN KEY (id_route_fk) REFERENCES route(id_route),
        ADD CONSTRAINT fk_service_type_route_service_type
        FOREIGN KEY (id_service_type_fk) REFERENCES service_type(id_service_type);

    ALTER TABLE station
        ADD CONSTRAINT fk_station_station_type
        FOREIGN KEY (id_station_type_fk) REFERENCES station_type(id_station_type);

    ALTER TABLE route_station
        ADD CONSTRAINT fk_route_station_route
        FOREIGN KEY (id_route_fk) REFERENCES route(id_route),
        ADD CONSTRAINT fk_route_station_station
        FOREIGN KEY (id_station_fk) REFERENCES station(id_station);

    ALTER TABLE card
        ADD CONSTRAINT fk_card_passenger
        FOREIGN KEY (id_passenger_fk) REFERENCES passenger(id_passenger),
        ADD CONSTRAINT fk_card_card_type
        FOREIGN KEY (id_card_type_fk) REFERENCES card_type(id_card_type),
        ADD CONSTRAINT fk_card_card_state
        FOREIGN KEY (id_card_state_fk) REFERENCES card_state(id_card_state);

    ALTER TABLE card_transaction
        ADD CONSTRAINT fk_card_transaction_card
        FOREIGN KEY (id_card_fk) REFERENCES card(id_card),
        ADD CONSTRAINT fk_card_transaction_transaction_type
        FOREIGN KEY (id_transaction_type_fk) REFERENCES transaction_type(id_transaction_type),
        ADD CONSTRAINT fk_card_transaction_station
        FOREIGN KEY (id_station_fk) REFERENCES station(id_station);
