## Why this matters to you
While SLURM jobs are the production way to run analyses, development nodes and visual access tools let you work interactively without the overhead of job submission. Dev nodes let you SSH directly to a compute node for testing and development. Hemera provides a web-based GUI desktop. VSCode Remote lets you edit code on the cluster from your local editor. These tools make your daily development workflow much more comfortable.

## Development nodes (dev nodes)
Dev nodes are compute nodes you can SSH into directly — no SLURM required. They're meant for:
- Testing code before submitting batch jobs
- Interactive debugging
- Running notebooks (Jupyter)
- Light analysis work

### Available dev nodes
| Node | Type | Use for |
|---|---|---|
| `arctrdcn017` | CPU | Python scripts, MATLAB testing, data exploration |
| `arctrdagn019` | GPU | GPU code testing, quick PyTorch experiments |
| `arctrdgndev101` | GPU | GPU development, file transfers (SFTP target) |

### SSH config for dev nodes
Add to your `~/.ssh/config` (with your actual CampusID):

```
Host arctrdcn017
  HostName arctrdcn017.rs.gsu.edu
  User <campusid>
  ForwardAgent yes
  CertificateFile ~/.ssh/id_<campusid>-cert.pub
  IdentityFile ~/.ssh/id_<campusid>

Host arctrdagn019
  HostName arctrdagn019.rs.gsu.edu
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

Then connect:
```
$ ssh arctrdcn017        # CPU dev node
$ ssh arctrdgndev101     # GPU dev node
```

### Dev node etiquette
Dev nodes are shared — multiple people may be using them simultaneously. Be mindful:
- Don't monopolize all CPU cores or memory
- Kill processes when done
- Use SLURM for large/long analyses instead
- Check who else is on: `who` or `top`

## Hemera (web-based GUI desktop)
[Hemera](https://hemera.rs.gsu.edu) provides a full graphical Linux desktop in your web browser. This is useful when you need:
- MATLAB GUI (GIFT's graphical interface)
- Brain visualization tools (FSLeyes, AFNI viewer)
- Jupyter notebooks with visual output
- Any application that requires a display

### How to use Hemera
1. Connect to VPN (if off-campus)
2. Navigate to [https://hemera.rs.gsu.edu](https://hemera.rs.gsu.edu) in your browser
3. Log in with GSU credentials
4. Select a session type (desktop, Jupyter, MATLAB, etc.)
5. Choose resources (CPU cores, memory, time limit)
6. Click "Launch" and wait for the session to start
7. Click "Connect" to open the desktop in your browser

### Available applications on Hemera
- **Desktop session**: Full Linux desktop with file manager, terminal, and all installed applications
- **Jupyter**: Browser-based Python notebooks (useful for data exploration and visualization)
- **MATLAB**: MATLAB with full GUI, including SPM and GIFT interfaces
- **RStudio**: R statistical environment

### Tips for Hemera
- Sessions have time limits — save your work periodically
- Performance depends on your internet connection (it's rendering the desktop remotely)
- For compute-intensive work, use Hemera to set up the analysis, then submit via SLURM
- You can copy/paste between your local machine and the Hemera session

## VSCode Remote SSH
[VSCode Remote SSH](https://code.visualstudio.com/docs/remote/ssh) lets you use your local VSCode editor to work on files on the cluster. This is the most comfortable way to edit code, view results, and use the integrated terminal — all from your local machine.

### Setup
1. Install [Visual Studio Code](https://code.visualstudio.com/) on your local machine
2. Install the **Remote - SSH** extension (by Microsoft) from the extensions marketplace
3. Make sure your SSH config has entries for the cluster (dev nodes, NOT the login node)

### Connect
1. Open VSCode
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) → type "Remote-SSH: Connect to Host"
3. Select a dev node (e.g., `arctrdcn017` or `arctrdgndev101`)
4. VSCode installs its server component on the cluster (first time only)
5. You can now edit files, use the terminal, and run code — all on the cluster

### Important rules
- **NEVER connect VSCode to the login node** (`arclogin`). The VSCode server consumes significant CPU and memory, which impacts all users on the login node.
- **Always connect to a dev node** (`arctrdcn017`, `arctrdagn019`, `arctrdgndev101`)
- Install extensions on the remote host as needed (Python, MATLAB, etc.)

### VSCode features on cluster
- **File explorer**: Browse cluster files in the sidebar
- **Integrated terminal**: Run commands directly on the cluster
- **Code editing**: Full editor features (syntax highlighting, autocomplete, linting)
- **Jupyter notebooks**: Install the Jupyter extension to run notebooks on the cluster
- **Git integration**: Manage your cluster-side repos through VSCode

## tmux and screen: keeping sessions alive
When you SSH to a dev node, your session dies if the connection drops (VPN disconnects, laptop sleeps). `tmux` keeps sessions alive:

```
$ tmux new -s mywork              # Start a new named session
# do your work...
$ tmux detach                     # Detach (Ctrl+B, then D)
# disconnect SSH, go home, reconnect later
$ tmux attach -t mywork           # Reattach to your session
```

All your programs keep running inside tmux even when you're disconnected.

## Resources for deeper learning
- 🔗 [Hemera — web-based cluster access](https://hemera.rs.gsu.edu)
- 📄 [VSCode Remote SSH documentation](https://code.visualstudio.com/docs/remote/ssh)
- 📄 [tmux cheat sheet](https://tmuxcheatsheet.com/)
- 🔗 [TReNDs Wiki — visual access](https://trendscenter.github.io/wiki/)
