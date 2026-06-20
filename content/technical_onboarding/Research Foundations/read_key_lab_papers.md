---
task_name: "Read Key Lab Papers"
emoji: "📚"
tier: Theory
order: 6
url: "https://scholar.google.com/citations?user=e35VA6sAAAAJ&hl=en&sortby=pubdate"
---
## Why this matters to you

Reading the foundational papers is how you learn the intellectual DNA of this lab. These aren't just citations — they define the methods you'll use daily, the questions the lab asks, and the scientific framework behind every project. You should read (not skim) at least the four required papers before starting hands-on analysis work.

## How to read a scientific paper

If you're new to reading journal articles, here's an efficient approach:

- **First pass (10 min)**: Read the abstract, look at all figures and their captions, read the conclusion. This tells you what they did and what they found.

- **Second pass (30-60 min)**: Read the introduction and discussion carefully. Skim the methods. Now you understand why they did it and what it means.

- **Third pass (if needed)**: Go through the methods line by line. This is for when you need to reproduce or build on the work.

Don't try to understand every equation on the first read. Focus on the big picture: what problem does this solve, and how does the method work conceptually?

## Required reading

### 1. Calhoun et al. (2001) — Group ICA Method

[A Method for Making Group Inferences from Functional MRI Data Using Independent Component Analysis](https://doi.org/10.1002/hbm.1048)

This is THE foundational paper for the lab. It introduced Group ICA — the method for applying ICA across multiple subjects, which you learned about in the previous task. Key contributions:

- Temporal concatenation approach to combine subjects

- Two-stage PCA for data reduction

- Back-reconstruction to get subject-specific components

- Demonstrated on both simulated and real fMRI data

**What to focus on**: Figure 1 (the pipeline diagram) and the explanation of how subject data is concatenated and reduced. Understanding this paper means you understand the core method behind nearly everything the lab does.

### 2. Iraji et al. (2019) — Neuromark Brain Network Maps

[The Spatial Chronnectome Reveals a Dynamic Interplay between Functional Segregation and Integration](https://doi.org/10.1002/hbm.24580)

This paper defines a commonly used set of large-scale brain networks and their sub-components that serve as one of the lab's standard references. Neuromark provides 53 components grouped into 7 domains, estimated from thousands of subjects.

**What to focus on**: The network parcellation figures and Table 1 listing all components. This is the atlas you'll use when identifying components in your own analyses.

### 3. Allen et al. (2014) — Dynamic Functional Network Connectivity

[Tracking Whole-Brain Connectivity Dynamics in the Resting State](https://doi.org/10.1093/cercor/bhs261)

This paper is a landmark because it introduced the concept of dynamic functional network connectivity (dFNC) — the idea that brain network interactions are not static but fluctuate over time through recurring "states." It established the sliding-window correlation approach that's still widely used.

**What to focus on**: The sliding window method, the k-means clustering of connectivity states, and the finding that subjects transition between distinct connectivity patterns during rest.

### 4. Allen et al. (2011) — A Baseline for Resting-State Networks

[A Baseline for the Multivariate Comparison of Resting-State Networks](https://doi.org/10.3389/fnsys.2011.00002)

This paper systematically characterized resting-state networks in a large sample and provided criteria for distinguishing genuine brain components from artifacts — using spatial maps, timecourse properties, and spectral characteristics.

**What to focus on**: The artifact identification criteria and the component classification methodology.

## Recommended reading

### Calhoun & Adali (2009) — ICA Review

[Feature-Based Fusion of Medical Imaging Data](https://doi.org/10.1016/j.neuroimage.2008.10.057)

A comprehensive review of ICA applied to neuroimaging. Covers spatial vs. temporal ICA, different algorithms, and multimodal extensions. Good for deepening your understanding beyond the original method paper.

### Additional recommended papers

The following represent recent key contributions from the lab — ask senior members for their current reading recommendations as the list grows:

- **Jensen et al. (2025)** — multi-scale whole-brain functional atlas from 100k+ datasets ([preprint](https://doi.org/10.1101/2024.09.09.612129))

- **Mirzaeian et al. (2025)** — ultra-high-order ICA for intrinsic connectivity networks ([Frontiers in Neuroscience](https://doi.org/10.3389/fnins.2025.1672129))

### Rashid et al. (2014) — Dynamic Connectivity States

[Dynamic Connectivity States Estimated from Resting fMRI Identify Differences Among Schizophrenia, Bipolar Disorder, and Healthy Control Subjects](https://doi.org/10.3389/fnhum.2014.00897)

A clinical application paper showing how dynamic FNC states differ between psychiatric conditions. This is the type of study design that many lab projects follow.

### Du et al. (2020) — Neuromark Pipeline

[NeuroMark: An Automated and Adaptive ICA Based Pipeline to Identify Reproducible fMRI Markers of Brain Disorders](https://doi.org/10.1016/j.nicl.2020.102375)

The technical companion to the Neuromark framework. Describes the automated pipeline for identifying reproducible brain network markers.

### Iraji et al. (2021) — Time-Varying Connectivity

[Tools of the trade: estimating time-varying connectivity patterns from fMRI data](https://doi.org/10.1093/scan/nsaa114)

A comprehensive review of methods for studying dynamic connectivity — sliding windows, time-frequency analysis, and other approaches. Essential reading for anyone working on dFNC.

### Soares et al. (2016) — A Hitchhiker's Guide to fMRI

[A Hitchhiker's Guide to Functional Magnetic Resonance Imaging](https://doi.org/10.3389/fnins.2016.00515)

An accessible overview of fMRI fundamentals — acquisition, preprocessing, analysis, and interpretation. Excellent starting point for someone new to the field.

### Taylor et al. (2023) — Data Visualization Best Practices

[Highlight Results, Don't Hide Them: Enhance Interpretation, Reduce Biases and Improve Reproducibility](https://doi.org/10.1016/j.neuroimage.2023.120138)

Argues for dual-coded visualization approaches that show subthreshold trends alongside significant results. Directly relevant to how the lab presents brain maps.

## Tips for keeping track

- Use [Zotero](https://www.zotero.org/) or [Mendeley](https://www.mendeley.com/) as a citation manager — you'll accumulate hundreds of papers

- Create a reading notes document where you summarize each paper in 2-3 sentences

- When a paper cites something you don't understand, add it to your reading queue rather than going down the rabbit hole immediately

- The lab's full publication list is on [Dr. Calhoun's Google Scholar](https://scholar.google.com/citations?user=e35VA6sAAAAJ&hl=en&sortby=pubdate)

## Resources for deeper learning

- 📺 [How to Read a Scientific Paper — step-by-step guide](https://www.youtube.com/watch?v=jO6wV4QL0dU)

- 📄 [Dr. Calhoun's Google Scholar — full publication list](https://scholar.google.com/citations?user=e35VA6sAAAAJ&hl=en&sortby=pubdate)

- 📄 [TReNDs Center publications page](https://trendscenter.org/publications/)

- 📑 [Du et al. (2020) — NeuroMark pipeline paper](https://doi.org/10.1016/j.nicl.2020.102375)
