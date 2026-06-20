---
task_name: "Interpret Functional Network Connectivity (FNC) Matrices"
emoji: "📊"
category: Research Foundations
tier: Theory
order: 8
url: "https://doi.org/10.1093/cercor/bhs261"
---
## Why this matters to you

After running Group ICA, you compute Functional Network Connectivity (FNC) — correlation matrices showing how strongly each pair of brain networks is connected. The term is deliberately *functional **network** connectivity*: it describes connectivity **between ICA-derived networks (components)**, which is distinct from voxel- or seed-level "functional connectivity." A matrix of 1,378 numbers (53 × 52 / 2 for Neuromark) is meaningless until you can read it. This task teaches you what the numbers mean, what patterns to expect, and how to interpret group differences — the bridge between computation and neuroscience.

## What an FNC matrix actually represents

Each cell in an FNC matrix contains the Pearson correlation between two ICA component timecourses for one subject. A value of:

- **+1.0**: Perfect positive correlation — the two networks activate and deactivate together

- **0.0**: No relationship — the networks fluctuate independently

- **-1.0**: Perfect negative correlation (anticorrelation) — when one activates, the other deactivates

Typical FNC values range from about -0.4 to +0.7 in resting-state fMRI. Very few connections reach extreme values.

## The structure of a well-organized FNC matrix

When using Neuromark's 53 components organized into 7 domains, the FNC matrix has a characteristic structure:

### Within-domain blocks (along the diagonal)

Components within the same functional domain (e.g., all visual components, all default mode components) tend to be positively correlated with each other. These appear as warm-colored (red/yellow) blocks along the diagonal of the FNC matrix.

This makes sense: sub-networks of the visual system (medial visual, lateral visual, occipital pole) fluctuate together because they're all involved in visual processing.

### Between-domain patterns (off-diagonal)

Connections between different domains follow known neurobiological patterns:

| Connection | Expected pattern | Why |

|---|---|---|

| DMN ↔ Visual | Weak negative (anticorrelation) | Task-negative (DMN) vs. task-positive (visual) |

| DMN ↔ Frontoparietal | Negative | DMN deactivates during focused cognition |

| Sensorimotor ↔ Auditory | Positive | Often co-activate during interactive tasks |

| Subcortical ↔ Sensorimotor | Positive | Basal ganglia involved in motor control |

| DMN ↔ DMN | Strong positive | Within-domain consistency |

| Salience ↔ DMN | Negative | Salience network switches between DMN and task-positive networks |

### The anti-correlation debate

DMN-frontoparietal anticorrelation is one of the most studied findings in resting-state fMRI. However, [Murphy et al. (2009)](https://doi.org/10.1152/jn.90777.2008) showed that global signal regression (a preprocessing step) can artificially introduce anticorrelations. If your study uses global signal regression, interpret negative FNC values with caution.

## Reading an FNC matrix — step by step

When you generate or see an FNC matrix:

1. **Check the diagonal blocks first**: Are within-domain correlations positive? If not, something may be wrong with your component ordering or domain assignment.

2. **Look for the DMN-task pattern**: DMN components should show negative correlations with attention and executive control networks. This is the most replicated finding in resting-state connectivity.

3. **Identify outlier connections**: Any extremely strong correlation (> 0.7) between components from different domains is suspicious — it might indicate two components that should be one, or a motion/physiological artifact.

4. **Check for motion contamination**: If ALL connections are uniformly shifted positive, global motion artifacts may be present. Compare high-motion and low-motion subjects.

## Group differences in FNC — what they mean

The typical research question: "Do patients with schizophrenia have different connectivity than healthy controls?"

### What "weaker connectivity" means

"Patients showed reduced FNC between DMN and frontoparietal network" means:

- The Pearson correlation between these networks' timecourses is lower (closer to zero) in patients

- The networks are more functionally independent in patients

- This does NOT mean a physical connection is broken

- Possible interpretations: altered neural synchrony, disrupted communication, compensatory reorganization

### What "stronger connectivity" means

Increased FNC can mean:

- Hyperconnectivity — networks that should operate independently are pathologically coupled

- Compensatory mechanism — the brain recruits additional connections to maintain function

- Reduced segregation — loss of the normal pattern of distinct, separable networks

### Be careful with interpretation

- A statistically significant group difference might be tiny in absolute terms (Δr = 0.05). Report effect sizes alongside p-values.

- Significant connectivity differences at the group level don't diagnose individuals — there's enormous overlap between groups.

- Always consider whether motion differences between groups could explain the connectivity differences (patients often move more than controls).

## Dynamic FNC interpretation

When you compute dFNC with sliding windows and k-means clustering, you get "states" — recurring connectivity patterns.

### What the states look like

- **State 1 (typical)**: Sparse connections, weakly connected — often the most common state at rest

- **State 2 (strongly connected)**: Many strong positive and negative connections — a highly organized configuration

- **State 3-5**: Various intermediate patterns

### What the state metrics mean

- **Dwell time**: How long a subject stays in each state. Patients might spend more time in a weakly connected state.

- **Transition frequency**: How often subjects switch between states. Higher frequency = more dynamic brain. Some disorders show reduced dynamics (getting "stuck").

- **Occupancy rate**: Fraction of time spent in each state. Some states may be entirely absent in certain groups.

- **Transition probabilities**: Given that you're in State A, what's the probability of transitioning to State B vs. C?

## Visualizing FNC for publications

For papers and presentations:

- Use the Neuromark domain structure to organize the matrix (group components by functional domain)

A well-organized FNC matrix (using the Neuromark domain structure) will show warm diagonal blocks (within-domain positive correlations) and characteristic off-diagonal patterns (DMN anticorrelated with sensory networks). You can plot one in MATLAB with:

```matlab
% Basic FNC matrix plot
imagesc(fnc_matrix);         % fnc_matrix is N_comp x N_comp
colormap(bluewhitered);      % diverging colormap centered at 0
colorbar; clim([-0.5 0.5]);
xticks(1:N); yticks(1:N);
xticklabels(component_labels); yticklabels(component_labels);
title('Mean FNC Matrix');
```

- Use a diverging colormap (e.g., blue-white-red) centered at zero

- Always include a colorbar with units (Pearson r)

- For group differences, show the difference matrix (patients minus controls) with significance masking

- Consider chord diagrams or circos plots for visualizing specific significant connections

## Common mistakes in FNC analysis

- **Not Fisher z-transforming correlations** before group statistics. Pearson r is bounded [-1, 1] and non-normally distributed. Apply Fisher z-transform (arctanh) before t-tests or ANOVA.

- **Including artifact components in FNC**. If you include motion or CSF components, their correlations with brain networks add noise or spurious connections.

- **Ignoring the effective degrees of freedom**. With 200 TRs but temporally autocorrelated data, the effective sample size for each correlation might be 30-40, not 200. This inflates significance.

- **Cherry-picking connections**. With 1,378 pairs, something will be significant by chance. Always correct for multiple comparisons.

## Resources for deeper learning

- 📑 [Allen et al. (2014) — Tracking Whole-Brain Connectivity Dynamics](https://doi.org/10.1093/cercor/bhs261)

- 📑 [Rashid et al. (2014) — Dynamic Connectivity States in Psychiatric Disorders](https://doi.org/10.3389/fnhum.2014.00897)

- 📄 [GIFT Manual — FNC and dFNC sections](https://trendscenter.org/software/gift/)

- 📑 [Murphy et al. (2009) — Impact of Global Signal Regression on Anticorrelations](https://doi.org/10.1152/jn.90777.2008)
