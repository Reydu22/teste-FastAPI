CREATE TABLE usuarios(
	id SERIAL PRIMARY KEY,
	nome VARCHAR(100),
	idade INTEGER
);
INSERT INTO usuarios (nome, idade) VALUES ('Gabriel', 18);
SELECT * FROM usuarios;