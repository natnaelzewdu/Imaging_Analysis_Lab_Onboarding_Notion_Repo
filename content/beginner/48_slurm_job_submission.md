## SLURM Job Submission

Follow the TReNDS cluster documentation to learn how to run interactive sessions, submit batch jobs, use array jobs, and load software modules.

**Start here**: [TReNDS Cluster — SLURM Overview](https://trendscenter.github.io/wiki/docs/SLURM_overview.html)

---

### Tips for first-time users

- **Never run computation on the login node** — always use `srun` (interactive) or `sbatch` (batch). The login node is shared and only for submitting jobs and light file operations.

- **Prompt change**: When your terminal prompt changes from `@arclogin` to `@arctrdcnXXX`, you are on a compute node and can run your work.

- **Account code**: You need your SLURM account code (e.g., `trends53cXX`) for every job. Find it on [elpis.rs.gsu.edu](https://elpis.rs.gsu.edu/) or ask your PI.

- **Modules**: Software on the cluster is managed through the `module` system. Use `module avail` to see everything, `module load <name>` to load.

- **Example scripts**: The wiki has fully annotated [example SLURM scripts](https://trendscenter.github.io/wiki/docs/Example_SLURM_scripts.html) you can copy and adapt.

---

### Evidence — post the following screenshots as replies

1. **Partitions** — output of `sinfo` showing available cluster partitions

2. **Interactive session** — `srun` command landing on a compute node (prompt showing `[campusid@arctrdcnXXX ~]$`)

3. **Batch job** — output of `sbatch JobSubmit.sh` showing the job ID, followed by `squeue -u <campusid>` showing the job in queue

4. **Module loading** — output of `module load` and `module list` showing a loaded tool (e.g., MATLAB)
