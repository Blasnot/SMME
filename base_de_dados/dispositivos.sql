-- Criação da Tabela de Dispositivos se ainda não existir
CREATE TABLE IF NOT EXISTS dispositivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    setor VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    endereco_ip VARCHAR(45) UNIQUE, -- IPv4 ou IPv6
    gasto_energia_watts DECIMAL(10, 2), -- Gasto de energia em Watts (ex: 100.50)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserção de Dispositivos de Exemplo
INSERT INTO dispositivos (nome, setor, tipo, endereco_ip, gasto_energia_watts) VALUES
('Servidor Web 01', 'Infraestrutura', 'Servidor', '192.168.1.10', 350.75),
('Estação de Trabalho RH', 'Recursos Humanos', 'Computador', '192.168.1.11', 120.00),
('Impressora Colorida', 'Administrativo', 'Impressora', '192.168.1.12', 60.50),
('Switch Principal', 'Redes', 'Equipamento de Rede', '192.168.1.1', 80.20),
('Câmera de Segurança 01', 'Segurança', 'Câmera IP', '192.168.1.13', 15.00),
('Notebook Desenvolvedor', 'Desenvolvimento', 'Notebook', '192.168.1.14', 45.00),
('Access Point Andar 2', 'Redes', 'Access Point', '192.168.1.20', 25.00),
('Servidor Banco de Dados', 'Infraestrutura', 'Servidor', '192.168.1.25', 400.00),
('Telefone VoIP Recepção', 'Administrativo', 'Telefone IP', '192.168.1.30', 10.00),
('Monitor de Vídeo Grande', 'Marketing', 'Monitor', NULL, 70.00); -- Exemplo sem IP, se aplicável

-- Selecionar todos os dispositivos para mostrar o resultado
SELECT * FROM dispositivos;

-- OUTPUT GERADO PREVIAMENTE--

+----+--------------------------+------------------+---------------------+--------------+---------------------+---------------------+
| id | nome                     | setor            | tipo                | endereco_ip  | gasto_energia_watts | created_at          |
+----+--------------------------+------------------+---------------------+--------------+---------------------+---------------------+
|  1 | Servidor Web 01          | Infraestrutura   | Servidor            | 192.168.1.10 |              350.75 | 2025-06-19 19:22:01 |
|  2 | Estação de Trabalho RH   | Recursos Humanos | Computador          | 192.168.1.11 |              120.00 | 2025-06-19 19:22:01 |
|  3 | Impressora Colorida      | Administrativo   | Impressora          | 192.168.1.12 |               60.50 | 2025-06-19 19:22:01 |
|  4 | Switch Principal         | Redes            | Equipamento de Rede | 192.168.1.1  |               80.20 | 2025-06-19 19:22:01 |
|  5 | Câmera de Segurança 01   | Segurança        | Câmera IP           | 192.168.1.13 |               15.00 | 2025-06-19 19:22:01 |
|  6 | Notebook Desenvolvedor   | Desenvolvimento  | Notebook            | 192.168.1.14 |               45.00 | 2025-06-19 19:22:01 |
|  7 | Access Point Andar 2     | Redes            | Access Point        | 192.168.1.20 |               25.00 | 2025-06-19 19:22:01 |
|  8 | Servidor Banco de Dados  | Infraestrutura   | Servidor            | 192.168.1.25 |              400.00 | 2025-06-19 19:22:01 |
|  9 | Telefone VoIP Recepção   | Administrativo   | Telefone IP         | 192.168.1.30 |               10.00 | 2025-06-19 19:22:01 |
| 10 | Monitor de Vídeo Grande  | Marketing        | Monitor             | NULL         |               70.00 | 2025-06-19 19:22:01 |
+----+--------------------------+------------------+---------------------+--------------+---------------------+---------------------+