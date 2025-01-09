from utils.database_utils import find_progetto_by_id, is_user_in_project, execute_query
import sys
import psycopg2
import os
import json
import pyslurm


def slurm_init():
    """Initialize the Slurm API.

    This function must be called first before certain RPC functions can be
    executed. slurm_init is automatically called when the pyslurm module is
    loaded.
    """


def slurm_fini():
    return


def job_submit_filter(time_limit, user_id, progetto_id, job_id):
    # enough budget ?
    query = "SELECT * FROM Budget WHERE progetto_id = %s AND tempo_fine IS NULL"
    records = execute_query(query, (progetto_id,))
    if len(records) == 0:
        return False, "Project has no budget"
    budget = records[0][2]
    # check if the project has enough budget
    # TODO  change this if, the budget might not been based only on time but more on a function 
    # of the resource coefficient for the requested resource
    if budget < time_limit:
        return False, "Project has not enough budget"
    else:

        # add job to database
        query = "INSERT INTO Job (costo_submit, job_id_slurm) VALUES (%s, %s) RETURNING job_id"
        job_id = execute_query(query, (time_limit, job_id))[0][0]
        return True, ""


def check_resources(max_nodes, num_tasks, cpus_per_task, num_gpu, num_cpu):
    # TODO: check if the request resources are available
    return

def database_init():
    query = """
        CREATE TABLE IF NOT EXISTS Progetto (
                progetto_id BIGINT PRIMARY KEY,
                nome TEXT NOT NULL,
                descrizione TEXT NOT NULL,
                tempo_inizio TIMESTAMP NOT NULL,
                tempo_fine TIMESTAMP
                );

        CREATE TABLE IF NOT EXISTS Utenti (
                user_id BIGINT PRIMARY KEY,
                user_name TEXT
                );

        CREATE TABLE IF NOT EXISTS Budget (
                id SERIAL PRIMARY KEY,
                progetto_id BIGINT NOT NULL REFERENCES Progetto(progetto_id) ON DELETE CASCADE,
                amount BIGINT NOT NULL,
                tempo_inizio TIMESTAMP NOT NULL,
                tempo_fine TIMESTAMP,
                );

        CREATE UNIQUE INDEX budget_tempo_fine
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
                utente_id BIGINT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE,
                ruolo_id INT NOT NULL REFERENCES Ruolo(id_ruolo) ON DELETE CASCADE,
                UNIQUE (utente_id, ruolo_id)
                );

        CREATE TABLE IF NOT EXISTS Job_Risorse (
                id SERIAL PRIMARY KEY,
                job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
                risorsa_id INT NOT NULL REFERENCES Risorse(id) ON DELETE CASCADE,
                quantita_richiesta DECIMALS(10,2) NOT NULL,
                quantita_consumata DECIMALS(10,2)
                );

        CREATE TABLE IF NOT EXISTS Job_Utenti (
                id BIGSERIAL PRIMARY KEY,
                job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
                user_id BIGINT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE
                );

        CREATE TABLE IF NOT EXISTS Progetto_Utenti (
                id SERIAL PRIMARY KEY,
                progetto_id BIGINT NOT NULL REFERENCES Progetto(progetto_id) ON DELETE CASCADE,
                user_id BIGINT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE
                );

        CREATE TABLE IF NOT EXISTS Transactions (
                id SERIAL PRIMARY KEY,
                job_id BIGINT NOT NULL REFERENCES Job(job_id) ON DELETE CASCADE,
                user_id BIGINT NOT NULL REFERENCES Utenti(user_id) ON DELETE CASCADE,
                amount BIGINT NOT NULL,
                tempo TIMESTAMP NOT NULL
                );
        """
    conn = psycopg2.connect("dbname=BudgetFlow user=postgres")
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    return


if __name__ == "__main__":
    time_limit = int(sys.argv[1])
    user_id = int(sys.argv[2])
    max_nodes = int(sys.argv[3])
    num_tasks = int(sys.argv[4])
    cpus_per_task = int(sys.argv[5])
    num_gpu = int(sys.argv[6])
    num_cpu = int(sys.argv[7])
    
    job_id = int(os.getenv('SLURM_JOB_ID', -1))
    if job_id == -1:
        print("Job id not found")
        sys.exit(1)

    print("Inserisci l'id del progetto")
    progetto_id = int(input())
    progetto = find_progetto_by_id(progetto_id)
    if len(progetto) == 0:
        print("Progetto non trovato")
        sys.exit(1)
    if not is_user_in_project(user_id, progetto_id):
        print("Utente non autorizzato")
        sys.exit(1)

    # job detail file creation
    file_name = "job_" + str(job_id) + ".txt"
    try:
        file = open(file_name, "x")
    except FileExistsError:
        print("Il job inviato ha un id non valido")


    with open(file_name, "w") as file:
        job_data = {
                "job_id:" : job_id,
                "num_gpu" : num_gpu,
                "num_cpu" : num_cpu
        }
        json.dump(job_data,file,indent=4)

    result, msg = job_submit_filter(time_limit, user_id, progetto_id, job_id)
    if not result:
        print(msg)
        sys.exit(1)
    sys.exit(0)
