-- =====================================================================
-- PROJECT: Public Transportation System - MILENEW
-- FILE:    milenew_db.sql
-- DESCRIPTION: PostgreSQL database creation script generated from the
--              entity-relationship model (ER diagram).
--
-- CLEAN CODE CONVENTIONS USED:
--   1. Table and column names in lowercase snake_case
--      (avoids having to quote identifiers in every query).
--   2. "id_" prefix for primary keys and "_fk" suffix for foreign
--      keys, so their role is obvious at a glance.
--   3. Constraint names are explicit: pk_<table>, fk_<source_table>_<referenced_table>.
--   4. Every table (and sensitive column) is documented with a
--      COMMENT ON statement directly in the database catalog.
--   5. ALL tables are created first (including their *_fk columns)
--      and the relationships (FOREIGN KEY constraints) are added
--      ONLY at the end via ALTER TABLE, grouped by the table where
--      each foreign key lives, exactly as requested.
--   6. "user" is a reserved word in PostgreSQL, so the "User" table
--      from the model is implemented as "app_user".
-- =====================================================================


-- =====================================================================
-- 1. DATABASE CREATION
-- =====================================================================
-- Run once, while connected to an existing database (e.g. postgres).
-- DROP DATABASE IF EXISTS milenew_db; -- Uncomment only in development environments.

CREATE DATABASE milenew_db
    WITH ENCODING = 'UTF8';

-- From this point on, the script must be executed while connected to milenew_db.
-- In psql:  \c milenew_db


-- =====================================================================
-- 2. TABLE CREATION
--    Order: modules with fewer functional dependencies first, but
--    WITHOUT foreign key constraints yet (those are added in
--    section 3). This avoids table-creation ordering errors.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 2.1 SECURITY AND USERS MODULE
-- ---------------------------------------------------------------------

-- Catalog of identity document types (ID card, passport, etc.)
CREATE TABLE document_type (
    id_doc_type      SERIAL PRIMARY KEY,
    name_doc_type    VARCHAR(50)  NOT NULL,
    acronym_doc_type VARCHAR(10)  NOT NULL,
    state_doc_type   BOOLEAN      NOT NULL DEFAULT TRUE
);

-- Personal data shared by any individual (passenger or employee)
CREATE TABLE person (
    id_person                SERIAL PRIMARY KEY,
    id_doc_type_fk           INT          NOT NULL,
    num_doc_person           VARCHAR(20)  NOT NULL UNIQUE,
    first_name_person        VARCHAR(50)  NOT NULL,
    second_name_person       VARCHAR(50),
    first_last_name_person   VARCHAR(50)  NOT NULL,
    second_last_name_person  VARCHAR(50),
    phone_number_person      VARCHAR(20),
    birthdate_person         DATE,
    email_person             VARCHAR(150) UNIQUE,
    state_person             BOOLEAN      NOT NULL DEFAULT TRUE
);

-- System roles (Administrator, Passenger, Driver, etc.)
CREATE TABLE rol (
    id_rol          SERIAL PRIMARY KEY,
    name_rol        VARCHAR(50)  NOT NULL,
    description_rol VARCHAR(200),
    state_rol       BOOLEAN      NOT NULL DEFAULT TRUE
);

-- Individual permissions that can be granted to a role
CREATE TABLE permission (
    id_permission          SERIAL PRIMARY KEY,
    name_permission        VARCHAR(50)  NOT NULL,
    description_permission VARCHAR(200),
    state_permission       BOOLEAN      NOT NULL DEFAULT TRUE
);

-- N:M bridge table between rol and permission (composite primary key)
CREATE TABLE rol_permission (
    id_rol_fk        INT NOT NULL,
    id_permission_fk INT NOT NULL,
    CONSTRAINT pk_rol_permission PRIMARY KEY (id_rol_fk, id_permission_fk)
);

-- System access account. A user is linked to a person and a role.
-- Renamed from "User" to "app_user" because USER is a reserved word in PostgreSQL.
CREATE TABLE app_user (
    id_user        SERIAL PRIMARY KEY,
    id_person_fk   INT          NOT NULL,
    id_rol_fk      INT          NOT NULL,
    username       VARCHAR(50)  NOT NULL UNIQUE,
    password       VARCHAR(255) NOT NULL, -- Must always be stored as a hash, never in plain text.
    state_user     BOOLEAN      NOT NULL DEFAULT TRUE
);

