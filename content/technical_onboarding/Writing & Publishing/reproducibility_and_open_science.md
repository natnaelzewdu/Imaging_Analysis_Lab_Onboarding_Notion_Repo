---
task_name: "Practice Reproducibility and Open Science"
emoji: "🔬"
category: Writing & Publishing
tier: Theory
order: 2
url: "https://osf.io/"
---
## Why this matters to you

Science advances by building on others' work — which requires that work to be reproducible. Neuroimaging has faced a [reproducibility crisis](https://doi.org/10.1038/s41586-022-04492-9), with many published findings failing to replicate. As a newcomer, you have the opportunity to do things right from the start. Reproducibility isn't extra work — it's fundamental to credible science and increasingly required by journals, funders, and collaborators.

## The reproducibility problem in neuroimaging

A [2020 study](https://doi.org/10.1038/s41586-022-04492-9) showed that different analysis teams given the same fMRI data reached substantially different conclusions. The reasons:

- **"Garden of forking paths"**: Hundreds of arbitrary decisions in preprocessing and analysis. Each studies chooses differently, and results depend on these choices.

- **Underpowered studies**: Small samples lead to noisy results that don't replicate.

- **Selective reporting**: Only reporting analyses that yielded significant results.

- **Software differences**: SPM, FSL, and AFNI give different results on the same data.

- **Lack of code sharing**: Methods sections are too vague to replicate.

## What you should do: practical reproducibility checklist

### 1. Set random seeds everywhere

ICA, k-means clustering, cross-validation splits, and deep learning all use random initialization. Without fixed seeds, you'll get different results every time.

```python
# Python
import numpy as np
import random
import torch

SEED = 42
np.random.seed(SEED)
random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
```

```matlab
% MATLAB
rng(42, 'twister');
```

In GIFT, ICASSO runs ICA with multiple random seeds to assess stability — this is good. But for your final reported analysis, document which seed or ICASSO settings you used.

### 2. Version-lock your software

Record exact versions of every tool used:

- MATLAB version (e.g., R2023a)

- GIFT version (e.g., GroupICATv4.0c)

- SPM version (e.g., SPM12, revision 7771)

- Python packages: `pip freeze > requirements.txt` or `conda env export > environment.yml`

- fmriprep version and container hash

Put these in your methods section AND in a README in your analysis directory.

### 3. Script everything — never use GUIs for final analyses

GUIs are great for exploration, but for your reported results:

- Write MATLAB scripts that call GIFT functions programmatically

- Write Python scripts with all parameters explicit

- Write SBATCH scripts for cluster submission

- Store all scripts in a Git repository

**Anyone should be able to run your scripts and get the same results.**

### 4. Use version control (Git) properly

```shell
my_project/
├── README.md                    # What this project does, how to run it
├── requirements.txt             # Python dependencies
├── environment.yml              # Conda environment specification
├── scripts/
│   ├── 01_preprocess.sh         # Preprocessing pipeline
│   ├── 02_run_ica.m             # ICA analysis
│   ├── 03_compute_fnc.m         # FNC computation
│   ├── 04_statistics.py         # Group statistics
│   └── 05_make_figures.py       # Generate publication figures
├── config/
│   ├── subjects.txt             # Subject list
│   └── parameters.json          # Analysis parameters
└── .gitignore                   # Exclude data files
```

Every analysis decision should be captured in code or configuration files, not in your memory.

### 5. Document exclusion decisions

Create a log documenting every subject excluded and why:

```shell
Subject exclusion log:
- sub-003: Excluded. Mean FD = 0.82mm (threshold: 0.5mm)
- sub-017: Excluded. Incidental finding on T1 (large cyst)
- sub-042: Excluded. Incomplete functional data (only 150/200 TRs acquired)
- sub-061: Excluded. Registration to MNI failed visual QC
Total: 4/100 excluded (4%)
```

Exclusion criteria MUST be decided before looking at analysis results.

## Pre-registration

Pre-registration means publicly documenting your hypotheses, methods, and analysis plan BEFORE analyzing data. This prevents:

- Changing hypotheses after seeing results (HARKing — Hypothesizing After Results are Known)

- Trying many analyses and reporting only the one that worked (p-hacking)

- Selective reporting of outcomes

### Where to pre-register

- [OSF (Open Science Framework)](https://osf.io/) — most common for neuroimaging

- [AsPredicted](https://aspredicted.org/) — simpler form-based pre-registration

- [ClinicalTrials.gov](https://clinicaltrials.gov/) — for clinical studies

### What goes in a pre-registration

- Research question and specific hypotheses

- Sample size and justification (power analysis)

- Inclusion/exclusion criteria

- Preprocessing pipeline with parameters

- Analysis methods with parameters

- Statistical tests and correction methods

- Primary vs. exploratory analyses (clearly labeled)

Pre-registration doesn't prevent exploratory analysis — it requires you to LABEL what's confirmatory vs. exploratory.

## Data sharing

Sharing data is increasingly required by journals (Nature, PNAS, eLife) and funders (NIH). Options:

- [OpenNeuro](https://openneuro.org/) — free hosting for BIDS-formatted neuroimaging data. De-identified data can be shared publicly.

- [NITRC](https://www.nitrc.org/) — neuroimaging tools and resources clearinghouse

- [Figshare](https://figshare.com/) — general-purpose data repository with DOIs

### What you can share

- **Always**: Analysis code, statistical maps, group-level results

- **Usually**: De-identified, defaced MRI data (check your DUA and IRB)

- **Never without approval**: Identifiable data, data under restrictive DUAs

### Data citation

When sharing data, assign a DOI and provide a citation format. When using others' data, cite it properly — data creators deserve credit.

## COBIDAS reporting checklist

The [COBIDAS guidelines](https://doi.org/10.1038/nn.4500) specify minimum reporting requirements for neuroimaging studies. For every paper, verify you've reported:

### Acquisition

- Scanner manufacturer and model

- Field strength (e.g., 3T)

- Coil type (e.g., 32-channel head coil)

- Sequence type (e.g., EPI for fMRI, MPRAGE for T1)

- TR, TE, flip angle, voxel size, number of slices, number of volumes

- Acceleration (multiband factor, GRAPPA/SENSE)

### Preprocessing

- Software and version

- Every step with parameters: realignment, coregistration, normalization (template, resolution), smoothing (kernel FWHM)

- Motion handling: censoring criteria, motion regressors included

- Temporal filtering: bandpass, high-pass frequency

### ICA specifics (for this lab)

- Number of components

- ICA algorithm (Infomax, FastICA, etc.)

- Back-reconstruction method (GICA, dual regression)

- Template used (Neuromark version, number of components)

- Criteria for component selection (artifact vs. network)

- GIFT version

### Statistics

- Statistical test with degrees of freedom

- Correction method (FDR, Bonferroni, permutation) with threshold used

- Effect sizes (Cohen's d, partial η²)

- Number of subjects excluded and reasons

## Resources for deeper learning

- 📑 [Botvinik-Nezer et al. (2020) — Variability in fMRI Analysis Across Teams](https://doi.org/10.1038/s41586-022-04492-9)

- 📄 [COBIDAS Reporting Guidelines](https://doi.org/10.1038/nn.4500)

- 📄 [Open Science Framework (OSF)](https://osf.io/)

- 📑 [Button et al. (2013) — Power Failure in Neuroscience](https://doi.org/10.1038/nrn3475)

- 📄 [The Turing Way — Guide to Reproducible Research](https://the-turing-way.netlify.app/)

- 📄 [OpenNeuro — open neuroimaging data repository](https://openneuro.org/)

- 📺 [Reproducibility in Neuroimaging — OHBM keynote](https://www.youtube.com/watch?v=BuP6wZJ3DNw)
