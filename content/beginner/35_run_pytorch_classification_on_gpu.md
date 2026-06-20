## Why this matters to you
Deep learning is increasingly central to the lab's work — classifying brain disorders from neuroimaging data, learning representations of brain networks, and predicting clinical outcomes. PyTorch is the framework of choice because of its flexibility and strong GPU support. This task gets you running your first neural network on the cluster's GPUs, establishing the workflow you'll use for research-grade deep learning projects.

## What you'll build
A simple convolutional neural network (CNN) that classifies handwritten digits from the [MNIST dataset](http://yann.lecun.com/exdb/mnist/). MNIST is the "Hello World" of deep learning — 28×28 pixel grayscale images of digits 0-9. It's trivial by modern standards, but it validates that your entire GPU pipeline works: conda environment, PyTorch, CUDA, GPU access, and SBATCH submission.

## Step 1: Set up the PyTorch environment
If you haven't already created a PyTorch conda environment:

```
$ srun -p qTRDGPU -A trends53c17 -c 4 --gres=gpu:1 --mem=8G --time=1:00:00 --pty -J setup /bin/bash

# On the GPU node:
$ source $MYDATA/bin/miniconda3/etc/profile.d/conda.sh
$ conda create -y --name cw_torch python=3.10
$ conda activate cw_torch
$ conda install -y pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
$ conda install -y -c conda-forge scikit-learn matplotlib
```

Verify GPU is accessible from PyTorch:
```
$ python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

This should print `True` and the GPU model name (e.g., `NVIDIA RTX A40`).

## Step 2: Get the example code
```
$ cd $MYDATA/ClusterWorkshop/Examples/PytorchClassification
$ ls
```

You should see:
- `mnist_classification.py` — The training script
- `JobSubmit.sh` — SBATCH submission script

## Step 3: Review the training script
The script contains these key steps:

```python
# 1. Load MNIST data
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)

# 2. Define a simple CNN
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 10)

# 3. Move model and data to GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = Net().to(device)

# 4. Train for N epochs
for epoch in range(num_epochs):
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        ...

# 5. Report accuracy
```

### Key PyTorch concepts
- **`model.to(device)`**: Moves model parameters to GPU memory
- **`data.to(device)`**: Moves training data to GPU for each batch
- **`torch.cuda.is_available()`**: Checks if GPU is accessible
- **DataLoader**: Handles batching, shuffling, and parallel data loading
- **Loss function**: CrossEntropyLoss for classification
- **Optimizer**: Typically Adam or SGD

## Step 4: Review the SBATCH script
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
#SBATCH -J pytorch_mnist
#SBATCH -e error%A.err
#SBATCH -o out%A.out

source $MYDATA/bin/miniconda3/etc/profile.d/conda.sh
conda activate cw_torch

echo "GPU Info:"
nvidia-smi

python mnist_classification.py
```

Note the key differences from CPU jobs:
- `-p qTRDGPU`: GPU partition
- `--gres=gpu:1`: Request 1 GPU
- conda activation for the PyTorch environment
- `nvidia-smi` logged for debugging

## Step 5: Submit and monitor

```
$ sbatch JobSubmit.sh
$ tail -f out*.out
```

Watch for:
- GPU detected and being used
- Training loss decreasing each epoch
- Final test accuracy (should be > 98% for MNIST)

Typical output:
```
Using device: cuda (NVIDIA RTX A40)
Epoch [1/10], Loss: 0.2134
Epoch [2/10], Loss: 0.0567
...
Test Accuracy: 99.12%
```

## Troubleshooting

### "CUDA not available"
- Check that you requested a GPU: `--gres=gpu:1`
- Check that you're on a GPU partition: `-p qTRDGPU`
- Verify CUDA version compatibility: `nvidia-smi` shows driver version, `torch.version.cuda` shows PyTorch's CUDA version
- They need to be compatible (CUDA 11.8 PyTorch works with driver ≥ 450)

### Out of GPU memory
- Reduce batch size in the training script
- Use `nvidia-smi` to check GPU memory usage
- If the GPU has 16 GB memory and your model needs more, you need to optimize (smaller model, gradient checkpointing, or multiple GPUs)

### Slow training
- Make sure data is on GPU: `images.to(device)` before computation
- Increase number of DataLoader workers: `num_workers=4`
- Check that you're not accidentally running on CPU

## From MNIST to neuroimaging
Once this pipeline works, the same pattern applies to neuroimaging classification:
- Replace MNIST data with ICA features (spatial maps, FNC matrices)
- Replace the simple CNN with an appropriate architecture
- Add cross-validation (next task)
- Scale up with array jobs

## Critical warnings for neuroimaging classification
MNIST is a useful validation, but neuroimaging classification is a fundamentally different problem. Be aware of these pitfalls BEFORE starting a real project:

### The curse of dimensionality
MNIST has 60,000 training samples and 784 features. Neuroimaging datasets typically have 100-500 subjects and 1,000-100,000 features. With more features than samples, overfitting is nearly guaranteed unless you:
- Apply aggressive dimensionality reduction (PCA to 10-50 components)
- Use domain knowledge to select relevant features (e.g., only FNC values, not raw voxels)
- Regularize heavily (dropout, weight decay, early stopping)

### Class imbalance is the norm
Clinical datasets rarely have 50/50 class balance. If you have 70 controls and 30 patients, a model that always predicts "control" achieves 70% accuracy. Always use:
- **Balanced accuracy**: Average of sensitivity and specificity
- **AUC-ROC**: Area under the receiver operating characteristic curve
- **Stratified sampling**: Ensure each CV fold maintains the class ratio
- **Class-weighted loss**: `CrossEntropyLoss(weight=class_weights)` in PyTorch

### Data leakage destroys results
Data leakage means information from the test set contaminates the training process. In neuroimaging, this commonly happens through:
- **Feature normalization across all subjects** before splitting into folds (normalize within training set only)
- **Group ICA on all subjects** then splitting into train/test (ICA itself uses  test data)
- **Feature selection using all data** then evaluating on a subset

Every preprocessing step that uses population statistics MUST be computed only on the training set within each fold.

### Permutation testing for significance
With small neuroimaging samples, a classifier might achieve 65% accuracy by chance. Use permutation testing: shuffle labels 1000+ times, retrain each time, and check whether your real accuracy exceeds the 95th percentile of the null distribution. If not, your result is not significant.

## Resources for deeper learning
- 📺 [PyTorch in 100 Seconds — high-level overview](https://www.youtube.com/watch?v=ORMx45xqWkA)
- 📄 [PyTorch Official Tutorials — comprehensive learning path](https://pytorch.org/tutorials/)
- 📄 [PyTorch Cheat Sheet](https://pytorch.org/tutorials/beginner/ptcheat.html)
- 📄 [CUDA Toolkit documentation](https://docs.nvidia.com/cuda/)
