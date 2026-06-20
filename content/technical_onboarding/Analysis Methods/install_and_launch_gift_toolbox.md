---
task_name: "Install & Launch GIFT Toolbox"
emoji: "🧰"
tier: Hands-On
order: 1
url: "https://trendscenter.org/software/gift/"
---
## Why this matters to you

GIFT (Group ICA of fMRI Toolbox) is the lab's flagship software — built right here at TReNDs. It's the tool you'll use for ICA, Group ICA, component visualization, FNC, dFNC, and statistical analysis. Getting it running on the cluster is your gateway to hands-on neuroimaging analysis.

> **Key Resource**: The [GIFT User Manual / Handbook](https://trendscenter.org/software/gift/) is the definitive reference for all GIFT operations. Consult it for detailed instructions, parameter explanations, and troubleshooting.

## What GIFT provides

GIFT is a comprehensive MATLAB toolbox that handles the entire ICA-based analysis pipeline:

- **Setup**: Configure ICA parameters (number of components, algorithm, data reduction)

- **Group ICA**: Run ICA across multiple subjects (PCA → ICA → back-reconstruction)

- **Visualization**: View component spatial maps as brain images, timecourses, and spectra

- **Sorting**: Classify components as brain networks vs. artifacts (spatial and temporal criteria)

- **FNC**: Compute static functional network connectivity between components

- **dFNC**: Compute dynamic FNC using sliding windows and k-means clustering

- **Statistics**: Mancovan toolbox for group comparisons, regression, ANOVA

- **Neuromark**: Pre-computed network templates for standardized analysis

> **Important — sorting is not fully automated**: GIFT can *assist* component and network sorting (spatial templates, ICLabel, Neuromark matching), but deciding which components are genuine networks vs. artifacts still requires hands-on expertise and careful attention to detail. This is especially true for blind (non-template) ICA and any non-NeuroMark analysis, where there is no template to match against. Always visually verify automated labels — sorting is not a button you press and trust.

## Step 1: Start an interactive session

GIFT requires MATLAB, which needs an interactive session on a compute node (NOT the login node):

```shell
$ srun -p qTRD -A trends53c17 -c 4 --nodes=1 --ntasks-per-node=1 --mem=16G --time=4:00:00 --pty -J gift /bin/bash
```

Request at least 4 cores and 16 GB RAM — GIFT's PCA and ICA steps can be memory-intensive.

## Step 2: Load MATLAB

```shell
$ module load matlab
```

## Step 3: Start MATLAB

For GUI access (requires Hemera, X11 forwarding, or VSCode with X11):

```shell
$ matlab
```

For command-line access:

```shell
$ matlab -nodisplay
```

## Step 4: Add GIFT to MATLAB path

In the MATLAB command window:

```matlab
>> addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'));
```

Verify GIFT is available:

```matlab
>> which icatb_setup_analysis
```

This should return the path to the function. If it returns "not found," the addpath didn't work — check the path.

## Step 5: Launch GIFT

```matlab
>> gift
```

The GIFT GUI should open with the main menu showing options:

- Setup ICA Analysis

- Run Analysis

- Display

- Utilities

- Stats

If you're working in command-line mode (no GUI), you can use GIFT's batch scripting interface:

```matlab
>> help icatb_batch_file_run
```

## Making GIFT load automatically

To avoid typing the `addpath` command every time, add it to your MATLAB startup file:

```shell
$ mkdir -p ~/Documents/MATLAB
$ nano ~/Documents/MATLAB/startup.m
```

Add these lines:

```matlab
% Load GIFT toolbox
addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'));

% Load SPM
addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));

% Set default figure properties
set(0, 'DefaultFigureWindowStyle', 'docked');
```

Now GIFT and SPM will be available every time MATLAB starts.

## GIFT version check

Check which version of GIFT you're using:

```matlab
>> icatb_get_version
```

Or check the directory name — `GroupICATv4.0c` indicates version 4.0c. The lab continuously develops GIFT, so newer versions may be available. Ask senior lab members if you should use a different version for your specific project.

## Troubleshooting

### "Out of memory" errors

ICA on large datasets needs significant RAM. Increase your SLURM memory request:

```shell
$ srun --mem=64G ...
```

### MATLAB can't find GIFT functions

Verify the path is correct:

```matlab
>> path
```

Look for GIFT directories in the output. If they're missing, re-run `addpath`.

### Display issues (no GUI)

If you get display errors, you need X11 forwarding or Hemera:

- **X11 forwarding**: Add `-X` to your SSH command: `ssh -X arclogin`

- **Hemera**: Use the MATLAB session at hemera.rs.gsu.edu (easier and more reliable)

- **No display available**: Use GIFT in batch/scripting mode instead

### Java errors

MATLAB's GUI depends on Java. If you see Java warnings, they're usually non-fatal. If the GUI fails to start, try:

```matlab
>> matlab -nodisplay
>> icatb_batch_file_run('my_batch_file.m')
```

## Resources for deeper learning

- 📄 [GIFT Manual — Section 3.1: Installing GIFT](https://trendscenter.org/software/gift/)

- 📄 [GIFT Toolbox download page (includes manual and example data)](https://trendscenter.org/software/gift/)

- 🔗 [TReNDs Wiki — MATLAB on the cluster](https://trendscenter.github.io/wiki/)
