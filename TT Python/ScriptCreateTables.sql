DROP TABLE DepartamentoProyecto CASCADE;
DROP TABLE EmpleadoProyecto CASCADE;
DROP TABLE Proyecto CASCADE;
DROP TABLE Empleado CASCADE;
DROP TABLE Departamento CASCADE;

CREATE TABLE Departamento(
	id int constraint pk_departamento primary key,
	nombre text not null,
	localidad text not null,
	id_director int
);

CREATE TABLE Empleado(
	id int constraint pk_empleado primary key,
	nombre text not null,
	trabajo text not null,
	fecha_contratacion date not null,
	salario float not null,
	comision float,
	id_jefe int references Empleado(id) ON DELETE SET NULL ON UPDATE CASCADE,
	id_departamento int references Departamento(id) ON DELETE SET NULL ON UPDATE CASCADE,
	constraint ch_salario check (salario >= 0),
	constraint ch_comision check (comision >= 0)
);

CREATE TABLE Proyecto(
	id int constraint pk_proyecto primary key,
	nombre text not null,
	localidad text not null
);

CREATE TABLE EmpleadoProyecto(
	id_empleado int references Empleado(id) ON DELETE CASCADE ON UPDATE CASCADE,
	id_proyecto int references Proyecto(id) ON DELETE CASCADE ON UPDATE CASCADE,
	horas int not null,
	constraint ch_horas check (horas >= 0)
);

CREATE TABLE DepartamentoProyecto(
	id_departamento int references Departamento(id) ON DELETE CASCADE ON UPDATE CASCADE,
	id_proyecto int references Proyecto(id) ON DELETE CASCADE ON UPDATE CASCADE
);