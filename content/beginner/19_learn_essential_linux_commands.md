## Why this matters to you
As a CS student, you likely already know basic Linux commands. This page serves as a **quick reference for cluster-specific usage patterns** rather than a tutorial. Skim what you know and focus on the system monitoring, GPU, and cluster-specific commands that may be new to you.

## Navigation

### Where am I?
```
$ pwd
```
Print Working Directory — shows your current location in the filesystem.

### What's here?
```
$ ls              # List files and directories
$ ls -la          # Long format with hidden files, permissions, and sizes
$ ls -lh          # Human-readable file sizes (KB, MB, GB)
$ ls -lt          # Sort by modification time (newest first)
```

### Move around
```
$ cd /data/users2/jsmith42      # Go to an absolute path
$ cd ..                          # Go up one directory
$ cd ~                           # Go to your home directory
$ cd -                           # Go back to the previous directory
$ cd $MYDATA                     # Go to your data directory (if MYDATA is set in .bashrc)
```

## Viewing files

```
$ cat file.txt            # Print entire file to screen (fine for small files)
$ head -n 20 file.txt     # Show first 20 lines
$ tail -n 20 file.txt     # Show last 20 lines
$ tail -f logfile.out     # Follow a file in real-time (great for monitoring running jobs)
$ less file.txt           # Scroll through file (q to quit, / to search)
$ wc -l file.txt          # Count number of lines in a file
```

## File operations

```
$ cp source.txt dest.txt           # Copy a file
$ cp -r sourcedir/ destdir/        # Copy a directory recursively
$ mv oldname.txt newname.txt       # Rename or move a file
$ rm file.txt                      # Delete a file (no undo!)
$ rm -r directory/                 # Delete a directory and all contents (careful!)
$ mkdir newdir                     # Create a directory
$ mkdir -p path/to/nested/dir      # Create nested directories
$ touch newfile.txt                # Create an empty file or update timestamp
```

**Warning**: There is no trash can on Linux. `rm` permanently deletes files. Double-check before using `rm -r`.

## Editing files

### nano (easiest)
```
$ nano file.txt
```
A simple text editor. Controls are shown at the bottom: `Ctrl+O` to save, `Ctrl+X` to exit. Good for quick edits.

### vim (powerful but steep learning curve)
```
$ vim file.txt
```
- Press `i` to enter insert mode (type text)
- Press `Esc` to exit insert mode
- Type `:wq` to save and quit
- Type `:q!` to quit without saving
- Type `/searchterm` to search

Vim is worth learning eventually because it's available on every Linux system and is extremely powerful, but nano is fine for getting started.

## Searching

```
$ grep "pattern" file.txt          # Search for text in a file
$ grep -r "pattern" directory/     # Search recursively in a directory
$ grep -i "pattern" file.txt       # Case-insensitive search
$ grep -n "pattern" file.txt       # Show line numbers
$ find /data -name "*.nii" -type f    # Find files by name pattern
$ find . -name "*.m" -mtime -7        # Find .m files modified in the last 7 days
```

## System information

```
$ lscpu                    # CPU information (number of cores, architecture)
$ free -h                  # Memory usage (total, used, available)
$ df -h                    # Disk space usage on all mounted filesystems
$ df -h /data              # Disk space specifically for /data
$ du -sh directory/        # Size of a specific directory
$ du -sh * | sort -h       # Size of each item in current directory, sorted
$ top                      # Live process monitor (q to quit)
$ htop                     # Better process monitor (if installed)
```

## GPU information
On GPU nodes:
```
$ nvidia-smi               # GPU status, memory usage, running processes
$ nvtop                    # Interactive GPU monitor (if installed)
$ watch -n 2 nvidia-smi    # Refresh nvidia-smi every 2 seconds
```

## Permissions

```
$ chmod 755 script.sh      # Make a script executable
$ chmod 600 private_key    # Restrict access to owner only
$ chown user:group file    # Change file ownership (may require sudo)
```

Linux permissions look like `-rwxr-xr-x`:
- First 3 characters (`rwx`): Owner can read, write, execute
- Next 3 (`r-x`): Group can read and execute
- Last 3 (`r-x`): Everyone else can read and execute

## Pipes and redirection

```
$ command > output.txt         # Redirect output to a file (overwrite)
$ command >> output.txt        # Append output to a file
$ command 2> errors.txt        # Redirect error messages to a file
$ command1 | command2          # Pipe output of command1 into command2
$ cat subjects.txt | wc -l    # Count subjects in a list
$ grep "ERROR" logfile | head  # Show first few errors in a log
```

## Environment and shell

```
$ echo $HOME                   # Print a variable's value
$ export MYVAR=/some/path      # Set an environment variable
$ source ~/.bashrc             # Reload your shell configuration
$ which python                 # Find where a command is located
$ history                      # Show command history
$ history | grep srun          # Search your command history
```

## tar and compression

```
$ tar -czf archive.tar.gz directory/    # Create compressed archive
$ tar -xzf archive.tar.gz              # Extract compressed archive
$ tar -tzf archive.tar.gz              # List contents without extracting
$ gzip file.nii                         # Compress a file (creates file.nii.gz)
$ gunzip file.nii.gz                    # Decompress
```

## Resources for deeper learning
- 📺 [Linux Command Line Basics — full crash course](https://www.youtube.com/watch?v=ZtqBQ68cfJc)
- 📄 [Linux Command Cheat Sheet](https://www.linuxtrainingacademy.com/linux-commands-cheat-sheet/)
- 📄 [Vim Tutorial — interactive browser-based tutorial](https://www.openvim.com/)
- 📄 [The Linux Command Line — free online book](https://linuxcommand.org/tlcl.php)