-- Catalog of token types (access, password recovery, session, etc.)
CREATE TABLE token_type (
    id_token_type    SERIAL PRIMARY KEY,
    name_token_type  VARCHAR(50) NOT NULL,
    state_token_type BOOLEAN     NOT NULL DEFAULT TRUE
);

-- Session/authentication tokens issued to a user
CREATE TABLE user_token (
    id_user_token     SERIAL PRIMARY KEY,
    id_token_type_fk  INT       NOT NULL,
    id_user_fk        INT       NOT NULL,
    start_time        TIMESTAMP NOT NULL DEFAULT now(),
    state_user_token  BOOLEAN   NOT NULL DEFAULT TRUE,
    end_time          TIMESTAMP
);

-- ---------------------------------------------------------------------
-- 2.2 EMPLOYEES MODULE
-- ---------------------------------------------------------------------

-- Possible employee positions (Driver, Supervisor, etc.)
CREATE TABLE employee_position (
    id_employee_position    SERIAL PRIMARY KEY,
    name_employee_position  VARCHAR(50) NOT NULL,
    state_employee_position BOOLEAN     NOT NULL DEFAULT TRUE
);

-- Company areas/departments an employee can belong to
CREATE TABLE employee_area (
    id_employee_area    SERIAL PRIMARY KEY,
    name_employee_area  VARCHAR(50)  NOT NULL,
    place_employee_area VARCHAR(100),
    state_employee_area BOOLEAN      NOT NULL DEFAULT TRUE
);

-- Employee: extends app_user, linked to a position and an area
CREATE TABLE employee (
    id_employee              SERIAL PRIMARY KEY,
    id_employee_position_fk  INT     NOT NULL,
    id_employee_area_fk      INT     NOT NULL,
    id_user_fk                INT     NOT NULL,
    working_hours             VARCHAR(50), -- Description of the assigned working schedule.
    state_employee             BOOLEAN NOT NULL DEFAULT TRUE
);

-- ---------------------------------------------------------------------
-- 2.3 PASSENGERS AND CARDS MODULE
-- ---------------------------------------------------------------------

-- Passenger: extends app_user (end user of the transportation service)
CREATE TABLE passenger (
    id_passenger    SERIAL PRIMARY KEY,
    id_user_fk      INT     NOT NULL,
    state_passenger BOOLEAN NOT NULL DEFAULT TRUE
);

-- Catalog of card types (Personal, Student, Senior Citizen, etc.)
CREATE TABLE card_type (
    id_card_type    SERIAL PRIMARY KEY,
    name_card_type  VARCHAR(50) NOT NULL,
    state_card_type BOOLEAN     NOT NULL DEFAULT TRUE
);

-- Catalog of card states (Active, Blocked, Lost, etc.)
CREATE TABLE card_state (
    id_card_state    SERIAL PRIMARY KEY,
    name_card_state  VARCHAR(50) NOT NULL,
    state_card_state BOOLEAN     NOT NULL DEFAULT TRUE
);

-- Top-up/payment card associated with a passenger
CREATE TABLE card (
    id_card           SERIAL PRIMARY KEY,
    id_passenger_fk   INT           NOT NULL,
    id_card_type_fk   INT           NOT NULL,
    id_card_state_fk  INT           NOT NULL,
    balance_card      NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (balance_card >= 0)
);

-- Catalog of transaction types (Top-up, Fare payment, Reversal, etc.)
CREATE TABLE transaction_type (
    id_transaction_type    SERIAL PRIMARY KEY,
    name_transaction_type  VARCHAR(50) NOT NULL,
    state_transaction_type BOOLEAN     NOT NULL DEFAULT TRUE
);

-- History of movements made with a card at a station
CREATE TABLE card_transaction (
    id_card_transaction    SERIAL PRIMARY KEY,
    id_card_fk             INT           NOT NULL,
    id_transaction_type_fk INT           NOT NULL,
    id_station_fk          INT           NOT NULL,
    amount_transaction     NUMERIC(10,2) NOT NULL,
    balance_before          NUMERIC(10,2) NOT NULL,
    balance_after           NUMERIC(10,2) NOT NULL,
    transaction_date_hour   TIMESTAMP     NOT NULL DEFAULT now(),
    state_transaction       BOOLEAN       NOT NULL DEFAULT TRUE
);

-- ---------------------------------------------------------------------
-- 2.4 BUSES AND ROUTES MODULE
-- ---------------------------------------------------------------------

