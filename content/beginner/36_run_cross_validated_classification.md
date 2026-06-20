## Why this matters to you
In the previous task, you trained on the full training set and tested on a separate test set. But in real neuroimaging research, you rarely have a separate test set — you have one dataset and need to estimate how well your model generalizes. Cross-validation (CV) solves this by systematically leaving out portions of data for testing. Combining CV with SBATCH array jobs is the standard approach for classification studies in the lab.

## What cross-validation does
K-fold cross-validation splits your data into K equal parts (folds). For each fold:
1. Hold out that fold as the test set
2. Train on the remaining K-1 folds
3. Evaluate on the held-out fold
4. Record the metrics

After all K folds, you have K accuracy scores. The mean gives your performance estimate, and the standard deviation tells you how stable the estimate is.

## Why arrays are perfect for cross-validation
Each fold is completely independent — fold 3's training doesn't depend on fold 1's results. This makes cross-validation embarrassingly parallel. With SBATCH arrays:
- Submit `--array=0-4` for 5-fold CV
- Each task trains and evaluates one fold
- All 5 folds run simultaneously on different GPUs
- Total wall time = time for 1 fold, not 5×

## Step 1: Get the example code

```
$ cd $MYDATA/ClusterWorkshop/Examples/PytorchClassificationCV
$ ls
```

You should see:
- `mnist_classification.py` — Training script modified to accept a fold index
- `JobSubmit.sh` — SBATCH array script

## Step 2: How the script uses the fold index
The key modification from the non-CV version:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-k', type=int, required=True, help='Fold index (0 to K-1)')
args = parser.parse_args()

# Create K-fold splitter
from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Get the k-th fold's train and test indices
for fold_idx, (train_idx, test_idx) in enumerate(kf.split(dataset)):
    if fold_idx == args.k:
        train_subset = Subset(dataset, train_idx)
        test_subset = Subset(dataset, test_idx)
        break

print(f"Fold {args.k}: {len(train_idx)} train, {len(test_idx)} test")
```

Important:
- `random_state=42`: Ensures the SAME splits across all folds. Without a fixed seed, each task would create different random splits, making the folds overlap.
- The fold index comes from `$SLURM_ARRAY_TASK_ID` via the command line argument `-k`

## Step 3: Review the SBATCH script
`JobSubmit.sh`:

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH --gres=gpu:1
#SBATCH --mem=8G
#SBATCH -t 1:00:00
#SBATCH -p qTRDGPU
#SBATCH -A trends53c17
#SBATCH -J cv_mnist
#SBATCH -e error%A-%a.err
#SBATCH -o out%A-%a.out

source $MYDATA/bin/miniconda3/etc/profile.d/conda.sh
conda activate cw_torch

echo "Fold: $SLURM_ARRAY_TASK_ID"
nvidia-smi

python mnist_classification.py -k $SLURM_ARRAY_TASK_ID
```

The critical line: `python mnist_classification.py -k $SLURM_ARRAY_TASK_ID` passes the array task index as the fold number.

## Step 4: Submit the 5-fold CV

```
$ sbatch --array=0-4 JobSubmit.sh
```

This submits 5 GPU jobs. Each trains on 4 folds and tests on 1 fold.

Monitor:
```
$ squeue -u $USER
```

## Step 5: Collect results
After all 5 tasks complete, check each fold's output:

```
$ grep "Test Accuracy" out*-0.out    # Fold 0 accuracy
$ grep "Test Accuracy" out*-1.out    # Fold 1 accuracy
$ grep "Test Accuracy" out*-2.out    # Fold 2 accuracy
...
```

Or in one command:
```
$ grep "Test Accuracy" out*-*.out | sort
```

Expected output (for MNIST):
```
out12345-0.out: Test Accuracy: 99.15%
out12345-1.out: Test Accuracy: 99.08%
out12345-2.out: Test Accuracy: 99.21%
out12345-3.out: Test Accuracy: 99.11%
out12345-4.out: Test Accuracy: 99.18%
```

Mean accuracy: 99.15% ± 0.05%

## 10-fold CV
For 10-fold cross-validation (often used in neuroimaging):
```
$ sbatch --array=0-9 JobSubmit.sh
```

Update the script to use `n_splits=10` in the KFold call.

## Nested cross-validation
For rigorous evaluation (common in publications):
- **Outer loop**: K-fold for performance estimation
- **Inner loop**: K-fold for hyperparameter tuning (within each outer fold's training set)

This prevents data leakage from hyperparameter selection. The outer loop is parallelized with arrays; the inner loop runs within each task.

## Applying to neuroimaging data
For real brain imaging classification:

```python
# Instead of MNIST:
import numpy as np

# Load ICA features (e.g., FNC matrices)
data = np.load('fnc_features.npy')    # Shape: (n_subjects, n_features)
labels = np.load('labels.npy')        # Shape: (n_subjects,) — 0 or 1

# Same KFold procedure
kf = KFold(n_splits=5, shuffle=True, random_state=42)
for fold_idx, (train_idx, test_idx) in enumerate(kf.split(data)):
    if fold_idx == args.k:
        X_train, X_test = data[train_idx], data[test_idx]
        y_train, y_test = labels[train_idx], labels[test_idx]
        break
```

## Important statistical considerations
- **Always report mean ± std** across folds, not just the best fold
- **Use the same random seed** for fold splitting across all runs
- **Stratified K-fold** (`StratifiedKFold`) maintains class proportions in each fold — important when classes are imbalanced
- **Never tune hyperparameters on the test fold** — this inflates accuracy (use nested CV instead)
- **Report balanced accuracy** when classes are unequal (e.g., 80 controls vs. 40 patients)
- **Permutation testing**: Shuffle labels 1000+ times to establish a null distribution. If your real accuracy doesn't exceed the 95th percentile of shuffled accuracies, your result is not significantly better than chance. With small samples, this is essential.
- **Report individual fold results**: Showing all fold accuracies (not just the mean) reveals whether performance is stable or driven by one lucky split
- **Feature normalization within folds**: If you z-score features, compute mean/std from the training set only, then apply to the test set. Computing statistics across all subjects before splitting is data leakage.

## Resources for deeper learning
- 🔗 [Cluster Workshop — PytorchClassificationCV example](https://github.com/trendscenter/ClusterWorkshop)
- 📄 [scikit-learn: Cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html)
- 📺 [StatQuest: Cross-validation explained](https://www.youtube.com/watch?v=fSytzGwwBVw)
- 📑 [Varoquaux et al. (2017) — Assessing and Tuning Brain Decoders](https://doi.org/10.1016/j.neuroimage.2016.10.038)
