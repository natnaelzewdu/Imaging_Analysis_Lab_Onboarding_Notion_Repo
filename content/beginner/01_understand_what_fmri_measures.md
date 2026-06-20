## Why this matters to you

Everything in this lab — ICA, brain networks, classification, dynamic functional connectivity — starts with fMRI data. If you don't understand what the scanner produces and what the signal represents, nothing downstream will make sense. This is your absolute starting point as a newcomer to neuroimaging.

## What is MRI?

MRI (Magnetic Resonance Imaging) uses powerful magnetic fields to create detailed images of the inside of the body without radiation. The scanner contains a superconducting magnet — typically 3 Tesla, which is about 60,000 times stronger than Earth's magnetic field. A few key concepts:

![MRI sagittal scan of a human head — what structural MRI data looks like](https://upload.wikimedia.org/wikipedia/commons/3/36/MRI_head_side.jpg)

- Hydrogen atoms in your body (mostly in water) have a property called spin — they behave like tiny magnets.

- When placed in the strong magnetic field, these atoms align with the field.

- The scanner sends a radiofrequency (RF) pulse that knocks the atoms out of alignment.

- As the atoms realign, they emit a signal that the scanner's receiver coils detect.

- Different tissues (gray matter, white matter, cerebrospinal fluid) realign at different rates, creating contrast.

This is a purely physical process — no injections, no radiation. The [MRI physics overview from Questions and Answers in MRI](https://mriquestions.com/how-does-mri-work.html) covers this in excellent detail.

### Structural MRI vs. Functional MRI

These are the two types you'll encounter constantly:

- Structural MRI (sMRI or T1-weighted): A single high-resolution 3D image of brain anatomy. Think of it as a very detailed photograph at one moment in time. Typical resolution is about 1mm × 1mm × 1mm. Used to measure brain volume, cortical thickness, detect lesions. When you see a pretty brain image in a textbook, it's usually structural MRI.

- Functional MRI (fMRI or T2*-weighted): A series of lower-resolution images captured very rapidly — one complete brain volume every 0.5-2 seconds (modern multiband/simultaneous multi-slice sequences achieve sub-second TRs; older sequences use 2s). This creates essentially a movie of brain activity over time, typically lasting 5-15 minutes. Resolution is typically 2-3mm × 2-3mm × 2-3mm (with 2mm becoming standard in newer studies), because we trade spatial detail for temporal speed.

The key difference: structural MRI tells you what the brain LOOKS LIKE, functional MRI tells you what the brain is DOING.

## The BOLD signal — what fMRI actually measures

This is the single most important concept to understand. fMRI does NOT directly measure neural activity. It measures an indirect proxy called the Blood-Oxygen-Level-Dependent (BOLD) signal. Here's the full chain of events:

- A brain region increases its local neural processing. Note that BOLD does not simply track the spiking (action-potential) *output* of neurons — it is most closely related to local field potentials and presynaptic/synaptic input, i.e. the incoming and local processing within a region. BOLD can even rise when a region's output activity is being *suppressed*, because inhibitory signaling is itself metabolically costly. So "active" here means "metabolically engaged," not strictly "firing more."

- This local processing consumes glucose and oxygen delivered by nearby blood vessels (capillaries).

- Within seconds, the vascular system responds by dramatically INCREASING blood flow to that region — far more than what was consumed. This is called the hemodynamic response.

- This means the ratio of oxygenated hemoglobin (oxyhemoglobin) to deoxygenated hemoglobin (deoxyhemoglobin) shifts.

- Deoxyhemoglobin is paramagnetic — it distorts the local magnetic field and reduces the MRI signal. When more oxygenated blood floods in, there's less deoxyhemoglobin, less signal distortion, and the T2* signal goes UP.

- The scanner detects this signal increase as a small brightness change in that voxel — typically only a 1-3% change above baseline.

### The Hemodynamic Response Function (HRF)

The BOLD response doesn't happen instantly. After neurons fire, it takes about 1-2 seconds for blood flow changes to begin, and the BOLD signal peaks around 5-6 seconds later. After the peak, it actually dips below baseline briefly (the post-stimulus undershoot) before returning to normal around 15-20 seconds total. This delay and shape is called the Hemodynamic Response Function (HRF).

This matters because: when we see a BOLD signal change at time T, the neural activity that caused it actually happened at around time T minus 5 seconds. Any analysis method needs to account for this delay.

For a clear visual explanation of the HRF, watch [this MIT lecture segment on the hemodynamic response](https://www.youtube.com/watch?v=pnHlO-B6oSA).

## What raw fMRI data looks like

A single fMRI scan (also called a 'run') produces a 4-dimensional dataset:

![Voxels — the 3D equivalent of pixels. Each voxel in fMRI represents a small cube of brain tissue](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Voxels.svg/500px-Voxels.svg.png)

- 3 spatial dimensions: typically around 64 × 64 × 35 voxels. A voxel is a 3D pixel — usually about 3mm × 3mm × 3mm in size. Each voxel represents a small cube of brain tissue containing roughly 5.5 million neurons.

- 1 time dimension: usually 150-300 timepoints, called volumes or TRs. The time between consecutive volumes is the TR (Repetition Time), typically 1-2 seconds.

So a typical resting-state scan might be: 64 × 64 × 35 voxels × 200 timepoints at TR = 2 seconds = 400 seconds (about 6.5 minutes) of data. The total size on disk is usually 50-200 MB per run in NIfTI format.

Each voxel has a timeseries — a sequence of numbers representing the BOLD signal intensity at that location over the scan duration. When we do ICA, we're finding groups of voxels whose timeseries are correlated — meaning they fluctuate together over time, forming functional networks.

The data is stored in [NIfTI format (.nii)](https://nifti.nimh.nih.gov/). You can view it using tools like [FSLeyes](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLeyes), [AFNI's viewer](https://afni.nimh.nih.gov/), or the GIFT toolbox we use in this lab.

## Task-based vs. resting-state fMRI

There are two main experimental paradigms:

![fMRI BOLD activation — yellow/red regions show where brain activity increases during a visual task compared to rest](https://upload.wikimedia.org/wikipedia/commons/8/87/Functional_magnetic_resonance_imaging.jpg)

### Task-based fMRI

The participant performs a structured task while being scanned — for example, looking at flashing checkerboards alternating with rest periods, pressing buttons in response to stimuli, or mentally rotating objects. Because the experimenter knows the exact timing of each task event, they can build a mathematical model (the General Linear Model or GLM) that predicts what the BOLD signal SHOULD look like if a voxel is involved in the task. This is the classical approach — very powerful but limited to what you choose to test.

### Resting-state fMRI

The participant lies still in the scanner. No task, no stimuli — they might fixate on a crosshair or simply close their eyes. During this 'rest,' the brain is far from idle. Spontaneous low-frequency BOLD fluctuations (typically < 0.1 Hz) show highly organized patterns — certain brain regions fluctuate in synchrony even though the person isn't doing anything. These synchronized regions form what we call resting-state networks or intrinsic connectivity networks.

Our lab primarily works with resting-state fMRI. This matters because without a task design, you can't use GLM to guide analysis. You need data-driven approaches that can discover patterns without prior assumptions — and this is exactly what Independent Component Analysis (ICA) provides. This is why ICA is so central to everything we do.

## How this connects to what you'll do next

Now that you understand fMRI data, the next tasks will cover:

- How ICA decomposes this 4D data into independent brain networks

- How Group ICA extends this to multiple subjects

- How to identify which components are real brain networks vs. artifacts (motion, physiological noise)

## Resources for deeper learning

- 📺 [How fMRI Works — clear 10-min overview (Neuroscientifically Challenged)](https://www.youtube.com/watch?v=djAxjtN_7VE)

- 📺 [fMRI Physics and BOLD Signal — MIT OpenCourseWare](https://www.youtube.com/watch?v=pnHlO-B6oSA)

- 📺 [Principles of fMRI — full free course by Lindquist & Wager](https://www.youtube.com/playlist?list=PLfXA4opIOVrGHncHRxI3Qa5GeCSudwmxM)

- 📄 [Introduction to fMRI (UC San Diego)](https://fmri.ucsd.edu/Research/whatisfmri.html)

- 📄 [BOLD signal deep dive (Wikipedia)](https://en.wikipedia.org/wiki/Blood-oxygen-level-dependent_imaging)

- 📄 [MRI Physics — Questions and Answers in MRI](https://mriquestions.com/how-does-mri-work.html)

- 📄 [NIfTI file format reference](https://nifti.nimh.nih.gov/)