-- Catalog of bus types (Articulated, Standard, Feeder, etc.)
CREATE TABLE bus_type (
    id_bus_type       SERIAL PRIMARY KEY,
    name_bus_type     VARCHAR(50) NOT NULL,
    capacity_bus_type INT         NOT NULL CHECK (capacity_bus_type > 0),
    state_bus_type    BOOLEAN     NOT NULL DEFAULT TRUE
);

-- Physical bus belonging to the fleet
CREATE TABLE bus (
    id_bus         SERIAL PRIMARY KEY,
    id_bus_type_fk INT         NOT NULL,
    code_bus       VARCHAR(20) NOT NULL UNIQUE,
    plate_bus      VARCHAR(10) NOT NULL UNIQUE,
    state_bus      BOOLEAN     NOT NULL DEFAULT TRUE
);

-- N:M bridge table between bus and employee (drivers assigned to a bus)
CREATE TABLE bus_employee (
    id_bus_fk      INT NOT NULL,
    id_employee_fk INT NOT NULL,
    CONSTRAINT pk_bus_employee PRIMARY KEY (id_bus_fk, id_employee_fk)
);

-- Time slots a route can follow
CREATE TABLE schedule (
    id_schedule    SERIAL PRIMARY KEY,
    start_time     TIME        NOT NULL,
    end_time       TIME        NOT NULL,
    day_type       VARCHAR(20) NOT NULL, -- E.g.: 'Weekday', 'Weekend', 'Holiday'.
    state_schedule BOOLEAN     NOT NULL DEFAULT TRUE
);

-- Transportation route, linked to a schedule
CREATE TABLE route (
    id_route          SERIAL PRIMARY KEY,
    id_schedule_fk    INT          NOT NULL,
    code_route        VARCHAR(20)  NOT NULL UNIQUE,
    description_route VARCHAR(200),
    state_route       BOOLEAN      NOT NULL DEFAULT TRUE
);

-- N:M bridge table between route and bus (buses assigned to a route)
CREATE TABLE route_bus (
    id_route_fk INT NOT NULL,
    id_bus_fk   INT NOT NULL,
    CONSTRAINT pk_route_bus PRIMARY KEY (id_route_fk, id_bus_fk)
);

-- Catalog of service types (Express, Special, Ordinary, etc.)
CREATE TABLE service_type (
    id_service_type    SERIAL PRIMARY KEY,
    name_service_type  VARCHAR(50) NOT NULL,
    state_service_type BOOLEAN     NOT NULL DEFAULT TRUE
);

-- N:M bridge table between route and service_type
CREATE TABLE service_type_route (
    id_route_fk        INT NOT NULL,
    id_service_type_fk INT NOT NULL,
    CONSTRAINT pk_service_type_route PRIMARY KEY (id_route_fk, id_service_type_fk)
);

-- ---------------------------------------------------------------------
-- 2.5 STATIONS MODULE
-- ---------------------------------------------------------------------

-- Catalog of station types (Terminal, Intermediate, Portal, etc.)
CREATE TABLE station_type (
    id_station_type    SERIAL PRIMARY KEY,
    name_station_type  VARCHAR(50) NOT NULL,
    state_station_type BOOLEAN     NOT NULL DEFAULT TRUE
);

-- Physical station of the system, with its geographic location
CREATE TABLE station (
    id_station          SERIAL PRIMARY KEY,
    id_station_type_fk  INT           NOT NULL,
    name_station         VARCHAR(100)  NOT NULL,
    address_station       VARCHAR(150),
    latitude_station       NUMERIC(9,6),
    longitude_station      NUMERIC(9,6),
    state_station           BOOLEAN       NOT NULL DEFAULT TRUE
);

-- N:M bridge table between route and station (stops on a route).
-- Includes an attribute of its own: the state of that stop within the route.
CREATE TABLE route_station (
    id_route_fk          INT     NOT NULL,
    id_station_fk        INT     NOT NULL,
    state_route_station  BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_route_station PRIMARY KEY (id_route_fk, id_station_fk)
);


-- =====================================================================
-- 3. RELATIONSHIPS (FOREIGN KEYS)
--    Added at the end, grouped by the table where each FK lives,
--    exactly as marked with "FK" in the entity-relationship model.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 3.1 Relationships of: person
-- ---------------------------------------------------------------------
ALTER TABLE person
    ADD CONSTRAINT fk_person_document_type
    FOREIGN KEY (id_doc_type_fk) REFERENCES document_type (id_doc_type);

-- ---------------------------------------------------------------------
-- 3.2 Relationships of: rol_permission
-- ---------------------------------------------------------------------
ALTER TABLE rol_permission
    ADD CONSTRAINT fk_rol_permission_rol
    FOREIGN KEY (id_rol_fk) REFERENCES rol (id_rol);

