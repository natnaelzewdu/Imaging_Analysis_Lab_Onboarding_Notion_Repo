---
task_name: "Visualize & Sort ICA Components"
emoji: "👁️"
category: Analysis Methods
tier: Hands-On
order: 3
url: "https://trendscenter.org/software/gift/"
---
## Why this matters to you

After running Group ICA, you have a set of components — but which ones are real brain networks and which are noise? This is one of the most important skills in ICA-based neuroimaging. Learning to visually identify and sort components separates someone who can push buttons from someone who understands the science. Every analysis you do will require this step.

## GIFT's visualization tools

### Opening the Display GUI

After running ICA analysis in GIFT:

```matlab
>> gift
```

Click **"Display"** and select your analysis parameter file (`*_ica_parameter_info.mat`).

### Component Explorer

The Component Explorer shows all components as montage images — multiple axial slices per component. This gives you a quick overview of all components at once.

For each component, you'll see:

- The spatial map (where in the brain it activates)

- The mean timecourse

- The power spectrum (frequency content of the timecourse)

### Orthogonal Viewer

For detailed examination of a single component:

- Three views: axial (top-down), sagittal (side), coronal (front)

- Navigate by clicking on any view — the other two update

- Crosshairs show the current voxel location

- Useful for precisely identifying which brain structures a component covers

### Composite Viewer

Overlays multiple components in different colors on a single brain image:

- Helps you see how networks relate spatially

- Color-coded: each component gets a distinct color

- Useful for publications and presentations

## How to identify brain networks

> **Figure to add**: Insert a real ICA component montage here — ideally a GIFT/Neuromark spatial-map montage that shows examples of both a genuine network and an artifact component side by side. A task-activation map is misleading because it does not represent ICA output. Export one from your own analysis or ask a senior lab member.

### Visual features of real brain networks

1. **Gray matter localization**: Real networks are in gray matter (cortex, subcortical nuclei), not white matter or CSF

2. **Bilateral symmetry**: Most brain networks are roughly symmetric between left and right hemispheres

3. **Anatomical plausibility**: The pattern corresponds to known brain regions

4. **Smooth, contiguous clusters**: Clear spatial clusters rather than scattered noise

5. **Low-frequency timecourse**: Power spectrum peaks below 0.1 Hz (resting-state networks fluctuate slowly)

### Visual features of artifacts

1. **Brain edges**: Ring-like patterns at the boundary between brain and skull → motion artifact

2. **Ventricles**: Activation in the fluid-filled spaces inside the brain → CSF pulsation

3. **White matter**: Activation in deep white matter tracts → vascular or physiological noise

4. **Single hemisphere, inferior**: Activation near sinuses or ear canals → susceptibility artifact

5. **High-frequency timecourse**: Power spectrum dominated by frequencies > 0.1 Hz → physiological noise (breathing, heartbeat)

6. **Spiky timecourse**: Abrupt jumps or spikes → motion artifact

## Sorting components

### Temporal sorting (for task data)

If your data has a task design, you can sort components by how well their timecourse matches the expected task pattern:

1. In GIFT: Display → Sort Components → Temporal Sort

2. Select your task timing model (SPM design matrix or event timing file)

3. GIFT computes Multiple Linear Regression (MLR) between each component timecourse and the task model

4. Components are ranked by correlation with the task

High-correlation components are likely task-related. But don't discard low-correlation components — they may be interesting resting-state networks or modulate the task in unexpected ways.

### Spatial sorting (using templates)

More commonly used, especially for resting-state data:

1. In GIFT: Display → Sort Components → Spatial Sort

2. Select a reference template (Neuromark templates, or specific network masks)

3. GIFT computes spatial correlation between each component and each template

4. Components are matched to their best-fitting template

This automatically identifies which component is the DMN, which is visual, etc. However, always visually verify — the automatic matching isn't perfect.

## Manual classification workflow

For a thorough classification:

1. **View all components** in Component Explorer

2. **For each component**, decide: brain network or artifact?

3. **Label brain networks** by comparing to known network anatomy:

- Does it match any of the commonly used large-scale networks?

- Is it a sub-network (e.g., medial visual vs. lateral visual)?

4. **Label artifacts** by type: motion, CSF, white matter, vascular, susceptibility

5. **Document your decisions**: Which components you kept and why. This goes in your Methods section

## GIFT's Network Summary Tool

GIFT includes tools that automate some of this classification:

- **ICLabel**: Automatic component classification (brain, artifact subtypes)

- **Neuromark matching**: Spatial correlation with Neuromark's 53 components

These are good starting points but should always be verified manually, especially for components near the classification boundary.

## What to do with classified components

After classification:

- **Keep brain network components** for downstream analysis (FNC, dFNC, statistics)

- **Remove artifact components** when computing FNC — including motion or CSF components adds noise to your connectivity estimates

- **Report component selection** in your Methods: "Of 75 components, 53 were identified as brain networks based on spatial correlation with Neuromark templates and manual visual inspection"

## Additional visualization tools

### MRICroGL / MRICron

[MRICroGL](https://www.nitrc.org/projects/mricrogl) is an extremely useful standalone viewer for both fMRI and structural MRI data. It runs outside MATLAB and provides high-quality rendering of brain images with overlay support. Available for download on [NITRC](https://www.nitrc.org/projects/mricrogl).

### Dual-coded visualization

Standard brain images show only suprathreshold (significant) voxels — everything below the threshold is invisible. [Allen et al. (2012)](https://doi.org/10.1016/j.neuron.2012.05.001) introduced a dual-coded approach that shows both subthreshold trends (as a color gradient) AND suprathreshold regions (with contour lines), giving readers a much more complete picture of the results. Sample code for generating dual-coded images can be found in the Allen et al. (2012) paper. Contact lab members for implementation assistance.

### Connectograms

For visualizing functional network connectivity as circular connectivity plots:

- **Option 1**: [CircularGraph MATLAB function](https://www.mathworks.com/matlabcentral/fileexchange/48576-circulargraph) — or alternatively [Circos](http://circos.ca/)

- **Option 2**: From the GIFT toolbox, use the function `icatb_plot_connectogram`

### Writing data to NIfTI format

Before visualizing in any tool, your results need to be in NIfTI (.nii) format. GIFT provides functions for writing component maps and statistical results to NIfTI files. In MATLAB, you can also use `niftiwrite()` or SPM's `spm_write_vol()`.

## Resources for deeper learning

- 📄 [GIFT Manual — Section 3.10: Display GUI](https://trendscenter.org/software/gift/)

- 📄 [GIFT Manual — Section 3.11: Sorting Components](https://trendscenter.org/software/gift/)

- 📑 [Allen et al. (2011) — Component identification criteria](https://doi.org/10.3389/fnsys.2011.00002)

- 📑 [Iraji et al. (2019) — Neuromark network templates](https://doi.org/10.1002/hbm.24580)

- 📄 [GIFT Toolbox website — tutorials and examples](https://trendscenter.org/software/gift/)
