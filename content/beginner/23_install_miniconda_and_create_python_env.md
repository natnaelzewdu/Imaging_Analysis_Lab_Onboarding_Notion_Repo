## Why this matters to you
While the cluster has a system Python, it's shared and you can't install your own packages into it. You need your OWN Python environment where you control the packages and versions. Miniconda gives you this — it's a lightweight package manager that lets you create isolated Python environments on the cluster, each with its own set of libraries. This is essential for running custom analyses, deep learning, and any Python-based neuroimaging tools.

## Why Miniconda (not Anaconda)
- **Anaconda**: Full distribution with 250+ pre-installed packages. Takes up ~5GB. More than you need on the cluster.
- **Miniconda**: Minimal installer with just Python, conda, and basic utilities. Takes up ~400MB. You install only what you need.

On a shared cluster with limited home directory space, Miniconda is the right choice.

## Step 1: Download Miniconda

SSH into the cluster and run:
```
$ cd $MYDATA
$ mkdir -p bin
$ cd bin
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda_install.sh
```

## Step 2: Install Miniconda

**Critical**: Install to your data directory, NOT your home directory. Home directory space is very limited.

```
$ bash miniconda_install.sh -b -u -p $MYDATA/bin/miniconda3
```

Flags:
- `-b`: Batch mode (no interactive prompts)
- `-u`: Update existing installation if present
- `-p`: Installation path — MUST point to your data directory

## Step 3: Initialize conda

```
$ $MYDATA/bin/miniconda3/bin/conda init bash
$ source ~/.bashrc
```

After reloading `.bashrc`, you should see `(base)` at the beginning of your prompt, indicating the base conda environment is active.

Verify:
```
$ conda --version
$ which python
$ python --version
```

## Step 4: Create your first environment

Never install packages into the `base` environment — keep it clean. Create a named environment for each project or purpose:

### General-purpose Python environment
```
$ conda create -n py310 python=3.10 -y
$ conda activate py310
$ pip install numpy scipy matplotlib pandas scikit-learn nibabel nilearn jupyter
```

### Deep learning environment
```
$ conda create -n torch python=3.10 -y
$ conda activate torch
$ conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
$ pip install scikit-learn matplotlib
```

### Neuroimaging tools environment
```
$ conda create -n neuro python=3.10 -y
$ conda activate neuro
$ pip install nibabel nilearn pybids templateflow mriqc
```

## Managing environments

### List all environments
```
$ conda env list
```

### Activate an environment
```
$ conda activate py310
```

### Deactivate (return to base)
```
$ conda deactivate
```

### Install additional packages
```
$ conda activate py310
$ pip install new_package
# or
$ conda install new_package
```

### Remove an environment
```
$ conda env remove -n env_name
```

### Export environment for reproducibility
```
$ conda activate py310
$ conda env export > environment.yml
```

Someone else can recreate your exact environment with:
```
$ conda env create -f environment.yml
```

## Using conda in SBATCH scripts
When submitting batch jobs, you need to initialize conda and activate your environment:

```bash
#!/bin/bash
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH --mem=8G
#SBATCH -t 2:00:00

# Initialize conda
source $MYDATA/bin/miniconda3/etc/profile.d/conda.sh
conda activate py310

python my_analysis_script.py
```

The `source` line is necessary because SBATCH jobs start with a minimal shell that doesn't have conda initialized.

## pip vs. conda
- **conda**: The conda package manager. Can install Python packages, C libraries, R, and other non-Python dependencies. Better for complex packages with compiled dependencies (numpy, scipy, pytorch).
- **pip**: The Python package manager. Only installs Python packages. Use when a package isn't available on conda.

**General rule**: Try `conda install` first. If the package isn't found, use `pip install`. Don't mix heavily — conda tracks its own dependencies, and pip installs can sometimes conflict.

## Storage tips
Conda environments can get large (1-5 GB each for deep learning environments). Monitor your space:
```
$ du -sh $MYDATA/bin/miniconda3/envs/*
```

Remove environments you're no longer using. Clean conda's package cache periodically:
```
$ conda clean --all -y
```

## Resources for deeper learning
- 📄 [Miniconda installation guide](https://docs.conda.io/en/latest/miniconda.html)
- 📄 [Conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)
- 📄 [Managing Python environments — conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- 📄 [PyTorch installation matrix](https://pytorch.org/get-started/locally/)
