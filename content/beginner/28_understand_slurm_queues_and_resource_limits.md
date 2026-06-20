## Why this matters to you
The cluster has multiple types of nodes with different capabilities and different rules. Submitting a GPU job to a CPU-only queue wastes your time waiting. Running a massive memory job on a standard node gets it killed. Understanding the queue system ensures your jobs run efficiently and you're a fair resource user — which matters on a shared cluster where your lab colleagues depend on the same resources.

## Available queues (partitions)

### qTRD — Standard CPU nodes
- **Hardware**: Up to 32 CPU cores, up to 768 GB RAM per node
- **Use for**: MATLAB/GIFT ICA, preprocessing with SPM, Python data analysis, general computation
- **Memory rule**: ~24 GB RAM per CPU core maximum. If you request 4 cores, request no more than ~96 GB RAM
- **This is the default queue** for most work

### qTRDGPU — GPU nodes (RTX/A40)
- **Hardware**: NVIDIA RTX or A40 GPUs, plus CPU cores and RAM
- **Use for**: Deep learning training/inference, GPU-accelerated computation
- **GPU request**: `--gres=gpu:1` (or `gpu:2` for multiple GPUs)
- **Fair usage rule**: Leave at least 8 CPUs and 128 GB RAM free for other GPU users. Don't use all the CPU resources on a GPU node for CPU-only work
- **DO NOT run CPU-only jobs here** — use qTRD instead

### qTRDHM — High-memory nodes
- **Hardware**: Up to 1.5 TB RAM, up to 96 CPU cores
- **Use for**: Memory-intensive analyses — large Group ICA runs, whole-brain connectivity matrices, very large datasets
- **Only use when you genuinely need > 768 GB RAM**

### qTRDGPUH / qTRDGPUM / qTRDGPUL — Priority GPU tiers
- **Hardware**: NVIDIA V100 or A100 GPUs — the most powerful GPUs on the cluster
- **H/M/L**: High, Medium, Low priority tiers
- **Use for**: Large-scale deep learning, massive model training
- **CRITICAL**: DO NOT run CPU-only jobs on these nodes. They have expensive GPUs that sit idle when used for CPU work

## Choosing the right queue

| Job type | Recommended queue | Typical resources |
|---|---|---|
| MATLAB/GIFT ICA | qTRD | -c 4 --mem=32G |
| SPM preprocessing | qTRD | -c 2 --mem=16G |
| Python analysis | qTRD | -c 2 --mem=8G |
| PyTorch training | qTRDGPU | -c 4 --gres=gpu:1 --mem=16G |
| Large Group ICA (1000+ subjects) | qTRDHM | -c 16 --mem=256G |
| Production DL training | qTRDGPUH | -c 8 --gres=gpu:1 --mem=32G |
| Quick GPU test | qTRDGPU | -c 2 --gres=gpu:1 --mem=8G |

## Resource limits and time limits
Each queue has maximum limits:

```
$ sinfo -p qTRD -o "%P %l %m %c"       # Max time, memory, CPUs for qTRD
```

Typical limits:
- **qTRD**: Max 48-72 hours, 768 GB RAM
- **qTRDGPU**: Max 24-48 hours
- **qTRDHM**: Max 48 hours, 1.5 TB RAM

If your job exceeds the time limit, SLURM kills it. Always set time limits slightly above your expected runtime. If your analysis takes 10 hours, set `--time=12:00:00`.

## Fair usage rules — be a good cluster citizen

### Resource etiquette
- **Request minimum needed**: Don't request 32 cores and 256 GB of RAM for a Python script that uses 1 core and 2 GB
- **Use appropriate queues**: CPU jobs on qTRD, GPU jobs on qTRDGPU
- **Don't hoard**: If you have 100 array tasks, use `%10` or `%20` to limit concurrency
- **Clean up**: Cancel jobs you don't need anymore. Don't leave idle interactive sessions
- **Check before requesting**: Use `sinfo` to see what's available

### What happens if you violate rules
- Jobs running on the wrong node type may be killed by administrators
- Excessive resource usage may result in priority reduction
- Persistent violations may lead to account restrictions
- You'll get frustrated emails from lab colleagues who can't get their jobs to run

## Monitoring commands

### Check node availability
```
$ sinfo                             # Overview of all partitions
$ sinfo -p qTRD                     # Specific partition
$ sinfo -N -l                       # Detailed node-by-node status
```

Node states:
- **idle**: Available for jobs
- **mixed**: Partially in use
- **alloc**: Fully allocated
- **drain**: Taken offline for maintenance

### Check your jobs
```
$ squeue -u $USER                   # Your running/pending jobs
$ squeue -u $USER --format="%.10i %.9P %.20j %.8u %.2t %.10M %.6D %R"   # More detail
```

### Job history and resource usage
```
$ sacct -u $USER --starttime=2024-01-01    # Jobs since a date
$ sacct -j 12345678 --format=JobID,JobName,State,Elapsed,MaxRSS,MaxVMSize
```

`MaxRSS` (maximum resident set size) tells you peak actual memory usage — use this to right-size your memory requests for future jobs.

### Who else is using the cluster?
```
$ squeue -p qTRDGPU                 # All jobs in GPU queue
$ squeue                            # All jobs on the cluster
```

## Resources for deeper learning
- 📄 [SLURM Partitions and QOS documentation](https://slurm.schedmd.com/slurm.conf.html)
- 🔗 [TReNDs Wiki — cluster queues and guidelines](https://trendscenter.github.io/wiki/)
- 📄 [SLURM sinfo documentation](https://slurm.schedmd.com/sinfo.html)
- 📄 [SLURM sacct documentation](https://slurm.schedmd.com/sacct.html)
