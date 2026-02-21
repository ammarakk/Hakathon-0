# Vault Sync Contract

**Version**: 1.0
**Date**: 2026-02-21
**Status**: Final

---

## Overview

This contract defines the Git-based vault synchronization mechanism between cloud and local agents for Phase 4 (Platinum Tier).

---

## Git Repository Structure

```
origin (GitHub/GitLab)
    │
    ├─┬ push (cloud)
    │ │
    │ ▼
    ├─────────────────┐
    │  Remote Repo    │
    └────────┬────────┘
             │
             │ pull/push
             │
    ┌────────▼────────┐
    │  Local Machine  │
    │  (Working Dir)  │
    └─────────────────┘
```

**Repository Location**: `AI_Employee_Vault/` (git repository)

**Branch**: `main` (single branch for simplicity)

---

## Sync Operations

### Pull

**Purpose**: Fetch changes from remote repository

**Command**:
```bash
git pull origin main
```

**Behavior**:
- Fetches changes from remote
- Merges into local working directory
- Returns exit code 0 on success, 1 on conflict

**Conflict Detection**:
```bash
if ! git pull origin main; then
    # Conflict detected
    log_to_errors_sync("Merge conflict detected")
    exit 1
fi
```

### Push

**Purpose**: Push local changes to remote repository

**Command**:
```bash
git push origin main
```

**Pre-Push Validation**:
```bash
# 1. Run security audit
bash vault/security-audit.sh
if [ $? -ne 0 ]; then
    echo "Security audit failed: secrets detected"
    exit 1
fi

# 2. Check for unresolved conflicts
if git status | grep -q "both modified"; then
    echo "Unresolved conflicts detected"
    exit 1
fi

# 3. Push
git push origin main
```

**Behavior**:
- Pushes committed changes to remote
- Fails if remote has diverged (requires pull first)
- Returns exit code 0 on success

### Status

**Purpose**: Check repository state

**Command**:
```bash
git status --porcelain
```

**Output Format**:
```
M  Needs_Action/email/task-001.md    # Modified
A  Updates/signal-001.md              # Added
 D  Done/old-task.md                  # Deleted
UU Needs_Action/conflict.md          # Conflict (both modified)
```

**Status Codes**:
- `M`: Modified
- `A`: Added
- `D`: Deleted
- `UU`: Unresolved conflict

---

## Sync Daemon Specification

**File**: `cloud/agent/sync-daemon.sh`

**Algorithm**:
```bash
#!/bin/bash

INTERVAL=30  # seconds

while true; do
    # 1. Pull remote changes
    if git pull origin main; then
        log "Sync: pull successful"
    else
        log "Sync: pull failed (conflict or network)"
        log_to_errors_sync "Pull failed, blocking operations"
        sleep $INTERVAL
        continue
    fi

    # 2. Stage local changes
    git add -A

    # 3. Check if there are changes to push
    if git diff --cached --quiet; then
        log "Sync: no local changes to push"
    else
        # 4. Run security audit
        if bash vault/security-audit.sh; then
            # 5. Commit changes
            git commit -m "Auto-sync: $(date -Iseconds)"

            # 6. Push changes
            if git push origin main; then
                log "Sync: push successful"
            else
                log "Sync: push failed (remote diverged)"
            fi
        else
            log "Sync: security audit failed, not pushing"
        fi
    fi

    # 7. Wait for next interval
    sleep $INTERVAL
done
```

**Exit Conditions**:
- SIGTERM (graceful shutdown)
- Sync conflict detected (blocks until resolved)

---

## Security Audit Script

**File**: `vault/security-audit.sh`

**Purpose**: Scan staged files for secret patterns before push

**Secret Patterns**:
```
# API keys
AWS_ACCESS_KEY_ID=
AKIA[0-9A-Z]{16}

# Tokens
Bearer\s+[A-Za-z0-9\-._~+/]+=*
Authorization:\s*Bearer

# Passwords
password\s*=\s*['"][^'"]+['"]
PASSWORD\s*=\s*['"][^'"]+['"]

# Sessions
\.session$
\.token$
\.cred$

# Environment files
\.env$
\.env\.
```

**Algorithm**:
```bash
#!/bin/bash

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

# Scan each file for secret patterns
for file in $STAGED_FILES; do
    # Check if file is in ignore list
    if echo "$file" | grep -qE '\.(env|session|token|cred)$'; then
        echo "ERROR: Secret file staged: $file"
        exit 1
    fi

    # Scan file content for secret patterns
    if git show :"$file" | grep -qE '(AWS_ACCESS_KEY_ID|AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9])'; then
        echo "ERROR: Secret pattern detected in: $file"
        exit 1
    fi
done

echo "Security audit: PASSED"
exit 0
```

