## What is Directory Traversal Prevention
Directory traversal prevention is about stopping attackers from accessing files or folders outside the intended directory on a server.

### What is directory traversal?
It’s an attack where someone manipulates file paths like:
```bash
../../etc/passwd
```
Instead of staying inside a safe folder, the system is tricked into going up the directory tree and reading sensitive files.

### Why it matters
If not prevented, an attacker can:
- Read system files
- Access config files (passwords, keys)
- Download private data
- In some cases, execute code

### Core Prevention Techniques
#### Validate and Sanitize input
Reject inputs containing:
- ../
- ..\
- %2e%2e/ (encoded forms)
Allow only expected patterns
Example: only filenames, not full paths

#### Use allowlists (not blocklists)
Bad approach:
- Trying to block “../”
Better approach:
- Only allow predefined file names or IDs

#### Normalize paths
Convert input into a clean, absolute path before use
- Resolve symbolic links
- Remove . and .. sequences
Then verify it stays inside the allowed directory

#### Restrict file access to a base directory
- Define a fixed root directory
- Ensure all file operations stay inside it
Example logic:
-> If requested path is outside base → reject

#### Use built-in secure APIs
Many frameworks provide safe file handling:
- Java: Paths.get().normalize()
- Python: os.path.realpath()
- Node.js: path.resolve()

#### Set proper file permissions
- Limit what the application can read
- Run with least privilege

### Quick checklist
- Input validated?
- Path normalized?
- Base directory enforced?
- Only allowed files accessible?

### Strongest Combo:
Allowlist → Normalize (APIs) → Enforce Base Directory Restriction → Block symlinks → Least privilege → Safe file access