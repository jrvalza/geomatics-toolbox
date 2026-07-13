
------------------------------------------------------------------
--Crete table est and insert data
------------------------------------------------------------------
drop table if exists est;
create table est (id serial primary key, t double precision, x double precision, y double precision);
insert into est (t, x, y) values (25,100,200);
insert into est (t, x, y) values (30,150,200);
insert into est (t, x, y) values (32,120,250);
insert into est (t, x, y) values (35,70,180);
insert into est (t, x, y) values (40,140,150);
insert into est (t, x, y) values (15,110,225);
insert into est (t, x, y) values (23,130,190);
insert into est (t, x, y) values (10,130,150);


------------------------------------------------------------------
--Which cities do not have another city within a 30-meter radius?
------------------------------------------------------------------

--Subquery
SELECT *
FROM est
WHERE id NOT IN (SELECT e1.id
				 FROM est e1, est e2
				 WHERE e1.id<>e2.id AND sqrt(pow(e2.x-e1.x,2)+pow(e2.y-e1.y,2)) < 30 
				 GROUP BY e1.id
				 )

--External concatenation
SELECT *
FROM est 
LEFT JOIN (SELECT e1.id as id2
		   FROM est e1, est e2
		   WHERE e1.id<>e2.id AND sqrt(pow(e2.x-e1.x,2)+pow(e2.y-e1.y,2)) < 30
		   GROUP BY e1.id) AS aux
ON est.id=aux.id2
WHERE id2 IS NULL
