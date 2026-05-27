-- TABLAS

create table usuario(
    id_usuario serial primary key,
    nombre varchar(100) not null unique,
    autorizado boolean default true not null,
    fecha_registro timestamp default now() not null,
    administrador boolean default false not null
);

create table acceso(
    id_acceso serial primary key,
    id_usuario integer references usuario(id_usuario),
    fecha timestamp default now() not null,
    autorizado boolean not null,
    confianza float not null
);