-- Crear usuario
CREATE USER 'practica3'@'%' IDENTIFIED BY 'practica3';

-- Crear base de datos
CREATE DATABASE practica3;
use practica3;

-- Crear tablas
CREATE TABLE users
(
    id        int auto_increment primary key not null,
    username  varchar(50)                    not null unique,
    email     varchar(50)                    not null unique,
    password  varchar(255)                   not null,
    recover   varchar(255)                   not null,
    avatar    varchar(255)                   not null default 'https://0sc4r24sisdis2024.s3.amazonaws.com/UZNjvpZW_400x400.jpg',
    biography varchar(255)                   not null default 'Sin biografia',
    validated boolean                        not null default true,
    tries     int                            not null default 0
);

CREATE TABLE messages
(
    id       int auto_increment primary key not null,
    user_id  int                            not null,
    message  varchar(255)                   not null,
    adjunct  varchar(255)                   not null default 'https://0sc4r24sisdis2024.s3.amazonaws.com/UZNjvpZW_400x400.jpg',
    datetime timestamp                      not null default current_timestamp,
    foreign key (user_id) references users (id)
);

CREATE TABLE followers
(
    user_id      int not null,
    following_id int not null,
    foreign key (user_id) references users (id),
    foreign key (following_id) references users (id),
    unique key (user_id, following_id)
);

CREATE TABLE likes
(
    message_id int                      not null,
    user_id    int                      not null,
    type       enum ('like', 'dislike') not null,
    foreign key (message_id) references messages (id),
    foreign key (user_id) references users (id),
    unique key (message_id, user_id)
);

CREATE TABLE replies
(
    id         int auto_increment primary key not null,
    message_id int                            not null,
    user_id    int                            not null,
    comment    varchar(255)                   not null,
    datetime   timestamp                      not null default current_timestamp,
    foreign key (message_id) references messages (id),
    foreign key (user_id) references users (id)
);

-- Insertar datos de prueba
INSERT INTO users
values (NULL, 'admin', 'admin@admin.es', 'admin', 'admin 12345 67890', 'https://0sc4r24sisdis2024.s3.amazonaws.com/UZNjvpZW_400x400.jpg', 'Administrador', true, 0),
       (NULL, 'usuario', 'usuario@usuario.es', 'usuario', 'usuario 12345 67890', 'https://0sc4r24sisdis2024.s3.amazonaws.com/UZNjvpZW_400x400.jpg', 'Usuario', true, 0);

INSERT INTO messages
values (NULL, 1, 'Mensaje de prueba 1', 'https://0sc4r24sisdis2024.s3.amazonaws.com/UZNjvpZW_400x400.jpg', current_timestamp),
       (NULL, 2, 'Mensaje de prueba 2', 'https://0sc4r24sisdis2024.s3.amazonaws.com/UZNjvpZW_400x400.jpg', current_timestamp);

INSERT INTO followers
values (1, 2);

INSERT INTO likes
values (1, 2, 'like');

INSERT INTO replies
values (NULL, 1, 2, 'Respuesta de prueba 1', current_timestamp),
       (NULL, 2, 1, 'Respuesta de prueba 2', current_timestamp);