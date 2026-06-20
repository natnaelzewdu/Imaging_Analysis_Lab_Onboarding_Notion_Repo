## Why this matters to you
Your home directory (`~`) on the cluster has very limited space — often just a few gigabytes. fMRI datasets can be hundreds of gigabytes. You need a dedicated data directory under `/data/users#/` where there's ample storage for your analyses. Setting up your directory and environment variables properly now saves you from storage headaches later.

## Step 1: Find available storage
The cluster has multiple user data partitions. Check which ones exist and how full they are:

```
$ df -h /data/users1 /data/users2 /data/users3 /data/users4
```

Choose the partition with the most available space. Ask your PI or lab colleagues which partition they typically use — it's good to be near your collaborators' data for convenience.

## Step 2: Create your data directory
Replace `<campusid>` with your actual ID and `#` with the partition number you chose:

```
$ mkdir /data/users#/<campusid>
```

For example:
```
$ mkdir /data/users2/jsmith42
```

Verify it was created:
```
$ ls -la /data/users2/jsmith42
```

## Step 3: Set up your .bashrc
Your `.bashrc` file runs every time you open a shell. It sets up your environment — paths, aliases, module system, and custom variables.

Edit your .bashrc:
```
$ nano ~/.bashrc
```

Add these lines at the end (adjust the users# to match your partition):

```bash
# Module system initialization
source /usr/share/lmod/lmod/init/bash
module use /application/ubuntumodules/localmodules

# Personal data directory
export MYDATA=/data/users#/<campusid>
alias go2data="cd $MYDATA"

# Useful aliases
alias ll="ls -lah"
alias jobs="squeue -u $USER"
alias gpu="nvidia-smi"
```

Save and exit (`Ctrl+O`, `Ctrl+X` in nano), then reload:
```
$ source ~/.bashrc
```

Now you can type `go2data` to jump to your data directory from anywhere.

## Step 4: Organize your data directory
Create a sensible directory structure from the start:

```
$ cd $MYDATA
$ mkdir -p projects
$ mkdir -p scripts
$ mkdir -p results
$ mkdir -p tools
```

A typical structure might look like:
```
/data/users2/jsmith42/
├── projects/           # One subdirectory per research project
│   ├── schiz_ica/
│   └── aging_fnc/
├── scripts/            # Shared scripts and utilities
├── results/            # Analysis outputs
├── tools/              # Miniconda, custom toolboxes
│   └── miniconda3/
└── ClusterWorkshop/    # Tutorial examples (from GitHub)
```

## Key cluster directories to know

### Your spaces
- `~` or `$HOME`: Home directory. Limited space (~5-10 GB). For config files (.bashrc, .ssh) and small scripts only
- `$MYDATA` (`/data/users#/<campusid>`): Your main workspace. Much larger. Put data, results, and tools here

### Shared data locations
- `/data/qneuromark/`: Neuromark datasets and templates
- `/data/neuromark2/`: Neuromark2 datasets
- `/data/collaboration/`: Shared collaborator data
- `/scratch/`: Temporary scratch space — files may be deleted automatically after 30-60 days. Good for intermediate results during active analysis

### Software and apps
- `/trdapps/`: TReNDs applications and toolboxes
- `/trdapps/linux-x86_64/matlab/toolboxes/`: MATLAB toolboxes including GIFT, SPM
- `/trdapps/linux-x86_64/bin/`: Additional binaries and executables

## Storage best practices
- **Never duplicate existing datasets**. If data exists in `/data/qneuromark/` or a shared location, use symlinks or point your analysis scripts there
- **Clean up intermediate files** after analysis is complete. ICA generates many intermediate files that can be removed once you have final results
- **Use compression**: `tar -czf results.tar.gz results/` reduces storage significantly
- **Check your usage periodically**: `du -sh $MYDATA` and `du -sh $MYDATA/*`

## Resources for deeper learning
- 🔗 [TReNDs Wiki — cluster storage information](https://trendscenter.github.io/wiki/)
- 📄 [Linux Environment Variables tutorial](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
- 📄 [Bash aliases and .bashrc guide](https://www.digitalocean.com/community/tutorials/an-introduction-to-useful-bash-aliases-and-functions)
