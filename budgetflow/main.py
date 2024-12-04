import sys


def slurm_init():
    """Initialize the Slurm API.

    This function must be called first before certain RPC functions can be
    executed. slurm_init is automatically called when the pyslurm module is
    loaded.
    """


def slurm_fini():


def job_submit_filter(job):
    return True, ""


if __name__ == "__main__":
    time_limit = int(sys.argv[1])
    user_id = int(sys.argv[2])
    result, msg = job_submit_filter(time_limit, user_id)
    if not result:
        print(msg)
        sys.exit(1)
    sys.exit(0)
