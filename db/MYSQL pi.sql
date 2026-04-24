CREATE TABLE eleitores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    titulo_eleitor VARCHAR(20) NOT NULL UNIQUE,
    chave_acesso VARCHAR(20) NOT NULL,
    ja_votou BOOLEAN DEFAULT FALSE,
    is_mesario BOOLEAN DEFAULT FALSE
);

CREATE TABLE candidatos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    numero INT NOT NULL UNIQUE,
    partido VARCHAR(50) NOT NULL
);

CREATE TABLE votos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    eleitor_id INT,
    candidato_id INT,
    tipo ENUM('VALIDO', 'BRANCO', 'NULO') NOT NULL,
    data_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (eleitor_id) REFERENCES eleitores(id),
    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) );
    
INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso, is_mesario) 
VALUES ('Matheus Mesario', '12345678901', '1010', 'admin123', TRUE);

INSERT INTO candidatos (nome, numero, partido) VALUES ('Candidato A', 11, 'Partido 1');
INSERT INTO candidatos (nome, numero, partido) VALUES ('Candidato B', 22, 'Partido 2');

