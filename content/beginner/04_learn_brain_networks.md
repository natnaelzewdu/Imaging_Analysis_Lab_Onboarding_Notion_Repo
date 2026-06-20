## Why this matters to you

When you run ICA on fMRI data, the output is a set of spatial maps — but which ones are real brain networks and which are artifacts? You need to know what brain networks look like, where they live, and what they do. The lab's work relies on identifying and labeling functional brain networks from ICA output, and this is a skill you'll use every day.

> **Note**: There is no single "correct" number of brain networks. Depending on the parcellation method and granularity, typical schemes recover anywhere from **about 7 to 15** large-scale networks (and finer schemes split these into many more sub-networks). The lab often references a set derived from [Iraji et al. (2019)](https://doi.org/10.1002/hbm.24580), but this is one choice among many. The grouping below is a general teaching reference — the specific framework you use will depend on your project and the Neuromark template version.

## What is a brain network?

A brain network (also called an intrinsic connectivity network or resting-state network) is a set of brain regions whose activity is temporally correlated — they consistently activate and deactivate together, even when the person is resting with no task. These aren't anatomical connections (though they often overlap with white matter tracts); they're functional connections revealed by correlated BOLD signal fluctuations.

The discovery that the resting brain has organized, reproducible network structure was one of the most important findings in modern neuroimaging. [Biswal et al. (1995)](https://doi.org/10.1002/mrm.1910340409) first showed that motor cortex regions fluctuate together at rest, and since then dozens of networks have been catalogued.

## Major brain network categories

The categories below are among the most commonly identified large-scale networks, but they are not a fixed or exhaustive list. Different parcellation schemes (e.g., Yeo 7-network, Neuromark 53-component) split and group them differently — the number you end up with depends on the method and the level of detail you choose.

> **Note**: For a broader introduction to brain network parcellation approaches, see [Yeo et al. (2011)](https://doi.org/10.1152/jn.00338.2011) for a widely used 7/17-network cortical parcellation, and [Beckmann et al. (2005)](https://doi.org/10.1098/rstb.2005.1634) for an early ICA-based characterization of resting-state networks. Ask senior lab members for their current recommended reading on network labeling.

![Brain lobes labeled — use this as a spatial reference when identifying ICA components below (Gray's Anatomy plate 728)](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Gray728.svg/500px-Gray728.svg.png)

### 1. Visual Network (VIS)

- **Where**: Occipital lobe — primary visual cortex (V1), secondary visual areas

- **Sub-networks**: Medial visual, lateral visual, occipital pole

- **What it does**: Processes visual information — even at rest, these regions fluctuate together

- **How to spot it**: Bright activation concentrated in the back of the brain

### 2. Sensorimotor Network (SM)

- **Where**: Pre- and post-central gyrus (motor and somatosensory cortex), supplementary motor area

- **Sub-networks**: Hand area, mouth/face area, supplementary motor

- **What it does**: Controls movement and processes touch/body sensation

- **How to spot it**: Bilateral strip across the top of the brain, running ear to ear

### 3. Auditory Network (AUD)

- **Where**: Superior temporal gyrus, Heschl's gyrus, insula

- **What it does**: Processes sound and auditory information

- **How to spot it**: Bilateral activation in the temporal lobes, near the ears

### 4. Default Mode Network (DMN)

- **Where**: Medial prefrontal cortex (mPFC), posterior cingulate cortex (PCC), angular gyrus, medial temporal lobe

- **Sub-networks**: Anterior DMN (mPFC-heavy), posterior DMN (PCC-heavy)

- **What it does**: Active during mind-wandering, self-referential thought, memory retrieval. Deactivates during focused tasks. The most studied network in neuroimaging.

- **How to spot it**: Midline structures — front and back — plus lateral parietal patches

- **Clinical relevance**: Altered in Alzheimer's disease, schizophrenia, depression, autism

### 5. Salience Network (SAL)

- **Where**: Anterior insula, dorsal anterior cingulate cortex (dACC)

- **What it does**: Detects important stimuli and switches between DMN and task-positive networks

- **How to spot it**: Look for anterior insula (deep lateral) and dACC (medial frontal, above corpus callosum)

### 6. Central Executive Network (CEN) / Frontoparietal

- **Where**: Dorsolateral prefrontal cortex (dlPFC), posterior parietal cortex

- **What it does**: Working memory, cognitive control, goal-directed behavior

- **How to spot it**: Lateral frontal and parietal regions, typically lateralized (separate left and right components)

### 7. Subcortical Network (SC)

- **Where**: Basal ganglia (caudate, putamen), thalamus

- **What it does**: Motor control, reward processing, relaying sensory information

- **How to spot it**: Deep brain structures, small bilateral blobs near the center of the brain

### 8. Cerebellar Network (CB)

- **Where**: Cerebellum (below and behind the cerebrum)

- **What it does**: Motor coordination, but increasingly recognized for cognitive roles

- **How to spot it**: Activation in the bottom slices of the brain

### 9. Dorsal Attention Network (DAN)

- **Where**: Frontal eye fields, intraparietal sulcus

- **What it does**: Top-down, voluntary attention — directing focus to locations or objects

- **How to spot it**: Similar to frontoparietal but more posterior/superior

### 10. Ventral Attention Network (VAN)

- **Where**: Temporoparietal junction, ventral frontal cortex

- **What it does**: Bottom-up attention — reorienting to unexpected but relevant stimuli

- **How to spot it**: Right-lateralized temporal and frontal regions

### 11. Language Network (LAN)

- **Where**: Broca's area (inferior frontal gyrus), Wernicke's area (superior temporal gyrus)

- **What it does**: Speech production and comprehension

- **How to spot it**: Left-lateralized frontal and temporal activations

### 12. Memory / Medial Temporal Network (MTL)

- **Where**: Hippocampus, parahippocampal gyrus, entorhinal cortex

- **What it does**: Memory encoding and retrieval, spatial navigation

- **How to spot it**: Deep temporal lobe structures, can be hard to see in ICA due to susceptibility artifacts

## Artifacts vs. networks: what to throw out

Not every ICA component is a brain network. Typically 30-50% of components are artifacts. Here's how to spot them:

- **Head motion**: Bright activation around the brain edges, ring-like patterns. Timecourse shows spikes.

- **White matter / CSF**: Activation in ventricles or deep white matter rather than gray matter. These are physiological noise.

- **Vascular**: Large blood vessels, often near sinuses or the circle of Willis. Very focal, high-intensity spots.

- **Susceptibility**: Signal near sinuses or ear canals where the magnetic field is distorted.

The timecourse also helps: real brain networks have smooth, low-frequency fluctuations (< 0.1 Hz). Artifacts often show high-frequency noise, spikes, or drift.

## How networks relate to the lab's work

The lab studies how these networks differ between clinical populations:

- **Schizophrenia**: Altered DMN, frontoparietal, and subcortical connectivity

- **Alzheimer's**: DMN breakdown is an early biomarker

- **Aging**: Gradual network fragmentation and reduced connectivity

- **Classification**: Using network features (spatial maps, FNC) as input to machine learning models to distinguish patients from controls

Understanding these networks is what makes the ICA output interpretable and scientifically meaningful.

## Resources for deeper learning

- 📑 [Iraji et al. (2019) — Spatial maps of 12 large-scale networks](https://doi.org/10.1002/hbm.24580)

- 📺 [Default Mode Network Explained — Neuroscientifically Challenged](https://www.youtube.com/watch?v=1BzGYgKDQ5o)

- 📑 [Beckmann et al. (2005) — Resting-State Networks Overview](https://doi.org/10.1098/rstb.2005.1634)

- 📑 [Yeo et al. (2011) — 7-Network Parcellation of the Human Cerebral Cortex](https://doi.org/10.1152/jn.00338.2011)

- 📄 [Neurosynth — searchable database linking brain regions to functions](https://neurosynth.org/)

- 📑 [Allen et al. (2011) — A Baseline for the Multivariate Comparison of Resting-State Networks](https://doi.org/10.3389/fnsys.2011.00002)
