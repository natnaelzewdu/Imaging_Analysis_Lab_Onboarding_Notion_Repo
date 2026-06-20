## Why this matters to you
Many neuroimaging analyses need to run the same computation on many subjects independently — ICA on 100 subjects, preprocessing 50 scans, or cross-validation with 10 folds. SBATCH array jobs let you submit all of these as a single command, with SLURM automatically parallelizing them across available nodes. Instead of writing 100 separate scripts or waiting for each subject to finish before starting the next, array jobs handle it automatically.

## What an array job is
An array job is a single SBATCH script that runs multiple instances (called "tasks") with different index values. Each task gets a unique index through the environment variable `$SLURM_ARRAY_TASK_ID`. Your script uses this index to figure out which subject, fold, or parameter set to process.

## Basic array job example
Create `JobArray.sh`:

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem=4G
#SBATCH -t 1:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -J arrayTest
#SBATCH -e error%A-%a.err
#SBATCH -o out%A-%a.out

echo "Array task ID: $SLURM_ARRAY_TASK_ID"
echo "Running on: $HOSTNAME"
echo "Date: $(date)"
```

Submit with 5 tasks (indices 0-4):
```
$ sbatch --array=0-4 JobArray.sh
```

This creates 5 independent jobs, each with `$SLURM_ARRAY_TASK_ID` set to 0, 1, 2, 3, or 4. They run on whatever nodes are available, potentially all in parallel.

### Log file naming
Note `%A-%a` in the log filenames:
- `%A`: The overall job ID
- `%a`: The array task index

So you get separate log files for each task: `out12345-0.out`, `out12345-1.out`, etc.

## Reading subjects from a file
The most common pattern: use the array index to select a line from a subject list file.

Create `subjects.txt`:
```
sub-001
sub-002
sub-003
sub-004
sub-005
```

In your SBATCH script:
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 4:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -J ica_array
#SBATCH -e error%A-%a.err
#SBATCH -o out%A-%a.out

# Read the subject ID from line (TASK_ID + 1) of subjects.txt
SUBJECT=$(sed -n "$(( $SLURM_ARRAY_TASK_ID + 1 )) p" subjects.txt)

echo "Processing subject: $SUBJECT"
echo "Array index: $SLURM_ARRAY_TASK_ID"

# Run analysis for this subject
module load matlab
matlab -nodisplay -r "process_subject('$SUBJECT'); exit"
```

Submit:
```
$ sbatch --array=0-4 JobArray.sh
```

Task 0 processes sub-001, task 1 processes sub-002, and so on.

## Array index ranges

```
$ sbatch --array=0-99 script.sh         # 100 tasks (0 to 99)
$ sbatch --array=1-50 script.sh         # 50 tasks (1 to 50)
$ sbatch --array=0,5,10,15 script.sh    # Specific indices only
$ sbatch --array=1-100%10 script.sh     # 100 tasks, max 10 running at a time
```

The `%N` syntax is critical for being a responsible cluster citizen — it limits how many of your tasks run simultaneously, leaving resources for others.

## Limiting concurrent tasks
If you submit `--array=0-999`, you could potentially consume all available nodes. Use `%N` to throttle:

```
$ sbatch --array=0-499%20 script.sh     # 500 tasks, max 20 concurrent
```

**Recommended**: For large arrays (> 50 tasks), always set a concurrent limit. Start conservative (10-20) and increase if the cluster is lightly loaded.

## Array maximum size
SLURM's default maximum array size is typically 5000 tasks. For larger analyses:
- Split into multiple array job submissions
- Or ask your system administrator to increase the limit

## Using arrays with Python

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t 2:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -e error%A-%a.err
#SBATCH -o out%A-%a.out

source $MYDATA/bin/miniconda3/etc/profile.d/conda.sh
conda activate py310

python my_script.py --subject-index $SLURM_ARRAY_TASK_ID
```

In your Python script:
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--subject-index', type=int, required=True)
args = parser.parse_args()

subjects = open('subjects.txt').read().strip().split('\n')
subject = subjects[args.subject_index]
print(f"Processing {subject}")
```

## Monitoring array jobs

```
$ squeue -u $USER                       # Shows all tasks
$ squeue -u $USER -j 12345678          # Show specific array job
$ sacct -j 12345678                    # History of all tasks in the array
```

Cancel specific tasks:
```
$ scancel 12345678_5                    # Cancel only task index 5
$ scancel 12345678                      # Cancel the entire array
```

## Resources for deeper learning
- 📄 [SLURM Job Array documentation](https://slurm.schedmd.com/job_array.html)
- 🔗 [Cluster Workshop — array job examples](https://github.com/trendscenter/ClusterWorkshop)
- 📄 [SLURM array tutorial](https://slurm.schedmd.com/job_array.html)
