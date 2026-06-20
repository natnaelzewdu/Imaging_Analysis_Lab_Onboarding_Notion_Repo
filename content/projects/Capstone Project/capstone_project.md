---
task_name: "Capstone: Schizophrenia vs Controls Analysis"
emoji: "🎓"
tier: Hands-On
order: 1
url: "https://openneuro.org/datasets/ds000030"
---
## Project Overview
This capstone project takes you through a complete neuroimaging analysis from start to finish — the same workflow used in real lab publications. You will analyze resting-state fMRI data from schizophrenia patients and healthy controls, extract brain networks using ICA, compute functional network connectivity, identify group differences, and build a classifier.

**Dataset**: [UCLA Consortium for Neuropsychiatric Phenomics (CNP) — OpenNeuro ds000030](https://openneuro.org/datasets/ds000030) — a publicly available dataset with ~50 schizophrenia patients, ~49 bipolar patients, ~43 ADHD patients, and ~130 healthy controls. Includes resting-state fMRI, task fMRI, and structural MRI. Already in BIDS format with direct download — no special access requests needed.

For this project you will compare **schizophrenia (SZ) vs. healthy controls (HC)** only.

**What you'll produce**:
- Quality-controlled, preprocessed fMRI data
- Neuromark ICA components for every subject
- Static functional network connectivity (sFNC) matrices
- Statistical maps showing connectivity differences between patients and controls
- A classifier distinguishing patients from controls using brain connectivity features
- Publication-quality figures

**Skills exercised**: fMRI fundamentals, brain anatomy, ICA, Group ICA, preprocessing, quality control, SLURM, GIFT, statistics, visualization, connectivity interpretation, and classification.

## Phase 1: Data Acquisition and Organization

### Step 1.1: Download the dataset from OpenNeuro
The UCLA CNP dataset is available for direct download from [OpenNeuro ds000030](https://openneuro.org/datasets/ds000030). It's already in BIDS format.

**Option A — Download via DataLad (recommended for cluster)**:
```
cd $MYDATA/projects/capstone
pip install datalad
datalad install https://github.com/OpenNeuroDatasets/ds000030.git
cd ds000030
datalad get sub-*/anat/ sub-*/func/*rest*
```

**Option B — Download via AWS CLI**:
```
aws s3 sync --no-sign-request s3://openneuro.org/ds000030 $MYDATA/projects/capstone/ds000030
```

The dataset includes:
- T1-weighted structural MRI (1 per subject)
- Resting-state fMRI (1 run per subject)
- Task fMRI (you'll use only resting-state for this project)
- Demographic information (age, sex, diagnosis) in `participants.tsv`

### Step 1.2: Set up your project directory
```
mkdir -p $MYDATA/projects/capstone
cd $MYDATA/projects/capstone
mkdir -p data/raw data/preprocessed results/ica results/fnc results/classification results/figures scripts logs
```

### Step 1.3: Create a subject list
The `participants.tsv` file in the dataset root contains diagnosis info. Extract the SZ and HC subjects:
```python
import pandas as pd

df = pd.read_csv('ds000030/participants.tsv', sep='\t')
sz = df[df['diagnosis'] == 'SCHZ']['participant_id']
hc = df[df['diagnosis'] == 'CONTROL']['participant_id']

sz.to_csv('subjects_sz.txt', index=False, header=False)
hc.to_csv('subjects_hc.txt', index=False, header=False)

all_subs = pd.concat([sz, hc])
all_subs.to_csv('subjects.txt', index=False, header=False)

print(f"SZ: {len(sz)}, HC: {len(hc)}, Total: {len(all_subs)}")
print(f"Age — SZ: {df[df['diagnosis']=='SCHZ']['age'].mean():.1f} +/- {df[df['diagnosis']=='SCHZ']['age'].std():.1f}")
print(f"Age — HC: {df[df['diagnosis']=='CONTROL']['age'].mean():.1f} +/- {df[df['diagnosis']=='CONTROL']['age'].std():.1f}")
```

### Step 1.4: Initialize version control
```
cd $MYDATA/projects/capstone
git init
echo "data/" >> .gitignore
echo "results/" >> .gitignore
echo "*.nii" >> .gitignore
echo "*.nii.gz" >> .gitignore
git add scripts/ .gitignore
git commit -m "Initial project setup"
```

**Checkpoint**: Clean project directory, subject lists (SZ and HC), demographics verified, git repo initialized.

## Phase 2: Quality Control of Raw Data

### Step 2.1: Visual inspection
Start an interactive session and visually inspect a handful of subjects:
```
srun -p qTRD -A trends53c17 -c 2 --mem=8G --time=2:00:00 --pty /bin/bash
module load matlab
matlab -nodisplay
```

In MATLAB, load a NIfTI file and check:
- Does the brain look normal? Any major artifacts?
- Is the full brain covered (no missing slices)?
- Scroll through timepoints — any sudden brightness changes?

### Step 2.2: Compute framewise displacement (FD)
FD summarizes head motion between consecutive volumes. Here's how to compute it step by step.

**Step A** — Run SPM realignment to get motion parameters:
```matlab
addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));
spm('defaults', 'fmri');

func_file = '/path/to/ds000030/sub-10159/func/sub-10159_task-rest_bold.nii';
matlabbatch{1}.spm.spatial.realign.estimate.data = {cellstr(spm_select('Expand', func_file))};
matlabbatch{1}.spm.spatial.realign.estimate.eoptions.quality = 0.9;
matlabbatch{1}.spm.spatial.realign.estimate.eoptions.sep = 4;
matlabbatch{1}.spm.spatial.realign.estimate.eoptions.rtm = 1;
spm_jobman('run', matlabbatch);
% Produces rp_*.txt with 6 motion parameters per volume (x, y, z, pitch, roll, yaw)
```

**Step B** — Compute FD from the motion parameter file:
```matlab
function fd = compute_fd(rp_file)
    % rp_file: path to rp_*.txt from SPM realignment
    % Returns: framewise displacement in mm for each volume
    mp = load(rp_file);            % N x 6: [x y z pitch roll yaw]
    mp(:,4:6) = mp(:,4:6) * 50;   % Convert rotations (radians) to mm (50mm head radius)
    dmp = diff(mp);                % (N-1) x 6: volume-to-volume change
    fd = [0; sum(abs(dmp), 2)];    % Sum of absolute displacements; first volume = 0
end
```

**Step C** — Apply exclusion criteria (define these BEFORE looking at results):
```matlab
rp_file = '/path/to/rp_sub-10159_task-rest_bold.txt';
fd = compute_fd(rp_file);
mean_fd = mean(fd);
pct_bad = sum(fd > 0.5) / length(fd) * 100;

fprintf('Subject: sub-10159\n');
fprintf('  Mean FD: %.3f mm\n', mean_fd);
fprintf('  Volumes with FD > 0.5mm: %.1f%%\n', pct_bad);

% Exclusion criteria:
%   Mean FD > 0.5mm         --> EXCLUDE
%   >20% of volumes FD>0.5  --> EXCLUDE
if mean_fd > 0.5 || pct_bad > 20
    fprintf('  DECISION: EXCLUDE\n');
else
    fprintf('  DECISION: INCLUDE\n');
end
```

**Step D** — Run for ALL subjects as a SBATCH array job:
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem=4G
#SBATCH -t 0:30:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -J qc_motion
#SBATCH -e logs/qc_%A-%a.err
#SBATCH -o logs/qc_%A-%a.out

module load matlab
SUBJECT=$(sed -n "$(( $SLURM_ARRAY_TASK_ID + 1 )) p" subjects.txt)
matlab -nodisplay -r "addpath('scripts'); compute_motion_qc('$SUBJECT'); exit"
```

Submit: `sbatch --array=0-149%30 scripts/qc_motion_job.sh`

Collect results into `logs/exclusion_log.txt` after all jobs complete.

### Step 2.3: Check demographic balance after exclusions
```python
import pandas as pd
from scipy import stats

included = pd.read_csv('logs/included_subjects.csv')
sz = included[included['group'] == 'SZ']
hc = included[included['group'] == 'HC']

print(f"Included — SZ: {len(sz)}, HC: {len(hc)}")

t, p = stats.ttest_ind(sz['age'], hc['age'])
print(f"Age: SZ={sz['age'].mean():.1f}+/-{sz['age'].std():.1f}, HC={hc['age'].mean():.1f}+/-{hc['age'].std():.1f}, p={p:.3f}")

from scipy.stats import chi2_contingency
table = pd.crosstab(included['group'], included['sex'])
chi2, p_sex, _, _ = chi2_contingency(table)
print(f"Sex balance: chi2={chi2:.2f}, p={p_sex:.3f}")
```

**Checkpoint**: Exclusion log with FD values for every subject, demographics verified balanced, at least ~40 subjects per group.

## Phase 3: Preprocessing

### Step 3.1: Preprocessing pipeline
Use **SPM12** with the standard pipeline: Realignment, Coregistration, Segmentation + Normalization (MNI, 3mm voxels), Smoothing (6mm FWHM).

### Step 3.2: Write a preprocessing script
Create `scripts/preprocess_subject.m`:
```matlab
function preprocess_subject(subject_id)
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));
    spm('defaults', 'fmri');
    spm_jobman('initcfg');

    base_dir = '/path/to/ds000030';
    out_dir  = '/path/to/data/preprocessed';
    func_file = fullfile(base_dir, subject_id, 'func', [subject_id '_task-rest_bold.nii']);
    anat_file = fullfile(base_dir, subject_id, 'anat', [subject_id '_T1w.nii']);
    subj_out  = fullfile(out_dir, subject_id);
    mkdir(subj_out);

    % Step 1: Realignment
    matlabbatch{1}.spm.spatial.realign.estwrite.data = {cellstr(spm_select('Expand', func_file))};

    % Step 2: Coregistration (mean EPI to T1)
    matlabbatch{2}.spm.spatial.coreg.estimate.ref = {anat_file};
    matlabbatch{2}.spm.spatial.coreg.estimate.source(1) = ...
        cfg_dep('Realign: Estimate & Reslice: Mean Image', substruct('.','val','{}',{1}), substruct('.','rmean'));

    % Step 3: Segment T1 (produces deformation field for normalization)
    matlabbatch{3}.spm.spatial.preproc.channel.vols = {anat_file};

    % Step 4: Normalize functional images to MNI space
    matlabbatch{4}.spm.spatial.normalise.write.subj.def(1) = ...
        cfg_dep('Segment: Forward Deformations', substruct('.','val','{}',{3}), substruct('()',{1},'.','fordef'));
    matlabbatch{4}.spm.spatial.normalise.write.subj.resample(1) = ...
        cfg_dep('Realign: Estimate & Reslice: Resliced Images', substruct('.','val','{}',{1}), substruct('.','rfiles'));
    matlabbatch{4}.spm.spatial.normalise.write.woptions.vox = [3 3 3];

    % Step 5: Smooth (6mm FWHM)
    matlabbatch{5}.spm.spatial.smooth.data(1) = ...
        cfg_dep('Normalise: Write: Normalised Images', substruct('.','val','{}',{4}), substruct('.','files'));
    matlabbatch{5}.spm.spatial.smooth.fwhm = [6 6 6];

    spm_jobman('run', matlabbatch);
    fprintf('Preprocessing complete for %s\n', subject_id);
end
```

### Step 3.3: Submit as SBATCH array job
```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 2
#SBATCH --mem=16G
#SBATCH -t 4:00:00
#SBATCH -p qTRD
#SBATCH -A trends53c17
#SBATCH -J preproc
#SBATCH -e logs/preproc_%A-%a.err
#SBATCH -o logs/preproc_%A-%a.out

module load matlab
SUBJECT=$(sed -n "$(( $SLURM_ARRAY_TASK_ID + 1 )) p" subjects.txt)
matlab -nodisplay -r "addpath('scripts'); preprocess_subject('$SUBJECT'); exit"
```

Submit: `sbatch --array=0-99%20 scripts/preprocess_job.sh`

### Step 3.4: Verify preprocessing quality
Spot-check several subjects:
- Overlay normalized brain on MNI template — do cortical boundaries match?
- Check that smoothed images look visibly blurred but retain brain shape
- Verify output file naming: `swrsub-XXXXX_task-rest_bold.nii`

**Checkpoint**: All subjects preprocessed, QC spot-checks passed.

## Phase 4: ICA with Neuromark

### Step 4.1: Run Neuromark back-reconstruction
Use the Neuromark template to extract 53 standardized brain network components per subject via spatially constrained ICA (GIG-ICA).

Create `scripts/run_neuromark.m`:
```matlab
function run_neuromark(subject_id)
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/GroupICATv4.0c/'));
    addpath(genpath('/trdapps/linux-x86_64/matlab/toolboxes/spm12/'));

    preproc_dir = '/path/to/data/preprocessed';
    results_dir = '/path/to/results/ica';
    template    = '/path/to/neuromark_template.nii';

    func_file  = fullfile(preproc_dir, subject_id, ['swr' subject_id '_task-rest_bold.nii']);
    output_dir = fullfile(results_dir, subject_id);
    mkdir(output_dir);

    % Run GIG-ICA (spatially constrained ICA using Neuromark template)
    % Consult GIFT documentation for exact batch function calls
    % Key function: icatb_gigicar()
    %
    % Inputs:  func_file (preprocessed 4D NIfTI), template (Neuromark 53 components)
    % Outputs: 53 spatial maps (.nii) and 53 timecourses (.mat)

    fprintf('Neuromark ICA complete for %s\n', subject_id);
end
```

Submit as SBATCH array job (same pattern as preprocessing).

### Step 4.2: Verify ICA results
For a few subjects:
- Load spatial maps in GIFT display tools
- Verify DMN is in medial prefrontal + PCC, visual is in occipital
- Check timecourses for spikes or flatlines
- Confirm spatial correlation with template is > 0.4 for most components

### Step 4.3: Extract timecourses
Collect all 53 component timecourses per subject:
```matlab
% For each subject: tc = 53 x T matrix (components x timepoints)
save(fullfile(results_dir, subject_id, 'timecourses.mat'), 'tc');
```

**Checkpoint**: 53 component spatial maps and timecourses for every included subject.

## Phase 5: Static Functional Network Connectivity

### Step 5.1: Compute sFNC for each subject
```matlab
function compute_sfnc(subject_id)
    results_dir = '/path/to/results';
    load(fullfile(results_dir, 'ica', subject_id, 'timecourses.mat'), 'tc');

    fnc = corr(tc');                              % 53 x 53 Pearson correlation
    fnc_z = atanh(fnc);                           % Fisher z-transform
    fnc_z(logical(eye(size(fnc_z)))) = 0;         % Zero diagonal

    save(fullfile(results_dir, 'fnc', [subject_id '_sfnc.mat']), 'fnc_z');
    fprintf('sFNC computed for %s\n', subject_id);
end
```

### Step 5.2: Aggregate all subjects into group arrays
```matlab
sz_subjects = readlines('subjects_sz.txt');
hc_subjects = readlines('subjects_hc.txt');
results_dir = '/path/to/results';

fnc_all_sz = zeros(53, 53, length(sz_subjects));
fnc_all_hc = zeros(53, 53, length(hc_subjects));

for i = 1:length(sz_subjects)
    load(fullfile(results_dir, 'fnc', [sz_subjects{i} '_sfnc.mat']), 'fnc_z');
    fnc_all_sz(:,:,i) = fnc_z;
end
for i = 1:length(hc_subjects)
    load(fullfile(results_dir, 'fnc', [hc_subjects{i} '_sfnc.mat']), 'fnc_z');
    fnc_all_hc(:,:,i) = fnc_z;
end

save(fullfile(results_dir, 'fnc', 'group_sfnc.mat'), 'fnc_all_sz', 'fnc_all_hc');
```

**Checkpoint**: sFNC matrices for all subjects, aggregated into group arrays.

## Phase 6: Group Comparison Statistics

### Step 6.1: Two-sample t-tests on each FNC pair
```python
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

fnc_sz = np.load('results/fnc/fnc_sz.npy')   # (N_sz, 53, 53)
fnc_hc = np.load('results/fnc/fnc_hc.npy')   # (N_hc, 53, 53)

n_components = 53
triu_idx = np.triu_indices(n_components, k=1)
n_pairs = len(triu_idx[0])   # 1378

sz_features = np.array([fnc_sz[i][triu_idx] for i in range(len(fnc_sz))])
hc_features = np.array([fnc_hc[i][triu_idx] for i in range(len(fnc_hc))])

t_stats = np.zeros(n_pairs)
p_values = np.zeros(n_pairs)
effect_sizes = np.zeros(n_pairs)

for j in range(n_pairs):
    t_stats[j], p_values[j] = stats.ttest_ind(sz_features[:, j], hc_features[:, j])
    pooled_std = np.sqrt((sz_features[:, j].var() + hc_features[:, j].var()) / 2)
    if pooled_std > 0:
        effect_sizes[j] = (sz_features[:, j].mean() - hc_features[:, j].mean()) / pooled_std

reject, p_corrected, _, _ = multipletests(p_values, method='fdr_bh', alpha=0.05)
print(f"Significant connections (FDR q<0.05): {reject.sum()} / {n_pairs}")
print(f"Largest effect size: d = {np.max(np.abs(effect_sizes)):.2f}")
```

### Step 6.2: Visualize group-average FNC matrices
```python
import matplotlib.pyplot as plt

mean_hc = np.mean(fnc_hc, axis=0)
mean_sz = np.mean(fnc_sz, axis=0)
diff = mean_sz - mean_hc

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
axes[0].imshow(mean_hc, cmap='RdBu_r', vmin=-0.5, vmax=0.5)
axes[0].set_title('Healthy Controls')
axes[1].imshow(mean_sz, cmap='RdBu_r', vmin=-0.5, vmax=0.5)
axes[1].set_title('Schizophrenia')
im = axes[2].imshow(diff, cmap='RdBu_r', vmin=-0.2, vmax=0.2)
axes[2].set_title('Difference (SZ - HC)')
plt.colorbar(im, ax=axes[2], label='Delta Fisher z')
plt.tight_layout()
plt.savefig('results/figures/fnc_group_comparison.png', dpi=300)
plt.show()
```

### Step 6.3: Map significant connections to brain networks
```python
sig_pairs = np.where(reject)[0]
print(f"\n{'Connection':>30s} {'t-stat':>8s} {'p(FDR)':>8s} {'d':>6s}")
print("-" * 60)
for idx in sig_pairs[:20]:
    i, j = triu_idx[0][idx], triu_idx[1][idx]
    print(f"  Component {i:2d} <-> {j:2d}            {t_stats[idx]:8.2f} {p_corrected[idx]:8.4f} {effect_sizes[idx]:6.2f}")
```

**Checkpoint**: Significant FNC differences identified with effect sizes, publication-quality figure of group comparison.

## Phase 7: Classification

### Step 7.1: Build the classification pipeline
```python
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, confusion_matrix

X = np.vstack([sz_features, hc_features])
y = np.array([1]*len(sz_features) + [0]*len(hc_features))

kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
fold_accuracies = []
fold_aucs = []
all_y_true = []
all_y_pred = []

for fold, (train_idx, test_idx) in enumerate(kf.split(X, y)):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X[train_idx])
    X_test = scaler.transform(X[test_idx])

    clf = SVC(kernel='linear', C=1.0, probability=True)
    clf.fit(X_train, y[train_idx])

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    acc = balanced_accuracy_score(y[test_idx], y_pred)
    auc = roc_auc_score(y[test_idx], y_prob)

    fold_accuracies.append(acc)
    fold_aucs.append(auc)
    all_y_true.extend(y[test_idx])
    all_y_pred.extend(y_pred)
    print(f"Fold {fold+1}: Balanced Accuracy = {acc:.1%}, AUC = {auc:.3f}")

print(f"\nOverall: {np.mean(fold_accuracies):.1%} +/- {np.std(fold_accuracies):.1%}")
print(f"AUC: {np.mean(fold_aucs):.3f} +/- {np.std(fold_aucs):.3f}")
print(f"\nConfusion Matrix:\n{confusion_matrix(all_y_true, all_y_pred)}")
```

### Step 7.2: Permutation testing
```python
n_permutations = 1000
null_accuracies = []

for perm in range(n_permutations):
    y_perm = np.random.permutation(y)
    perm_accs = []
    for train_idx, test_idx in kf.split(X, y_perm):
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X[train_idx])
        X_test = scaler.transform(X[test_idx])
        clf = SVC(kernel='linear', C=1.0)
        clf.fit(X_train, y_perm[train_idx])
        perm_accs.append(balanced_accuracy_score(y_perm[test_idx], clf.predict(X_test)))
    null_accuracies.append(np.mean(perm_accs))
    if (perm + 1) % 100 == 0:
        print(f"  Permutation {perm+1}/{n_permutations}")

