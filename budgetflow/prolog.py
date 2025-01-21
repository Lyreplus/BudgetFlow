from utils.database_utils import (
    find_progetto_by_id,
    is_user_in_project,
    execute_query,
    database_init,
)
from utils.utils import job_cost
import sys
import psycopg2
import os
import json
from typing import List, Tuple


def slurm_init() -> None:
    return


def slurm_fini() -> None:
    return


"""
@:param time_limit: 
@:param user_id: the user that submit the job
@:param progetto_id: the project id
@:param job_id: the job id
@:return: True if the job can be submitted, False otherwise
"""


def job_submit_filter(
    job_cost: float, progetto_id: str, job_id: str
) -> Tuple[bool, str]:
    # enough budget ?
    query: str = "SELECT * FROM Budget WHERE progetto_id = %s AND tempo_fine IS NULL"
    records: List = execute_query(query, progetto_id)
    if len(records) == 0:
        return False, "Project has no budget"
    budget: float = float(records[0][2])

    if budget < job_cost:
        return False, "Project has not enough budget"
    else:

        # add job to database
        query = "INSERT INTO Job (costo_submit, job_id_slurm) VALUES (%s, %s) RETURNING job_id"
        job_id = execute_query(query, (time_limit, job_id))[0][0]
        return True, ""


def check_resources(max_nodes, num_tasks, cpus_per_task, num_gpu, num_cpu):
    # TODO: check if the request resources are available
    return


if __name__ == "__main__":
    time_limit: int = int(sys.argv[1])
    user_id: str = str(sys.argv[2])
    max_nodes: int = int(sys.argv[3])
    num_tasks: int = int(sys.argv[4])
    cpus_per_task: int = int(sys.argv[5])
    num_gpu: int = int(sys.argv[6])
    num_cpu: int = int(sys.argv[7])
    database_init()

    # if the env var SLURM_JOB_ID isn't defined return error
    job_id: int = int(os.getenv("SLURM_JOB_ID", -1))
    if job_id == -1:
        print("Job id not found")
        sys.exit(1)

    # check to which project the user belongs
    project_list: List = execute_query(
        "SELECT progetto_id FROM Progetto_Utenti WHERE user_id = %s", (user_id)
    )
    if len(project_list) == 0:
        print("Utente non autorizzato")
        sys.exit(1)
    print("Inserisci l'id del progetto")

    # select the project, make sure the project is valid
    progetto_id: str = str(input())

    if progetto_id not in project_list:
        print("Progetto non valido")
        sys.exit(1)

    progetto = find_progetto_by_id(progetto_id)
    if not is_user_in_project(user_id, progetto_id):
        print("Utente non autorizzato")
        sys.exit(1)

    # job detail file creation
    file_name: str = "job_" + str(job_id) + ".txt"
    try:
        file = open(file_name, "x")
    except FileExistsError:
        print("Il job inviato ha un id non valido")

    with open(file_name, "w") as file:
        job_data = {"job_id:": job_id, "num_gpu": num_gpu, "num_cpu": num_cpu}
        json.dump(job_data, file, indent=4)

    job_c = job_cost(time_limit, num_gpu, num_cpu)
    result, msg = job_submit_filter(job_c, progetto_id, str(job_id))
    if not result:
        print(msg)
        sys.exit(1)
    sys.exit(0)
