---
description: Delegation via synced vault using Git or Syncthing with claim-by-move rules.
---

# COMMAND: Vault Sync & Delegation

## CONTEXT

Implement vault synchronization for:

- Delegation between cloud and local
- Claim-by-move workflow rules
- Single-writer for Dashboard.md
- Update propagation via /Updates
- Double-work prevention

## YOUR ROLE

Act as a distributed systems architect with expertise in:

- File synchronization
- Conflict resolution
- Distributed workflows
- Git-based collaboration

## IMPLEMENTATION

### 1. Sync Methods

#### Option A: Git-Based Sync

```bash
# Setup git repository
cd /path/to/vault
git init
git config user.name "AI Employee"
git config user.email "ai-employee@local"

# Create .gitignore
cat > .gitignore << EOF
# Ignore sensitive data
.env
credentials/
*.session.json
# Ignore Obsidian cache
.obsidian/
.obsidian.plugins/
# Ignore temporary files
*.tmp
.DS_Store
EOF

# Initial commit
git add .
git commit -m "Initial vault setup"

# Add remote (GitHub, GitLab, or private server)
git remote add origin https://github.com/yourusername/ai-employee-vault.git
git push -u origin main
```

```python
# git_sync.py

import subprocess
from pathlib import Path
from datetime import datetime


class VaultSync:
    """Synchronize vault using Git."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path

    def commit_changes(self, message: str = None):
        """Commit local changes."""
        if message is None:
            message = f"Update {datetime.now().isoformat()}"

        subprocess.run(
            ['git', 'add', '.'],
            cwd=self.vault_path,
            capture_output=True
        )

        result = subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=self.vault_path,
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    def pull_changes(self):
        """Pull remote changes."""
        result = subprocess.run(
            ['git', 'pull', '--rebase'],
            cwd=self.vault_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Handle conflicts
            self._resolve_conflicts()

        return result.returncode == 0

    def push_changes(self):
        """Push local changes."""
        # Pull first to avoid conflicts
        self.pull_changes()

        result = subprocess.run(
            ['git', 'push'],
            cwd=self.vault_path,
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    def _resolve_conflicts(self):
        """Resolve merge conflicts."""
        # Mark all conflicts as resolved
        subprocess.run(
            ['git', 'add', '-A'],
            cwd=self.vault_path
        )

        # Continue rebase
        subprocess.run(
            ['git', 'rebase', '--continue'],
            cwd=self.vault_path
        )

    def sync(self):
        """Full sync: pull and push."""
        self.pull_changes()
        self.commit_changes()
        self.push_changes()
```

#### Option B: Syncthing

```bash
# Install Syncthing
sudo apt install syncthing  # Linux
brew install syncthing      # Mac

# Start Syncthing
syncthing

# Access Web UI
open http://localhost:8384

# Configure:
# 1. Add folder: /path/to/vault
# 2. Set "Folder Path" to your vault directory
# 3. Generate Device ID and share with other machines
# 4. Set "Sync Type" to "Send & Receive"
# 5. Enable "File Pull Order" = "Random"
```

### 2. Claim-by-Move Workflow

