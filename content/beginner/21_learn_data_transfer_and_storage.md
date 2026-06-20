## Why this matters to you
You will frequently need to move files between your local machine and the cluster — analysis scripts, result figures, configuration files. You also need to understand the rules around data movement, because neuroimaging data is often protected under Data Use Agreements (DUAs) and HIPAA regulations. Violating these rules can have serious consequences.

## Data transfer rules — READ THESE CAREFULLY

### What you MUST NOT do
- **DO NOT download full imaging datasets to your local machine**. Most datasets are covered by DUAs that restrict where data can be stored and processed. The cluster is an approved location; your laptop usually is not.
- **DO NOT transfer PHI (Protected Health Information)** without explicit PI approval and IRB authorization. PHI includes identifiable patient data, specific dates, imaging data with facial features in structural scans.
- **DO NOT email data files or share via personal cloud storage** (Google Drive, Dropbox) unless approved for your specific dataset.
- **DO NOT store data on USB drives** or removable media.

### What you CAN do
- Transfer your own analysis scripts and code
- Transfer result files (statistical maps, figures, tables — not raw data)
- Transfer small sample datasets explicitly designated for teaching/testing
- Use approved methods (SFTP, Globus) for authorized transfers

When in doubt, ask your PI before transferring any data.

## Transfer method 1: SFTP (small files)
SFTP (SSH File Transfer Protocol) uses your existing SSH connection. Good for small files and scripts.

### Connect
```
$ sftp arctrdgndev101
```
(Use a dev node, not the login node, to avoid burdening it with file transfers)

### Upload files to cluster
```
sftp> cd /data/users2/<campusid>/scripts
sftp> put local_script.py
sftp> put -r local_directory/        # Upload a directory recursively
```

### Download files from cluster
```
sftp> get remote_file.txt
sftp> get -r remote_directory/       # Download a directory recursively
```

### Exit
```
sftp> exit
```

### SCP (alternative command-line tool)
```
$ scp local_file.py <campusid>@arctrdgndev101:/data/users2/<campusid>/scripts/
$ scp <campusid>@arctrdgndev101:/data/users2/<campusid>/results/fig1.png ./
$ scp -r local_dir/ <campusid>@arctrdgndev101:/data/users2/<campusid>/
```

## Transfer method 2: Globus (large transfers)
For transferring large datasets (gigabytes to terabytes), use [Globus](https://www.globus.org/). Globus is a managed file transfer service that handles:
- Automatic retry on network failures
- Integrity verification (checksums)
- Transfer scheduling and monitoring
- High-speed parallel transfer streams

### How to use Globus
1. Go to [app.globus.org](https://app.globus.org/) and log in with your GSU credentials
2. Search for the GSU/TReNDs endpoint
3. Set up a "Globus Connect Personal" endpoint on your local machine (if transferring to/from your computer)
4. Use the web interface to browse files and initiate transfers
5. Globus emails you when the transfer completes

Ask your PI or a senior lab member for the exact endpoint name and any access requirements.

## Transfer method 3: rsync (synchronization)
rsync is powerful for keeping directories in sync between machines:

```
$ rsync -avz --progress local_dir/ <campusid>@arctrdgndev101:/data/users2/<campusid>/remote_dir/
```

Flags:
- `-a`: Archive mode (preserves permissions, timestamps, directory structure)
- `-v`: Verbose output
- `-z`: Compress data during transfer
- `--progress`: Show transfer progress

rsync only transfers files that have changed, making it efficient for repeated syncs.

## Storage best practices

### Don't duplicate datasets
Before copying data, check if it already exists on the cluster:
```
$ ls /data/qneuromark/
$ ls /data/neuromark2/
$ ls /data/collaboration/
```

If the dataset is already there, work with it in place or create symbolic links:
```
$ ln -s /data/qneuromark/dataset_name $MYDATA/projects/my_project/data
```

### Clean up regularly
After an analysis is complete:
- Keep: Final results, scripts, and key intermediate files
- Remove: Temporary files, duplicate preprocessed data, failed analysis outputs
- Compress: Archive completed projects with `tar -czf project_archive.tar.gz project/`

### Use GitHub for code
Store all your scripts and code on GitHub, not just on the cluster. If cluster storage fails, your code is safe. But never put data on GitHub — use `.gitignore` to exclude data files.

### Monitor your usage
```
$ du -sh $MYDATA                   # Total size of your data directory
$ du -sh $MYDATA/* | sort -rh     # Size of each subdirectory, largest first
```

## TReNDS databases and data resources
Many codes, software, and datasets are available within the TReNDs ecosystem. Explore these early to understand what data is already accessible:

### Code and software
- [TReNDsCenter GitHub](https://github.com/trendscenter) — lab repositories, analysis scripts, toolboxes
- [GIFT Toolbox](https://trendscenter.org/software/gift/) — ICA software and documentation

### Data on the cluster
Most datasets used in the lab are stored on the cluster. Key locations:
- `/data/qneuromark/` — Neuromark datasets
- `/data/neuromark2/` — Neuromark2 datasets
- `/data/collaboration/` — Collaborator shared data

### Brain network templates
Pre-computed ICA templates (Neuromark) for back-reconstruction can be obtained from:
- [TReNDS Data page](https://trendscenter.org/data/)

## Resources for deeper learning
- 🔗 [Globus — managed file transfer service](https://www.globus.org/)
- 📄 [TReNDs Wiki — data management](https://trendscenter.github.io/wiki/)
- 📄 [rsync documentation](https://rsync.samba.org/documentation.html)
- 📄 [SFTP command reference](https://www.ssh.com/academy/ssh/sftp)
