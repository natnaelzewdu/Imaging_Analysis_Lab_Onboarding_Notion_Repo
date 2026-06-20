## Why this matters to you

The neuroimaging software ecosystem can be overwhelming — there are dozens of tools, each with different strengths, file formats, and communities. Knowing the major players and when to use each prevents you from reinventing the wheel and helps you follow methods sections in papers. The lab primarily uses SPM and GIFT, but you'll frequently encounter others.

## The major tools

### SPM (Statistical Parametric Mapping)

- **What**: MATLAB-based package for preprocessing, GLM analysis, and visualization

- **Developed by**: Wellcome Centre for Human Neuroimaging, UCL (London)

- **Lab uses it for**: Preprocessing (realignment, normalization, smoothing)

- **Strengths**: Mature, well-validated, excellent documentation, huge user community

- **Limitations**: MATLAB-only, GUI can be slow, some algorithms (especially normalization) are showing their age compared to newer tools

- **Website**: [fil.ion.ucl.ac.uk/spm](https://www.fil.ion.ucl.ac.uk/spm/)

### GIFT (Group ICA of fMRI Toolbox)

- **What**: MATLAB-based toolbox for ICA, Group ICA, FNC, and dFNC analysis

- **Developed by**: TReNDs Center (our lab!)

- **Lab uses it for**: Everything ICA-related — this is the lab's flagship software

- **Strengths**: The most comprehensive ICA toolbox available, actively developed, includes Neuromark, Mancovan, dFNC, and many other analysis tools

- **Key features**: Group ICA, back-reconstruction, component visualization, sorting, FNC/dFNC, spatial chronnectome, Mancovan stats

- **Website**: [trendscenter.org/software/gift](https://trendscenter.org/software/gift/)

### AFNI (Analysis of Functional NeuroImages)

- **What**: C-based command-line toolkit with extensive fMRI analysis capabilities

- **Developed by**: NIMH (National Institute of Mental Health)

- **Lab uses it for**: Specific preprocessing steps (e.g., 3dDespike for removing signal spikes); GIFT uses some AFNI functions internally

- **Strengths**: Blazing fast, extremely flexible, powerful command-line tools, excellent visualization (AFNI viewer), great documentation and training workshops

- **Limitations**: Steep learning curve, Unix-centric

- **Key commands**: 3dDespike, 3dresample, 3dcalc, 3dDeconvolve, 3dttest++

- **Website**: [afni.nimh.nih.gov](https://afni.nimh.nih.gov/)

### FSL (FMRIB Software Library)

- **What**: Comprehensive toolkit for fMRI, diffusion MRI, and structural analysis

- **Developed by**: University of Oxford (FMRIB group)

- **Lab uses it for**: Occasional cross-validation of results; FSL's ICA implementation (MELODIC) is an alternative to GIFT

- **Strengths**: Excellent preprocessing (BET brain extraction, FLIRT/FNIRT registration), MELODIC for ICA, FSLeyes viewer is superb for data visualization

- **Key tools**: BET (brain extraction), FAST (tissue segmentation), FLIRT/FNIRT (registration), FEAT (GLM), MELODIC (ICA), FSLeyes (viewer)

- **Website**: [fsl.fmrib.ox.ac.uk](https://fsl.fmrib.ox.ac.uk/fsl/)

### ANTs (Advanced Normalization Tools)

- **What**: C++-based toolkit focused on image registration and normalization

- **Developed by**: UPenn (Brian Avants, Nick Tustison)

- **Lab uses it for**: When high-quality normalization is critical

- **Strengths**: Generally considered the gold standard for non-linear brain registration. The SyN algorithm consistently wins registration accuracy benchmarks

- **Website**: [stnava.github.io/ANTs](https://stnava.github.io/ANTs/)

### FreeSurfer

- **What**: Toolkit for surface-based analysis of structural MRI

- **Developed by**: Harvard/MIT (Martinos Center)

- **Lab uses it for**: Cortical thickness measurements, surface-based analyses

- **Strengths**: Reconstructs the cortical surface (pial and white matter boundaries), computes thickness, area, volume, curvature. Essential for vertex-wise analyses

- **Limitations**: Very slow (~8-12 hours per subject for full recon-all)

- **Website**: [surfer.nmr.mgh.harvard.edu](https://surfer.nmr.mgh.harvard.edu/)

### Python ecosystem (nilearn, nibabel, MNE-Python)

- **[nilearn](https://nilearn.github.io/)**: Machine learning for neuroimaging — GLM, connectivity analysis, decoding, plotting brain maps

- **[nibabel](https://nipy.org/nibabel/)**: Load/save NIfTI, GIFTI, and other neuroimaging file formats in Python

- **[MNE-Python](https://mne.tools/)**: EEG/MEG analysis (relevant for multimodal work)

- **Lab uses these for**: Custom analyses, scripting, data manipulation, ML/DL pipelines

### Visualization Tools

- **[MRIcron](https://www.nitrc.org/projects/mricron)**: Lightweight NIfTI viewer for quick visualization of brain images and overlays. Good for checking your data and creating publication figures.

- **[MRIcroGL](https://www.nitrc.org/projects/mricrogl)**: A newer, GPU-accelerated viewer with 3D rendering, scripting support, and volume rendering. Excellent for creating high-quality brain visualizations.

- **[FSLeyes](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLeyes)**: FSL's viewer — interactive, supports overlays, time series, and lightbox views. Often used alongside other tools.

## How they fit together in the lab's workflow

A typical pipeline:

1. **SPM** or **fmriprep**: Preprocess raw fMRI data

2. **GIFT**: Run Group ICA, extract components, compute FNC/dFNC

3. **GIFT Mancovan**: Group statistics

4. **Python (scikit-learn, PyTorch)**: Classification/deep learning on ICA features

5. **FSLeyes / AFNI viewer / GIFT display**: Visualization

6. **MATLAB scripts**: Custom analysis steps, batch processing

## File formats you'll encounter

- **.nii / .nii.gz**: NIfTI format — the standard for brain images

- **.mat**: MATLAB files — used extensively by SPM and GIFT

- **.gii**: GIFTI — surface-based data format

- **.txt / .csv / .tsv**: Tabular data (motion parameters, subject lists, results)

- **.dcm**: DICOM — raw scanner format (you'll rarely work with these directly)

## Resources for deeper learning

- 📄 [Andy's Brain Book — Overview of fMRI Software](https://andysbrainbook.readthedocs.io/en/latest/)

- 📄 [Neuroimaging Data Processing Tools — comprehensive comparison](https://doi.org/10.3389/fninf.2019.00035)

- 📄 [GIFT Toolbox download and documentation](https://trendscenter.org/software/gift/)

- 📺 [AFNI Academy — training workshops](https://www.youtube.com/c/AFNIacademy)

- 📄 [FSL Course materials](https://fsl.fmrib.ox.ac.uk/fslcourse/)
