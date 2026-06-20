---
task_name: "Run Multi-Subject ICA with Array Jobs"
emoji: "👥"
tier: Hands-On
order: 7
url: "https://github.com/trendscenter/ClusterWorkshop"
---
## Why this matters to you

Real studies involve dozens to thousands of subjects. Running ICA on each one sequentially would take forever. By combining SBATCH array jobs with the single-subject Neuromark ICA pipeline from the previous task, you can process all subjects in parallel — each running on its own compute node simultaneously. This is the production workflow for large-scale analyses in the lab.

## The concept

An array job runs the same SBATCH script multiple times with different indices. Each task uses its index (`$SLURM_ARRAY_TASK_ID`) to select a different subject from the subject list. So if you have 100 subjects and submit `--array=0-99`, SLURM launches 100 jobs, each processing one subject independently.

## Step 1: Get the example files

```shell
$ cd $MYDATA/ClusterWorkshop/Examples/MultiSubjectICA
$ ls
```

You should see:

- `JobArray.sh` — SBATCH array submission script

- `gigica_step1.m` — MATLAB script modified to accept a subject index

## Step 2: Review the MATLAB script

The key difference from the single-subject version: the MATLAB script reads the array task ID from an environment variable to determine which subject to process:

```matlab
% Get the array task ID from SLURM
task_id = str2double(getenv('SLURM_ARRAY_TASK_ID'));

% Read the subject list
fid = fopen('subjects.txt');
subjects = textscan(fid, '%s');
fclose(fid);

% Select this task's subject
subject_file = subjects{1}{task_id + 1};  % +1 because MATLAB is 1-indexed

fprintf('Processing subject %d: %s\n', task_id, subject_file);
```

Review and modify paths as needed for your data.

## Step 3: Review the SBATCH array script

`JobArray.sh`:

```shell
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 4:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -J multiICA
#SBATCH -e error%A-%a.err
#SBATCH -o out%A-%a.out

module load matlab

echo "Array Task ID: $SLURM_ARRAY_TASK_ID"
echo "Running on: $HOSTNAME"

matlab -nodisplay -nosplash -r "
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'));
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));
    gigica_step1;
    exit;
"
```

Note:

- `%A-%a` in log filenames: `%A` = overall job ID, `%a` = array task index. This gives you separate log files per subject.

- The MATLAB script inside reads `$SLURM_ARRAY_TASK_ID` to determine which subject to process.

## Step 4: Submit the array job

For the 5-subject example:

```shell
$ sbatch --array=0-4 JobArray.sh
```

This launches 5 jobs simultaneously. Each processes one subject.

For larger analyses with concurrency limits:

```shell
$ sbatch --array=0-99%20 JobArray.sh    # 100 subjects, max 20 at a time
```

## Step 5: Monitor the array

### Check all tasks

```shell
$ squeue -u $USER
```

You'll see entries like:

```shell
JOBID          PARTITION  NAME       ST  TIME  NODES  NODELIST
12345678_0     qTRD       multiICA   R   5:23  1      arctrdcn003
12345678_1     qTRD       multiICA   R   5:23  1      arctrdcn005
12345678_2     qTRD       multiICA   PD  0:00  1      (Resources)
...
```

### Check specific tasks

```shell
$ tail -f out12345678-0.out     # Follow output of task 0
$ tail -f out12345678-3.out     # Follow output of task 3
```

### Cancel specific tasks

```shell
$ scancel 12345678_2            # Cancel only task 2
$ scancel 12345678              # Cancel the entire array
```

## Step 6: Verify all tasks completed

After all tasks finish:

```shell
$ sacct -j 12345678 --format=JobID,State,ExitCode,Elapsed,MaxRSS
```

Check that all tasks show `COMPLETED` with `ExitCode` `0:0`. Any failed tasks need investigation:

```shell
$ cat error12345678-3.err       # Check error log for failed task 3
```

Common reasons for individual task failures:

- **Memory**: One subject had unusually large data → increase `--mem`

- **File not found**: Subject file was missing or path was wrong

- **Convergence failure**: ICA didn't converge for that subject's data

- **Time limit**: Processing took longer than expected for one subject

You can resubmit just the failed tasks:

```shell
$ sbatch --array=3,7,15 JobArray.sh    # Rerun only tasks 3, 7, and 15
```

## Step 7: Collect results

After all subjects are processed, verify all output files exist:

```shell
# Count how many subjects have output
$ ls output_directory/sub_*/ica_results.mat | wc -l

# Compare to expected number
$ wc -l subjects.txt
```

## Scaling up

For production analyses with hundreds of subjects:

```shell
# 500 subjects, 30 at a time, 8 hours per subject
$ sbatch --array=0-499%30 JobArray.sh
```

Monitor overall progress:

```shell
# How many are done?
$ sacct -j 12345678 --format=State -n | sort | uniq -c
```

Output might show:

```shell
    412 COMPLETED
     18 RUNNING
     70 PENDING
```

## Resources for deeper learning

- 🔗 [Cluster Workshop — MultiSubjectICA example](https://github.com/trendscenter/ClusterWorkshop)

- 📄 [SLURM Job Array documentation](https://slurm.schedmd.com/job_array.html)

- 📑 [Du et al. (2020) — NeuroMark automated pipeline](https://doi.org/10.1016/j.nicl.2020.102375)
