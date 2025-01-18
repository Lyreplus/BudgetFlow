import os


def get_env_var_int(var_name):
    
    try:
        value = os.getenv(var_name)
        if value is None:
            print(f"La variabile d'ambiente {var_name} non è impostata")
            return None
        return int(value)
    except ValueError:
        print(f"Non posso convertire la variabile di ambiente '{var_name}'")
        return None

