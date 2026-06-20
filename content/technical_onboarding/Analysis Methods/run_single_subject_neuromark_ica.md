---
task_name: "Run Single-Subject Neuromark ICA on Cluster"
emoji: "🏃"
tier: Hands-On
order: 6
url: "https://github.com/trendscenter/ClusterWorkshop"
---
## Why this matters to you

Now you'll combine several skills into a real analysis workflow: SBATCH scripts, MATLAB on the cluster, and GIFT's Neuromark pipeline. Running single-subject Neuromark ICA means taking the pre-computed Neuromark template and using spatially constrained ICA (GIG-ICA) to extract each subject's individual version of the 53 standard brain network components. This is the lab's standard approach for production analyses.

## What Neuromark single-subject ICA does

Instead of running full Group ICA from scratch (which requires all subjects' data at once), Neuromark takes a different approach:

1. **Template**: Start with the Neuromark template — 53 brain network components estimated from thousands of subjects

2. **Spatially constrained ICA (GIG-ICA)**: For each subject, find that subject's version of each template component. The spatial constraint ensures that the output components correspond to the same networks as the template

3. **Output**: 53 subject-specific spatial maps and timecourses, in the same order across all subjects

This is faster, more memory-efficient, and produces directly comparable components without needing everyone's data simultaneously.

## Step 1: Get the example files

The Cluster Workshop repository has example scripts for this workflow:

```shell
$ cd $MYDATA
$ git clone https://github.com/trendscenter/ClusterWorkshop.git   # If not already cloned
$ cd ClusterWorkshop/Examples/SingleSubjectICA
$ ls
```

You should see files like:

- `JobSubmit.sh` — SBATCH submission script

- `gigica_step1.m` — MATLAB script that runs the GIG-ICA analysis

## Step 2: Get the subject list

Copy or create a subject list file:

```shell
$ cp /data/users2/bbaker/fbirn_subject_list.txt $MYDATA/ClusterWorkshop/Examples/
```

This file contains paths to preprocessed fMRI files, one per line. Each path points to a 4D NIfTI file for one subject.

If using your own data, create a text file with one file path per line:

```shell
/data/qneuromark/subjects/sub001/func/sub001_preprocessed.nii
/data/qneuromark/subjects/sub002/func/sub002_preprocessed.nii
```

## Step 3: Review the MATLAB script

Open `gigica_step1.m` and check:

```matlab
% Key parameters to verify:
% - Path to Neuromark template
% - Path to subject list
% - Output directory
% - Number of components (53 for standard Neuromark)
```

Modify paths if needed to match your directory structure.

## Step 4: Review the SBATCH script

Open `JobSubmit.sh`:

```shell
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 4:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -e error%A.err
#SBATCH -o out%A.out

module load matlab

matlab -nodisplay -nosplash -r "
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'));
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));
    gigica_step1;
    exit;
"
```

Make sure:

- The account (`-A`) matches your allocation

- Memory and time are sufficient (32G and 4 hours is usually enough for 1 subject)

- GIFT and SPM paths are correct

## Step 5: Submit the job

```shell
$ cd $MYDATA/ClusterWorkshop/Examples/SingleSubjectICA
$ sbatch JobSubmit.sh
```

Monitor:

```shell
$ squeue -u $USER
$ tail -f out*.out
```

## Step 6: Check the output

When the job completes, verify:

```shell
$ ls -la output_directory/
```

You should find:

- Subject-specific spatial map files (`.nii`)

- Timecourse files

- A parameter file recording all settings

Check the error log for any warnings:

```shell
$ cat error*.err
```

Even if the job returned exit code 0, check for MATLAB warnings about memory, convergence, or data issues.

## Common issues and fixes

### Out of memory

Increase `--mem` in the SBATCH script. Single-subject GIG-ICA typically needs 16-32 GB depending on the data dimensions.

### File not found errors

Double-check paths in the MATLAB script. Remember that cluster paths are case-sensitive (Linux), unlike Windows.

### Convergence warnings

GIG-ICA may warn that some components didn't converge well. This usually means the subject's brain organization differs significantly from the template for those components. Check the specific components — they may still be usable.

### Job killed (time limit)

Increase `--time`. If it's taking very long, check that you're not accidentally loading unprocessed data or data with excessive timepoints.

## Resources for deeper learning

- 🔗 [Cluster Workshop — SingleSubjectICA example](https://github.com/trendscenter/ClusterWorkshop)

- 📄 [GIFT Manual — GIG-ICA / Neuromark pipeline](https://trendscenter.org/software/gift/)

- 📑 [Du et al. (2020) — NeuroMark pipeline paper](https://doi.org/10.1016/j.nicl.2020.102375)

- 📑 [Iraji et al. (2019) — Neuromark template](https://doi.org/10.1002/hbm.24580)
