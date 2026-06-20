## Why this matters to you
The TReNDs computing cluster is where all your heavy computation happens — ICA analyses, deep learning training, large-scale data processing. Your laptop can't handle fMRI datasets that are hundreds of gigabytes. Getting cluster access is the first step to doing any hands-on work.

## Step 1: Request a cluster allocation

### Navigate to elpis
Go to [https://elpis.rs.gsu.edu/](https://elpis.rs.gsu.edu/) and log in with your GSU credentials (CampusID and password). This is the cluster management portal where you request and manage allocations.

### If you don't have an allocation
Your PI (Principal Investigator) needs to create or add you to an allocation. Contact your PI and ask them to add your CampusID to their cluster allocation. The typical allocation name follows the pattern `trends53cXX`.

### If you need a new allocation
Your PI can request one through elpis. Allocations specify:
- Which queues (partitions) you can use (CPU, GPU, high-memory)
- Resource limits (max cores, max memory, max runtime)

## Step 2: Install SSH

SSH (Secure Shell) is how you connect to the cluster from your local machine. It provides encrypted command-line access.

### Mac/Linux
SSH is built into the terminal. Open Terminal and you're ready. No installation needed.

### Windows
You have several options:
- **OpenSSH** (recommended): Built into Windows 10/11. Check if it's installed by opening PowerShell and typing `ssh`. If it's not recognized, you may need IT to enable the optional feature: Settings → Apps → Optional Features → Add a Feature → OpenSSH Client
- **PuTTY**: A standalone SSH client. Download from [putty.org](https://www.chiark.greenend.org.uk/~sgtatham/putty/). Works well but uses a different key format (.ppk instead of OpenSSH format)
- **Windows Subsystem for Linux (WSL)**: Gives you a full Linux terminal inside Windows. SSH is built in. Install via `wsl --install` in PowerShell

**Recommendation**: Use OpenSSH on Windows. It's compatible with the same commands and key formats used in the cluster documentation, making everything simpler.

## Step 3: Verify access
Once your allocation is active and SSH is installed, test basic connectivity. You'll configure the full connection in the next tasks (keypair generation, SSH config), but for now confirm:

```
$ ssh -V
```
This should print the OpenSSH version number. If it does, SSH is properly installed.

## What the cluster looks like
The TReNDs cluster has several types of nodes:

- **Login node** (arctrdlogin001): Where you land after SSH. ONLY for submitting jobs and light file management. DO NOT run analyses here.
- **CPU compute nodes** (qTRD): Standard compute nodes with up to 32 cores and 768GB RAM
- **GPU compute nodes** (qTRDGPU): Nodes with NVIDIA GPUs (RTX, A40) for deep learning and GPU-accelerated analysis
- **High-memory nodes** (qTRDHM): Nodes with up to 1.5TB RAM for memory-intensive jobs
- **Dev nodes**: Interactive development nodes you can SSH into directly (no job scheduler needed)

You'll learn to use all of these in upcoming tasks.

## Resources for deeper learning
- 🔗 [Elpis — cluster management portal](https://elpis.rs.gsu.edu/)
- 🔗 [TReNDs Wiki — Getting Started](https://trendscenter.github.io/wiki/docs/Getting_Started.html)
- 🔗 [Cluster Workshop GitHub — examples and tutorials](https://github.com/trendscenter/ClusterWorkshop)
- 📄 [OpenSSH documentation](https://www.openssh.com/manual.html)
