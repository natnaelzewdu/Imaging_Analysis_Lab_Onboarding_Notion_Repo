## Why this matters to you
The lab isn't limited to fMRI. Multimodal analysis — combining different types of brain data (fMRI + EEG, fMRI + structural MRI, EEG alone) — provides a more complete picture of brain function than any single modality. As the lab expands into multimodal and EEG analysis, understanding these approaches positions you for the full range of research happening here.

## Why multiple modalities?
Each brain imaging modality captures different aspects of brain function:

![DTI fiber tracts — white matter connections between brain regions, visualized by diffusion tensor imaging](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/DTI-sagittal-fibers.jpg/600px-DTI-sagittal-fibers.jpg)

| Modality | What it measures | Temporal resolution | Spatial resolution |
|---|---|---|---|
| fMRI | Hemodynamic response (BOLD) | ~1-2 seconds | ~2-3 mm |
| EEG | Electrical activity (voltage) | ~1 millisecond | ~1 cm (scalp) |
| Structural MRI (sMRI) | Brain anatomy | N/A (single snapshot) | ~1 mm |
| Diffusion MRI (dMRI) | White matter tracts | N/A | ~2 mm |

fMRI has excellent spatial resolution but poor temporal resolution (the BOLD response takes 5-6 seconds to peak). EEG has excellent temporal resolution (milliseconds) but poor spatial resolution (scalp electrodes can't pinpoint deep sources precisely). Combining them gives you both — high spatial AND temporal precision.

Structural MRI tells you about brain anatomy — cortical thickness, gray matter volume, morphological patterns. This complements functional data by revealing structural differences that may underlie functional abnormalities.

## EEG analysis with EEGIFT
The lab's GIFT toolbox includes [EEGIFT](https://trendscenter.org/software/gift/) — an extension for applying ICA to EEG data. The same conceptual framework applies:

### Spatial ICA for EEG
- **Input**: EEG recordings (channels × timepoints)
- **Output**: Independent components with associated scalp maps and timecourses
- **Use**: Identify brain sources, separate brain signals from artifacts (eye blinks, muscle activity, line noise)

### Key differences from fMRI ICA
- EEG components have scalp topography maps instead of brain volume maps
- EEG has much higher temporal resolution — timecourses capture fast neural oscillations (alpha, beta, gamma rhythms)
- Artifact types are different: eye blinks, muscle activity, heartbeat, line noise
- Source localization (estimating where in the brain the EEG signal originates) requires additional modeling

### EEG frequency bands
EEG analysis often focuses on oscillatory activity in specific frequency bands:
- **Delta (0.5-4 Hz)**: Deep sleep, brain injury
- **Theta (4-8 Hz)**: Memory, navigation, drowsiness
- **Alpha (8-13 Hz)**: Relaxed wakefulness, visual processing
- **Beta (13-30 Hz)**: Active thinking, motor planning
- **Gamma (30-100 Hz)**: Attention, perception, binding

ICA on EEG can separate sources with different spectral profiles — a component dominated by alpha oscillations vs. one with broadband gamma activity.

## Source-Based Morphometry (SBM)
SBM applies ICA to structural MRI data:

### How it works
- Collect T1-weighted structural images from many subjects
- Compute gray matter concentration (or thickness/volume) maps
- Stack all subjects' maps into a matrix (subjects × voxels)
- Run ICA to find independent spatial patterns of structural covariation

### What it reveals
SBM finds groups of brain regions that vary together across subjects. For example, one SBM component might show that when frontal cortex volume is larger in a person, parietal cortex volume tends to be larger too — they covary.

### Clinical applications
Structural covariance patterns are altered in psychiatric and neurological disorders:
- Schizophrenia: Reduced gray matter in frontal and temporal components
- Alzheimer's: Progressive atrophy patterns in medial temporal and parietal components
- Aging: Gradual gray matter loss following specific spatial patterns

SBM is covered in [GIFT Manual — Section 3.17](https://trendscenter.org/software/gift/).

## Multimodal fusion approaches
The lab is active in developing fusion methods that combine information across modalities:

### Joint ICA (jICA)
- Combine features from two modalities (e.g., fMRI spatial maps + sMRI gray matter maps)
- Run ICA on the combined data
- Each component has both an fMRI part (functional) and an sMRI part (structural)
- Reveals linked patterns: aspects of structure and function that covary together

### Parallel ICA
- Run ICA separately on each modality
- Find correlations between components from different modalities
- Identifies which functional networks relate to which structural patterns

### Multimodal Canonical Correlation Analysis (mCCA) + jICA
- First use CCA to find maximally correlated features across modalities
- Then apply jICA to the CCA-linked features
- Generates multimodal components with linked spatial patterns

## EEG-fMRI fusion
Combining EEG and fMRI is particularly powerful because they have complementary strengths:

### Simultaneous EEG-fMRI
- Record EEG while the subject is in the MRI scanner
- Extremely challenging technically (MRI gradients create massive artifacts in EEG)
- Requires specialized hardware and artifact removal algorithms
- Allows direct correlation between BOLD changes and EEG features at each moment

### Separate-session fusion
- Collect EEG and fMRI in separate sessions from the same subjects
- Extract features from each modality independently
- Use fusion methods (jICA, mCCA) to find linked patterns
- Easier technically but assumes brain patterns are consistent across sessions

## How this connects to the lab's work
The lab is actively expanding into multimodal analysis:
- Combining fMRI connectivity features with structural features for more accurate classification
- Using EEG temporal dynamics to complement fMRI spatial precision
- Developing new fusion methods that can handle more than two modalities simultaneously
- Applying these to large-scale datasets like the [UK Biobank](https://www.ukbiobank.ac.uk/) and [ABCD Study](https://abcdstudy.org/)

As a newcomer, you should be aware of these directions even if your initial projects focus on fMRI alone. The skills you've learned — ICA, connectivity, classification — all extend naturally to multimodal settings.

## Resources for deeper learning
- 📄 [GIFT Manual — Section 3.17: Source Based Morphometry](https://trendscenter.org/software/gift/)
- 📺 [EEG-fMRI Basics — overview of the technique](https://www.youtube.com/watch?v=kB3Lfp3cXgE)
- 📑 [Calhoun & Sui (2016) — Multimodal Fusion of Brain Imaging Data: A Key to Finding the Missing Link(s) in Complex Mental Illness](https://doi.org/10.1016/j.biopsych.2015.12.005)
- 📑 [Sui et al. (2012) — A Review of Multivariate Methods for Multimodal Fusion](https://doi.org/10.1016/j.neuroimage.2012.08.074)
- 📄 [MNE-Python — open-source EEG/MEG analysis library](https://mne.tools/)
- 📄 [EEGIFT documentation — ICA for EEG data](https://trendscenter.org/software/gift/)
