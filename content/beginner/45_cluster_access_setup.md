## Cluster Access Setup

This task consolidates everything you need to get connected to the TReNDs computing cluster: requesting an account, setting up VPN, generating SSH keys, and configuring your connection.

> **Note**: Much of this information is also available in the [TReNDs Cluster Documentation](https://trendscenter.github.io/wiki/docs/Getting_Started.html). Refer to that for the most up-to-date instructions.

---

### Step 1: Request a Cluster Allocation

Go to [elpis.rs.gsu.edu](https://elpis.rs.gsu.edu/) and log in with your GSU credentials. Your PI needs to create or add you to an allocation (typically named `trends53cXX`). Contact your PI and ask them to add your CampusID.

---

### Step 2: Set Up VPN (for off-campus access)

The cluster is only accessible from the GSU campus network. If you're off-campus, you need the **GlobalProtect VPN**.

1. Set up [DUO two-factor authentication](https://icollege.gsu.edu/) if you haven't already
2. Download GlobalProtect from the [GSU VPN page](https://technology.gsu.edu/technology-services/it-services/security/virtual-private-network/)
3. Portal address: `secureaccess.gsu.edu`
4. Log in with your CampusID and password, then approve the DUO push

**Tip**: Always connect VPN before SSH. Use `tmux` or `screen` on the cluster so your sessions survive VPN drops.

---

### Step 3: Install SSH

- **Mac/Linux**: SSH is built into the terminal. No installation needed.
- **Windows**: Use the built-in OpenSSH client (check by typing `ssh` in PowerShell). If not available, install via Settings → Apps → Optional Features → OpenSSH Client.

---

### Step 4: Generate & Sign SSH Keypairs

```bash
# Create .ssh directory
mkdir -p ~/.ssh && chmod 700 ~/.ssh && cd ~/.ssh

# Generate keypair (replace <campusid> with yours)
ssh-keygen -f id_<campusid>
```

Then sign your key on elpis:
1. Display your public key: `cat ~/.ssh/id_<campusid>.pub`
2. Go to [elpis.rs.gsu.edu](https://elpis.rs.gsu.edu/) → SSH key signing section
3. Paste the public key and submit
4. Download the certificate (`id_<campusid>-cert.pub`) and move it to `~/.ssh/`

---

### Step 5: Configure SSH & Connect

Create/edit `~/.ssh/config`:

```
Host arclogin
  HostName arctrdlogin001.rs.gsu.edu
  User <campusid>
  ForwardAgent yes
  CertificateFile ~/.ssh/id_<campusid>-cert.pub
  IdentityFile ~/.ssh/id_<campusid>
```

Then connect: `ssh arclogin`

**Login node rules**: The login node is shared. Do NOT run analyses, MATLAB, or heavy computation there. Only use it for submitting jobs (`sbatch`, `srun`), monitoring (`squeue`), and light file operations.

---

### Lab-Specific Note
Ask your PI about the specific compute node assigned to Armin's lab — when possible, prefer that node over shared partitions for interactive analysis work.

---

### Resources
- 🔗 [TReNDs Wiki — Getting Started](https://trendscenter.github.io/wiki/docs/Getting_Started.html)
- 🔗 [Elpis — cluster management portal](https://elpis.rs.gsu.edu/)
- 🔗 [GSU VPN setup](https://technology.gsu.edu/technology-services/it-services/security/virtual-private-network/)
- 🔗 [Cluster Workshop GitHub](https://github.com/trendscenter/ClusterWorkshop)
