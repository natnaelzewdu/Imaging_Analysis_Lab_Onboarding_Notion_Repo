## Why this matters to you

The General Linear Model (GLM) is the workhorse statistical framework of neuroimaging — ordinary linear regression applied to brain data. It is most famous for task-based fMRI, but the same model also underlies group analyses, regressions against behaviour, and many of the statistics in the lab's ICA pipelines (t-tests and ANOVA are both special cases of the GLM). While the lab primarily uses ICA (which is model-free for decomposition), you'll encounter the GLM constantly in papers and in your own group statistics, and understanding it will help you appreciate how the two approaches complement each other.

## What the GLM does

The GLM is a general statistical framework — ordinary multiple linear regression — for explaining a measured signal as a weighted sum of one or more predictors. It is **not** specific to task fMRI, and it does **not** require a task design. The same machinery is used for first-level task analysis, for group/second-level analyses (one-sample and two-sample t-tests, ANOVA), and for regressing brain measures against continuous variables like age or symptom scores. A t-test and an ANOVA are both special cases of the GLM.

A common first-level use is task fMRI: you have a timeseries at each voxel (say, 200 timepoints) and a design describing the experiment (e.g., the subject saw a flashing checkerboard for 20 seconds, then rest for 20 seconds, repeated 5 times). The GLM tests whether the voxel's signal goes up when the checkerboard is on and down when it's off. But the predictors in X can equally be group membership, age, motion, or any covariate — there does not need to be a "task" at all.

Mathematically: Y = X × β + ε

- **Y**: The observed BOLD timeseries at one voxel (200 × 1 vector)

- **X**: The design matrix — your model of what the signal SHOULD look like if the voxel is involved in the task

- **β**: The parameter estimates — how much each column of X contributes to the signal (what we want to estimate)

- **ε**: The residual error — whatever the model doesn't explain

The GLM is fit independently at every voxel in the brain (this is called a "mass univariate" approach). With ~50,000 voxels, you're running 50,000 separate regressions.

## The design matrix

The design matrix X is the heart of the GLM. Each column represents one experimental condition or confound:

### Task regressors

For a simple block design (checkerboard on/off):

1. Create a boxcar function: 1 when checkerboard is on, 0 when off

2. Convolve this boxcar with the Hemodynamic Response Function (HRF) — because the BOLD response is delayed and smoothed relative to neural activity

3. The result is your task regressor — what the BOLD signal would look like if the voxel perfectly followed the task

For event-related designs (brief stimuli like single button presses), each event is a delta function convolved with the HRF.

### Confound regressors

Additional columns account for nuisance signals:

- 6 motion parameters from realignment

- Linear/polynomial drift terms

- Physiological noise regressors (CompCor components from white matter and CSF)

- Outlier/scrubbing regressors (one column per censored timepoint)

## Contrasts: asking specific questions

After estimating β for each condition, you use contrasts to ask specific questions:

- **"Does visual cortex activate during checkerboards?"** → test if βcheckerboard > 0

- **"Is the response to faces stronger than houses?"** → test if βfaces - βhouses > 0

- **"Are motor regions active for any movement?"** → test if (βleft_hand + βright_hand) / 2 > 0

Each contrast produces a t-statistic at every voxel. Apply a statistical threshold (correcting for multiple comparisons across 50,000 voxels), and you get a thresholded statistical map showing which brain regions are "significantly" involved.

## Multiple comparisons: the critical challenge

With 50,000 voxels, testing each at p < 0.05 would yield ~2,500 false positives by chance alone. Common corrections:

- **Bonferroni**: Divide α by the number of voxels. Very conservative — almost nothing survives.

- **Random Field Theory (RFT)**: SPM's approach. Uses the spatial smoothness of the data to estimate the effective number of independent tests. Less conservative than Bonferroni.

- **False Discovery Rate (FDR)**: Controls the expected proportion of false positives among all significant voxels. A good balance between sensitivity and specificity.

