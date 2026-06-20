## Why this matters to you
Before ICA or any analysis can happen, raw data from the MRI scanner needs to be converted, organized, and validated. A CS student's instinct is to jump straight to code — but in neuroimaging, data preparation is where most mistakes happen and where you'll spend a surprising amount of time. Incorrect data preparation silently corrupts every downstream analysis.

## What comes off the scanner: DICOM files
MRI scanners (Siemens, GE, Philips) produce data in [DICOM format](https://www.dicomstandard.org/) — a medical imaging standard dating back to the 1980s. DICOM is:

- **One file per 2D slice**: A single fMRI run of 200 volumes × 35 slices = 7,000 DICOM files
- **Metadata-rich**: Each file contains acquisition parameters (TR, TE, flip angle, slice thickness, scanner model, patient ID, date)
- **Vendor-specific**: Siemens, GE, and Philips encode metadata differently in their DICOM headers
- **Contains PHI**: Patient names, dates of birth, and medical record numbers may be embedded. This data MUST be handled according to HIPAA and your IRB protocol

You will rarely work with DICOM directly. It needs to be converted.

## NIfTI — the analysis format
[NIfTI (Neuroimaging Informatics Technology Initiative)](https://nifti.nimh.nih.gov/) is the standard format for neuroimaging analysis. Key differences from DICOM:

- **One file per scan**: A 4D fMRI run is a single .nii or .nii.gz file
- **Simple header**: Contains dimensions, voxel sizes, orientation, and affine transformation matrix
- **No PHI**: NIfTI files contain only image data and spatial metadata
- **Two variants**: .nii (single file, larger) and .nii.gz (gzip compressed, standard practice)

### DICOM to NIfTI conversion
The conversion step is critical — mistakes here propagate through the entire analysis. Common tools:

- **[dcm2niix](https://github.com/rordenlab/dcm2niix)** (recommended): Fast, reliable, open-source command-line tool by Chris Rorden. Handles Siemens, GE, and Philips DICOM. Also outputs JSON sidecar files with metadata.
  ```
  $ dcm2niix -o /output/path -f %p_%s /path/to/dicom/folder
  ```
- **[HeuDiConv](https://heudiconv.readthedocs.io/)**: Wraps dcm2niix and automates conversion into BIDS format (see below). Requires writing a heuristic file to map DICOM series to BIDS naming.
- **[dcm2bids](https://unfmontreal.github.io/Dcm2Bids/)**: Another BIDS conversion wrapper. Uses a JSON configuration file instead of Python heuristics.
- **SPM's DICOM Import**: Available in SPM's GUI, but less flexible than dcm2niix.

### What to verify after conversion
- **Correct number of volumes**: If you know the scan had 200 TRs, the NIfTI should have 200 volumes in the 4th dimension
- **Correct orientation**: Load in a viewer (FSLeyes, AFNI) and check that left/right, anterior/posterior are correct. Incorrect orientation can flip the brain
- **Correct voxel size**: Check the header matches expected acquisition resolution (e.g., 3mm × 3mm × 3mm)
- **JSON sidecar metadata**: If using dcm2niix, verify TR, TE, and other parameters match the acquisition protocol

## BIDS — the modern standard for organizing data
[BIDS (Brain Imaging Data Structure)](https://bids.neuroimaging.io/) is a standardized way to organize neuroimaging datasets. It's rapidly becoming required for:
- Submitting data to public repositories (OpenNeuro)
- Using fmriprep (which requires BIDS input)
- Collaborating with other labs
- Reproducible research

### BIDS directory structure
```
my_dataset/
├── dataset_description.json          # Required: dataset metadata
├── participants.tsv                   # Subject demographics
├── sub-001/
│   ├── anat/
│   │   ├── sub-001_T1w.nii.gz       # Structural MRI
│   │   └── sub-001_T1w.json         # Acquisition parameters
│   └── func/
│       ├── sub-001_task-rest_bold.nii.gz    # Functional MRI
│       ├── sub-001_task-rest_bold.json      # Acquisition parameters
│       └── sub-001_task-rest_events.tsv     # Event timing (task data only)
├── sub-002/
│   ├── anat/
│   └── func/
└── ...
```

### BIDS naming conventions
- File names encode key metadata: `sub-<label>_ses-<label>_task-<label>_run-<index>_bold.nii.gz`
- Every NIfTI file has a companion JSON sidecar with acquisition parameters
- Task event timing goes in TSV (tab-separated values) files
- Derivatives (preprocessed data, analysis results) go in a `derivatives/` subfolder

### Validating BIDS
After creating a BIDS dataset, validate it with the [BIDS Validator](https://bids-standard.github.io/bids-validator/):
```
$ pip install bids-validator
$ bids-validator /path/to/bids_dataset
```
Or use the web-based validator at [bids-standard.github.io/bids-validator](https://bids-standard.github.io/bids-validator/).

## Raw data quality checks (before preprocessing)
Before investing hours in preprocessing and analysis, quickly verify the raw data isn't obviously problematic:

### Visual inspection
- Load each subject's T1 in a viewer: Does the brain look normal? Any major artifacts, ghosting, or incomplete coverage?
- Load the functional data: Scroll through volumes. Are there sudden brightness changes (spikes)? Is the brain fully covered?
- Check for signal dropout: Temporal pole, orbitofrontal cortex, and inferior temporal regions often have poor signal due to proximity to air-filled sinuses

### Automated QC with MRIQC
[MRIQC](https://mriqc.readthedocs.io/) runs on BIDS-formatted data and generates:
- Image Quality Metrics (IQMs): SNR, CNR, EFC (entropy-focus-criterion), FBER (foreground-background energy ratio)
- Visual reports with carpet plots, mosaic views, and motion traces
- Group-level comparisons across all subjects

Run MRIQC BEFORE preprocessing to catch bad data early:
```
$ mriqc /bids_dataset /output participant --participant-label sub-001
```

### Exclusion criteria to define BEFORE analysis
Decide your exclusion criteria before looking at results (to avoid bias):
- Maximum mean framewise displacement (often 0.5mm)
- Maximum percentage of high-motion volumes (often 20-30%)
- Minimum brain coverage
- Minimum SNR threshold
- Structural abnormalities (incidental findings — have a protocol for this)

Document these criteria in your methods section. Report how many subjects were excluded and why.

## De-identification and PHI handling
Raw DICOM files often contain Protected Health Information. Before sharing or storing data:

- **Defacing structural MRIs**: Facial features in T1 images can identify subjects. Use [pydeface](https://github.com/poldracklab/pydeface) or [mri_deface](https://surfer.nmr.mgh.harvard.edu/fswiki/mri_deface) to remove facial structures
- **Stripping DICOM headers**: Remove or anonymize patient name, date of birth, MRN from DICOM headers before conversion
- **Following your IRB protocol**: Know what your specific protocol allows for data storage, sharing, and retention

## Resources for deeper learning
- 📄 [BIDS Specification — the full standard](https://bids.neuroimaging.io/)
- 📄 [dcm2niix — DICOM to NIfTI converter](https://github.com/rordenlab/dcm2niix)
- 📄 [HeuDiConv — automated BIDS conversion](https://heudiconv.readthedocs.io/)
- 📄 [BIDS Validator](https://bids-standard.github.io/bids-validator/)
- 📄 [MRIQC — automated quality control](https://mriqc.readthedocs.io/)
- 📄 [OpenNeuro — open repository for BIDS datasets](https://openneuro.org/)
- 📺 [BIDS tutorial — Stanford Center for Reproducible Neuroscience](https://www.youtube.com/watch?v=K9hVAr5fvJg)
