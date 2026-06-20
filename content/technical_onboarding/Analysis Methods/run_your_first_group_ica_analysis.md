---
task_name: "Run Your First Group ICA Analysis"
emoji: "🧪"
category: Analysis Methods
tier: Hands-On
order: 2
url: "https://trendscenter.org/software/gift/"
---
## Why this matters to you

This is where everything you've learned comes together. You'll set up a complete Group ICA analysis from start to finish using GIFT — selecting data, configuring parameters, running the pipeline, and viewing components. This is the core workflow of the lab, and you'll do variations of it in every project.

## Prerequisites

Before starting, make sure you have:

- An interactive session with enough resources (`srun -p qTRD -c 4 --mem=32G --time=4:00:00 ...`)

- MATLAB loaded (`module load matlab`)

- GIFT on your path (`addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'))`)

- Access to fMRI data files (the Cluster Workshop has example data, or ask your PI for a small dataset)

## Step 1: Launch GIFT and open Setup

```matlab
>> gift
```

Click **"Setup ICA Analysis"** in the GIFT GUI.

## Step 2: Configure the analysis

### Output Directory

Choose where results will be saved. Create a dedicated directory:

```matlab
% In a terminal before starting MATLAB:
$ mkdir -p $MYDATA/projects/first_ica/results
```

Point GIFT to this directory.

### Output Prefix

A short string that prefixes all output files (e.g., `test_ica`). Choose something descriptive.

### Select Data Files

Click "Select" to browse for your preprocessed fMRI .nii files. GIFT expects:

- Preprocessed (realigned, normalized, optionally smoothed) functional images

- One 4D NIfTI file per subject per session

- All subjects should have the same spatial dimensions

If using example data from the Cluster Workshop:

```shell
/data/users2/bbaker/fbirn_subject_list.txt
```

### Number of Components

How many ICA components to extract. Common choices:

- **20**: Quick test, captures only major networks

- **53**: Neuromark standard — good for most analyses

- **75-100**: Fine-grained splitting of networks — used in many lab publications

For your first analysis, start with **20** to keep things fast and manageable.

### Algorithm

Select the ICA algorithm:

- **Infomax** (recommended): The lab standard. Robust, well-validated, fast

- **FastICA**: Alternative, sometimes used for comparison

- **JADE**: Deterministic (no random initialization), but slower

### Data Reduction Steps

GIFT handles PCA automatically in two stages:

- Subject-level PCA: Reduces each subject's data in a first dimensionality-reduction step. The exact number of retained components is a configurable parameter (not a fixed value) and is typically chosen relative to the number of timepoints and the final number of components you want.

- Group-level PCA: Reduces the concatenated group data down toward the final number of components.

For most analyses, the defaults are a reasonable starting point — but check the values GIFT chose for your data rather than assuming a fixed number.

## Step 3: Run the analysis

Click **"Run Analysis"** → select **"All***"** to run the complete pipeline:

1. **Parameter initialization**: Sets up file paths and parameters

2. **Data reduction (PCA)**: Compresses each subject's data

3. **ICA**: Runs the actual decomposition on the group data

4. **Back-reconstruction**: Projects group components back to individual subjects

This process takes minutes to hours depending on sample size and number of components. For a small dataset (5-10 subjects, 20 components), expect 10-30 minutes.

### Monitoring progress

GIFT shows a progress bar and prints status messages to the MATLAB command window. Watch for:

- "Step 1: Parameter Initialization — Done"

- "Step 2: Data Reduction — Done"

- "Step 3: Group ICA — Done"

- "Step 4: Back Reconstruction — Done"

If you see errors about memory, increase your SLURM memory allocation and restart.

## Step 4: View results

After analysis completes, click **"Display"** to open the visualization tools.

### Component Explorer

Shows all components as montages — multiple axial slices for each component. This is your first look at what ICA found. Browse through them:

- **Brain networks**: Clear, bilateral, anatomically plausible patterns in gray matter

- **Artifacts**: Edge effects, white matter/CSF patterns, single spots

### Orthogonal Viewer

Navigate through a single component slice by slice in three orthogonal views (axial, sagittal, coronal). Use this for detailed examination of promising components.

### Composite Viewer

Overlay multiple components simultaneously using different colors. Useful for seeing how networks relate spatially — do they overlap? Are they adjacent?

## What to look for in your results

With 20 components, you should be able to identify several major networks:

- **Default Mode Network**: Medial prefrontal + posterior cingulate (midline front-to-back)

- **Visual**: Occipital lobe (back of brain)

- **Sensorimotor**: Pre/post-central gyrus (strip across the top)

- **Auditory**: Superior temporal gyrus (sides of brain, near ears)

- **Frontoparietal**: Lateral frontal + parietal (left or right dominant)

You'll also see artifact components:

- **Motion**: Ring-like patterns at brain edges

- **CSF/Ventricles**: Activation in fluid-filled spaces

- **Vascular**: Intense focal spots near major blood vessels

## Output files

GIFT creates many output files in your results directory:

- `*_sub*.nii`: Subject-specific spatial maps

- `*_timecourses_*.nii`: Component timecourses

- `*_ica_c*.nii`: Group-level component images

- `*_pca_r*.mat`: PCA results

- `*_ica_parameter_info.mat`: All analysis parameters (for reproducibility)

## Resources for deeper learning

- 📄 [GIFT Manual — Section 3.9: Analysis Functions](https://trendscenter.org/software/gift/)

- 📄 [GIFT Manual — Section 3.10: Display GUI](https://trendscenter.org/software/gift/)

- 📄 [GIFT example datasets and tutorials](https://trendscenter.org/software/gift/)

- 🔗 [Cluster Workshop — ICA examples](https://github.com/trendscenter/ClusterWorkshop)