- **Cluster-level correction**: First threshold at a lenient voxel level (e.g., p < 0.001), then test whether clusters of contiguous suprathreshold voxels are larger than expected by chance. Note: [Eklund et al. (2016)](https://doi.org/10.1073/pnas.1602413113) showed that certain cluster thresholds (particularly p < 0.01 uncorrected) lead to inflated false positive rates. Use p < 0.001 uncorrected as the minimum cluster-forming threshold.

### Temporal autocorrelation — a hidden assumption violation

GLM assumes that the error terms (residuals) at each timepoint are independent. But fMRI data is heavily temporally autocorrelated — each timepoint is correlated with the next due to the slow hemodynamic response, physiological fluctuations, and scanner drift. Without correction, this makes standard errors too small and p-values too optimistic.

SPM and FSL handle this by "prewhitening" — estimating the autocorrelation structure and removing it before computing statistics. But the correction isn't perfect, especially for short scanning sessions. Always be aware that fMRI statistics are approximate, and marginal results (p ≈ 0.05) should be interpreted cautiously.

### Reverse inference — the logical trap

When interpreting GLM results, beware of reverse inference: "We saw activation in region X, therefore the subject was doing cognitive process Y." This is logically invalid because most brain regions are involved in MANY different processes. Amygdala activates during fear, but also positive emotion, novelty, and attention. Just because a region lit up doesn't tell you what caused it. Valid inference goes the other direction: "We designed a task to elicit process Y, and observed activation in region X, which is consistent with our hypothesis."

## First-level vs. second-level analysis

GLM is done in two stages:

### First level (single subject)

- Fit the GLM at every voxel for one subject

- Produces contrast maps (statistical maps) for that subject

- One analysis per subject

### Second level (group analysis)

- Takes the first-level contrast maps from all subjects

- Performs group statistics:

- One-sample t-test: "Is this contrast significant across the group?"

- Two-sample t-test: "Do patients and controls differ?"

- ANOVA: "Do three or more groups differ?"

- This is where you draw population-level conclusions

## GLM vs. ICA: when to use each

| Feature | GLM | ICA |

|---|---|---|

| Requires task design | No (a task is just one possible design) | No |

| Data-driven | No (model-based) | Yes |

| Finds unexpected patterns | No (only tests what you model) | Yes |

| Resting-state data | Not applicable | Ideal |

| Statistical inference | Built-in (t-tests, F-tests) | Requires additional steps |

| Artifact separation | Needs explicit modeling | Automatic |

| Sensitivity | High for modeled effects | May split effects across components |

The lab uses ICA as the primary method because most work is with resting-state data. But when task data is available, combining ICA (to find components) with GLM (to test task-relatedness of components) is a powerful approach.

## Note on statistical approaches in the lab

> Statistical methods vary across studies in the lab. The choice of correction method (FDR, cluster-level, etc.) depends on the specific research question and dataset. Consult with your PI and review the methods of prior lab publications for guidance on what is appropriate for your analysis.

## Resources for deeper learning

These existing resources provide excellent coverage — recommended over trying to learn from scratch:

- 📺 [GLM for fMRI — Jeanette Mumford (excellent walkthrough)](https://www.youtube.com/watch?v=gRhM04LfA2E)

- 📺 [Design Matrices Explained — Mumford Brain Stats](https://www.youtube.com/watch?v=OYNlUQlMSBY)

- 📄 [Andy's Brain Book — First-Level Analysis with GLM](https://andysbrainbook.readthedocs.io/en/latest/fMRI_Short_Course/fMRI_05_1stLevelAnalysis.html)

- 📺 [Principles of fMRI — GLM lectures](https://www.youtube.com/playlist?list=PLfXA4opIOVrGHncHRxI3Qa5GeCSudwmxM)

- 📄 [Wikipedia: General Linear Model](https://en.wikipedia.org/wiki/General_linear_model)

- 📑 [Friston et al. (1994) — Statistical Parametric Maps in Functional Imaging](https://doi.org/10.1002/hbm.460020402)
