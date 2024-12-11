from utils.database_utils import find_progetto_by_id, is_user_in_project, execute_query
import os
import sys

def get_job_id():
    job_id_slurm = os.getenv('SLURM_JOB_ID')
    query = "SELECT job_id FROM Job WHERE job_id_slurm = %s"
    job_id = execute_query(query, (job_id_slurm,))
    if len(job_id) == 0:
        return None
    return job_id[0][0]


def execute_payment(job_id):
    query = "SELECT costo_submit FROM Job WHERE job_id = %s"
    costo_submit = execute_query(query, (job_id,))[0][0]

    # TODO: implement payment calculation
    # budget -= time_limit
    # query = "UPDATE Budget SET amount = %s WHERE progetto_id = %s AND tempo_fine IS NULL"
    # execute_query(query, (budget, progetto_id))

    return


def end_job():
    exit_code = os.getenv('SLURM_EXIT_CODE', -1)
    if exit_code == -1:
        print("Exit code not found")
        return -1
    if exit_code != 0:
        print("Job failed")
        return exit_code
    return 0


if __name__ == "__main__":
    job_id = get_job_id()
    exit_code = end_job()
    if exit_code != 0:
        execute_payment(job_id)
        sys.exit(exit_code)
    
    execute_payment(job_id)
    sys.exit(0)
        
        

