---
task_name: "Debug and Troubleshoot ICA Analyses"
emoji: "🔍"
category: Analysis Methods
tier: Hands-On
order: 5
url: "https://trendscenter.org/software/gift/"
---
## Why this matters to you

ICA analyses fail. Components look wrong. Jobs crash. Results don't replicate. None of the other tasks teach you what to do when things go wrong — and things WILL go wrong. This task is your troubleshooting reference for the most common problems you'll encounter with GIFT, ICA, and the analysis pipeline.

## Problem: All ICA components look like noise/artifacts

### Possible causes and fixes

**Bad preprocessing**

- Did you preprocess the data at all? Load the input files in a viewer and check: Are they in MNI space? Are they smoothed?

- Check for excessive motion: Plot the motion parameters. If mean FD > 0.5mm, the data may be unsalvageable.

- Check spatial normalization quality: Overlay the normalized brain on the MNI template. Major misalignment means your normalization failed.

**Wrong number of components**

- Too few components (e.g., 5-10) will produce mixed components that look like noise because each is a blend of multiple networks

- Too many components (e.g., 200+) will split networks into tiny fragments and generate many noise components

- Try a standard number first (20 for exploratory, 53 for Neuromark, 75-100 for detailed analysis)

**Insufficient data**

- If your scan is very short (< 5 minutes / < 150 TRs), ICA may not have enough data to separate sources reliably

- Rule of thumb: at least 5 minutes of clean data (after censoring high-motion volumes)

**Data is corrupted**

- Check for NaN or Inf values in the NIfTI files

- Check that all subjects have the same spatial dimensions (ICA requires consistent matrix sizes)

## Problem: ICA doesn't converge

### What convergence means

ICA iteratively searches for the unmixing matrix. "Convergence" means the algorithm found a stable solution — components stopped changing between iterations. Non-convergence means it never stabilized.

### Possible causes and fixes

**Try a different algorithm**

- Infomax (default) usually converges well, but try FastICA or JADE for comparison

- If Infomax doesn't converge, the data may have unusual statistical properties

**Increase maximum iterations**

- In GIFT: Setup → Algorithm Parameters → increase max iterations (default is usually 512; try 1024 or 2048)

**Reduce the number of components**

- Requesting too many components relative to the data dimensionality can cause convergence problems

- Rule: number of components should be much less than the number of timepoints

**Check input data quality**

- A single corrupt subject can prevent group-level convergence

- Remove subjects one at a time to identify the problematic dataset

**Try multiple runs**

- ICA starts from random initial conditions. Run it 5-10 times with different random seeds. If most runs converge but a few don't, use the converged results. GIFT's ICASSO framework does this automatically.

## Problem: Group differences in FNC are not significant

**First, an important caveat**: a non-significant result does **not** automatically mean something went wrong. The most basic explanation is that **there may be no true group difference** to detect — a null result can be the correct answer, not a failure of your pipeline. Treat "no difference" as a legitimate scientific outcome, and use the checks below only to rule out *methodological* reasons for missing a real effect.

### Possible reasons you might miss a real effect

**Underpowered study**

- With small samples (< 30 per group), you won't have enough power to detect typical neuroimaging effect sizes (d ≈ 0.3-0.5)

- Calculate required sample size with G*Power before starting

**Many comparisons with strict correction**

- With 53 components, you have 1,378 FNC pairs. Correcting across all of them lowers sensitivity, so small true effects can fall below threshold — how much depends on the correction method and the effect size

- Consider hypothesis-driven approaches: test specific connections based on prior literature instead of testing everything

**Motion confounding**

- If patients move more than controls, apparent connectivity differences may be motion artifacts

- Include mean FD as a covariate and check if results survive

**Component selection**

- If you included artifact components, they add noise to the FNC matrix

- Re-run with only confirmed brain network components

## Problem: GIFT gives "Out of Memory" errors

### Fixes

**Increase SLURM memory allocation**

```shell
#SBATCH --mem=64G    # or even 128G for large datasets
```

**Estimate memory needs**

- Rule of thumb: memory ≈ (num_subjects × num_voxels × num_timepoints × 8 bytes) × 2-3x for working space

