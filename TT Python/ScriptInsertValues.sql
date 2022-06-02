insert into departamento (id, nombre, localidad, id_director) values (1, 'Corunet', 'A Coruña', 1);
insert into departamento (id, nombre, localidad, id_director) values (2, 'Inycom', 'Pontevedra', 1);
insert into departamento (id, nombre, localidad, id_director) values (3, 'Hyndra', 'Vigo', 2);

insert into empleado (id, nombre, trabajo, fecha_contratacion, salario, comision, id_departamento) values (1, 'Guillermo', 'Supervisor', '2021/12/12', 1800, 50, 1);
insert into empleado (id, nombre, trabajo, fecha_contratacion, salario, id_jefe, id_departamento) values (2, 'Pepe', 'Desarrollador', '2022/02/13', 1200, 1, 2);
insert into empleado (id, nombre, trabajo, fecha_contratacion, salario, comision, id_jefe, id_departamento) values (3, 'Emilio', 'Testet', '2022/04/04', 1500, 25, 1, 3);

insert into proyecto (id, nombre, localidad)
values (1, 'Web Inditex', 'A Coruña');
insert into proyecto (id, nombre, localidad)
values (2, 'App e-commerce', 'Santiago de Compostela');
insert into proyecto (id, nombre, localidad)
values (3, 'Hacking', 'Vigo');

insert into EmpleadoProyecto (id_empleado, id_proyecto, horas) 
values (1,1,10);
insert into EmpleadoProyecto (id_empleado, id_proyecto, horas) 
values (1,2,10);
insert into EmpleadoProyecto (id_empleado, id_proyecto, horas) 
values (1,3,10);
insert into EmpleadoProyecto (id_empleado, id_proyecto, horas) 
values (2,1,50);
insert into EmpleadoProyecto (id_empleado, id_proyecto, horas) 
values (3,1,0);

insert into DepartamentoProyecto (id_departamento, id_proyecto) values (1,1);
insert into DepartamentoProyecto (id_departamento, id_proyecto) values (1,2);
insert into DepartamentoProyecto (id_departamento, id_proyecto) values (1,3);
insert into DepartamentoProyecto (id_departamento, id_proyecto) values (2,1);
insert into DepartamentoProyecto (id_departamento, id_proyecto) values (3,1);

ALTER TABLE Departamento ADD CONSTRAINT fk_director FOREIGN KEY(id_director) references Empleado(id) ON DELETE NO ACTION ON UPDATE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
