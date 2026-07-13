
-- ESQUEMA Y DOMINIOS
create schema JR;

create domain JR.d_categoria as varchar
  check (value in ('A','B','C','Desconocido'));

create domain JR.d_numcamiseta as integer
  check (value >= 1 and value <= 99);

-- TABLAS
create table JR.equipo(
  id integer,
  nombre varchar unique,
  constraint pk_equipo primary key (id)
);

create table JR.entrenador(
  dni integer,
  nombre varchar not null,
  categoria JR.d_categoria not null default 'Desconocido',
  equipo integer unique not null,
  constraint pk_entrenador primary key (dni)
);

create table JR.jugador(
  dni integer,
  nombre varchar not null,
  edad integer default null constraint edad_check check (edad >= 15 and edad <=20),
  estatura integer default -1,
  equipo integer not null,
  num_camiseta JR.d_numcamiseta,
  constraint pk_jugador primary key (dni),
  constraint ru_jugador unique(equipo, num_camiseta)
);

-- INTEGRIDAD REFERENCAL
-- EQUIPO 1..1 ENTRENADOR
-- Un equipo solo puede tener un entrenador y un entrenador solo puede entrenar a un equipo
alter table JR.entrenador add constraint fk_equipo
  foreign key (equipo) references JR.equipo (id) on delete cascade on update cascade;

-- EQUIPO 1..M JUGADOR
-- Un jugador solo puede pertenecer a un equipo y un equipo puede tener muchos jugadores
alter table JR.jugador add constraint fk_equipo
  foreign key (equipo) references JR.equipo (id) on delete cascade on update cascade;
