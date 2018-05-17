create database EICO;
use EICO;

drop database EICO;

create table if not exists Sitio_Interes(
	id int auto_increment,
    titulo varchar(100),
    contenido text,
    
    primary key(id)
);


create table if not exists Servicio(
	id int auto_increment,
    titulo varchar(100),
    contenido text,
    
    primary key(id)
);

#
create table if not exists Tipo_Usuario(
	id int auto_increment,
    nombre varchar(13),
    
    primary key(id)
);

create table if not exists Tipo_Calificacion(
	id int auto_increment,
    nombre varchar(20),
    
    primary key(id)
);

#create table if not exists Tipo_Media(
#	id int auto_increment,
#    nombre varchar(20),
    
#    primary key(id)
#);




#create table if not exists Tipo_Formacion(
#	id int auto_increment,
#    nombre varchar(9),
    
#    primary key(id)
#);


#create table if not exists Media(
#	id int auto_increment,
#    link text,
#    tipo_media_fk int,
    
#    primary key(id),
#    foreign key(tipo_media_fk) references Tipo_Media(id)
#);


create table if not exists Usuario(
	id int auto_increment,
    nombre_usuario varchar(50),
    contrasena varchar(50),
    correo_electronico varchar(40),
    titulo varchar(100),
    profesion varchar(100),
    lugar_trabajo varchar(200),
    
    media text, #cloudinay
    tipo_usuario_fk int,
    
    
    primary key(id),
    foreign key(tipo_usuario_fk) references Tipo_Usuario(id) on delete cascade
    #foreign key(media_fk) references Media(id)
);



create table if not exists Educacion(
	id int auto_increment,
    nombre_titulo varchar(200),
    centro_educativo varchar(200),
    fecha_inicio date,
    fecha_final date,
    descripcion text,
    usuario_fk int,
    #tipo_formacion_fk int,
    
    primary key(id),
    #foreign key(tipo_formacion_fk) references Tipo_Formacion(id)
    foreign key(usuario_fk) references Usuario(id) on delete cascade
);



create table if not exists Experiencia_O_Proyecto(
	id int auto_increment,
    nombre varchar(200),
    lugar_trabajo varchar(200),
    fecha_inicio date,
    fecha_final date,
    descripcion text,
    usuario_fk int,
    #tipo_formacion_fk int,
    
    primary key(id),
    #foreign key(tipo_formacion_fk) references Tipo_Formacion(id)
    foreign key(usuario_fk) references Usuario(id) on delete cascade
);









create table if not exists Publicacion(
	id int auto_increment,
    titulo varchar(100),
    descripcion text,
    link_video text,
    fecha date,
    media text,
    usuario_fk int,
    
    primary key(id),
    foreign key(usuario_fk) references Usuario(id) on delete cascade
);

create table if not exists Calendario(
	id int auto_increment,
    titulo varchar(100),
    descripcion text,
    fecha date,
    
    primary key(id)
);

create table if not exists Comentario(
	id int auto_increment,
    descripcion text,
    usuario_fk int,
    fecha date,
    publicacion_fk int,
    
    primary key(id),
    foreign key(usuario_fk) references Usuario(id) on delete cascade,
    foreign key(publicacion_fk) references Publicacion(id) on delete cascade
);

create table if not exists CalificacionXPublicacion(
	publicacion_fk int,
    calificacion_fk int,
    usuario_fk int,
    fecha date,
    
    foreign key(publicacion_fk) references Publicacion(id) on delete cascade,
    foreign key(calificacion_fk) references Tipo_Calificacion(id) on delete cascade,
    foreign key(usuario_fk) references Usuario(id) on delete cascade
);


create table Visita(
	id int auto_increment,
    fecha date,
    
    primary key(id)

)





#create table if not exists MediaXPublicacion(
#	publicacion_fk int,
#    media_fk int,
    
#    foreign key(publicacion_fk) references Publicacion(id),
#    foreign key(media_fk) references Media(id)
#);

#create table if not exists FormacionXUsuario(
#	usuario_fk int,
#    formacion_fk int,
    
#    foreign key(usuario_fk) references Usuario(id),
#    foreign key(formacion_fk) references Formacion(id)
#);

