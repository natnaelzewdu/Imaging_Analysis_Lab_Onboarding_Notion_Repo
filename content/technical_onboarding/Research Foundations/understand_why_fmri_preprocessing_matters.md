---
task_name: "Understand Why fMRI Preprocessing Matters"
emoji: "🔧"
tier: Theory
order: 9
url: "https://andysbrainbook.readthedocs.io/en/latest/fMRI_Short_Course/fMRI_04_Preprocessing.html"
---
## Why this matters to you

Raw fMRI data is noisy, distorted, and misaligned. If you analyze it directly, your results will be dominated by artifacts rather than brain activity. Preprocessing is the set of steps that cleans the data and puts it into a standard format before analysis. Every fMRI study — whether ICA, GLM, or connectivity — requires preprocessing first. Understanding what each step does (and what can go wrong) is critical for producing trustworthy results.

## What's wrong with raw data?

When fMRI data comes off the scanner, it has several problems:

- **Head motion**: Even small movements (< 1mm) cause large signal changes. A voxel that was gray matter at time T might be white matter at time T+1 if the head moved. Motion is the single biggest source of artifacts in fMRI.

- **Slice timing differences**: The scanner doesn't acquire the whole brain simultaneously. It collects one 2D slice at a time, taking 1-2 seconds to cover all slices. The bottom slice and top slice were acquired at different times within the same TR.

- **Spatial distortion**: The magnetic field isn't perfectly uniform, especially near air-tissue interfaces (sinuses, ear canals). This warps the images in predictable ways.

- **Each subject's brain is different**: Brains vary in size, shape, and folding patterns. To compare across subjects, data must be transformed into a common space.

- **Low signal-to-noise ratio**: The BOLD signal change is only 1-3%. It sits on top of physiological noise (breathing, heartbeat), thermal noise from the scanner, and slow signal drifts.

## The standard preprocessing steps (in order)

### 1. Slice timing correction

Adjusts the timing of each slice so they appear as if all slices were acquired simultaneously. Uses temporal interpolation to shift each slice's timeseries by the appropriate fraction of a TR. Some modern approaches skip this step and instead include slice timing as a regressor in the analysis model.

### 2. Motion correction (realignment)

Estimates the 6 parameters of rigid-body motion (3 translations: x, y, z; 3 rotations: pitch, roll, yaw) for each volume relative to a reference volume (usually the first or middle volume). Each volume is then spatially transformed to align with the reference. This produces a set of motion parameters that are also saved for later use as confound regressors.

**Key detail**: Motion correction fixes the images but doesn't remove motion-related signal changes. Spin-history effects (changes in magnetization due to movement through the magnetic field) persist even after realignment. This is why motion parameters are included as regressors in analysis.

### 3. Coregistration

Aligns the functional (fMRI) images to the structural (T1) image of the same subject. The functional images are low-resolution and have distortions; the structural image is high-resolution and anatomically detailed. Coregistration links the two so you know exactly which brain structures each functional voxel corresponds to.

### 4. Spatial normalization

Transforms each subject's brain into a standard template space — usually [MNI (Montreal Neurological Institute)](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009) space. This involves non-linear warping: stretching, compressing, and bending the brain to match the template. After normalization, the same coordinate (e.g., MNI x=0, y=-52, z=26) refers to approximately the same brain structure in every subject.

This step is essential for group analysis. Without it, you can't average or compare brain maps across subjects because their brains don't line up.

### 5. Spatial smoothing

Blurs each volume with a 3D Gaussian kernel (typically 6-8mm FWHM — Full Width at Half Maximum). This seems counterintuitive — why blur your data? Three reasons:

- Increases signal-to-noise ratio by averaging neighboring voxels

- Accounts for small remaining misalignments between subjects

- Makes the data conform better to the statistical assumptions of later analysis (random field theory)

Note: For ICA, some labs use less smoothing (or none) because ICA can handle unsmoothed data and excessive smoothing can blur out fine spatial features of networks.

## What "good" vs. "bad" preprocessing looks like

After preprocessing, you should check:

- **Motion parameters**: Subjects with head motion > 3mm translation or 3° rotation are typically excluded. Even smaller motion can be problematic.

- **Normalization quality**: Overlay the normalized brain on the template — major misalignments mean the warping failed.

## Critical warning: preprocessing does NOT fully remove motion artifacts

A common misconception is that motion correction (realignment) eliminates motion problems. It does NOT. Realignment corrects the spatial misalignment, but:

- **Spin-history effects**: When the head moves through the magnetic field, the magnetization state of tissue changes. Realignment can't fix this because it's a signal change, not a spatial change.

- **Residual motion-related signal**: [Power et al. (2012)](https://doi.org/10.1016/j.neuroimage.2011.10.018) showed that motion artifacts in resting-state connectivity survive standard preprocessing. Even after realignment and regressing out 6 motion parameters, systematic distance-dependent connectivity biases remain.

- **What to do**: Use expanded motion regressors (24 parameters: 6 motion + their derivatives + squares of both), scrub high-motion volumes (framewise displacement > 0.5mm), and always include mean FD as a covariate in group analyses. For connectivity studies, consider ICA-based denoising ([ICA-AROMA](https://github.com/maartenmennes/ICA-AROMA)).

- **Signal dropout**: Check for regions with no signal (black holes), especially in orbitofrontal and temporal pole areas near sinuses.

- **Temporal SNR**: Compute the mean signal divided by the standard deviation over time for each voxel. Low tSNR regions have unreliable data.

Quality control is so important that the next tasks cover it specifically.

## How this connects to what you'll do

In the lab, preprocessing is typically done with either SPM or fmriprep before data enters the ICA pipeline. When you run GIFT, your input data should already be preprocessed. Understanding what has been done (and whether it was done well) is essential for troubleshooting unexpected results.

## Key External Resources

Rather than reinventing the wheel, leverage these excellent existing resources for deeper understanding:

- 📺 [Andy's Brain Blog — fMRI Preprocessing (video series)](https://www.youtube.com/watch?v=Qy4Jrgx3KSg) — highly recommended first stop

- 📄 [Andy's Brain Book — Preprocessing Chapter](https://andysbrainbook.readthedocs.io/en/latest/fMRI_Short_Course/fMRI_04_Preprocessing.html)

- 📑 [A Hitchhiker's Guide to Functional Magnetic Resonance Imaging](https://doi.org/10.3389/fnins.2016.00515) — accessible overview of fMRI fundamentals

- 📺 [Principles of fMRI — Preprocessing lectures (Tor Wager & Martin Lindquist)](https://www.youtube.com/playlist?list=PLfXA4opIOVrGHncHRxI3Qa5GeCSudwmxM)

- 📺 [Motion Correction explained](https://www.youtube.com/watch?v=bP-dPLJuFfc)

- 📄 [MNI template and standard space](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009)

- 📑 [Power et al. (2012) — Spurious Correlations in Resting-State fMRI Due to Motion](https://doi.org/10.1016/j.neuroimage.2011.10.018)
