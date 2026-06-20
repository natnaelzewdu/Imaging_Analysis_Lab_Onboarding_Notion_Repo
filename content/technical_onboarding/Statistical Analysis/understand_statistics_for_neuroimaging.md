---
task_name: "Understand Statistics for Neuroimaging"
emoji: "⚠️"
category: Statistical Analysis
tier: Theory
order: 3
url: "https://doi.org/10.1073/pnas.1602413113"
---
## Why this matters to you

Lab members come from many backgrounds — computer science, engineering, physics, psychology, neuroscience, and more — and neuroimaging statistics have unique pitfalls that everyday analysis or machine-learning intuitions don't cover. Understanding these issues prevents you from producing results that look impressive but are actually artifacts of poor statistical practice. Many published neuroimaging studies have been criticized or retracted for the exact issues covered here.

## The multiple comparisons catastrophe

This is THE central statistical problem in neuroimaging. When you run a statistical test at every voxel in the brain, you're performing tens of thousands of simultaneous tests.

### The math

- A typical brain image has ~50,000 gray matter voxels

- Testing each at p < 0.05 means: 50,000 × 0.05 = 2,500 expected false positives

- That's 2,500 voxels that look "significant" by pure chance

This isn't a theoretical concern — it's been spectacularly demonstrated. [Bennett et al. (2009)](https://doi.org/10.1016/S1053-8119(09)71202-9) famously found "significant brain activation" in a dead salmon by not correcting for multiple comparisons.

### Correction methods

- **Bonferroni**: Divide the significance threshold by the number of tests. For 50,000 voxels at α=0.05: threshold = 0.05/50,000 = 0.000001. This is very conservative when the number of tests is large, so little survives at the whole-brain voxel level. But Bonferroni should not be avoided on principle — when you are correcting across a small, well-defined set of tests (e.g., a handful of pre-specified FNC connections or ROIs), it is simple, exact, and entirely appropriate. Match the correction to the number of comparisons you are actually making.

- **Random Field Theory (RFT)**: Exploits spatial smoothness — neighboring voxels aren't independent, so the effective number of tests is much less than 50,000. SPM uses this. Requires sufficient smoothing to work correctly.

- **False Discovery Rate (FDR)**: Instead of controlling the chance of ANY false positive (like Bonferroni), FDR controls the PROPORTION of false positives among significant results. At q=0.05, you accept that 5% of your "significant" results are false. Much more powerful than Bonferroni while still being principled.

- **Permutation testing**: Randomly shuffle group labels thousands of times, recompute the test statistic each time, and build an empirical null distribution. Makes no assumptions about the data distribution. Computationally expensive but the gold standard.

- **Cluster-level correction**: Threshold at a lenient voxel level (e.g., p < 0.001 uncorrected), then ask whether clusters of contiguous significant voxels are larger than expected by chance. Common but has been [criticized for inflated false positive rates with certain thresholds](https://doi.org/10.1073/pnas.1602413113).

### What the lab uses

Most lab publications use FDR correction at q < 0.05 for FNC analyses (correcting across component pairs) and voxel-level FDR or permutation testing for spatial map comparisons.

## Temporal autocorrelation — the hidden violation

fMRI timeseries are NOT independent observations. Each timepoint is correlated with the next because:

- The hemodynamic response is slow (peaks at 5-6 seconds), so BOLD values at consecutive TRs are similar

- Low-frequency physiological fluctuations (breathing, heart rate) create slow drifts

- Scanner drift adds additional temporal correlation

### Why this matters

Most standard statistical tests (t-tests, correlations) assume independent observations. If you compute a correlation between two timeseries of 200 TRs, the effective sample size might be only 20-30 independent observations, not 200. This means:

- Standard p-values are WAY too small (anti-conservative)

- Confidence intervals are too narrow

- You get false confidence in effects that don't exist

### How to handle it

- **Prewhitening**: Model the autocorrelation structure and remove it before statistical testing. SPM and FSL do this automatically in first-level GLM analysis.

- **Adjusted degrees of freedom**: Use the Bartlett correction or effective degrees of freedom to account for reduced independence.

- **For connectivity**: When computing FNC correlations, the effective degrees of freedom are much smaller than the number of timepoints. GIFT accounts for this in its statistical tools.

## Power analysis — how many subjects do you need?

Statistical power is the probability of detecting a real effect. In neuroimaging, most studies are chronically underpowered.

### The reality

- [Button et al. (2013)](https://doi.org/10.1038/nrn3475) estimated the median statistical power in neuroscience studies at ~20% — meaning 80% of real effects are MISSED

- A typical fMRI effect size for group differences is Cohen's d = 0.3-0.5 (small to medium)

- To detect d = 0.5 with 80% power in a two-sample t-test: you need ~64 subjects PER GROUP (128 total)

- To detect d = 0.3: you need ~175 per group (350 total)

### Rules of thumb for the lab

| Analysis type | Minimum subjects | Recommended |

|---|---|---|

| Group ICA (exploratory) | 20-30 | 50+ |

| Two-group comparison (patients vs. controls) | 50 per group | 100+ per group |

| Classification (ML) | 100 total | 200-500 total |

| Dynamic FNC states | 50+ | 100+ |

| Brain-behavior correlation | 80+ | 200+ |

### What to do about underpowered studies

- Report effect sizes (Cohen's d, partial η²) alongside p-values — always

- Use power analysis tools ([G*Power](https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower), Python's `statsmodels`) to plan sample sizes BEFORE collecting data

- If your sample is small, be transparent about limitations and avoid overclaiming

## Correlation vs. causation in connectivity

Functional connectivity means "correlated BOLD timeseries." It does NOT mean:

- Brain region A causes activity in brain region B

- There is a direct anatomical connection between A and B

- The two regions are working together on the same task

Correlation can arise from:

- Direct neural interaction (what we hope to measure)

- Shared input from a third region (confound)

- Global signals (respiration, heart rate, scanner drift)

- Residual motion artifacts

When you see "reduced connectivity between DMN and frontoparietal network in schizophrenia," this means their BOLD signals are less correlated — not that there's a broken wire between them. The neurobiological interpretation requires additional evidence.

## Reverse inference — the logical fallacy

"We observed activation in the amygdala, therefore the subjects were experiencing fear."

This is reverse inference, and it's logically invalid. The amygdala activates during fear, but also during positive emotions, novelty, uncertainty, and attention. Observing amygdala activation doesn't tell you which process caused it.

### The correct logic

- **Forward inference** (valid): "We induced fear → we expect amygdala activation → we observe it → consistent with our hypothesis"

- **Reverse inference** (invalid): "We observe amygdala activation → therefore fear was experienced"

Tools like [Neurosynth](https://neurosynth.org/) can help by showing how selectively a region is associated with a particular function. If a region activates in only 5% of studies but 80% of fear studies, reverse inference is more plausible (but still not proof).

## Covariates — when to include them and when NOT to

Including covariates (age, sex, motion, site) in your statistical model can remove confounds — but including the WRONG covariates creates bias.

### When to include

- **Confounders**: Variables that influence both your independent variable and your outcome. Example: age affects both brain connectivity AND cognitive scores. Include it.

- **Nuisance variables**: Variables that add noise but don't confound. Example: scanner site affects signal quality but not diagnosis. Including it reduces noise and increases power.

### When NOT to include

- **Mediators**: Variables on the causal pathway between your independent and dependent variable. Example: if medication affects brain connectivity in schizophrenia patients, including medication status as a covariate removes the very effect you're trying to study.

- **Colliders**: Variables caused by both your independent and dependent variable. Including a collider creates spurious associations. This is subtle but dangerous.

### Practical rule

Draw a causal diagram (directed acyclic graph / DAG) before deciding on covariates. If you can't justify why a covariate should be included based on causal reasoning, leave it out.

## Reporting standards — what you MUST include

The [COBIDAS guidelines](https://doi.org/10.1038/nn.4500) (Committee on Best Practices in Data Analysis and Sharing) specify what neuroimaging papers must report:

- Sample size and how it was determined (power analysis)

- Exact statistical tests with software versions and parameters

- Effect sizes for all reported results

- Correction method for multiple comparisons with exact thresholds

- Motion exclusion criteria applied before analysis

- Number of subjects excluded and reasons

## Resources for deeper learning

- 📑 [Button et al. (2013) — Power Failure: Why Small Sample Size Undermines Neuroscience](https://doi.org/10.1038/nrn3475)

- 📑 [Eklund et al. (2016) — Cluster Failure: False Positive Rates in fMRI](https://doi.org/10.1073/pnas.1602413113)

- 📑 [Bennett et al. (2009) — Neural Correlates in a Dead Salmon (the famous example)](https://doi.org/10.1016/S1053-8119(09)71202-9)

- 📄 [COBIDAS Reporting Guidelines](https://doi.org/10.1038/nn.4500)

- 📺 [Multiple Comparisons in fMRI — Jeanette Mumford](https://www.youtube.com/watch?v=bWfY2g3gNLo)

- 📄 [G*Power — free power analysis tool](https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower)

- 📄 [FDR correction explained — Matthew Brett](https://matthew-brett.github.io/teaching/fdr.html)
