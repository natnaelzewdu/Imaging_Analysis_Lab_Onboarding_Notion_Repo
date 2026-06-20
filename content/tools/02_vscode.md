## VS Code for Remote Development

VS Code with the Remote-SSH extension lets you edit code and run scripts directly on the cluster from your local machine. This is the recommended way to work on the cluster — you get a full code editor with syntax highlighting, file browsing, and integrated terminal without needing a separate GUI session.

### Setup tutorial

- 📺 [VS Code Remote SSH setup — complete walkthrough](https://www.youtube.com/watch?v=EUJlVYggR1Y)

### Step-by-step

1. Install [VS Code](https://code.visualstudio.com/)

2. Install the **Remote - SSH** extension (search in the Extensions panel)

3. Open the Command Palette (Ctrl+Shift+P) → **Remote-SSH: Connect to Host**

4. Enter `arclogin` (or whichever SSH host alias you configured in `~/.ssh/config`)

5. Once connected, use **File → Open Folder** to browse your cluster home directory

### Recommended Resources

- [VS Code Remote Development docs](https://code.visualstudio.com/docs/remote/ssh)

- [TReNDS Wiki — VS Code Remote setup](https://trendscenter.github.io/wiki/docs/Configure_SSH_for_easy_access_to_DEV_machines.html)
