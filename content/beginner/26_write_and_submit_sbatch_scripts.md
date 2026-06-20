## Why this matters to you
Interactive sessions are great for testing, but real analyses need to run unattended — often for hours. SBATCH scripts let you submit a job that runs on a compute node without you being logged in. If your VPN drops or you close your laptop, the job keeps running. This is how all production analyses on the cluster are done.

## What SBATCH is
SBATCH (Submit BATCH) is the SLURM command for submitting non-interactive jobs. You write a shell script with special `#SBATCH` directives that specify the resources you need, then submit it. SLURM queues the job, runs it when resources are available, and saves the output to files.

## Your first SBATCH script
Create a file called `JobSubmit.sh`:

```bash
#!/bin/bash
#SBATCH -N 1                    # Number of nodes
#SBATCH -n 1                    # Number of tasks
#SBATCH -c 1                    # CPUs per task
#SBATCH --mem=10G               # Memory
#SBATCH -t 1:00:00              # Time limit (HH:MM:SS)
#SBATCH -p qTRD                 # Partition/queue
#SBATCH -A trends53c17          # Account/allocation
#SBATCH -J myFirstJob           # Job name
#SBATCH -e error%A.err          # Error log file (%A = job ID)
#SBATCH -o out%A.out            # Output log file (%A = job ID)
#SBATCH --oversubscribe         # Allow sharing nodes

sleep 10s
echo "Hello from SBATCH!"
echo "Running on node: $HOSTNAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Date: $(date)"
sleep 10s
echo "Job complete."
```

## Submit the job
```
$ sbatch JobSubmit.sh
```

You'll see: `Submitted batch job 12345678`

The number is your job ID — you'll use it to monitor and manage the job.

## Monitor your job

### Check job status
```
$ squeue -u $USER               # Show your running/pending jobs
```

Output columns:
- **JOBID**: The job ID
- **PARTITION**: Which queue
- **NAME**: Job name
- **ST**: Status (R=Running, PD=Pending, CG=Completing)
- **TIME**: How long it's been running
- **NODELIST**: Which node it's running on

### Check job details
```
$ scontrol show job 12345678    # Detailed info about a specific job
```

### View output while running
```
$ tail -f out12345678.out       # Follow the output file in real-time
```

### Cancel a job
```
$ scancel 12345678              # Cancel a specific job
$ scancel -u $USER              # Cancel ALL your jobs (careful!)
```

### Job history
```
$ sacct -j 12345678             # Details of a completed job
$ sacct --format=JobID,JobName,State,Elapsed,MaxRSS -j 12345678   # Specific fields
```

`MaxRSS` shows peak memory usage — useful for tuning your memory requests.

## SBATCH directive reference

| Directive | Meaning | Common values |
|---|---|---|
| `-N` | Nodes | 1 (almost always) |
| `-n` | Tasks | 1 for serial, >1 for MPI |
| `-c` | CPUs per task | 1-32 |
| `--mem` | Total memory | 4G, 16G, 64G |
| `-t` | Time limit | 1:00:00, 12:00:00, 48:00:00 |
| `-p` | Partition | qTRD, qTRDGPU, qTRDHM |
| `-A` | Account | Your allocation name |
| `-J` | Job name | Descriptive name |
| `-e` | Error file | error%A.err |
| `-o` | Output file | out%A.out |
| `--gres` | Generic resources | gpu:1, gpu:2 |
| `--mail-type` | Email notifications | BEGIN, END, FAIL, ALL |
| `--mail-user` | Email address | your.email@gsu.edu |

## A real analysis example: MATLAB/GIFT job

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 8:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -J ica_analysis
#SBATCH -e error%A.err
#SBATCH -o out%A.out

module load matlab

matlab -nodisplay -nosplash -r "
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'));
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));
    run('/data/users2/$USER/projects/my_analysis/run_ica.m');
    exit;
"
```

## A Python job example

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t 2:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -J python_analysis
#SBATCH -e error%A.err
#SBATCH -o out%A.out

source $MYDATA/bin/miniconda3/etc/profile.d/conda.sh
conda activate py310

python /data/users2/$USER/scripts/analysis.py
```

## Email notifications
Add these directives to get notified when jobs start, finish, or fail:

```bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your.email@gsu.edu
```

This is especially useful for long jobs — you'll know immediately if something failed instead of checking hours later.

## Tips for writing good SBATCH scripts
- **Always set a time limit**. If your code has a bug that causes an infinite loop, the time limit will kill the job instead of consuming resources indefinitely
- **Log everything important** — print the date, hostname, input parameters, and key milestones to your output file
- **Test interactively first**: Use `srun` to verify your commands work before putting them in a script
- **Check output and error files**: The error file often has important warnings even when the job seems to succeed

## Resources for deeper learning
- 📄 [SLURM sbatch documentation](https://slurm.schedmd.com/sbatch.html)
- 🔗 [Cluster Workshop — JobSubmit examples](https://github.com/trendscenter/ClusterWorkshop)
- 📄 [SLURM Quick Start guide](https://slurm.schedmd.com/quickstart.html)