```python
# claim_system.py

from pathlib import Path
from typing import Optional
import shutil


class ClaimByMove:
    """Implement claim-by-move workflow for delegation."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.in_progress = vault_path / "In_Progress"
        self.pending_approval = vault_path / "Pending_Approval"
        self.done = vault_path / "Done"

        # Ensure directories exist
        for dir in [self.needs_action, self.in_progress, self.pending_approval, self.done]:
            dir.mkdir(parents=True, exist_ok=True)

    def claim_task(self, task_file: str, owner: str) -> Path:
        """
        Claim a task by moving it to In_Progress.

        Args:
            task_file: Name of task file in Needs_Action
            owner: Who is claiming the task (cloud/local/user)

        Returns:
            Path to claimed task in In_Progress
        """
        source = self.needs_action / task_file
        if not source.exists():
            raise FileNotFoundError(f"Task not found: {task_file}")

        # Read content
        content = source.read_text()

        # Add owner tag
        owner_tag = f"\n**Claimed by:** {owner} at {datetime.now().isoformat()}\n"
        content = content.replace("\n---\n", owner_tag + "\n---\n")

        # Create destination path
        dest = self.in_progress / f"{owner}_{task_file}"

        # Write claimed file
        dest.write_text(content)

        # Remove from Needs_Action
        source.unlink()

        return dest

    def complete_task(self, task_file: str) -> Path:
        """
        Mark task as complete by moving to Done.

        Args:
            task_file: Name of task file in In_Progress

        Returns:
            Path to completed task in Done
        """
        source = self.in_progress / task_file
        if not source.exists():
            raise FileNotFoundError(f"Task not found: {task_file}")

        # Read content
        content = source.read_text()

        # Add completion tag
        completion_tag = f"\n**Completed:** {datetime.now().isoformat()}\n"
        content = content.replace("\n---\n", completion_tag + "\n---\n")

        # Create destination path
        dest = self.done / task_file

        # Write completed file
        dest.write_text(content)

        # Remove from In_Progress
        source.unlink()

        return dest

    def request_approval(self, task_file: str) -> Path:
        """Move task to Pending_Approval."""
        source = self.in_progress / task_file
        dest = self.pending_approval / task_file

        shutil.move(str(source), str(dest))
        return dest

    def is_claimable(self, task_file: str) -> bool:
        """Check if task can be claimed."""
        return (self.needs_action / task_file).exists()
```

### 3. Single-Writer Dashboard

```python
# single_writer.py

import fcntl
import time
from pathlib import Path


class SingleWriterFile:
    """Ensure only one writer at a time for critical files."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.lock_file = Path(str(filepath) + '.lock')
        self.lock_fd = None

    def __enter__(self):
        """Acquire lock."""
        # Try to acquire exclusive lock
        self.lock_fd = open(self.lock_file, 'w')
        try:
            fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return self
        except IOError:
            # File is locked by another process
            self.lock_fd.close()
            raise FileLockedError(f"{self.filepath} is locked by another process")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release lock."""
        if self.lock_fd:
            fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_UN)
            self.lock_fd.close()
            self.lock_file.unlink(missing_ok=True)

    def read(self) -> str:
        """Read file content."""
        return self.filepath.read_text()

    def write(self, content: str):
        """Write file content."""
        self.filepath.write_text(content)


class FileLockedError(Exception):
    """Raised when file is locked by another writer."""
    pass


# Usage for Dashboard.md
def update_dashboard(vault_path: Path, update_func):
    """Safely update Dashboard.md with single-writer guarantee."""
    dashboard = vault_path / "Dashboard.md"

    try:
        with SingleWriterFile(dashboard) as f:
            content = f.read()
            updated = update_func(content)
            f.write(updated)
    except FileLockedError:
        # Dashboard is being updated by another process
        # Add to queue or skip
        pass
```

### 4. Update Propagation

```python
# update_propagation.py

from pathlib import Path
from datetime import datetime


class UpdatePropagator:
    """Propagate updates via /Updates directory."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.updates_dir = vault_path / "Updates"
        self.updates_dir.mkdir(parents=True, exist_ok=True)

    def create_update(self, component: str, message: str, details: str = ""):
        """Create an update entry."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{component}.md"
        filepath = self.updates_dir / filename

        content = f"""# Update from {component}

**Time:** {datetime.now().isoformat()}

## Message
{message}

{f'## Details\n{details}' if details else ''}

---
"""
        filepath.write_text(content)
        return filepath

    def get_recent_updates(self, hours: int = 24) -> list:
        """Get updates from last N hours."""
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(hours=hours)
        updates = []

        for file in self.updates_dir.glob("*.md"):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime > cutoff:
                updates.append({
                    'file': file.name,
                    'time': mtime,
                    'content': file.read_text()
                })

        return sorted(updates, key=lambda x: x['time'], reverse=True)
```

## ACCEPTANCE CRITERIA

- Vault syncs between cloud and local
- Claim-by-move prevents double-work
- Dashboard.md has single-writer guarantee
- Updates propagate via /Updates
- Conflicts are resolved automatically

## FOLLOW-UPS

- Add conflict detection
- Implement merge strategies
- Create sync status dashboard
- Add automatic retry logic
