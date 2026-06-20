## Why this matters to you
The cluster is only accessible from the GSU campus network. If you're working from home, a coffee shop, or anywhere off-campus, you need a VPN (Virtual Private Network) to tunnel into the GSU network first. Without VPN, your SSH connections to the cluster will be refused.

## What a VPN does
A VPN creates an encrypted tunnel between your computer and the GSU network. Once connected, your computer behaves as if it's physically on campus. All your network traffic routes through GSU's servers, giving you access to:
- The TReNDs cluster (SSH)
- Internal GSU resources (library, databases)
- Hemera web interface
- Any other campus-restricted services

## Step 1: Set up DUO two-factor authentication
GSU's VPN requires [DUO](https://duo.com/) two-factor authentication. If you haven't already:

1. Visit [iCollege](https://icollege.gsu.edu/) or check your GSU email for DUO enrollment instructions
2. Install the DUO Mobile app on your phone (iOS or Android)
3. Follow the enrollment process to link your phone to your GSU account
4. Test by logging into any GSU service that requires DUO

DUO sends a push notification to your phone that you approve to complete login. It also supports phone calls and SMS codes as backup methods.

## Step 2: Download and install the VPN client
GSU uses the GlobalProtect VPN client.

1. Go to [GSU VPN page](https://technology.gsu.edu/technology-services/it-services/security/virtual-private-network/)
2. Follow the instructions for your operating system (Windows, Mac, or Linux)
3. **For managed machines**: Your IT department may need to install the client for you. Ask your department's IT support

### Configuration
- **Portal address**: `secureaccess.gsu.edu`
- **Username**: Your CampusID
- **Password**: Your GSU password
- **Second factor**: Approve the DUO push notification on your phone

## Step 3: Connect and verify
1. Open GlobalProtect
2. Enter portal: `secureaccess.gsu.edu`
3. Log in with GSU credentials
4. Approve DUO push
5. The status indicator should show "Connected"

To verify it's working, try to SSH to the cluster (you'll set up SSH in later tasks, but if it's already configured):
```
$ ssh arclogin
```

If you get a connection instead of a timeout, VPN is working correctly.

## Tips for daily use
- **Connect before SSH**: Always start VPN before trying to SSH into the cluster
- **Disconnect when done**: VPN routes all your traffic through GSU, which can slow down regular browsing
- **Auto-connect**: You can configure GlobalProtect to connect automatically on startup, but this may slow down your normal internet
- **VPN drops**: If your VPN disconnects, your SSH sessions will die. Use `tmux` or `screen` on the cluster to keep your sessions alive even if the connection drops (you'll learn these tools later)
- **Split tunneling**: Some VPN configurations allow split tunneling (only GSU traffic goes through VPN, everything else is direct). Check with IT if this is available

## Troubleshooting
- **"Connection timed out"**: Check that you're connected to the internet first, then try reconnecting VPN
- **DUO not sending push**: Make sure your phone has internet access. Try the "Call Me" or "Passcode" options in DUO
- **"Portal not found"**: Make sure you're using `secureaccess.gsu.edu` (not any other address)
- **Managed machine issues**: Contact GSU IT helpdesk

## Resources for deeper learning
- 🔗 [GSU VPN Setup Guide](https://technology.gsu.edu/technology-services/it-services/security/virtual-private-network/)
- 🔗 [DUO Two-Factor Authentication](https://duo.com/)
- 📄 [GlobalProtect User Guide](https://docs.paloaltonetworks.com/globalprotect)
