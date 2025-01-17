import fcntl
import os
import sys

# Nome del file di lock
lock_file = "/tmp/script.lock"

def main():
    print("Tentativo di acquisire il lock...")

    # Apri il file di lock in modalità append
    with open(lock_file, "w") as lockfile:
        try:
            # Lock esclusivo (bloccante)
            fcntl.flock(lockfile, fcntl.LOCK_EX)
            print("Lock acquisito. Script in esecuzione.")

            # codice del plugin
            #
            # -----------------
            print("Lavoro completato.")

        except BlockingIOError:
            print("Un'altra istanza dello script è già in esecuzione.")
            sys.exit(1)

        finally:
            # Rilascia il lock (non strettamente necessario: accade automaticamente con la chiusura del file)
            fcntl.flock(lockfile, fcntl.LOCK_UN)

    print("Script terminato.")

if __name__ == "__main__":
    main()
