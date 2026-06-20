## Why this matters to you
While SPM is the lab's primary preprocessing tool, [fmriprep](https://fmriprep.org/en/stable/) is an increasingly popular alternative that emphasizes reproducibility and robustness. It's a fully automated pipeline that combines the best algorithms from multiple software packages (FSL, FreeSurfer, ANTs, AFNI) into a single, well-tested workflow. You should know about it because you'll encounter it in papers, collaborations, and it may be the best choice for certain projects.

## What fmriprep is
fmriprep is developed by the [NiPreps community](https://www.nipreps.org/) (led by the Poldrack Lab at Stanford). It's an open-source Python tool that preprocesses fMRI data with minimal user intervention. You give it raw data in [BIDS format](https://bids.neuroimaging.io/), and it produces fully preprocessed images plus a detailed visual quality report.

![MRI scanner — a Philips MRI machine, similar to scanners used in neuroimaging research](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/MRI-Philips.JPG/600px-MRI-Philips.JPG)

The key philosophy: **preprocessing should not require expertise-dependent decisions** that vary from lab to lab. fmriprep makes opinionated choices based on the latest research, uses the best available algorithm for each step, and documents exactly what was done.

## How it differs from SPM

| Aspect | SPM | fmriprep |
|---|---|---|
| Language | MATLAB | Python |
| Interface | GUI or scripts | Command line |
| Input format | Flexible | Requires BIDS format |
| Algorithm choices | You choose | Pre-selected best practices |
| Flexibility | High (many options) | Low (opinionated pipeline) |
| Normalization | SPM's segmentation | ANTs registration (generally more accurate) |
| Surface analysis | Not built-in | Integrates FreeSurfer |
| QC reports | Manual inspection | Automatic HTML reports |
| Reproducibility | Depends on user choices | High (containerized) |

## The fmriprep pipeline
fmriprep runs several steps automatically:

### Anatomical processing
- Skull stripping using ANTs or FreeSurfer
- Tissue segmentation (gray matter, white matter, CSF)
- Surface reconstruction with FreeSurfer (optional but recommended)
- Spatial normalization to MNI space using ANTs (SyN non-linear registration — generally considered higher quality than SPM's normalization)

### Functional processing
- Reference image estimation (from the single-band reference or the initial volumes)
- Head motion estimation and correction
- Slice timing correction (if metadata is available)
- Susceptibility distortion correction (using fieldmaps if available, or fieldmap-less approaches)
- Coregistration to the structural image
- Confound estimation: framewise displacement, DVARS, CompCor (aCompCor, tCompCor), motion parameters and their derivatives

### Output
fmriprep produces:
- Preprocessed functional images in multiple spaces (MNI, native, fsaverage surface)
- A confounds TSV file with dozens of potential regressors
- An HTML quality report with visualizations of every step

**Important**: fmriprep does NOT do smoothing or temporal filtering. These are left to the analysis pipeline (e.g., GIFT, FSL, etc.) since the optimal parameters depend on your analysis method.

## Running fmriprep on the cluster
fmriprep runs inside a container ([Singularity](https://sylabs.io/guides/3.0/user-guide/) on the cluster, since Docker requires root access). The basic command is:

```
singularity run fmriprep.sif \
    /path/to/bids_dataset \
    /path/to/output \
    participant \
    --participant-label sub-01 \
    --fs-license-file /path/to/freesurfer_license.txt
```

This is typically wrapped in an SBATCH script. fmriprep is computationally intensive — expect 6-12 hours per subject, depending on whether you run FreeSurfer surface reconstruction.

## BIDS format requirement
fmriprep requires data in [BIDS (Brain Imaging Data Structure)](https://bids.neuroimaging.io/) format. BIDS is a standardized way to organize neuroimaging data:

```
dataset/
  sub-01/
    anat/
      sub-01_T1w.nii.gz
    func/
      sub-01_task-rest_bold.nii.gz
      sub-01_task-rest_bold.json
  sub-02/
    ...
  dataset_description.json
  participants.tsv
```

If your data isn't in BIDS format, you'll need to convert it first using tools like [HeuDiConv](https://heudiconv.readthedocs.io/) or [dcm2bids](https://unfmontreal.github.io/Dcm2Bids/).

## When to use fmriprep vs. SPM
- **Use SPM** when: Working within the existing lab pipeline, data is already SPM-preprocessed, you need specific SPM-only features, or you're doing task-based analysis that flows into SPM's GLM
- **Use fmriprep** when: You want maximum reproducibility, working with a new dataset from scratch, collaborating with labs that use BIDS, or when ANTs registration quality matters for your analysis
- **Both work fine as input to GIFT** — the ICA step doesn't care which preprocessing tool you used, as long as the data is properly preprocessed and in a compatible format

## Resources for deeper learning
- 📄 [fmriprep Documentation — comprehensive user guide](https://fmriprep.org/en/stable/)
- 📺 [fmriprep Overview — video tutorial](https://www.youtube.com/watch?v=J0npRWV2zTY)
- 📑 [Esteban et al. (2019) — fMRIPrep: a robust preprocessing pipeline](https://doi.org/10.1038/s41592-018-0235-4)
- 📄 [BIDS Specification — data format required by fmriprep](https://bids.neuroimaging.io/)
- 📄 [NiPreps — the broader ecosystem of preprocessing pipelines](https://www.nipreps.org/)
