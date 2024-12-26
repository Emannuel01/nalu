ALTER TABLE pacientes
ADD COLUMN endereco VARCHAR(255);

ALTER TABLE medicos
ADD COLUMN email VARCHAR(100),
ADD COLUMN telefone VARCHAR(20);

ALTER TABLE prontuarios
ADD COLUMN exames TEXT,
ADD COLUMN diagnosticos TEXT,
ADD COLUMN tratamentos TEXT,
ADD COLUMN evolucao_clinica TEXT;

