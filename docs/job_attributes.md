##
# Attributi di `job_ptr`

## Stringhe
- `account`
- `admin_comment`
- `alloc_node`
- `batch_features`
- `batch_host`
- `burst_buffer`
- `comment`
- `container`
- `cpus_per_tres`
- `extra`
- `features`
- `gres`
- `gres_req`
- `gres_used`
- `licenses`
- `mcs_label`
- `mem_per_tres`
- `name`
- `nodes`
- `origin_cluster`
- `partition`
- `qos` (da `qos_ptr->name`)
- `resv_name`
- `selinux_context`
- `spank_job_env` (tabella con valori stringa)
- `std_err` (da `details`)
- `std_in` (da `details`)
- `std_out` (da `details`)
- `tres_alloc_str`
- `tres_bind`
- `tres_fmt_alloc_str`
- `tres_fmt_req_str`
- `tres_freq`
- `tres_per_job`
- `tres_per_node`
- `tres_per_socket`
- `tres_per_task`
- `tres_req_str`
- `user_name`
- `wckey`
- `work_dir` (da `details`)

## Numerici
- `array_job_id`
- `array_task_cnt` (da `array_recs->task_cnt`)
- `array_task_id`
- `best_switch`
- `delay_boot`
- `derived_ec`
- `direct_set_prio`
- `end_time`
- `exit_code`
- `group_id`
- `het_job_id` (alias: `pack_job_id`)
- `het_job_id_set` (alias: `pack_job_id_set`)
- `het_job_offset` (alias: `pack_job_offset`)
- `job_id`
- `job_state`
- `max_cpus` (da `details`)
- `max_nodes` (da `details`)
- `min_cpus` (da `details`)
- `min_mem_per_node` (da `details`)
- `min_mem_per_cpu` (da `details`)
- `min_nodes` (da `details`)
- `nice` (da `details`)
- `pn_min_cpus` (da `details`)
- `pn_min_memory` (da `details`)
- `priority`
- `reboot`
- `req_switch`
- `resizing` (calcolato)
- `restart_cnt`
- `site_factor`
- `spank_job_env_size`
- `start_time`
- `submit_time` (da `details`)
- `time_limit`
- `time_min`
- `total_cpus`
- `total_nodes`
- `user_id`
- `wait4switch`
- `wait4switch_start`

## Tabelle
- `argv` (da `details->argv`, tabella)
- `spank_job_env` (tabella con indice e stringhe)

## Note
- **Attributi derivati da `details`:** Alcuni attributi (es. `std_err`, `work_dir`, ecc.) vengono presi dalla struttura collegata `job_ptr->details`.
- **Alias:** Alcuni attributi sono accessibili con più nomi (es. `pack_job_id` è un alias di `het_job_id`).

# Attributi di `job_desc` (job_desc_msg_t)

## Stringhe (string)
- `account`
- `acctg_freq`
- `admin_comment`
- `alloc_node`
- `argv` (array di stringhe)
- `array_inx`
- `assoc_comment`
- `assoc_qos`
- `batch_features`
- `burst_buffer`
- `clusters`
- `comment`
- `container`
- `cpus_per_tres`
- `default_account`
- `default_qos`
- `dependency`
- `environment`
- `exc_nodes`
- `extra`
- `features`
- `gres`
- `licenses`
- `mail_user`
- `mcs_label`
- `mem_per_tres`
- `network`
- `qos`
- `reboot`
- `req_context`
- `req_nodes`
- `reservation`
- `script`
- `selinux_context`
- `spank_job_env` (array di stringhe)
- `std_err`
- `std_in`
- `std_out`
- `tres_bind`
- `tres_freq`
- `tres_per_job`
- `tres_per_node`
- `tres_per_socket`
- `tres_per_task`
- `user_name`
- `work_dir`
- `wckey`

## Interi (integer)
- `argc`
- `bitflags`
- `boards_per_node`
- `begin_time`
- `contiguous`
- `cores_per_socket`
- `cpu_freq_min`
- `cpu_freq_max`
- `cpu_freq_gov`
- `cpus_per_task`
- `cron_job` (booleano, ma gestito come intero)
- `delay_boot`
- `group_id`
- `immediate`
- `mail_type`
- `max_cpus`
- `max_nodes`
- `min_cpus`
- `min_nodes`
- `nice`
- `ntasks_per_board`
- `ntasks_per_core`
- `ntasks_per_gpu`
- `ntasks_per_node`
- `ntasks_per_socket`
- `ntasks_per_tres`
- `num_tasks`
- `pack_job_offset`
- `het_job_offset`
- `pn_min_cpus`
- `pn_min_memory`
- `pn_min_tmp_disk`
- `priority`
- `requeue`
- `req_switch`
- `shared` (booleano, ma gestito come intero)
- `site_factor`
- `sockets_per_board`
- `sockets_per_node`
- `spank_job_env_size`
- `threads_per_core`
- `time_limit`
- `time_min`
- `user_id`
- `wait4switch`

## Booleani (boolean)
- `cron_job`
- `shared` (sebbene trattato come intero, rappresenta un valore booleano)
- `oversubscribe` (trattato come booleano)

## Numeri (float, double, long, ecc.)
- `site_factor` (gestito come valore long, con offset per NICE)
- `begin_time` (potrebbe essere gestito come valore temporale, tipo long)
- `time_limit` (tempo limite, float o long)
- `time_min` (tempo minimo, float o long)