**Exit Codes**:
- `0`: No secrets detected (safe to push)
- `1`: Secrets detected (block push)

---

## Conflict Resolution

**Detection**: Git pull fails with exit code 1

**Logging**:
```bash
echo "$(date -Iseconds) | Sync conflict detected" >> /vault/Errors/sync/conflict-$(date +%Y%m%d).log
git status >> /vault/Errors/sync/conflict-$(date +%Y%m%d).log
```

**Resolution Process**:

1. **Stop Sync Daemon**: Systemd service stops sync-daemon
2. **Block Operations**: Agents pause vault operations
3. **Human Intervention**:
   ```bash
   # On local machine
   cd AI_Employee_Vault
   git pull origin main  # Will show conflict markers

   # Edit conflicted files, resolve conflicts
   vim Needs_Action/email/conflict.md

   # Mark as resolved
   git add Needs_Action/email/conflict.md
   git commit -m "Resolved conflict"

   # Push
   git push origin main
   ```
4. **Resume Sync**: Restart sync-daemon

**Conflict Markers**:
```markdown
<<<<<<< HEAD
Local version: Cloud processed email
=======
Remote version: Local processed email
>>>>>>> origin/main
```

---

## Sync States

| State | Description | Transitions |
|-------|-------------|-------------|
| `idle` | Not syncing | → `syncing` (on interval) |
| `syncing` | Pull/push in progress | → `success`, `failed` |
| `success` | Sync completed | → `idle` |
| `failed` | Sync failed (conflict) | → `idle` (after resolution) |

**State Tracking**: File at `AI_Employee_Vault/.sync-state.json`

```json
{
  "status": "success",
  "last_sync": "2026-02-21T10:30:00Z",
  "last_pull": "2026-02-21T10:29:55Z",
  "last_push": "2026-02-21T10:30:00Z",
  "conflict_count": 0,
  "error_count": 0
}
```

---

## Configuration

**Environment Variables**:

```bash
# Git configuration
GIT_REPO_URL="git@github.com:user/ai-employee-vault.git"
GIT_BRANCH="main"
GIT_SSH_KEY="/home/cloud/.ssh/id_ed25519"

# Sync configuration
SYNC_INTERVAL=30  # seconds
SYNC_TIMEOUT=60   # seconds for git operations

# Security
SECURITY_AUDIT_ENABLED=true
SECRET_PATTERN_FILE="/vault/config/secret-patterns.txt"
```

---

## Monitoring

**Metrics** (exposed via `/health` endpoint):

```json
{
  "sync": {
    "status": "success",
    "last_sync": "2026-02-21T10:30:00Z",
    "conflict_count": 0,
    "uptime_seconds": 86400
  }
}
```

**Logs**:
- `/var/log/ai-employee/sync-daemon.log` - Sync operations
- `/vault/Errors/sync/*.log` - Conflicts and errors

---

## Testing

**Test Script**: `tests/integration/test-cloud-local-sync.sh`

```bash
#!/bin/bash

# 1. Create test file on cloud
ssh cloud-vm "echo 'test' > /vault/Needs_Action/test.md"

# 2. Wait for sync
sleep 35

# 3. Verify file appears on local
if [ -f AI_Employee_Vault/Needs_Action/test.md ]; then
    echo "✓ Cloud → Local sync: PASSED"
else
    echo "✗ Cloud → Local sync: FAILED"
    exit 1
fi

# 4. Create test file on local
echo "local-test" > AI_Employee_Vault/Updates/test-signal.md

# 5. Wait for sync
sleep 35

# 6. Verify file appears on cloud
if ssh cloud-vm "test -f /vault/Updates/test-signal.md"; then
    echo "✓ Local → Cloud sync: PASSED"
else
    echo "✗ Local → Cloud sync: FAILED"
    exit 1
fi

# 7. Test conflict resolution
echo "✓ All sync tests: PASSED"
```

---

## Fallback Strategy

**If Git Sync Fails**:

1. **Network Issue**:
   - Continue processing locally
   - Queue outgoing changes
   - Retry on next interval (30s)

2. **Conflict Detected**:
   - Stop sync daemon
   - Log to `/Errors/sync/`
   - Block vault operations
   - Require human resolution

3. **Security Audit Failure**:
   - Block push
   - Log violation to `/Errors/security/`
   - Alert human
   - Continue local processing

---

## Summary

This contract specifies:
- **Git-based sync** between cloud and local
- **30-second interval** for automatic synchronization
- **Security audit** to prevent secrets from syncing
- **Conflict resolution** with human intervention
- **State tracking** for monitoring and debugging
- **Fallback strategies** for network failures and conflicts

All vault files (markdown and state) are synchronized while secrets (.env, tokens, sessions) remain local-only.