ALTER TABLE rol_permission
    ADD CONSTRAINT fk_rol_permission_permission
    FOREIGN KEY (id_permission_fk) REFERENCES permission (id_permission);

-- ---------------------------------------------------------------------
-- 3.3 Relationships of: app_user
-- ---------------------------------------------------------------------
ALTER TABLE app_user
    ADD CONSTRAINT fk_app_user_person
    FOREIGN KEY (id_person_fk) REFERENCES person (id_person);

ALTER TABLE app_user
    ADD CONSTRAINT fk_app_user_rol
    FOREIGN KEY (id_rol_fk) REFERENCES rol (id_rol);

-- ---------------------------------------------------------------------
-- 3.4 Relationships of: user_token
-- ---------------------------------------------------------------------
ALTER TABLE user_token
    ADD CONSTRAINT fk_user_token_token_type
    FOREIGN KEY (id_token_type_fk) REFERENCES token_type (id_token_type);

ALTER TABLE user_token
    ADD CONSTRAINT fk_user_token_app_user
    FOREIGN KEY (id_user_fk) REFERENCES app_user (id_user);

-- ---------------------------------------------------------------------
-- 3.5 Relationships of: employee
-- ---------------------------------------------------------------------
ALTER TABLE employee
    ADD CONSTRAINT fk_employee_employee_position
    FOREIGN KEY (id_employee_position_fk) REFERENCES employee_position (id_employee_position);

ALTER TABLE employee
    ADD CONSTRAINT fk_employee_employee_area
    FOREIGN KEY (id_employee_area_fk) REFERENCES employee_area (id_employee_area);

ALTER TABLE employee
    ADD CONSTRAINT fk_employee_app_user
    FOREIGN KEY (id_user_fk) REFERENCES app_user (id_user);

-- ---------------------------------------------------------------------
-- 3.6 Relationships of: passenger
-- ---------------------------------------------------------------------
ALTER TABLE passenger
    ADD CONSTRAINT fk_passenger_app_user
    FOREIGN KEY (id_user_fk) REFERENCES app_user (id_user);

-- ---------------------------------------------------------------------
-- 3.7 Relationships of: bus
-- ---------------------------------------------------------------------
ALTER TABLE bus
    ADD CONSTRAINT fk_bus_bus_type
    FOREIGN KEY (id_bus_type_fk) REFERENCES bus_type (id_bus_type);

-- ---------------------------------------------------------------------
-- 3.8 Relationships of: bus_employee
-- ---------------------------------------------------------------------
ALTER TABLE bus_employee
    ADD CONSTRAINT fk_bus_employee_bus
    FOREIGN KEY (id_bus_fk) REFERENCES bus (id_bus);

ALTER TABLE bus_employee
    ADD CONSTRAINT fk_bus_employee_employee
    FOREIGN KEY (id_employee_fk) REFERENCES employee (id_employee);

-- ---------------------------------------------------------------------
-- 3.9 Relationships of: route
-- ---------------------------------------------------------------------
ALTER TABLE route
    ADD CONSTRAINT fk_route_schedule
    FOREIGN KEY (id_schedule_fk) REFERENCES schedule (id_schedule);

-- ---------------------------------------------------------------------
-- 3.10 Relationships of: route_bus
-- ---------------------------------------------------------------------
ALTER TABLE route_bus
    ADD CONSTRAINT fk_route_bus_route
    FOREIGN KEY (id_route_fk) REFERENCES route (id_route);

ALTER TABLE route_bus
    ADD CONSTRAINT fk_route_bus_bus
    FOREIGN KEY (id_bus_fk) REFERENCES bus (id_bus);

-- ---------------------------------------------------------------------
-- 3.11 Relationships of: service_type_route
-- ---------------------------------------------------------------------
ALTER TABLE service_type_route
    ADD CONSTRAINT fk_service_type_route_route
    FOREIGN KEY (id_route_fk) REFERENCES route (id_route);

ALTER TABLE service_type_route
    ADD CONSTRAINT fk_service_type_route_service_type
    FOREIGN KEY (id_service_type_fk) REFERENCES service_type (id_service_type);

-- ---------------------------------------------------------------------
-- 3.12 Relationships of: station
-- ---------------------------------------------------------------------
ALTER TABLE station
    ADD CONSTRAINT fk_station_station_type
    FOREIGN KEY (id_station_type_fk) REFERENCES station_type (id_station_type);

