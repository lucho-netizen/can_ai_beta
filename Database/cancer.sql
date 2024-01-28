CREATE DATABASE cancer;

USE cancer;

CREATE TABLE roles (
    id_role INT PRIMARY KEY,
    role_name VARCHAR(20)
);

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255) NOT NULL,
    tipo_documento varchar(20),
    celular INT,
    identificacion INT,
    edad INT,
    peso INT,
    correo VARCHAR(255) ,
    password VARCHAR(255),
    id_rwol INT,
    FOREIGN KEY (id_rol) REFERENCES roles(id_role)
);

CREATE TABLE resultados (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT,
    fechaExamen DATE,
    resultadoCancer BOOLEAN,
    FOREIGN KEY (id_user) REFERENCES usuario(id)
);

CREATE TABLE sintomas (
    id_sintomas INT PRIMARY KEY,
    sintoma VARCHAR(255)
);

CREATE TABLE diagnostico (
    id_paciente INT PRIMARY KEY,
    diagnostico VARCHAR(255),
    id_rol INT,
    id_sintomas INT,
    FOREIGN KEY (id_paciente) REFERENCES usuario(id),
    FOREIGN KEY (id_sintomas) REFERENCES sintomas(id_sintomas),
    FOREIGN KEY (id_rol) REFERENCES roles(id_role)
);

CREATE TABLE atributos (
    id_atributo INT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion VARCHAR(255)
);

CREATE TABLE sintomasxuser (
    id_sintomasxuser INT PRIMARY KEY,
    id_user INT,
    id_sintomas INT,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    FOREIGN KEY (id_user) REFERENCES usuario(id),
    FOREIGN KEY (id_sintomas) REFERENCES sintomas(id_sintomas)
);

CREATE TABLE atributoxuser (
    id_atributoxuser INT PRIMARY KEY,
    id_user INT,
    id_atributo INT,
    valor VARCHAR(255),
    descripcion VARCHAR(255),
    FOREIGN KEY (id_user) REFERENCES usuario(id),
    FOREIGN KEY (id_atributo) REFERENCES atributos(id_atributo)
);

-- INSERT ROLES --
INSERT INTO roles (id_role, role_name) VALUES (1, 'paciente'), (2, 'administrador');
