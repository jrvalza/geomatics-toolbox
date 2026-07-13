
/*
=================================Tabla Jugador=================================
clave primaria
restriccion unicidad (equipo, numcamiseta)
edad (entre 15 y 20)
numcamiseta (dominio)
*/

--Insertar jugador con dni existente (viola restriccion clave primaria)
insert into JR.jugador (dni, nombre, edad, estatura, equipo, num_camiseta)
    values (228800, 'Jose', 20, 170, 1, 11);
--Insertar nuevo jugador en un equipo con dorsal ya existente (viola restricción de unicidad)
insert into JR.jugador (dni, nombre, edad, estatura, equipo, num_camiseta)
    values (228811, 'Jose', 20, 170, 2, 10);
--Insertar nuevo jugador con 25 años de edad (restricción check)
insert into JR.jugador (dni, nombre, edad, estatura, equipo, num_camiseta)
    values (228811, 'Jose', 25, 170, 2, 3);
--Insertar nuevo jugador con dorsal fuera de rango (restricción check en dominio)
insert into JR.jugador (dni, nombre, edad, estatura, equipo, num_camiseta)
    values (228811, 'Jose', 25, 170, 2, 100);

/*
=================================Tabla Entrenador=================================
dominio (categoria)
no nulo (campo nombre)
unicidad ( campo equipo)
*/

--Actualizar categoria de un entrenador (restriccion check en dominio)
update JR.entrenador set categoria='D' where dni=586547

--Actualizar nombre y equipo de un entrenador (restriccion unicidad y no nulo)
update JR.entrenador set nombre=null, equipo=1 where dni=586547
update JR.entrenador set equipo=1 where dni=586547


/*=================================Tabla Equipo=================================
unicidad (campo nombre)
clave primaria (id)
*/

--Actualizar el nombre de un equipo a otro ya existente (restriccion unicidad)
update JR.equipo set nombre='Patriotas' where id=2

--Insertar equipo con id existente (clave primaria)
insert into JR.equipo (id, nombre) values (2, 'Mestalla');


/*==============================================================================
==============================INTEGRIDAD REFERENCIA=============================
================================================================================
*/

--Tabla jugador
--actualización en cascada
update JR.equipo set id=4 where id=1
--borrado en cascada
delete from jr.equipo where id=4;

--Tabla Entrenador
--actualización en cascada
update JR.equipo set id=4 where id=2
--borrado en cascada
delete from jr.equipo where id=100;
