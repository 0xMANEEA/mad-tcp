# Mad TCP

Mad-TCP is a multi-process, multi-threaded program that scans a host aggresively. Unlike other host scanning tools, Mad-TCP reports open ports immediatly once it finds one. It also gives the user the flexibility to tweak some parameters directly in the form of command-line arguments.

# Usage
Mad-TCP can only be ran as root. If you're logged in as root, this would run it:
```bash
./mad-tcp <ip_or_host_name>
```

To tweak other options, run:
```bash
./mad-tcp --help
```
