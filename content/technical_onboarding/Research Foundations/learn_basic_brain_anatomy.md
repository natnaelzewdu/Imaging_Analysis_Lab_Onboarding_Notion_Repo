---
task_name: "Learn Basic Brain Anatomy for Neuroimaging"
emoji: "🧠"
category: Research Foundations
tier: Theory
order: 2
url: "https://neurosynth.org/"
---
## Why this matters to you

You know data structures, algorithms, and code — but you've never studied the brain. Every task in this onboarding uses anatomical terms like "posterior cingulate cortex" or "dorsolateral prefrontal cortex" as if you know where those are. Without a basic spatial map of the brain, ICA components, network descriptions, and paper figures will be incomprehensible. This task gives you the minimum anatomy you need.

## How the brain is organized

The brain has three major divisions:

- **Cerebrum**: The large, wrinkled outer structure — this is where most fMRI analysis focuses. It's divided into left and right hemispheres connected by the corpus callosum (a thick bundle of white matter fibers).

- **Cerebellum**: The smaller structure at the back and bottom of the brain. Traditionally associated with motor coordination, but increasingly recognized for cognitive roles.

- **Brainstem**: Connects the brain to the spinal cord. Controls basic life functions (breathing, heart rate). Rarely the focus of fMRI studies due to poor signal quality.

## Tissue types in MRI

MRI can distinguish three main tissue types, and you need to recognize them:

- **Gray matter (GM)**: The outer layer of the cerebrum (cortex) plus deep nuclei. Contains neuron cell bodies — where computation happens. This is where the BOLD signal originates. On a T1 MRI, gray matter appears medium gray.

- **White matter (WM)**: Bundles of myelinated axons connecting brain regions. These are the "cables." On a T1 MRI, white matter appears bright/white. ICA components in white matter are usually artifacts.

- **Cerebrospinal fluid (CSF)**: Fluid filling the ventricles (internal cavities) and surrounding the brain. On a T1 MRI, CSF appears dark/black. ICA components in ventricles are artifacts.

## The four lobes of the cerebrum

Each hemisphere has four lobes. When reading about brain networks, these are the regions you'll reference constantly:

