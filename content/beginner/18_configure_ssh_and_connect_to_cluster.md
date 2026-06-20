## Why this matters to you
With your SSH keys set up, you now need to configure SSH so that connecting to the cluster is as simple as typing `ssh arclogin`. A proper SSH config file saves you from typing long hostnames, specifying key paths, and remembering options every time. This is also critical for VSCode Remote, which uses the same config.

## The SSH config file
The SSH config file lives at `~/.ssh/config` (Mac/Linux) or `%USERPROFILE%\.ssh\config` (Windows). If it doesn't exist, create it.

### Basic cluster config
Create or edit the file with the following content (replace `<campusid>` with your actual CampusID):

```
Host arclogin
  HostName arctrdlogin001.rs.gsu.edu
  User <campusid>
  ForwardAgent yes
  CertificateFile ~/.ssh/id_<campusid>-cert.pub
  IdentityFile ~/.ssh/id_<campusid>
```

### What each line means
- **Host arclogin**: A nickname — after this, you just type `ssh arclogin` instead of the full hostname
- **HostName**: The actual server address
- **User**: Your CampusID (so you don't need `ssh <campusid>@arctrdlogin001.rs.gsu.edu`)
- **ForwardAgent yes**: Passes your SSH key to the login node so you can hop to compute nodes without re-authenticating
- **CertificateFile**: Path to your signed certificate
- **IdentityFile**: Path to your private key

## Connect for the first time
```
$ ssh arclogin
```

The first time you connect, you'll see a message about the host's fingerprint:
```
The authenticity of host 'arctrdlogin001.rs.gsu.edu' can't be established.
ECDSA key fingerprint is SHA256:xxxxx
Are you sure you want to continue connecting (yes/no)?
```

Type `yes`. This adds the server to your `~/.ssh/known_hosts` file so you won't be asked again.

If successful, you'll see a welcome message and a shell prompt on the login node.

## CRITICAL: Login node rules
The login node is shared by all cluster users. It is NOT for computation. Violating these rules can slow down the login node for everyone and may result in your processes being killed or your access being restricted.

**DO NOT:**
- Run analysis scripts or MATLAB on the login node
- Run VSCode Server or any GUI application on the login node
- Copy or move large files on the login node
- Run anything that uses significant CPU, memory, or disk I/O

**DO:**
- Submit SLURM jobs (`sbatch`, `srun`)
- Monitor your jobs (`squeue`, `sacct`)
- Edit small files (`nano`, `vim`)
- Navigate directories (`cd`, `ls`, `pwd`)
- Quick file operations (check file sizes, read small files)

All actual computation should happen on compute nodes via SLURM (you'll learn this in upcoming tasks) or on dev nodes.

## Adding dev nodes to your config
You'll eventually want direct SSH access to development nodes for interactive work. Add these to your config:

```
Host arctrdcn017
  HostName arctrdcn017.rs.gsu.edu
  User <campusid>
  ForwardAgent yes
  CertificateFile ~/.ssh/id_<campusid>-cert.pub
  IdentityFile ~/.ssh/id_<campusid>

Host arctrdgndev101
  HostName arctrdgndev101.rs.gsu.edu
  User <campusid>
  ForwardAgent yes
  CertificateFile ~/.ssh/id_<campusid>-cert.pub
  IdentityFile ~/.ssh/id_<campusid>
```

- `arctrdcn017`: CPU dev node
- `arctrdgndev101`: GPU dev node (for development/testing GPU code)

## Windows-specific notes
On Windows with OpenSSH, the config file paths use backslashes or forward slashes:
```
Host arclogin
  HostName arctrdlogin001.rs.gsu.edu
  User <campusid>
  ForwardAgent yes
  CertificateFile C:\Users\<username>\.ssh\id_<campusid>-cert.pub
  IdentityFile C:\Users\<username>\.ssh\id_<campusid>
```

Make sure the config file has no file extension (not `config.txt` — just `config`).

## Troubleshooting
- **"Permission denied (publickey)"**: Your certificate may be expired (re-sign on elpis), the file paths in config may be wrong, or the key isn't loaded in ssh-agent
- **"Connection timed out"**: You're probably off-campus without VPN. Connect to VPN first
- **"Connection refused"**: The server may be down for maintenance. Check with lab members
- **Slow connection**: Normal — the cluster is not on the fastest network. Once connected, commands are responsive
- **"Bad owner or permissions on config"**: On Mac/Linux, run `chmod 600 ~/.ssh/config`

## Keeping sessions alive
SSH connections can drop due to network timeouts or VPN disconnects. Add these to your config to keep connections alive:

```
Host *
  ServerAliveInterval 60
  ServerAliveCountMax 3
```

This sends a keepalive packet every 60 seconds. If 3 packets go unanswered, SSH disconnects cleanly. Place this at the top of your config file so it applies to all hosts.

## Resources for deeper learning
- 🔗 [TReNDs Wiki — cluster access instructions](https://trendscenter.github.io/wiki/docs/Getting_Started.html)
- 🔗 [Cluster Workshop GitHub — examples](https://github.com/trendscenter/ClusterWorkshop)
- 📄 [SSH Config File documentation](https://www.ssh.com/academy/ssh/config)
- 📄 [Visual Studio Code Remote SSH documentation](https://code.visualstudio.com/docs/remote/ssh)
