## Why this matters to you
Interactive jobs let you work directly on a compute node — running commands, testing code, debugging scripts — with dedicated CPU, memory, and optionally GPU resources. This is where you test your analysis pipeline before submitting it as a batch job. Unlike the login node (where you must NOT run analyses), compute nodes are meant for real work.

## What srun does
`srun` requests resources from the SLURM scheduler and starts an interactive shell on a compute node. While the job is running, you have a terminal on that node and can run whatever you need — MATLAB, Python, GPU code, etc.

## Running a CPU interactive job

```
$ srun -p qTRD -A trends53c17 -c 4 --nodes=1 --ntasks-per-node=1 --mem=4G --time=1:00:00 --pty -J myJob /bin/bash
```

### What each flag means
| Flag | Meaning | Example |
|---|---|---|
| `-p qTRD` | Queue/partition | qTRD = standard CPU nodes |
| `-A trends53c17` | Account/allocation | Your PI's allocation name |
| `-c 4` | Number of CPU cores | Request 4 cores |
| `--nodes=1` | Number of nodes | Always 1 for interactive |
| `--ntasks-per-node=1` | Tasks per node | 1 for a single shell |
| `--mem=4G` | Memory | 4 GB RAM |
| `--time=1:00:00` | Max runtime | 1 hour (HH:MM:SS) |
| `--pty` | Allocate a pseudo-terminal | Required for interactive use |
| `-J myJob` | Job name | Shows in squeue |
| `/bin/bash` | Shell to start | Bash terminal |

When resources are available, you'll be connected to a compute node. Your prompt will change to show the node name (e.g., `[jsmith42@arctrdcn003 ~]$`).

## Running a GPU interactive job

```
$ srun -p qTRDGPU -A trends53c17 -c 4 --gres=gpu:1 --nodes=1 --ntasks-per-node=1 --mem=4G --time=1:00:00 --pty -J myGPUJob /bin/bash
```

The key differences:
- `-p qTRDGPU`: Use the GPU partition
- `--gres=gpu:1`: Request 1 GPU (use `gpu:2` for 2 GPUs, etc.)

Once connected, verify the GPU is available:
```
$ nvidia-smi
```

You should see GPU information — model, memory, temperature. If you get "command not found," the GPU node may need CUDA loaded:
```
$ module load cuda
$ nvidia-smi
```

## Practical tips

### Request minimum resources
Only request what you actually need. Over-requesting means:
- Longer wait times (scheduler needs to find a node with enough free resources)
- Wasting resources that others could use
- Potential policy violations if you consistently over-request

Common resource ranges:
- **Quick testing**: -c 1 --mem=2G --time=0:30:00
- **MATLAB/GIFT**: -c 4 --mem=16G --time=4:00:00
- **Python analysis**: -c 2 --mem=8G --time=2:00:00
- **GPU deep learning**: -c 4 --gres=gpu:1 --mem=16G --time=4:00:00

### Don't leave sessions idle
When you're done working, exit the interactive session:
```
$ exit
```

This releases the resources for others. Leaving an idle session running for hours is poor cluster etiquette and may consume your allocation's CPU-hours budget.

### What to do while waiting
If no resources are available, your `srun` command will wait (you'll see "srun: job XXXXX queued and waiting for resources"). You can:
- Try a different partition with more availability
- Reduce your resource request
- Wait — jobs usually start within minutes during off-peak hours

### Check the queue before requesting
```
$ sinfo -p qTRD           # Check which nodes are available in qTRD
$ squeue -p qTRD           # See what jobs are running/pending in qTRD
```

## What to test in interactive sessions
Interactive sessions are perfect for:
- Testing MATLAB/GIFT commands before putting them in a batch script
- Debugging Python scripts with real data
- Checking that your conda environment has all needed packages
- Running quick analyses that don't need to be automated
- Verifying GPU access and CUDA compatibility for deep learning

Once your interactive commands work, convert them into an SBATCH script for automated batch processing (next task).

## Resources for deeper learning
- 📄 [SLURM srun documentation](https://slurm.schedmd.com/srun.html)
- 🔗 [TReNDs Wiki — running jobs](https://trendscenter.github.io/wiki/)
- 🔗 [Cluster Workshop — example commands](https://github.com/trendscenter/ClusterWorkshop)
