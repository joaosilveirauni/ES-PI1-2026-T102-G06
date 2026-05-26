DROP DATABASE IF EXISTS ladpy;

CREATE DATABASE ladpy;
USE ladpy;

CREATE TABLE eleitores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(24) NOT NULL UNIQUE,
    titulo_eleitor VARCHAR(12) NOT NULL UNIQUE,
    chave_acesso VARCHAR(20) NOT NULL,
    ja_votou BOOLEAN DEFAULT FALSE,
    is_mesario BOOLEAN DEFAULT FALSE
);

CREATE TABLE candidatos(
id INT PRIMARY KEY auto_increment,
nome varchar(100) not null,
numero int not null unique,
partido varchar(50) not null
);

CREATE TABLE votos(
id int primary key auto_increment,
candidato_id int,
tipo ENUM('VALIDO', 'NULO') not null,
protocolo varchar(30) not null,
data_voto timestamp default current_timestamp,
foreign key (candidato_id) references candidatos(id)
);

INSERT INTO candidatos (nome, numero, partido) VALUES ('Candidato A', 11, 'Partido 1');
INSERT INTO candidatos (nome, numero, partido) VALUES ('Candidato B', 22, 'Partido 2');
