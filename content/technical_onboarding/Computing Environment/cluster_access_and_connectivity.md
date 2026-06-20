---
task_name: "Cluster Access & Connectivity"
emoji: "🔑"
tier: Hands-On
order: 2
url: "https://trendscenter.github.io/wiki/docs/Getting_Started.html"
---
## Cluster Access & Connectivity

Follow the TReNDS cluster documentation to set up your account, VPN, SSH keys, and verify you can access the cluster and development environments.

**Start here**: [TReNDS Cluster — Getting Started](https://trendscenter.github.io/wiki/docs/Getting_Started.html)

---

### Tips for first-time setup

- **DUO first**: Set up DUO two-factor authentication before configuring VPN. You'll need it for the GlobalProtect VPN login.

- **VPN portal**: `secureaccess.gsu.edu` — always connect VPN before attempting SSH.

- **Windows users**: Use the built-in OpenSSH client (not PuTTY). Check by typing `ssh` in PowerShell. If unavailable, install via Settings → Apps → Optional Features → OpenSSH Client.

- **Certificate expiration**: SSH certificates expire approximately every 3 months. When `ssh arclogin` suddenly gives "Permission denied", re-sign your key on [elpis.rs.gsu.edu](https://elpis.rs.gsu.edu/).

- **Lab node**: Ask your PI about the specific compute/dev node assigned to the lab and prefer using that when possible.

---

### Evidence — post the following screenshots as replies

1. **Elpis dashboard** showing your active allocation

2. **VPN connected** — GlobalProtect status showing "Connected"

3. **SSH login** — terminal showing successful `ssh arclogin` with `[campusid@arclogin ~]$` prompt

4. **Hemera or VS Code** — either the Hemera web interface ([hemera.rs.gsu.edu](https://hemera.rs.gsu.edu/)) logged in, OR VS Code status bar showing `SSH: arctrdgndev101`
