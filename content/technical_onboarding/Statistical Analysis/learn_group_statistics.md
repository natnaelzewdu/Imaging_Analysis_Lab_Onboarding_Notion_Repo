---
task_name: "Learn Group Statistics (t-tests, ANOVA)"
emoji: "📈"
tier: Theory
order: 2
url: "https://www.youtube.com/watch?v=0Nc1NyBmUPU"
---
## Why this matters to you

After running ICA and getting brain network components, you need statistical tools to answer the actual research questions: "Is this network different in patients compared to controls?" "Does connectivity change with age?" These questions require group-level statistics. Understanding t-tests, ANOVA, and how they're implemented in the GIFT toolbox will let you go from pretty brain maps to publishable scientific results.

## The big picture

In a typical ICA-based study, the statistical analysis flow is:

1. Run Group ICA → get components per subject

2. Extract features: spatial map values, timecourse amplitudes, FNC matrices

3. Run group statistics on these features to test your hypotheses

4. Correct for multiple comparisons

5. Report results with effect sizes and confidence intervals

## One-sample t-test

**Question**: "Is this ICA component significantly present across subjects?"

After back-reconstruction, each subject has a spatial map for each component. At every voxel, you have N values (one per subject). A one-sample t-test checks whether the mean across subjects is significantly different from zero.

**Example**: You have component #15 (looks like DMN). For each subject, the voxel at posterior cingulate cortex has a loading value. If the mean loading across 100 subjects is significantly > 0 (t = 12.3, p < 0.001), you confirm this component is consistently present in the group.

This is how you create group-level spatial maps — threshold the one-sample t-test results to show only significant voxels.

## Two-sample t-test

**Question**: "Does this component differ between two groups?"

**Example**: You compare spatial maps of the DMN between 50 schizophrenia patients and 50 healthy controls. At each voxel, you test whether the mean loading differs between groups. Voxels with significant differences indicate regions where the DMN is stronger or weaker in patients.

**For FNC**: Each subject has a 53 × 53 correlation matrix. At each cell (pair of components), you test whether the mean correlation differs between groups. This tells you which network connections are disrupted in the clinical group.

## ANOVA (Analysis of Variance)

**Question**: "Do three or more groups differ?"

When you have more than two groups (e.g., healthy controls, schizophrenia, bipolar disorder), a two-sample t-test can't compare all groups simultaneously. ANOVA tests whether there's any significant difference among the groups. If significant, you follow up with post-hoc pairwise tests (with correction for multiple comparisons) to identify which specific groups differ.

## Regression (continuous variables)

**Question**: "Does connectivity change with age/cognition/symptom severity?"

When your variable of interest is continuous rather than categorical, use regression instead of t-tests. For example: correlate each FNC value with age across subjects. This identifies connections that strengthen or weaken with aging.

## Check your assumptions — validity before significance

A p-value is only meaningful if the test's assumptions hold. Before trusting any t-test, ANOVA, or regression, verify:

- **Normality**: t-tests and ANOVA assume the residuals are approximately normally distributed. Check with histograms, Q–Q plots, or tests like Shapiro–Wilk. This matters most with small samples; with large samples the tests are fairly robust to mild departures.

- **Homogeneity of variance (homoscedasticity)**: Two-sample t-tests and ANOVA assume similar variance across groups. Check with Levene's test; if violated, use Welch's t-test or an equivalent correction.

- **Independence of observations**: Standard tests assume each data point is independent. This is frequently violated in neuroimaging — repeated measures, multiple scanner sites, family/sibling data, and temporally autocorrelated timeseries all break independence. Use mixed-effects models or otherwise account for the dependence structure.

- **Linearity** (for regression): the relationship between predictor and outcome should be approximately linear; check residual plots.

When assumptions are seriously violated, switch to alternatives: **non-parametric tests** (Mann–Whitney, Kruskal–Wallis), **permutation testing** (makes minimal distributional assumptions), or **robust / mixed-effects models**. Reporting a significant result from a test whose assumptions are violated can produce conclusions that don't replicate.

## The Mancovan toolbox in GIFT

GIFT includes the [Mancovan toolbox](https://trendscenter.org/software/gift/) for group-level statistics. MANCOVA (Multivariate Analysis of Covariance) extends standard statistics by:

- Testing multiple dependent variables simultaneously (e.g., all components at once)

- Including covariates (age, sex, site, motion) to control for confounds

- Applying FDR correction for multiple comparisons

- Outputting results as brain maps and tables

### How to use Mancovan in GIFT

1. After running Group ICA and back-reconstruction

2. Open GIFT → Stats → Mancovan

3. Define your design: groups, covariates

4. Select features to test: spatial maps, timecourses, spectra, or FNC

5. Run the analysis

6. View results: significant components, significant voxels within components

## Multiple comparisons (again)

Group ICA analyses involve massive multiple comparisons:

- 53 components × ~50,000 voxels per component = millions of tests for spatial map comparisons

- 53 × 52 / 2 = 1,378 FNC pairs for connectivity tests

- Multiply by number of contrasts and covariates

**FDR correction** is the standard approach in the lab. It controls the false discovery rate at q < 0.05, meaning that among all results called significant, no more than 5% are expected to be false positives.

**Permutation testing** is an alternative for small samples or when standard assumptions are violated. It shuffles group labels thousands of times to build an empirical null distribution. More computationally expensive but makes fewer assumptions.

## Covariates: what to control for

Almost every neuroimaging study needs to account for confounding variables:

- **Age**: Brain structure and connectivity change substantially across the lifespan

- **Sex**: Some brain networks show reliable sex differences

- **Head motion**: Even after preprocessing, residual motion effects can create group differences. Include mean FD as a covariate

- **Scanner site**: Multi-site studies must account for scanner differences (field strength, coil type, sequence parameters)

- **Intracranial volume**: For structural analyses, brain size affects almost everything

## Effect sizes

Statistical significance (p-values) tells you whether an effect exists, not how large it is. Always report effect sizes:

- **Cohen's d**: For group comparisons. d = 0.2 (small), 0.5 (medium), 0.8 (large)

- **Partial η²**: For ANOVA. How much variance the factor explains

- **Correlation r**: For regression. r = 0.1 (small), 0.3 (medium), 0.5 (large)

In neuroimaging, effect sizes tend to be small (d = 0.2-0.5), which is why large sample sizes are needed.

## Resources for deeper learning

- 📺 [Group Analysis in fMRI — Jeanette Mumford](https://www.youtube.com/watch?v=0Nc1NyBmUPU)

- 📄 [GIFT Manual — Section 3.12.4: Stats on Beta Weights](https://trendscenter.org/software/gift/)

- 📄 [GIFT Manual — Section 3.12.5: SPM Stats](https://trendscenter.org/software/gift/)

- 📺 [Multiple Comparisons Problem in fMRI — Mumford](https://www.youtube.com/watch?v=bWfY2g3gNLo)

- 📑 [Nichols & Holmes (2002) — Nonparametric Permutation Tests for Neuroimaging](https://doi.org/10.1002/hbm.1058)

- 📄 [FDR correction explained — Matthew Brett](https://matthew-brett.github.io/teaching/fdr.html)

- 📑 [Button et al. (2013) — Power Failure: Why Small Samples Undermine Neuroscience](https://doi.org/10.1038/nrn3475)

- 📄 [G*Power — free power analysis tool](https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower)