![Brain lobes color-coded: blue=frontal, yellow=parietal, green=temporal, pink=occipital (Gray's Anatomy)](https://upload.wikimedia.org/wikipedia/commons/0/0e/Lobes_of_the_brain_NL.svg)

### Frontal lobe (front of brain)

- **Where**: Everything anterior to the central sulcus (the deep groove running ear-to-ear across the top)

- **Key regions**: Prefrontal cortex (planning, decision-making), motor cortex (movement commands), Broca's area (speech production)

- **In ICA**: Frontoparietal network components, default mode network (medial prefrontal), salience network (anterior cingulate)

### Parietal lobe (top-back of brain)

- **Where**: Behind the central sulcus, above the temporal lobe

- **Key regions**: Somatosensory cortex (touch, body awareness), posterior parietal cortex (attention, spatial processing), angular gyrus (language, memory)

- **In ICA**: Sensorimotor network, dorsal attention network, default mode network (angular gyrus)

### Temporal lobe (sides of brain, near ears)

- **Where**: Below the lateral fissure (Sylvian fissure), on the sides

- **Key regions**: Auditory cortex (hearing), Wernicke's area (language comprehension), hippocampus (memory — deep inside, not visible on surface)

- **In ICA**: Auditory network, language network, memory/medial temporal network

### Occipital lobe (back of brain)

- **Where**: The most posterior part of the brain

- **Key regions**: Primary visual cortex (V1), secondary visual areas (V2, V3, V4, V5/MT)

- **In ICA**: Visual network components — the easiest to identify because they're concentrated at the back

## Key anatomical terms you'll see constantly

These adjectives describe WHERE in the brain something is:

![Motor and sensory regions of the cerebral cortex — labeled anatomical reference](https://upload.wikimedia.org/wikipedia/commons/b/bb/Blausen_0102_Brain_Motor%26Sensory_%28flipped%29.png)

| Term | Meaning | Example |

|---|---|---|

| Anterior / Rostral | Toward the front | Anterior cingulate = front part of cingulate |

| Posterior / Caudal | Toward the back | Posterior cingulate = back part of cingulate |

| Superior / Dorsal | Toward the top | Dorsolateral prefrontal = top-side of prefrontal |

| Inferior / Ventral | Toward the bottom | Inferior frontal gyrus = bottom of frontal lobe |

| Medial | Toward the midline | Medial prefrontal = inner surface, near the midline |

| Lateral | Toward the sides | Lateral occipital = outer surface of occipital lobe |

| Ipsilateral | Same side | |

| Contralateral | Opposite side | |

### Putting it together

"Dorsolateral prefrontal cortex (dlPFC)" = the top-side part of the prefrontal area of the frontal lobe. Once you know these building blocks, most anatomical names are self-describing.

## Critical deep structures

Not everything is on the surface. These subcortical structures appear frequently in ICA:

![Basal ganglia (red) and related structures (blue) within the brain](https://upload.wikimedia.org/wikipedia/commons/8/85/Basal_ganglia_and_related_structures_%282%29.svg)

- **Thalamus**: A relay station deep in the center of the brain. Almost all sensory information passes through it. Appears in subcortical ICA components.

- **Basal ganglia** (caudate, putamen, globus pallidus): A group of nuclei involved in motor control, learning, and reward. Appear as small bilateral blobs in subcortical ICA components.

- **Hippocampus**: Seahorse-shaped structure deep in the medial temporal lobe. Critical for memory formation. Hard to image with fMRI due to susceptibility artifacts near air-filled sinuses.

- **Amygdala**: Adjacent to the hippocampus. Involved in emotion processing, particularly fear. Also affected by susceptibility artifacts.

- **Insula**: Hidden deep in the lateral sulcus. Part of the salience network. Involved in interoception (awareness of body states), pain, and emotional processing.

- **Cingulate cortex**: A band of cortex wrapping around the corpus callosum on the medial surface. Anterior cingulate (ACC) is part of the salience network; posterior cingulate (PCC) is the hub of the default mode network.

## MRI coordinate systems

When viewing brain images or reading coordinates in papers, you need to know the standard spaces:

### MNI space (Montreal Neurological Institute)

The standard coordinate system for group analyses. After spatial normalization, every brain is warped into MNI space so coordinates are comparable across subjects.

- **x-axis**: Left (-) to Right (+). x=0 is the midline.

- **y-axis**: Posterior (-) to Anterior (+). y=0 is at the anterior commissure.

- **z-axis**: Inferior (-) to Superior (+). z=0 is at the anterior commissure.

Example: MNI coordinates (0, -52, 26) = midline, posterior, superior = posterior cingulate cortex (PCC), the hub of the default mode network.

### Viewing orientations

Brain images are displayed in three standard views:

- **Axial** (horizontal slice): Looking down from above. Left side of image = right side of brain (radiological convention) or left side of brain (neurological convention). GIFT uses neurological convention.

- **Sagittal** (side view): Looking from the side. Front of brain = left side of image.

- **Coronal** (front view): Looking at the face. Like a slice through the ears.

## Interactive brain atlases

Bookmark these — you'll use them constantly:

- [Neurosynth](https://neurosynth.org/) — type a brain region or function, see which regions activate. Essential for interpreting ICA components.

- [Brain Atlas by Allen Institute](https://atlas.brain-map.org/) — detailed anatomical reference

- [MNI coordinate lookup](http://www.oneroi.org/mni/) — enter MNI coordinates, get anatomical labels

- [3D Brain by Genes to Cognition](https://www.g2conline.org/) — interactive 3D model for learning anatomy

## Resources for deeper learning

- 📺 [Neuroanatomy Crash Course — 2-Minute Neuroscience series](https://www.youtube.com/playlist?list=PLSQl0a2vh4HA5LRGBZQ6sXBn-LBihRyr0)

- 📄 [Atlas of the Human Brain — comprehensive reference](https://www.thehumanbrain.info/)

- 📺 [Brain Lobes and Functions — quick overview](https://www.youtube.com/watch?v=HVGlfcP3ATI)

- 📄 [Neurosynth — searchable brain function database](https://neurosynth.org/)
