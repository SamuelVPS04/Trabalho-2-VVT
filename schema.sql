-- Schema de criação do banco de dados e tabela para o Trabalho 3
-- Banco: db_vvt

CREATE DATABASE IF NOT EXISTS db_vvt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_vvt;

CREATE TABLE IF NOT EXISTS codigos_sequenciais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(8) NOT NULL UNIQUE,
    sec INT NOT NULL,
    Grupo CHAR(1) NOT NULL,
    Tipo_Alimento CHAR(1) NOT NULL,
    Pais CHAR(2) NOT NULL,
    CONSTRAINT chk_sec_positivo CHECK (sec > 0),
    CONSTRAINT uq_pais_grupo_sec UNIQUE (Pais, Grupo, sec)
) ENGINE=InnoDB;

INSERT IGNORE INTO codigos_sequenciais (codigo, sec, Grupo, Tipo_Alimento, Pais) VALUES
    ('BRC0001A', 1, 'C', 'A', 'BR'),
    ('BRD0001I', 1, 'D', 'I', 'BR'),
    ('BRA0001K', 1, 'A', 'K', 'BR'),
    ('BRF0001F', 1, 'F', 'F', 'BR'),
    ('BRG0001A', 1, 'G', 'A', 'BR'),
    ('BRC0002A', 2, 'C', 'A', 'BR'),
    ('BRD0002K', 2, 'D', 'K', 'BR'),
    ('BRF0002A', 2, 'F', 'A', 'BR'),
    ('BRC0003C', 3, 'C', 'C', 'BR');
