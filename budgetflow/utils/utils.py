import os


def get_env_var(var_name):
    value = os.getenv(var_name)
    if value is None:
        print(f"La variabile di ambiente '{var_name}' non è impostata.")
        return None
    try:
        return int(value)
    except ValueError:
        print(f"Non posso convertire la variabile di ambiente '{var_name}'")
        return None

