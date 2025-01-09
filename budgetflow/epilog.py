from utils import database_utils as dbutil
import utils as utils
import os
import sys
import json


def get_job_id():
    job_id_slurm = os.getenv('SLURM_JOB_ID')
    query = "SELECT job_id FROM Job WHERE job_id_slurm = %s"
    job_id = dbutil.execute_query(query, (job_id_slurm,))
    if len(job_id) == 0:
        return None
    return job_id[0][0]

def read_resource_coefficients():
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



def execute_payment(job_id, expected_time):
    # get slurm start and end time
    start_time = utils.utils.get_env_var('SLURM_JOB_START_TIME') 
    end_time =  utils.utils.get_env_var('SLURM_JOB_END_TIME')
    # TODO implement query to get budget
    budget = 0
    cost = 0

    if expected_time == None or len(expected_time) == 0:
        print("Expected time not found")
        return
     
    # job finished
    if start_time is not None and end_time is not None:
        actual_time = end_time - start_time
        
        if expected_time != actual_time:
            # query = "INSERT INTO Job (costo_submit, costo_effettivo, job_id_slurm) VALUES (%s, %s, %s)"
            # dbutil.execute_query(query, (expected_time, actual_time, job_id))
            
            file_name = "job_" + str(job_id) + ".txt"
            try:
                with open(file_name, "r") as file:
                    job_data = json.load(file)
            except FileNotFoundError:
                print("File con dettagli job inesistente")
            except json.JSONDecodeError:
                print("Errore nel formato del file JSON dei dettagli del job")
            else:
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

                cost = gpu_cost * num_gpu_req + cpu_cost * num_cpu_req
                
                if cost is None:
                    cost = 0

    # TODO: implement payment calculation
    budget = budget - cost
    # query = "UPDATE Budget SET amount = %s WHERE progetto_id = %s AND tempo_fine IS NULL"
    # dbutil.execute_query(query, (budget, progetto_id))

    return


def end_job(job_id):
    exit_code = os.getenv('SLURM_EXIT_CODE', -1)
    expected_time = dbutil.execute_query("SELECT costo_submit FROM Job WHERE job_id_slurm = %s", (job_id))
    if expected_time == None or len(expected_time) == 0:
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
        return 0, exit_code
    return expected_time, 0


if __name__ == "__main__":
    job_id = get_job_id()
    expected_time, exit_code = end_job(job_id)
    if exit_code != 0:
        sys.exit(exit_code)
    
    execute_payment(job_id, expected_time)
    sys.exit(0)
        
        