p_value = np.mean(np.array(null_accuracies) >= np.mean(fold_accuracies))
print(f"\nReal accuracy: {np.mean(fold_accuracies):.1%}")
print(f"Permutation p-value: {p_value:.4f}")
```

### Step 7.3: Feature importance
```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
clf_full = SVC(kernel='linear', C=1.0)
clf_full.fit(X_scaled, y)

weights = np.abs(clf_full.coef_[0])
weight_matrix = np.zeros((n_components, n_components))
weight_matrix[triu_idx] = weights
weight_matrix = weight_matrix + weight_matrix.T

plt.figure(figsize=(8, 7))
plt.imshow(weight_matrix, cmap='hot')
plt.colorbar(label='|SVM weight|')
plt.title('Most Discriminative Connections')
plt.savefig('results/figures/feature_importance.png', dpi=300)
plt.show()

top_idx = np.argsort(weights)[-10:][::-1]
print("\nTop 10 most discriminative connections:")
for idx in top_idx:
    i, j = triu_idx[0][idx], triu_idx[1][idx]
    print(f"  Component {i:2d} <-> {j:2d} (weight={weights[idx]:.4f})")
```

**Checkpoint**: Classification accuracy with CI, permutation p-value, feature importance map.

## Phase 8: Figures and Presentation

### Create final figures
- **Figure 1**: Group-average sFNC matrices (HC and SZ side by side + difference)
- **Figure 2**: Significant connections highlighted (FDR-corrected)
- **Figure 3**: Classification confusion matrix + feature importance heatmap

### Present to the lab
Prepare a 15-minute presentation:
- Dataset and sample description
- Pipeline overview (preprocessing → ICA → FNC → statistics → classification)
- Key results (show figures)
- What you learned and what you'd do differently

## Deliverables checklist
- [ ] Project directory with organized code and scripts
- [ ] Git repository with all analysis scripts
- [ ] Exclusion log with FD values and criteria for every subject
- [ ] Preprocessed data with QC verification
- [ ] Neuromark ICA results for all subjects
- [ ] sFNC matrices for all subjects
- [ ] Group comparison results with FDR correction and effect sizes
- [ ] Classification accuracy with permutation test
- [ ] Key figures (3 minimum)
- [ ] Lab presentation

## Resources
- 📑 [UCLA CNP Dataset on OpenNeuro (ds000030)](https://openneuro.org/datasets/ds000030)
- 📄 [GIFT Toolbox](https://trendscenter.org/software/gift/)
- 📑 [Iraji et al. (2019) — Neuromark](https://doi.org/10.1002/hbm.24580)
- 📑 [Du et al. (2020) — Neuromark Pipeline](https://doi.org/10.1016/j.nicl.2020.102375)
- 📄 [scikit-learn SVM Guide](https://scikit-learn.org/stable/modules/svm.html)