- Example: 100 subjects × 50,000 voxels × 200 timepoints × 8 bytes ≈ 80 GB → request 128-256 GB

**Reduce data dimensions**

- Use more aggressive PCA reduction (fewer principal components retained)

- Reduce the number of ICA components requested

- Use Neuromark (back-reconstruction only) instead of full Group ICA — requires much less memory

**Use batch/scripting mode**

- The GUI consumes additional memory for display. Run in `-nodisplay` mode for large analyses

## Problem: Component ordering differs between ICA runs

### Why this happens

ICA components come out in arbitrary order — there's no inherent "Component 1 is always DMN." Different random initializations produce different orderings. This is a fundamental property of ICA, not a bug.

### Fixes

**Use Neuromark templates**

- Neuromark's spatially constrained ICA (GIG-ICA) forces components to match the template order. Component 7 is always the same network across all subjects and all runs.

**Use ICASSO for stability**

- ICASSO runs ICA multiple times and clusters similar components, identifying which are stable (reproducible across runs) and which are unstable

**Spatial sorting**

- After ICA, sort components by spatial correlation with a reference template. GIFT's spatial sorting tool does this automatically.

**For publication**: Always describe how components were ordered and matched. "Components were ordered by spatial correlation with the Neuromark template (Iraji et al., 2019)."

## Problem: Preprocessing QC — how to verify it worked

### Check motion correction

- Plot motion parameters (rp_*.txt from SPM): Look for sudden jumps > 1mm

- Calculate framewise displacement: mean FD should be < 0.2mm for high-quality data

- Compare pre- and post-realignment: overlay two volumes that were misaligned — are they now aligned?

### Check coregistration

- Overlay functional (EPI) on structural (T1): Boundaries should match. Sulci in functional should align with sulci in structural.

- Common failure mode: the functional is flipped left-right relative to the structural

### Check normalization

- Overlay normalized brain on MNI template at several z-levels

- Check cortical boundaries, ventricle shapes, and brainstem alignment

- Common failure modes: severely stretched/compressed brain, failed skull stripping, incorrect tissue priors

### Check smoothing

- Compare smoothed and unsmoothed data: smoothed images should be visibly blurred

- Verify smoothing kernel was applied: `fslinfo smoothed_image.nii.gz` should show larger voxel dimensions or the header should match

## Problem: Different subjects give wildly different ICA results

### Possible causes

**Age/population differences**

- If your sample includes children and elderly adults, brain network organization differs substantially. Consider age-stratified analyses.

**Scanner differences (multi-site)**

- Different scanners produce different signal characteristics even with identical protocols

- Use site as a covariate or apply [ComBat harmonization](https://doi.org/10.1016/j.neuroimage.2017.11.024) to remove scanner effects

**Pathology**

- Patients with severe brain atrophy, lesions, or structural abnormalities may not fit the standard template

- Consider excluding subjects with gross structural abnormalities or running them separately

**Data quality variation**

- Some subjects may have marginal data quality that passes your threshold but still differs

- Run QC metrics for all subjects and look for outliers

## Quick reference: diagnostic checklist

When your analysis looks wrong, work through this list in order:

1. Check raw data quality (visual inspection, MRIQC metrics)

2. Verify preprocessing completed without errors (check log files)

3. Verify normalization quality (overlay on MNI template)

4. Check motion parameters (mean FD, max displacement)

5. Verify correct number of components was extracted

6. Check PCA variance explained (should be > 95%)

7. Run spatial sorting against Neuromark template

8. Compare a few components to known network anatomy

9. If FNC: verify Fisher z-transform was applied

10. If group comparison: check sample sizes and effect sizes

## Resources for deeper learning

- 📄 [GIFT Manual — troubleshooting section](https://trendscenter.org/software/gift/)

- 📄 [FSLeyes — viewer for inspecting brain images](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLeyes)

- 📑 [Himberg et al. (2004) — ICASSO: Validating ICA components by clustering and visualization](https://doi.org/10.1016/j.neuroimage.2003.10.015)

- 📑 [Fortin et al. (2018) — Harmonization of multi-site imaging data with ComBat](https://doi.org/10.1016/j.neuroimage.2017.11.024)