-- ---------------------------------------------------------------------
-- 3.13 Relationships of: route_station
-- ---------------------------------------------------------------------
ALTER TABLE route_station
    ADD CONSTRAINT fk_route_station_route
    FOREIGN KEY (id_route_fk) REFERENCES route (id_route);

ALTER TABLE route_station
    ADD CONSTRAINT fk_route_station_station
    FOREIGN KEY (id_station_fk) REFERENCES station (id_station);

-- ---------------------------------------------------------------------
-- 3.14 Relationships of: card
-- ---------------------------------------------------------------------
ALTER TABLE card
    ADD CONSTRAINT fk_card_passenger
    FOREIGN KEY (id_passenger_fk) REFERENCES passenger (id_passenger);

ALTER TABLE card
    ADD CONSTRAINT fk_card_card_type
    FOREIGN KEY (id_card_type_fk) REFERENCES card_type (id_card_type);

ALTER TABLE card
    ADD CONSTRAINT fk_card_card_state
    FOREIGN KEY (id_card_state_fk) REFERENCES card_state (id_card_state);

-- ---------------------------------------------------------------------
-- 3.15 Relationships of: card_transaction
-- ---------------------------------------------------------------------
ALTER TABLE card_transaction
    ADD CONSTRAINT fk_card_transaction_card
    FOREIGN KEY (id_card_fk) REFERENCES card (id_card);

ALTER TABLE card_transaction
    ADD CONSTRAINT fk_card_transaction_transaction_type
    FOREIGN KEY (id_transaction_type_fk) REFERENCES transaction_type (id_transaction_type);

ALTER TABLE card_transaction
    ADD CONSTRAINT fk_card_transaction_station
    FOREIGN KEY (id_station_fk) REFERENCES station (id_station);


-- =====================================================================
-- 4. SCHEMA DOCUMENTATION (COMMENT ON)
--    Clean code best practice: documentation lives right next to the
--    object it describes, inside PostgreSQL's own catalog.
--    It can later be inspected with \dt+ or \d+ <table> in psql.
-- =====================================================================
COMMENT ON DATABASE milenew_db IS 'Database for the Milenew public transportation system.';

COMMENT ON TABLE document_type      IS 'Catalog of identity document types.';
COMMENT ON TABLE person             IS 'Base personal data, shared by passengers and employees.';
COMMENT ON TABLE rol                IS 'Roles available within the system.';
COMMENT ON TABLE permission         IS 'Individual permissions that can be assigned to a role.';
COMMENT ON TABLE rol_permission     IS 'N:M relationship between roles and permissions.';
COMMENT ON TABLE app_user           IS 'System access account, linked to a person and a role.';
COMMENT ON TABLE token_type         IS 'Catalog of authentication token types.';
COMMENT ON TABLE user_token         IS 'Session/authentication tokens issued to a user.';
COMMENT ON TABLE employee_position  IS 'Catalog of positions an employee can hold.';
COMMENT ON TABLE employee_area      IS 'Company areas or departments.';
COMMENT ON TABLE employee           IS 'System employee, extends app_user.';
COMMENT ON TABLE passenger          IS 'System passenger, extends app_user.';
COMMENT ON TABLE bus_type           IS 'Catalog of bus types.';
COMMENT ON TABLE bus                IS 'Physical bus that makes up the fleet.';
COMMENT ON TABLE bus_employee       IS 'N:M relationship between buses and employees (assigned drivers).';
COMMENT ON TABLE schedule           IS 'Time slots a route can follow.';
COMMENT ON TABLE route              IS 'Transportation route.';
COMMENT ON TABLE route_bus          IS 'N:M relationship between routes and buses.';
COMMENT ON TABLE service_type       IS 'Catalog of service types for a route.';
COMMENT ON TABLE service_type_route IS 'N:M relationship between routes and service types.';
COMMENT ON TABLE station_type       IS 'Catalog of station types.';
COMMENT ON TABLE station            IS 'Physical station of the system, with geographic location.';
COMMENT ON TABLE route_station      IS 'N:M relationship between routes and stations (stops on the route).';
COMMENT ON TABLE card_type          IS 'Catalog of card types.';
COMMENT ON TABLE card_state         IS 'Catalog of card states.';
COMMENT ON TABLE card               IS 'Top-up/payment card associated with a passenger.';
COMMENT ON TABLE transaction_type   IS 'Catalog of transaction types performed with a card.';
COMMENT ON TABLE card_transaction   IS 'History of movements made with a card at a station.';

-- =====================================================================
-- END OF SCRIPT
-- =====================================================================