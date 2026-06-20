## Why this matters to you
The cluster uses a module system to manage software — instead of having one global installation of every tool, modules let you load and unload specific software versions on demand. This prevents version conflicts and ensures reproducibility. Understanding modules is essential before you can use MATLAB, Python, SPM, GIFT, or any other tool on the cluster.

## What the module system is
[Lmod](https://lmod.readthedocs.io/) is the module system used on the cluster. When you "load" a module, it modifies your shell environment (PATH, LD_LIBRARY_PATH, etc.) so the software becomes available. When you "unload" it, those changes are reversed.

This means:
- Different users can use different versions of the same software simultaneously
- You can switch between Python 3.8 and 3.10,  or between MATLAB R2022a and R2023a, without conflicts
- Your environment is clean and predictable

## Prerequisites: module system initialization
Before using modules, your `.bashrc` needs the initialization lines (you should have added these in the "Set Up Your Data Directory" task):

```bash
source /usr/share/lmod/lmod/init/bash
module use /application/ubuntumodules/localmodules
```

If these aren't in your `.bashrc`, add them and run `source ~/.bashrc`.

## Essential module commands

### See what's available
```
$ module avail                    # List all available modules
$ module avail matlab             # Search for matlab modules
$ module avail python             # Search for python modules
```

### Load software
```
$ module load matlab              # Load the default MATLAB version
$ module load matlab/R2023a       # Load a specific version
$ module load python              # Load Python
$ module load cuda/11.8           # Load CUDA for GPU work
```

### Check what's loaded
```
$ module list                     # Show currently loaded modules
```

### Unload software
```
$ module unload matlab            # Unload MATLAB
$ module purge                    # Unload ALL modules (clean slate)
```

### Get info about a module
```
$ module show matlab              # Show what the module changes (PATH, variables, etc.)
```

## Loading MATLAB and toolboxes
MATLAB is the primary language for SPM and GIFT:

```
$ module load matlab
$ matlab -nodisplay               # Start MATLAB in command-line mode
```

Or for GUI (on dev nodes or via Hemera):
```
$ matlab
```

Once in MATLAB, add GIFT to your path:
```matlab
>> addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'));
>> gift    % Launch GIFT GUI
```

Add SPM:
```matlab
>> addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));
>> spm     % Launch SPM GUI
```

**Tip**: Add these `addpath` lines to your MATLAB startup file (`~/Documents/MATLAB/startup.m`) so they load automatically every time MATLAB starts.

## TReNDs applications directory
Some software isn't available as modules but lives in `/trdapps/`:

```
$ ls /trdapps/linux-x86_64/
```

You can add the binary directory to your PATH:
```bash
export PATH=$PATH:/trdapps/linux-x86_64/bin/
```

Add this to your `.bashrc` if you use these tools regularly.

### Key software in /trdapps
- `/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/` — GIFT toolbox
- `/trdapps/linux-x86_64/matlab/toolboxes/spm12/` — SPM12
- `/trdapps/linux-x86_64/bin/` — Various utilities

## Common module combinations
For different types of work, you'll load different module sets:

### ICA analysis (MATLAB/GIFT)
```
$ module load matlab
```

### Python data analysis
```
$ module load python
# Or use your own Miniconda environment (next task)
```

### GPU deep learning
```
$ module load cuda/11.8
$ conda activate my_torch_env
```

## Modules in SBATCH scripts
When submitting batch jobs, include module loads in your SBATCH script:

```bash
#!/bin/bash
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH --mem=16G
#SBATCH -t 4:00:00

module load matlab
matlab -nodisplay -r "run_my_analysis; exit"
```

This ensures the job has the right software available regardless of what your interactive shell has loaded.

## Resources for deeper learning
- 📄 [Lmod documentation — module system user guide](https://lmod.readthedocs.io/en/latest/010_user.html)
- 🔗 [TReNDs Wiki — software on the cluster](https://trendscenter.github.io/wiki/)
- 📄 [GIFT Toolbox installation guide](https://trendscenter.org/software/gift/)
