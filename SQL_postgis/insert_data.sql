
--EQUIPOS
insert into JR.equipo (id, nombre) values (1, 'Patriotas');

insert into JR.equipo (id, nombre) values (2, 'Valencia B');

insert into JR.equipo (id, nombre) values (3, 'Tudelano');

--JUGADORES
insert into JR.jugador (dni,nombre, edad, estatura, equipo, num_camiseta)
  values (602321, 'Juan', 15, 170, 1, 10);

insert into JR.jugador (dni,nombre, edad, estatura, equipo, num_camiseta)
  values (520479, 'Miguel', 16, 180, 1, 55);

insert into JR.jugador (dni,nombre, edad, estatura, equipo, num_camiseta)
  values (985203, 'Ramon', 15, 175, 1, 5);

insert into JR.jugador (dni,nombre, edad, estatura, equipo, num_camiseta)
  values (987563, 'Luis', 20, 178, 2, 10);

insert into JR.jugador (dni,nombre, edad, estatura, equipo, num_camiseta)
  values (487520, 'Mateo', 18, 177, 2, 7);

insert into JR.jugador (dni,nombre, edad, estatura, equipo, num_camiseta)
  values (228800, 'David', 19, 182, 2, 4);


--ENTRENADORES
insert into JR.entrenador (dni, nombre, categoria, equipo) values (603589, 'Mario','A', 1);

insert into JR.entrenador (dni, nombre, categoria, equipo) values (586547, 'Julian','C', 2);
