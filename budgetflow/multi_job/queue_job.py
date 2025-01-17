import queue
from threading import Thread

job_queue = queue.Queue()

def worker():
    while True:
        job_id = job_queue.get()
        if job_id is None:
            break
        # job_esecution
        fetch_and_save_job_details(job_id)
        job_queue.task_done()

# Aggiungi i job alla coda
for job_id in job_ids:
    job_queue.put(job_id)

# Avvia i worker
threads = []
for _ in range(5):  # Numero di thread worker
    t = Thread(target=worker)
    t.start()
    threads.append(t)

# Attendi il completamento
job_queue.join()
