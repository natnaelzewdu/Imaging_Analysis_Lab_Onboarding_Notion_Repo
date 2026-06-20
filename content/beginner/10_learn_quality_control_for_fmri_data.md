## Why this matters to you

Quality control (QC) is the most underappreciated step in neuroimaging. If bad data makes it into your analysis, your results are meaningless — no amount of sophisticated statistics can fix garbage input. Learning to spot bad data early will save you weeks of wasted analysis time and prevent embarrassing retractions. Every subject in every study should be quality-checked before inclusion.

## What can go wrong

Even with a cooperative participant and a well-functioning scanner, fMRI data can be compromised by:

- **Excessive head motion**: The #1 data killer. Motion causes signal changes that dwarf the BOLD effect and create systematic biases (motion-related connectivity artifacts)

- **Signal dropout**: Brain regions near air-tissue interfaces (orbitofrontal cortex, temporal poles) lose signal due to susceptibility artifacts. Some dropout is normal; extreme dropout is a problem

- **Ghosting**: Copies of the brain appearing as faint echoes in the phase-encoding direction, caused by scanner timing issues

- **Spikes**: Single volumes with dramatically different signal intensity, caused by RF interference, gradient coil issues, or sudden head motion

- **Drift**: Slow changes in overall signal intensity over the scan, caused by scanner instability or physiological changes

- **Incomplete brain coverage**: If the field of view doesn't cover the entire brain, you'll have missing data in certain regions

## Key quality metrics

### Framewise Displacement (FD)

[Framewise displacement](https://doi.org/10.1016/j.neuroimage.2011.10.018) is the single most important motion metric. It summarizes how much the head moved between consecutive volumes by combining all 6 motion parameters (3 translations + 3 rotations) into one number in millimeters.

- **FD < 0.2mm**: Excellent — minimal motion

- **FD 0.2-0.5mm**: Acceptable for most analyses

- **FD > 0.5mm**: Problem volumes — consider scrubbing (censoring) these timepoints

- **Mean FD > 0.5mm for entire run**: Consider excluding this subject

FD is particularly important because even after motion correction (realignment), motion-related signal changes persist and can create spurious connectivity patterns. This is why [Power et al. (2012)](https://doi.org/10.1016/j.neuroimage.2011.10.018) showed that motion artifacts in resting-state connectivity survived standard preprocessing.

### DVARS

DVARS measures the rate of signal change across the entire brain between consecutive volumes. The name stands for Derivative of VARiance. High DVARS at the same timepoints as high FD confirms motion-related signal changes. DVARS spikes without corresponding FD spikes may indicate scanner artifacts rather than motion.

### Temporal Signal-to-Noise Ratio (tSNR)

For each voxel, tSNR = mean signal / standard deviation of signal over time. Higher is better. Typical values:

- Gray matter: 40-100

- White matter: 50-150 (higher because it's more stable)

- Near sinuses: 10-30 (poor due to susceptibility)

Low tSNR regions have unreliable BOLD estimates. If a key region of interest has very low tSNR, results from that region are suspect.

### Signal dropout maps

Create images showing where signal is below a threshold. Signal dropout in regions you care about (e.g., orbitofrontal cortex for emotion studies) may be a deal-breaker.

## QC tools

### MRIQC

[MRIQC](https://mriqc.readthedocs.io/en/latest/) is an automated QC tool that generates visual reports and image quality metrics for both structural and functional MRI. It runs on BIDS-formatted data and produces:

- Individual subject reports with carpet plots, motion traces, and spatial maps

- Group-level reports comparing QC metrics across all subjects

- Machine-learning classifiers to flag potentially problematic scans

### fmriprep QC reports

If you preprocessed with fmriprep, it provides comprehensive HTML reports showing:

- Brain mask overlays on functional data

- Normalization quality (overlay on MNI template)

- Confound correlation matrices

- Carpet plots showing the full timeseries

### Manual inspection in GIFT

Even with automated tools, visual inspection is important:

- Load the preprocessed data and scroll through volumes looking for artifacts

- Check the ICA components after analysis — do the spatial maps look like brain networks or noise?

- Look at component timecourses for spikes or abnormal patterns

## Carpet plots (grayplots)

A [carpet plot](https://doi.org/10.1016/j.neuroimage.2016.08.009) shows the entire fMRI timeseries as a 2D image: voxels on the y-axis, time on the x-axis. This gives you a bird's-eye view of the data quality. Look for:

- **Vertical stripes**: Motion artifacts affecting many voxels simultaneously

- **Horizontal bands**: Voxels with persistently abnormal signal

- **Global signal fluctuations**: Slow waves affecting all voxels (may be respiratory or scanner drift)

Clean data should look like relatively uniform low-contrast noise. Prominent vertical stripes at specific timepoints are red flags.

## Motion handling strategies

When motion is detected, you have several options:

- **Scrubbing (censoring)**: Remove high-motion timepoints entirely from analysis. Typically remove volumes with FD > 0.5mm plus 1 volume before and 2 after. If more than 30% of volumes are censored, exclude the subject.

- **Regression**: Include motion parameters (and their derivatives and squares = 24 parameters) as confound regressors in the analysis model.

- **ICA-based denoising**: Use ICA to identify motion-related components and remove them. [ICA-AROMA](https://github.com/maartenmennes/ICA-AROMA) automates this.

- **Global signal regression**: Controversial but effective at removing motion artifacts. Introduces negative correlations, which complicates interpretation.

## QC for preprocessed data (often overlooked)

Most QC guides focus on raw data. But preprocessing itself can fail silently. After preprocessing, always verify:

### Coregistration quality

- Overlay the mean functional image on the T1 structural image. Sulci and gyri should align. If the functional looks shifted, flipped, or misaligned, coregistration failed.

- Common failure mode: left-right flip (functional is mirrored relative to structural)

### Normalization quality

- Overlay the normalized brain on the MNI template at several z-levels (z = -20, 0, +20, +40, +60)

- Check: Do the ventricles match? Do cortical boundaries align? Is the brainstem in the right place?

- Common failure modes: brain severely stretched/compressed, failed skull stripping (skull included in the brain mask), incorrect tissue priors

### Smoothing verification

- Compare an unsmoothed and smoothed volume side by side. The smoothed version should look visibly blurred but maintain the same overall brain shape.

### Post-preprocessing carpet plots

- Generate a carpet plot from the preprocessed data. Vertical stripes that survived preprocessing indicate persistent motion artifacts.

- Compare carpet plots before and after denoising — artifacts should be reduced.

## Lab Standard Practices

> **Important**: The lab has specific QC conventions. When in doubt, ask a senior lab member about the current standard QC pipeline and thresholds used for ongoing studies. Practices may vary across projects.

## Resources for deeper learning

- 📄 [MRIQC Documentation — full user guide](https://mriqc.readthedocs.io/en/latest/)

- 📺 [How to Check Your fMRI Data Quality](https://www.youtube.com/watch?v=sE3eNpBQa10)

- 📑 [Power et al. (2012) — Spurious Correlations from Motion in Resting-State fMRI](https://doi.org/10.1016/j.neuroimage.2011.10.018)

- 📑 [Power (2017) — A Simple but Useful Way to Assess fMRI Data Quality (Carpet Plots)](https://doi.org/10.1016/j.neuroimage.2016.08.009)

- 📑 [Parkes et al. (2018) — An Evaluation of the Efficacy of Denoising Strategies](https://doi.org/10.1016/j.neuroimage.2017.12.073)
