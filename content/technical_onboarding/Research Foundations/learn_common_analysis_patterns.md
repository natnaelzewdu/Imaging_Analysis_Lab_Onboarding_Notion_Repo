---
task_name: "Learn Common Analysis Patterns in the Lab"
emoji: "🔬"
tier: Theory
order: 7
url: "https://trendscenter.org/software/gift/"
---
## Why this matters to you

Now that you know the core methods (fMRI, ICA, Group ICA, brain networks), you need to understand how the lab actually uses them in research. There are recurring analysis patterns — pipelines that get applied across many different studies. Knowing these patterns will help you understand lab meetings, read lab papers faster, and design your own analyses.

## Pattern 1: Static Functional Network Connectivity (sFNC)

This is the simplest connectivity analysis. After running Group ICA, you have a set of timecourses — one per component per subject. Static FNC asks: how correlated are these timecourses across the entire scan?

### How it works

- Run Group ICA to get N components per subject (e.g., 53 Neuromark components)

- For each subject, compute the Pearson correlation between every pair of component timecourses

- This produces an N × N correlation matrix per subject (e.g., 53 × 53 = 1,378 unique pairs)

- Compare these matrices across groups (patients vs. controls) using statistical tests

### What it tells you

Which brain networks are talking to each other, and whether those connections differ between groups. For example: "In schizophrenia, the connection between DMN and frontoparietal network is weaker than in controls."

**Important**: Remember to Fisher z-transform correlations (arctanh) before running group statistics — raw Pearson r values are bounded and non-normal. Also, FNC correlations are computed from temporally autocorrelated timeseries, so the effective degrees of freedom are much lower than the number of TRs. GIFT accounts for this, but if you compute FNC manually, you must adjust.

For a deeper guide to reading and interpreting FNC matrices, see the "Interpret Functional Network Connectivity (FNC) Matrices" task.

### Limitations

Static FNC assumes connectivity is constant over the entire scan. But brain connectivity actually fluctuates moment to moment — which leads to the next pattern.

## Pattern 2: Dynamic Functional Network Connectivity (dFNC)

[Dynamic FNC](https://doi.org/10.1093/cercor/bhs261) captures how connectivity changes over time. This is one of the lab's most distinctive contributions to the field.

### How it works

- Start with component timecourses from Group ICA

- Slide a window (typically 30-44 seconds wide) across the timecourses, one TR at a time

- At each window position, compute the FNC matrix for just that time segment

- This gives you a sequence of FNC matrices over time — a "movie" of connectivity

### K-means clustering of states

The key innovation: apply [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering) to all the windowed FNC matrices (from all subjects). This reveals a small number (typically 4-6) of recurring connectivity "states" — distinct patterns that brains cycle through during rest.

**Practical warning**: K-means results depend on random initialization. Always run k-means multiple times (100+ repetitions with different seeds) and use the solution with the lowest sum of squared distances. Also try different values of k (2-7) and use the elbow method or silhouette scores to choose. GIFT's dFNC toolbox handles this, but understand that state definitions are not unique.

Each window gets assigned to a state, so you can answer questions like:

- How much time does a patient spend in State 3 vs. a control? (dwell time)

- How often do they switch between states? (transition frequency)

- Do they avoid certain states entirely? (occupancy rate)

### What it tells you

Brain connectivity is not static — it flows through different configurations. Clinical populations often show abnormal dynamics: schizophrenia patients may get "stuck" in a weakly connected state, while healthy controls transition fluidly between states.

## Pattern 3: Classification / Machine Learning

Many lab projects use brain features as input to classifiers — predicting diagnosis, age, cognitive scores, or treatment response from neuroimaging data.

### Typical pipeline

- Extract features: spatial maps (voxel values), FNC matrices, dFNC state features, or timecourse properties

- Select features: Reduce dimensionality to avoid overfitting (thousands of features but maybe hundreds of subjects)

- Train classifier: Support Vector Machine (SVM), deep learning (CNNs, autoencoders), or simpler methods like logistic regression

- Evaluate: Cross-validation (usually 5-fold or 10-fold) to get unbiased accuracy estimates

### Important considerations

- **Cross-validation is mandatory** — never report training accuracy

- **Feature leakage**: Make sure no information from test subjects leaks into training (e.g., through group ICA or normalization computed on all subjects)

- **Class imbalance**: Clinical datasets often have unequal group sizes; use balanced accuracy or AUC

- **Sample size**: Deep learning needs large datasets (hundreds to thousands); SVMs work with smaller samples

## Pattern 4: ICA + GLM (task-based)

When the lab does task-based studies (less common than resting-state), the pattern is:

- Run ICA to decompose the data into components

- Sort components to find task-related ones (using temporal correlation with the task design)

- Analyze task-related components at the group level using GLM-based statistics

This combines the data-driven nature of ICA with the hypothesis-testing power of GLM.

## Pattern 5: Neuromark pipeline

The increasingly standard approach in the lab:

- Take the pre-computed Neuromark template (53 components)

- Back-reconstruct to each subject using spatially constrained ICA (also called GIG-ICA)

- Compute sFNC and/or dFNC

- Run group comparisons or classification

This is fully automated using the [NeuroMark pipeline](https://doi.org/10.1016/j.nicl.2020.102375) and ensures consistency across studies.

## Pattern 6: Analysis of component spatial maps

FNC analyzes the *timecourses* of components, but the component **spatial maps** themselves carry information and are analyzed directly. After back-reconstruction, each subject has their own version of each component's spatial map (a loading value at every voxel).

### How it works

- For a given component (e.g., the DMN), take each subject's spatial map

- Run a voxel-wise group statistic across subjects — e.g., a one-sample t-test to show where the network is reliably present, or a two-sample t-test / regression to test where the map differs between groups or varies with a covariate (age, symptom severity)

- Correct for multiple comparisons across voxels (FDR, cluster-level, or permutation)

### What it tells you

Whether and *where* the spatial extent or strength of a network differs across subjects or groups. For example: "In schizophrenia, the DMN component shows reduced loading in posterior cingulate cortex." This is complementary to FNC — spatial-map analysis asks *where networks are and how strong they are*, while FNC asks *how networks interact*. GIFT's Mancovan toolbox supports spatial-map statistics alongside FNC, timecourse spectra, and amplitude measures.

## When to use ICA vs. GLM

| Scenario | Use |

|---|---|

| Resting-state data | ICA (no task design available) |

| Task data, known timing | GLM for hypothesis testing; ICA for exploration |

| Comparing brain networks across groups | Group ICA + FNC |

| Temporal dynamics | dFNC |

| Predicting diagnosis | ICA features + classifier |

| Preprocessing artifacts | ICA for artifact identification |

## Resources for deeper learning

- 📑 [Allen et al. (2014) — Tracking Whole-Brain Connectivity Dynamics](https://doi.org/10.1093/cercor/bhs261)

- 📄 [GIFT Manual — Sections 3.13.2 (Mancovan) and 3.13.3 (dFNC)](https://trendscenter.org/software/gift/)

- 📺 [Functional Connectivity Analysis explained](https://www.youtube.com/watch?v=KoikGwyFfBA)

- 📑 [Rashid et al. (2014) — Dynamic Connectivity States in Psychiatric Disorders](https://doi.org/10.3389/fnhum.2014.00897)

- 📑 [Du et al. (2020) — NeuroMark Pipeline](https://doi.org/10.1016/j.nicl.2020.102375)
