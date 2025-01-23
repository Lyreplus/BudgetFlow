import psycopg2
from psycopg2 import sql, OperationalError, connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from typing import List, Tuple, Optional
import re


def find_progetto_by_id(progetto_id: str) -> Optional[List[Tuple]]:
    query = "SELECT * FROM Progetto WHERE progetto_id = %s"
    return execute_query(query, (progetto_id))


def is_user_in_project(user_id, progetto_id) -> bool:
    query = "SELECT * FROM Progetto_Utenti WHERE progetto_id = %s AND user_id = %s"
    result: Optional[List[Tuple]] = execute_query(query, (progetto_id, user_id))
    if not result:
        return False
    if len(result) == 0:
        return False
    return True


def create_database() -> None:
    user: str = os.getenv("DB_USER", "")
    password: str = os.getenv("DB_PASSWORD", "")
    host: str = os.getenv("DB_HOST", "")
    db_name: str = os.getenv("DB_NAME", "")

    try:
        con = connect(dbname=db_name, user=user, host=host, password=password)
    except OperationalError as e:
        if e.args:
            msg = e.args[0]
            m = re.match(r".*database \"(.*)\" does not exist.*", msg, re.IGNORECASE)
            if m and m.endpos == len(msg):
                con = connect(user=user, host=host, password=password)
                # secure the connection
                con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = con.cursor()
                cur.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                )

                print("Database created successfully")

                cur.close()
                con.close()
            else:
                raise
    return


def execute_query(
    query: str, *args, return_output: bool = True
) -> Optional[List[Tuple]]:
    db_name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    pg_connection_dict = {
        "dbname": db_name,
        "user": user,
        "password": password,
        "host": host,
        "port": port,
    }

    conn = psycopg2.connect(**pg_connection_dict)
    cursor = conn.cursor()
    cursor.execute(query, args)
    if return_output:
        try:
            records = cursor.fetchall()
        except psycopg2.ProgrammingError:
            records = None
    else:
        records = None
    conn.commit()
    conn.close()
    cursor.close()
    return records


def database_init() -> None:
    query = """
CREATE TABLE IF NOT EXISTS Progetto (
                progetto_id BIGINT PRIMARY KEY,
                nome TEXT NOT NULL,
                descrizione TEXT NOT NULL,
                tempo_inizio TIMESTAMP NOT NULL,
                tempo_fine TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Utenti (
                user_id TEXT PRIMARY KEY,
                user_name TEXT
);

CREATE TABLE IF NOT EXISTS Budget (
                id SERIAL PRIMARY KEY,
                progetto_id BIGINT NOT NULL REFERENCES Progetto(progetto_id) ON DELETE CASCADE,
                amount BIGINT NOT NULL,
                tempo_inizio TIMESTAMP NOT NULL,
                tempo_fine TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS budget_tempo_fine
ON Budget (progetto_id)
WHERE tempo_fine IS NOT NULL;

CREATE TABLE IF NOT EXISTS Job(
                job_id BIGSERIAL PRIMARY KEY,
                costo_submit BIGINT NOT NULL,
                costo_effettivo BIGINT,
                job_id_slurm BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Risorse(
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                peso DECIMAL(5, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Ruolo (
                            id_ruolo INT NOT NULL PRIMARY KEY,
                            nome TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Utenti_Ruoli (
                id SERIAL PRIMARY KEY,
                utente_id TEXT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE,
                ruolo_id INT NOT NULL REFERENCES Ruolo(id_ruolo) ON DELETE CASCADE,
                UNIQUE (utente_id, ruolo_id)
);

CREATE TABLE IF NOT EXISTS Job_Risorse (
                id SERIAL PRIMARY KEY,
                job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
                risorsa_id INT NOT NULL REFERENCES Risorse(id) ON DELETE CASCADE,
                quantita_richiesta DECIMAL(10,2) NOT NULL,
                quantita_consumata DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS Job_Utenti (
                id BIGSERIAL PRIMARY KEY,
                job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
                user_id TEXT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Progetto_Utenti (
                id SERIAL PRIMARY KEY,
                progetto_id BIGINT NOT NULL REFERENCES Progetto(progetto_id) ON DELETE CASCADE,
                user_id TEXT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Transactions (
                id SERIAL PRIMARY KEY,
                job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
                user_id TEXT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE,
                amount BIGINT NOT NULL,
                tempo TIMESTAMP NOT NULL
);
        """
    execute_query(query)
    return
