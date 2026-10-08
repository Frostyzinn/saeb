-- Base de demonstração do SAEP. Importar em banco novo; não remove dados existentes.
CREATE DATABASE IF NOT EXISTS saep_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE saep_db;
CREATE TABLE usuario (idusuario INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL) ENGINE=InnoDB;
CREATE TABLE produtos (id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100) NOT NULL, marca VARCHAR(60) NOT NULL, modelo VARCHAR(60) NOT NULL, material VARCHAR(60) NOT NULL, tamanho VARCHAR(30) NOT NULL, peso DECIMAL(8,2) NOT NULL, tensao VARCHAR(30) NOT NULL, estoque INT NOT NULL DEFAULT 0, estoque_minimo INT NOT NULL DEFAULT 0) ENGINE=InnoDB;
CREATE TABLE movimentacoes (id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, produto_id INT UNSIGNED NOT NULL, usuario_id INT UNSIGNED NOT NULL, tipo ENUM('entrada','saida') NOT NULL, quantidade INT NOT NULL, data_movimentacao DATE NOT NULL, FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT ON UPDATE CASCADE, FOREIGN KEY (usuario_id) REFERENCES usuario(idusuario) ON DELETE RESTRICT ON UPDATE CASCADE) ENGINE=InnoDB;
INSERT INTO usuario (idusuario, name, email, password) VALUES (1, 'Administrador', 'admin@teste.com', '$2y$10$5vL/0R8uFehTEJcUvA5u3.dZ4sxWe1lmAE6KNI2CTAMQtGGfzu5dK');
INSERT INTO usuario (idusuario, name, email, password) VALUES (2, 'Ana Souza', 'ana@teste.com', '$2y$10$5vL/0R8uFehTEJcUvA5u3.dZ4sxWe1lmAE6KNI2CTAMQtGGfzu5dK');
INSERT INTO usuario (idusuario, name, email, password) VALUES (3, 'Carlos Lima', 'carlos@teste.com', '$2y$10$5vL/0R8uFehTEJcUvA5u3.dZ4sxWe1lmAE6KNI2CTAMQtGGfzu5dK');
INSERT INTO produtos (id, nome, marca, modelo, material, tamanho, peso, tensao, estoque, estoque_minimo) VALUES (1, 'Martelo de Borracha', 'Tramontina', 'MB-500', 'Borracha e madeira', '30 cm', '0.50', 'Não se aplica', 12, 5);
INSERT INTO produtos (id, nome, marca, modelo, material, tamanho, peso, tensao, estoque, estoque_minimo) VALUES (2, 'Chave de Fenda Isolada', 'Vonder', 'CF-6', 'Aço e polímero', '20 cm', '0.15', 'Não se aplica', 2, 4);
INSERT INTO produtos (id, nome, marca, modelo, material, tamanho, peso, tensao, estoque, estoque_minimo) VALUES (3, 'Alicate Universal', 'Gedore', 'AU-8', 'Aço', '8 polegadas', '0.30', 'Não se aplica', 8, 3);
INSERT INTO produtos (id, nome, marca, modelo, material, tamanho, peso, tensao, estoque, estoque_minimo) VALUES (4, 'Furadeira de Impacto', 'Bosch', 'GSB-550', 'Aço e plástico', '25 cm', '1.80', '220V', 0, 2);
INSERT INTO movimentacoes (id, produto_id, usuario_id, tipo, quantidade, data_movimentacao) VALUES (1, 1, 1, 'entrada', 12, '2026-01-15');
INSERT INTO movimentacoes (id, produto_id, usuario_id, tipo, quantidade, data_movimentacao) VALUES (2, 2, 2, 'entrada', 2, '2026-01-15');
INSERT INTO movimentacoes (id, produto_id, usuario_id, tipo, quantidade, data_movimentacao) VALUES (3, 3, 3, 'entrada', 8, '2026-01-15');
