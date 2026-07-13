--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

-- Started on 2024-03-20 20:27:08

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 9 (class 2615 OID 23256)
-- Name: jr; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA jr;


ALTER SCHEMA jr OWNER TO postgres;

--
-- TOC entry 1707 (class 1247 OID 23258)
-- Name: d_categoria; Type: DOMAIN; Schema: jr; Owner: postgres
--

CREATE DOMAIN jr.d_categoria AS character varying
	CONSTRAINT d_categoria_check CHECK (((VALUE)::text = ANY ((ARRAY['A'::character varying, 'B'::character varying, 'C'::character varying, 'Desconocido'::character varying])::text[])));


ALTER DOMAIN jr.d_categoria OWNER TO postgres;

--
-- TOC entry 1711 (class 1247 OID 23261)
-- Name: d_numcamiseta; Type: DOMAIN; Schema: jr; Owner: postgres
--

CREATE DOMAIN jr.d_numcamiseta AS integer
	CONSTRAINT d_numcamiseta_check CHECK (((VALUE >= 1) AND (VALUE <= 99)));


ALTER DOMAIN jr.d_numcamiseta OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 245 (class 1259 OID 23272)
-- Name: entrenador; Type: TABLE; Schema: jr; Owner: postgres
--

CREATE TABLE jr.entrenador (
    dni integer NOT NULL,
    nombre character varying NOT NULL,
    categoria jr.d_categoria DEFAULT 'Desconocido'::character varying NOT NULL,
    equipo integer NOT NULL
);


ALTER TABLE jr.entrenador OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 23263)
-- Name: equipo; Type: TABLE; Schema: jr; Owner: postgres
--

CREATE TABLE jr.equipo (
    id integer NOT NULL,
    nombre character varying
);


ALTER TABLE jr.equipo OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 23282)
-- Name: jugador; Type: TABLE; Schema: jr; Owner: postgres
--

CREATE TABLE jr.jugador (
    dni integer NOT NULL,
    nombre character varying NOT NULL,
    edad integer,
    estatura integer DEFAULT '-1'::integer,
    equipo integer NOT NULL,
    num_camiseta jr.d_numcamiseta,
    CONSTRAINT edad_check CHECK (((edad >= 15) AND (edad <= 20)))
);


ALTER TABLE jr.jugador OWNER TO postgres;

--
-- TOC entry 5807 (class 0 OID 23272)
-- Dependencies: 245
-- Data for Name: entrenador; Type: TABLE DATA; Schema: jr; Owner: postgres
--

INSERT INTO jr.entrenador (dni, nombre, categoria, equipo) VALUES (603589, 'Mario', 'A', 1);
INSERT INTO jr.entrenador (dni, nombre, categoria, equipo) VALUES (586547, 'Julian', 'C', 2);


--
-- TOC entry 5806 (class 0 OID 23263)
-- Dependencies: 244
-- Data for Name: equipo; Type: TABLE DATA; Schema: jr; Owner: postgres
--

INSERT INTO jr.equipo (id, nombre) VALUES (1, 'Patriotas');
INSERT INTO jr.equipo (id, nombre) VALUES (2, 'Valencia B');
INSERT INTO jr.equipo (id, nombre) VALUES (3, 'Tudelano');


--
-- TOC entry 5808 (class 0 OID 23282)
-- Dependencies: 246
-- Data for Name: jugador; Type: TABLE DATA; Schema: jr; Owner: postgres
--

INSERT INTO jr.jugador (dni, nombre, edad, estatura, equipo, num_camiseta) VALUES (602321, 'Juan', 15, 170, 1, 10);
INSERT INTO jr.jugador (dni, nombre, edad, estatura, equipo, num_camiseta) VALUES (520479, 'Miguel', 16, 180, 1, 55);
INSERT INTO jr.jugador (dni, nombre, edad, estatura, equipo, num_camiseta) VALUES (985203, 'Ramon', 15, 175, 1, 5);
INSERT INTO jr.jugador (dni, nombre, edad, estatura, equipo, num_camiseta) VALUES (987563, 'Luis', 20, 178, 2, 10);
INSERT INTO jr.jugador (dni, nombre, edad, estatura, equipo, num_camiseta) VALUES (487520, 'Mateo', 18, 177, 2, 7);
INSERT INTO jr.jugador (dni, nombre, edad, estatura, equipo, num_camiseta) VALUES (228800, 'David', 19, 182, 2, 4);


--
-- TOC entry 5649 (class 2606 OID 23281)
-- Name: entrenador entrenador_equipo_key; Type: CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.entrenador
    ADD CONSTRAINT entrenador_equipo_key UNIQUE (equipo);


--
-- TOC entry 5645 (class 2606 OID 23271)
-- Name: equipo equipo_nombre_key; Type: CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.equipo
    ADD CONSTRAINT equipo_nombre_key UNIQUE (nombre);


--
-- TOC entry 5651 (class 2606 OID 23279)
-- Name: entrenador pk_entrenador; Type: CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.entrenador
    ADD CONSTRAINT pk_entrenador PRIMARY KEY (dni);


--
-- TOC entry 5647 (class 2606 OID 23269)
-- Name: equipo pk_equipo; Type: CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.equipo
    ADD CONSTRAINT pk_equipo PRIMARY KEY (id);


--
-- TOC entry 5653 (class 2606 OID 23290)
-- Name: jugador pk_jugador; Type: CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.jugador
    ADD CONSTRAINT pk_jugador PRIMARY KEY (dni);


--
-- TOC entry 5655 (class 2606 OID 23292)
-- Name: jugador ru_jugador; Type: CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.jugador
    ADD CONSTRAINT ru_jugador UNIQUE (equipo, num_camiseta);


--
-- TOC entry 5656 (class 2606 OID 23293)
-- Name: entrenador fk_equipo; Type: FK CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.entrenador
    ADD CONSTRAINT fk_equipo FOREIGN KEY (equipo) REFERENCES jr.equipo(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 5657 (class 2606 OID 23298)
-- Name: jugador fk_equipo; Type: FK CONSTRAINT; Schema: jr; Owner: postgres
--

ALTER TABLE ONLY jr.jugador
    ADD CONSTRAINT fk_equipo FOREIGN KEY (equipo) REFERENCES jr.equipo(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2024-03-20 20:27:09

--
-- PostgreSQL database dump complete
--

