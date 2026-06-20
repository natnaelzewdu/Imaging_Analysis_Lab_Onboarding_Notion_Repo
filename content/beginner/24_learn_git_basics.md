## Why this matters to you
As a CS student, you likely already use Git. This page focuses on the **lab-specific Git practices and the TReNDsCenter GitHub organization** — not Git basics. Skim what you know and focus on the lab rules and repo setup sections.

## Essential Git commands

### First-time setup
```
$ git config --global user.name "Your Name"
$ git config --global user.email "your.email@gsu.edu"
```

### Starting a project
```
$ git init                          # Initialize a new Git repo in the current directory
$ git clone https://github.com/trendscenter/ClusterWorkshop.git   # Clone an existing repo
```

### Daily workflow
```
$ git status                        # What's changed since last commit?
$ git add .                         # Stage all changes for commit
$ git add specific_file.py          # Stage a specific file
$ git commit -m "Add ICA analysis script"   # Save a snapshot with a message
$ git push                          # Upload commits to GitHub
$ git pull                          # Download latest changes from GitHub
```

### Viewing history
```
$ git log                           # Show commit history
$ git log --oneline                 # Compact history (one line per commit)
$ git diff                          # Show unstaged changes
$ git diff --staged                 # Show staged changes
```

### Branches (for experimenting)
```
$ git branch new-feature            # Create a new branch
$ git checkout new-feature          # Switch to it
$ git checkout -b new-feature       # Create AND switch (shortcut)
$ git checkout main                 # Switch back to main
$ git merge new-feature             # Merge new-feature into current branch
```

## Setting up GitHub

### Create a GitHub account
If you don't have one, create an account at [github.com](https://github.com). Use your GSU email so you qualify for [GitHub Education benefits](https://education.github.com/).

### Authentication
GitHub no longer accepts passwords for Git operations. Use one of:
- **SSH keys**: Add your public key to GitHub → Settings → SSH Keys. Then clone with `git@github.com:username/repo.git`
- **Personal Access Token**: Create at GitHub → Settings → Developer Settings → Personal Access Tokens. Use as password when prompted

### Join the TReNDsCenter organization
Ask your PI or a senior lab member to add you to the [TReNDsCenter GitHub organization](https://github.com/trendscenter). This gives you access to private repositories and the ability to contribute to lab code.

## Lab rules for GitHub

### DO
- Put all your analysis scripts and code on GitHub
- Write clear commit messages that describe WHAT changed and WHY
- Add a README.md to every repository explaining what it does and how to run it
- Use `.gitignore` to exclude data files, results, and temporary files
- Add documentation and comments to your code

### DO NOT
- Upload large data files (NIfTI images, datasets) — Git is for code, not data
- Upload passwords, API keys, or file system paths specific to the cluster
- Upload sensitive subject data or PHI
- Commit without testing that your code runs

## The .gitignore file
Create a `.gitignore` file in your repo to prevent accidentally committing data:

```
# Data files
*.nii
*.nii.gz
*.mat
*.hdf5

# Results and outputs
results/
output/
*.log

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/

# OS files
.DS_Store
Thumbs.db

# Environment
.env
*.tar.gz
```

## Your first task: clone the Cluster Workshop
```
$ cd $MYDATA
$ git clone https://github.com/trendscenter/ClusterWorkshop.git
$ cd ClusterWorkshop
$ ls
```

This repo contains example scripts for SLURM jobs, ICA analysis, and PyTorch classification that you'll use in upcoming hands-on tasks.

## Resources for deeper learning
- 📺 [Git & GitHub Crash Course — Traversy Media](https://www.youtube.com/watch?v=RGOj5yH7evk)
- 📄 [Git Cheat Sheet — GitHub Education](https://education.github.com/git-cheat-sheet-education.pdf)
- 🔗 [TReNDsCenter GitHub organization](https://github.com/trendscenter)
- 📄 [Pro Git book — free online](https://git-scm.com/book/en/v2)
- 📄 [GitHub Docs — Getting Started](https://docs.github.com/en/get-started)
