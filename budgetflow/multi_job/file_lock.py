from filelock import FileLock
import time

lock_file = "script.lock"

# Lock con timeout personalizzato
lock = FileLock(lock_file)

print("Tentativo di acquisire il lock...")

# Acquisisce il lock, aspettando se necessario
with lock:
    print("Lock acquisito. Script in esecuzione.")
    # Codice del plugin
    #
    # -----------------
    print("Lavoro completato. Lock rilasciato.")

print("Script terminato.")
