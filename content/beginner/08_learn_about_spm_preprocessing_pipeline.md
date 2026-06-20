## Why this matters to you
[SPM (Statistical Parametric Mapping)](https://www.fil.ion.ucl.ac.uk/spm/) is a MATLAB-based software package that's been the standard in neuroimaging for over 25 years. The lab uses SPM for preprocessing fMRI data before running ICA in GIFT. Since SPM and GIFT both run in MATLAB, the workflow is seamless. Understanding SPM's preprocessing pipeline will help you troubleshoot data quality issues and know exactly what happened to your data before analysis.

## What SPM is
SPM is developed by the [Wellcome Centre for Human Neuroimaging](https://www.fil.ion.ucl.ac.uk/) at UCL (London). It's free, open-source, and runs in MATLAB. SPM handles the full neuroimaging pipeline: preprocessing, statistical analysis (GLM), and visualization. The current version is SPM12.

On the cluster, SPM is available as part of the MATLAB toolboxes:
```
>> addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));
```

## SPM's preprocessing steps in detail

### Realignment (motion correction)
SPM estimates rigid-body transformations (3 translations + 3 rotations = 6 parameters) for each volume relative to the first (or mean) volume. It uses a least-squares approach to minimize the difference between volumes.

What you get:
- Realigned images (prefix: r)
- A text file (rp_*.txt) with 6 motion parameters per timepoint — plot these to check for excessive motion
- A mean functional image (mean*.nii) used as reference for coregistration

**Practical tip**: Always look at the motion parameter plots. Sudden jumps > 1mm indicate the subject moved abruptly. Steady drift is less problematic but still adds noise.

### Coregistration
Aligns the mean functional image to the subject's T1 structural image (or vice versa). SPM uses mutual information as the cost function — this works well even though T1 and functional images have very different contrasts.

**Why this step matters**: The structural image has higher resolution and clearer anatomy. By linking functional and structural images, you get better normalization because the structural image provides the detailed anatomical information needed for accurate warping to MNI space.

### Segmentation
SPM segments the T1 structural image into tissue classes:
- Gray matter (GM)
- White matter (WM)
- Cerebrospinal fluid (CSF)
- Bone, soft tissue, air/outside

This step also estimates the non-linear deformation field — the warping parameters needed to transform this subject's brain into MNI template space. SPM uses a probabilistic atlas (tissue probability maps) as the reference.

What you get:
- Tissue probability maps (c1 = GM, c2 = WM, c3 = CSF)
- Forward deformation field (y_*.nii) — transforms native space → MNI
- Inverse deformation field (iy_*.nii) — transforms MNI → native space

### Normalization (spatial normalization)
Applies the deformation field from segmentation to warp the functional images into MNI space. After this step, all subjects' brains are in the same standard coordinate system.

SPM offers two normalization approaches:
- **Through segmentation** (recommended): Use the deformation field estimated during segmentation of the T1 image. More accurate because it uses the high-resolution structural anatomy.
- **Direct normalization**: Warp the functional images directly to an EPI template. Faster but less accurate.

Typical output voxel size: 2mm × 2mm × 2mm or 3mm × 3mm × 3mm (you choose). Smaller voxels preserve spatial detail but increase file size and computation time.

### Smoothing
Convolves each volume with a 3D Gaussian kernel. SPM asks for the kernel size in mm FWHM (Full Width at Half Maximum).

Common choices:
- 6mm FWHM: Standard for most analyses, good balance of SNR and spatial resolution
- 8mm FWHM: More smoothing, better for group analyses with large subject variability
- 4mm or less: Used when spatial precision matters (e.g., fine-grained cortical analyses)

**For ICA**: The lab typically uses 6mm smoothing or sometimes no smoothing at all, since ICA is less sensitive to noise and excessive smoothing can merge adjacent network components.

## The SPM batch editor
In practice, you don't run each step manually. SPM has a batch editor (accessible via `spm('defaults', 'fMRI'); spm_jobman('initcfg')`) where you chain steps together:

1. Open the SPM batch editor
2. Add modules: Realign → Coregister → Segment → Normalize → Smooth
3. Set the inputs: file paths, parameters
4. Save as a MATLAB script (for reproducibility)
5. Run the batch

For cluster processing, you'll typically write MATLAB scripts that call SPM functions programmatically rather than using the GUI.

## File naming conventions
SPM uses prefixes to track what's been done to each file:
- `f.nii` — original functional
- `rf.nii` — realigned
- `wrf.nii` — normalized (warped)
- `swrf.nii` — smoothed, normalized

So `swrf_sub01_run1.nii` means: smoothed → warped (normalized) → realigned → original functional data for subject 01, run 1.

## Resources for deeper learning
- 📄 [SPM Documentation — official manual](https://www.fil.ion.ucl.ac.uk/spm/doc/)
- 📺 [SPM12 Preprocessing Tutorial — step by step](https://www.youtube.com/watch?v=J_aT2M0e40g)
- 📄 [Andy's Brain Book — SPM preprocessing walkthrough](https://andysbrainbook.readthedocs.io/en/latest/SPM/SPM_Overview.html)
- 📑 [Ashburner & Friston (2005) — Unified Segmentation](https://doi.org/10.1016/j.neuroimage.2005.02.018)
- 📄 [A Practical Guide to fMRI Preprocessing Pipelines](https://doi.org/10.3389/fnins.2018.01007)
