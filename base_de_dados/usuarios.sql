-- Criação da Tabela de Usuários se ainda não existir
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Adiciona a coluna 'cargo' à tabela 'usuarios' se ainda não existir
-- Verifica se a coluna 'cargo' já existe para evitar erro
DELIMITER //
CREATE PROCEDURE AddCargoColumnIfNeeded()
BEGIN
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'cargo') THEN
        ALTER TABLE usuarios
        ADD COLUMN cargo VARCHAR(100) DEFAULT 'Desenvolvedor(a) Júnior';
    END IF;
END //
DELIMITER ;

CALL AddCargoColumnIfNeeded();
DROP PROCEDURE IF EXISTS AddCargoColumnIfNeeded;


-- Inserção ou Atualização dos Usuários com Cargos e Senhas Numéricas Aleatórias
-- ATENÇÃO: Para fins educacionais, estamos usando senhas em texto puro.
-- EM UM AMBIENTE REAL, SEMPRE HASH AS SENHAS!

-- Limpa a tabela para inserir os novos dados com cargos e senhas atualizadas
TRUNCATE TABLE usuarios;

INSERT INTO usuarios (username, password_hash, cargo) VALUES
('Nicollas Martins', '13122006', 'Técnico em Redes de Computadores'),
('Ricardo Gomes', '11031976', 'Técnico em Redes de Computadores'),
('Ana Silva', '87654321', 'Desenvolvedor(a) Back-end'),
('Bruno Costa', '12345678', 'Cientista de Dados'),
('Carla Dias', '98765432', 'Especialista em Cibersegurança'),
('Daniel Rocha', '34567890', 'Administrador(a) de Redes'),
('Eduarda Lima', '67890123', 'Arquiteto(a) de Software'),
('Felipe Mendes', '21098765', 'Engenheiro(a) de DevOps'),
('Gabriela Nunes', '54321098', 'Designer UX/UI'),
('Hugo Pereira', '90123456', 'Analista de Qualidade (QA)'),
('Isabela Santos', '78901234', 'Especialista em Banco de Dados'),
('Joao Oliveira', '45678901', 'Desenvolvedor(a) Front-end');

-- Selecionar todos os usuários para mostrar o resultado
SELECT * FROM usuarios;
-- OUTPUT GERADO PREVIAMENTE--

+----+------------------+---------------+---------------------+-----------------------------------+
| id | username         | password_hash | created_at          | cargo                             |
+----+------------------+---------------+---------------------+-----------------------------------+
|  1 | Nicollas Martins | 13122006      | 2025-06-19 19:16:58 | Técnico em Redes de Computadores  |
|  2 | Ricardo Gomes    | 11031976      | 2025-06-19 19:16:58 | Técnico em Redes de Computadores  |
|  3 | Ana Silva        | 87654321      | 2025-06-19 19:16:58 | Desenvolvedor(a) Back-end         |
|  4 | Bruno Costa      | 12345678      | 2025-06-19 19:16:58 | Cientista de Dados                |
|  5 | Carla Dias       | 98765432      | 2025-06-19 19:16:58 | Especialista em Cibersegurança    |
|  6 | Daniel Rocha     | 34567890      | 2025-06-19 19:16:58 | Administrador(a) de Redes         |
|  7 | Eduarda Lima     | 67890123      | 2025-06-19 19:16:58 | Arquiteto(a) de Software          |
|  8 | Felipe Mendes    | 21098765      | 2025-06-19 19:16:58 | Engenheiro(a) de DevOps           |
|  9 | Gabriela Nunes   | 54321098      | 2025-06-19 19:16:58 | Designer UX/UI                    |
| 10 | Hugo Pereira     | 90123456      | 2025-06-19 19:16:58 | Analista de Qualidade (QA)        |
| 11 | Isabela Santos   | 78901234      | 2025-06-19 19:16:58 | Especialista em Banco de Dados    |
| 12 | Joao Oliveira    | 45678901      | 2025-06-19 19:16:58 | Desenvolvedor(a) Front-end        |
+----+------------------+---------------+---------------------+-----------------------------------+