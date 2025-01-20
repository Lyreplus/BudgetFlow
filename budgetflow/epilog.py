from utils.utils import get_env_var_int, job_cost
from utils import database_utils as dbutil
import utils as utils
import os
import sys
import json
from typing import Tuple


def get_job_id() -> int:
    job_id_slurm = os.getenv("SLURM_JOB_ID")
    query = "SELECT job_id FROM Job WHERE job_id_slurm = %s"
    job_id = dbutil.execute_query(query, (job_id_slurm,))
    if len(job_id) == 0:
        return -1
    return job_id[0][0]


def read_resource_coefficients() -> Tuple[float | None, float | None, float | None]:
    try:
        with open("resources_coefficients.txt", "r") as file:
            job_data = json.load(file)
    except FileNotFoundError:
        print("File delle risorse inesistente")
        return None, None, None
    except json.JSONDecodeError as e:
        print(f"Errore nel formato del file JSON delle risorse: {e}")
        return None, None, None
    else:
        if not isinstance(job_data, dict):
            print("Il JSON delle risorse non è un dizionario")
            return None, None, None

        gpu_cost = job_data.get("gpu_cost", None)
        cpu_cost = job_data.get("cpu_cost", None)
        ram_cost = job_data.get("ram_cost", None)

        return gpu_cost, cpu_cost, ram_cost


def execute_payment(job_id: int, expected_time: int) -> None:
    start_time = get_env_var_int("SLURM_JOB_START_TIME")
    end_time = get_env_var_int("SLURM_JOB_END_TIME")

    budget = 0
    cost = 0

    # TODO  decide if budget in db should be a float or a bigint, in the last case normalize to int the cost and the budget variable

    # TODO  possibly change db structure? not useful if tempo fine and tempo inizio is in progetto and also in budget. maybe
    # join budget into Progetto

    # TODO create a intermediate table Job_Progetto that links each job to each project, to solve the problem that one user
    # can send a job, but that user could be a member of different projects and in this way isn't clear for which project is+
    # running the job

    # search budget
    query = "SELECT amount FROM Budget WHERE progetto_id = (SELECT progetto_id FROM Job WHERE job_id = %s) AND tempo_fine IS NULL"
    budget = dbutil.execute_query(query, (job_id))
    if budget is None or len(budget) == 0:
        print("Budget not found")
        return

    budget_float = float(budget[0][0])

    if expected_time == 0:
        print("Expected time not found")
        return

    # job finished
    if end_time is None or start_time is None:
        print(
            "Le variabili del tempo di inizio o di fine del job non sono inizializzate"
        )
        return

    actual_time = end_time - start_time
    if actual_time == 0:
        print("Job hasn't started")
        if expected_time != actual_time:
            # query = "INSERT INTO Job (costo_submit, costo_effettivo, job_id_slurm) VALUES (%s, %s, %s)"
            # dbutil.execute_query(query, (expected_time, actual_time, job_id))

            # TODO check the resource requested by the job by asking the database
            file_name = "job_" + str(job_id) + ".txt"
            try:
                with open(file_name, "r") as file:
                    job_data = json.load(file)
            except FileNotFoundError:
                print("File con dettagli job inesistente")
            except json.JSONDecodeError:
                print("Errore nel formato del file JSON dei dettagli del job")
            else:
                # TODO  la ram è da inserire nella formula ?
                gpu_cost, cpu_cost, ram_cost = read_resource_coefficients()
                # TODO crea formula per il costo e moltiplica i coefficienti per quantità risorse utilizzate
                num_gpu_req = job_data.get("num_gpu", None)
                num_cpu_req = job_data.get("num_cpu", None)
                if num_gpu_req is None or num_cpu_req is None:
                    print("Numero di GPU o CPU non trovato")
                    return
                # TODO definire formula costo: deve essere coefficiente risorsa per numero risorsa richiesta per tempo?
                # deve essere calcolata diversamente
                # TODO definire nel dettaglio se il budget è solo risorsa*num_risorsa richiesta o c'è anche il tempo
                # e com'è presente nella formula

                # cost = gpu_cost * num_gpu_req + cpu_cost * num_cpu_req
                if gpu_cost is None or cpu_cost is None:
                    print(
                        "Il coefficiente di costo della gpu o della cpu non è inizializzato (None)"
                    )
                    return
                job_cost(actual_time, num_gpu_req, num_cpu_req, gpu_cost, cpu_cost)

    # TODO: implement payment calculation
    budget_remaining = budget_float - cost
    # query = "UPDATE Budget SET amount = %s WHERE progetto_id = %s AND tempo_fine IS NULL"
    # dbutil.execute_query(query, (budget, progetto_id))

    return


def end_job(job_id: int) -> Tuple[int, int]:
    exit_code = os.getenv("SLURM_EXIT_CODE", -1)
    # TODO  test this query
    expected_time = dbutil.execute_query(
        "SELECT costo_submit FROM Job WHERE job_id_slurm = %s", (job_id)
    )
    if expected_time is None or len(expected_time) == 0:
        print("Expected time not found")
        return 0, -1
    if len(expected_time) > 1:
        print("Error: multiple jobs with the same job_id_slurm")
        return 0, -1
    if exit_code == -1:
        print("Exit code not found")
        return 0, -1
    if exit_code != 0:
        print("Job failed")
        return 0, int(exit_code)
    return expected_time[0][0], 0


if __name__ == "__main__":
    job_id: int = get_job_id()
    if job_id == -1:
        print("Job id not found")
        sys.exit(1)
    end_job_details: Tuple[int, int] = end_job(job_id)
    expected_time: int = end_job_details[0]
    exit_code: int = end_job_details[1]
    if exit_code != 0:
        sys.exit(exit_code)

    execute_payment(job_id, expected_time)
    sys.exit(0)
