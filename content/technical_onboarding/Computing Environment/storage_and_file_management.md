---
task_name: "Storage & File Management"
emoji: "📂"
category: Computing Environment
tier: Hands-On
order: 3
url: "https://trendscenter.github.io/wiki/docs/Storage_guide.html"
---
## Storage & File Management

Follow the TReNDS cluster documentation to understand the filesystem layout, set up your data directory, and learn how to transfer files.

**Start here**: [TReNDS Cluster — Storage Guide](https://trendscenter.github.io/wiki/docs/Storage_guide.html)

---

### Tips for first-time setup

- **Which directory?** Ask your PI which `/data/usersX/` directory to use for your work. Do not store analysis data in your home directory — it has a small quota.

- **Extra tools**: Run `export PATH=/trdapps/linux-x86_64/bin/:$PATH` to access additional tools like `dust` for visualizing directory sizes.

- **File transfer**: Use `scp` for small files, [Globus](https://trendscenter.github.io/wiki/docs/File_transfer_with_Globus.html) for large transfers.

- **Clean up regularly**: Storage is shared across all lab members. Remove duplicate or unneeded data from your user directory periodically.

---

### Evidence — post the following screenshots as replies

1. **Data directory** — output of `ls -la /data/users2/<campusid>` (or whichever `/data/usersX/` your PI assigned) showing your directory exists

2. **Navigation** — output of `pwd` and `ls` while inside your data directory

3. **File transfer** — successful `scp` of a test file to/from the cluster, or a Globus transfer confirmation
