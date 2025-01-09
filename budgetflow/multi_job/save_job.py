from concurrent.futures import ThreadPoolExecutor
import requests

def fetch_and_save_job_details(job_id):
    try:
        url = f"https://your-slurm-server:6820/slurm/v0.0.37/job/{job_id}"
        headers = {"X-SLURM-USER-TOKEN": "your_token_here"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            job_details = response.json()
            # Funzione per salvare nel database
            save_to_database(job_details)
        else:
            print(f"Errore per il job {job_id}: {response.status_code}")
    except Exception as e:
        print(f"Errore durante il fetch del job {job_id}: {e}")

job_ids = [12345, 12346, 12347]  # Esempio di ID jobs simultanei
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(fetch_and_save_job_details, job_ids)

