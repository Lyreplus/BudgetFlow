function slurm_job_submit(job_desc, part_list, submit_uid)
    if (job_desc.max_nodes == nil or job_desc.max_nodes > 10000) --[[ magic number, can be fixed by adding here the sum of nodes by reading the slurm.conf or by the output of slurm commands such as sinfo--]]
    then
        slurm.user_msg("define number of node to use with -N <n> or --nodelist=<NodeName1>,<NodeName2>")
        return slurm.ERROR
    end

    if (job_desc.num_tasks == nil or job_desc.num_tasks > 10000)
    then
        slurm.user_msg("define number of tasks with -n <n> o --ntasks=<n> or set the environment variable SLURM_NTASKS")
        return slurm.ERROR
    end

    if (job_desc.cpus_per_task == nil or job_desc.cpus_per_task > 10000)
    then
        slurm.user_msg("define number of CPU per task with --cpus-per-task=<n>")
        return slurm.ERROR
    end

    if (job_desc.gres == nil)
    then
        slurm.user_msg("define GPU request. If you don't need any GPU use '--gres=gpu:0'")
        return slurm.ERROR
    else
        --slurm.user_msg("#else:" ..tostring(job_desc.gres) ..type(job_desc.gres))
        a, num_gpu = string.match(job_desc.gres, "gpu:(.*)(%d+)")
        num_gpu = tonumber(num_gpu)
        --slurm.user_msg("dbg num_gpu: " ..tostring(num_gpu) ..type(num_gpu))
    end

    num_cpu = job_desc.num_tasks * job_desc.cpus_per_task
    --slurm.user_msg("dbg num_cpu:" ..tostring(num_cpu))

    if (num_gpu == 0)
    then
        if (num_cpu > 8)
        then
            slurm.user_msg("Without GPU you can't request more than 8 CPU")
            return slurm.ERROR
        end
    else
        ratio = num_cpu / num_gpu
        if (ratio > 12)
        then
            slurm.user_msg("You can't ask more than 12 CPU per GPU")
            return slurm.ERROR
        end
    end

    --begin calling to budgetflow plugin

    time_limit = job_desc.time_limit
    user_id = submit_uid

    cmd = string.format("python3 ../budgetflow/prolog.py %d %d %d %d %d %d %d", time_limit, user_id, job_desc.max_nodes,
        job_desc.num_tasks,
        job_desc.cpus_per_task,
        num_gpu, num_cpu)
    handle = io.popen(cmd)
    result = handle:read("*a")
    success, msg = handle:close()

    if not success then
        slurm.log_user("Job rejected: " .. result)
        return slurm.ERROR
    end

    return slurm.SUCCESS
end

function slurm_job_modify(j, p, s)
    return slurm.SUCCESS
end
