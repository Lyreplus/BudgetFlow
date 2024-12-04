# Relational (PostgreSQL) Database

```postgresql
CREATE TABLE Progetto (
    progetto_id BIGINT PRIMARY KEY (Esiste???),
    nome TEXT NOT NULL,
    descrizione TEXT NOT NULL,
    tempo_inizio TIMESTAMP NOT NULL,
    tempo_fine TIMESTAMP
);

CREATE TABLE Utenti (
    user_id BIGINT PRIMARY KEY,
    user_name TEXT
);

CREATE TABLE Budget (
    id SERIAL PRIMARY KEY,
    progetto_id BIGINT NOT NULL REFERENCES Progetto(progetto_id) ON DELETE CASCADE,
    amount BIGINT NOT NULL,
    tempo_inizio TIMESTAMP NOT NULL,
    tempo_fine TIMESTAMP,
);

CREATE UNIQUE INDEX budget_tempo_fine
ON Budget (progetto_id)
WHERE tempo_fine IS NOT NULL;

CREATE TABLE Job(
    job_id BIGSERIAL PRIMARY KEY,
    costo_submit BIGINT NOT NULL,
    costo_effettivo BIGINT,
    job_id_slurm BIGINT NOT NULL //(?? c'è già job id)
);

CREATE TABLE Risorse(
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    peso DECIMAL(5, 2) NOT NULL
);

CREATE TABLE Ruolo ( 
    id_ruolo INT NOT NULL PRIMARY KEY,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE Utenti_Ruoli (
    id SERIAL PRIMARY KEY,
    utente_id BIGINT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE,
    ruolo_id INT NOT NULL REFERENCES Ruolo(id_ruolo) ON DELETE CASCADE,
    UNIQUE (utente_id, ruolo_id) 
);

CREATE TABLE Job_Risorse (
    id SERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
    risorsa_id INT NOT NULL REFERENCES Risorse(id) ON DELETE CASCADE,
    quantita_richiesta DECIMALS(10,2) NOT NULL,
    quantita_consumata DECIMALS(10,2)
);

CREATE TABLE Job_Utenti (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE
);

CREATE TABLE Progetto_Utenti (
    id SERIAL PRIMARY KEY,
    progetto_id BIGINT NOT NULL REFERENCES Progetto(progetto_id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE
);

```
