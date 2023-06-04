/* SQL Export using CockroachDB SQL Migration Tool */

-- Statement 1
SET default_int_size = 8;

-- Statement 2
CREATE TABLE users (
	id VARCHAR(255) PRIMARY KEY,
	nome_completo VARCHAR(255),
	genero VARCHAR(255) NOT NULL,
	cpf VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	data_nascimento DATE NOT NULL,
	senha VARCHAR(255) NOT NULL,
	preferencia_comunicacao VARCHAR(255) NOT NULL,
	cep VARCHAR(255) NOT NULL,
	telefone VARCHAR(255) NOT NULL,
	endereco VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL
);

-- Statement 3
CREATE TABLE dados_bancarios_pagamento (
	id VARCHAR(255) PRIMARY KEY,
	nome_titular VARCHAR(255) NOT NULL,
	data_nasc DATE NOT NULL,
	numero_cartao VARCHAR(255) NOT NULL,
	data_validade DATE NOT NULL,
	user_id VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL
);

-- Statement 4
CREATE TABLE dados_bancarios_recebimento (
	id VARCHAR(255) PRIMARY KEY,
	conta_corrente VARCHAR(255) NOT NULL,
	banco VARCHAR(255) NOT NULL,
	agencia INT NOT NULL,
	user_id VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL
);

-- Statement 5
ALTER TABLE dados_bancarios_pagamento
	ADD FOREIGN KEY (user_id) REFERENCES users (id);

-- Statement 6
ALTER TABLE dados_bancarios_recebimento
	ADD FOREIGN KEY (user_id) REFERENCES users (id);