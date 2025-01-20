import os


def get_env_var_int(var_name) -> int | None:

    try:
        value = os.getenv(var_name)
        if value is None:
            print(f"La variabile d'ambiente {var_name} non è impostata")
            return None
        return int(value)
    except ValueError:
        print(f"Non posso convertire la variabile di ambiente '{var_name}'")
        return None


def job_cost(
    time_limit: int,
    num_gpu: int,
    num_cpu: int,
    gpu_coefficient: float = 100.0,
    cpu_coefficient: float = 10.0,
) -> float:
    job_cost = time_limit * (num_gpu * gpu_coefficient + num_cpu * cpu_coefficient)
    return job_cost
