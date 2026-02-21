# Git Sync Setup Guide for Phase 4

**Purpose**: Complete guide for Git-based vault synchronization between Local and Cloud
**Last Updated**: 2026-02-21
**Status**: Ready for Implementation

---

## Overview

This guide provides step-by-step instructions for setting up Git-based vault synchronization for the Personal AI Employee (Platinum Tier). The sync ensures bidirectional coordination between cloud and local agents while maintaining strict secrets isolation.

**Key Features**:
- Bidirectional sync: Cloud ↔ Local via GitHub
- Secrets isolation: `.gitignore` blocks all sensitive files
- Claim-by-move: Atomic file moves prevent duplicate work
- Single-writer Dashboard.md: Local only, Cloud writes to `/Updates/`
- Conflict detection: Git merge conflicts logged to `/Errors/sync/`

---

## Prerequisites

1. **GitHub Account**: Free account with private repository
2. **Git Installed**: Version 2.34+ on both cloud and local
3. **SSH Keys**: For passwordless authentication
4. **Vault Location**: `AI_Employee_Vault/` on local machine

---

## Step 1: Create Private GitHub Repository

### 1.1 Create Repository

1. Go to https://github.com/new
2. Repository name: `ai-employee-vault-sync`
3. Visibility: **Private** (important!)
4. **Do NOT** initialize with README, .gitignore, or license
5. Click **Create repository**

### 1.2 Note Repository URL

Your repository URL will be:
```
git@github.com:YOUR_USERNAME/ai-employee-vault-sync.git
```

---

## Step 2: Setup on Local Machine

### 2.1 Navigate to Vault

```bash
cd ~/AI_Employee_Vault
# Or wherever your vault is located
```

### 2.2 Initialize Git Repository

```bash
git init
git branch -M main
```

### 2.3 Create Comprehensive .gitignore

```bash
cat > .gitignore << 'EOF'
# ==================================================
# AI Employee Vault - Git Sync Ignore Patterns
# IMPORTANT: Never sync secrets or cache files
# ==================================================

# Obsidian cache & plugins
.obsidian/
.obsidian.vimrc
.obsidian.css
.obsidian/plugins/

# Python artifacts
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
venv/
env/
.venv/

# Node.js artifacts
node_modules/
npm-debug.log
yarn-error.log
package-lock.json
yarn.lock
pnpm-lock.yaml

# ==================================================
# CRITICAL: Secrets - NEVER COMMIT THESE
# ==================================================
.env
.env.*
*.env
secrets/
creds/
credentials/
tokens/
auth/
WhatsApp/
whatsapp/
banking/
payments/
financial/
*.key
*.pem
*.cert
*.crt
*.der
*.keystore
*.jks
*.p12
*.pfx
session.json
session.data
*.session
*.token
*.token.txt
api_keys.txt
passwords.txt
secrets.txt

# Claude Code settings (may contain tokens)
.claude/
claude.json

# Database files (may contain sensitive data)
*.db
*.sqlite
*.sqlite3
*.sql

# Logs (may contain sensitive data)
*.log
logs/

# ==================================================
# Temporary & OS files
# ==================================================
*.tmp
*.bak
*.swp
*.swo
*~
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini

# IDE & Editor files
.vscode/
.idea/
*.sublime-project
*.sublime-workspace
*.code-workspace
.history/

# ==================================================
# Git itself
# ==================================================
.git/
.gitignore
EOF
```

### 2.4 Commit .gitignore

```bash
git add .gitignore
git commit -m "Add comprehensive .gitignore for secrets isolation"
```

### 2.5 Generate SSH Key (if needed)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "ai-employee-vault-2026" -f ~/.ssh/id_ed25519_vault

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519_vault

# Copy public key
cat ~/.ssh/id_ed25519_vault.pub
```

### 2.6 Add SSH Key to GitHub

1. Copy the output of `cat ~/.ssh/id_ed25519_vault.pub`
2. Go to: https://github.com/settings/ssh/new
3. Paste public key
4. Title: `AI Employee Vault Sync`
5. Click **Add SSH key**

### 2.7 Test SSH Connection

```bash
ssh -T git@github.com
# Should see: Hi YOUR_USERNAME! You've successfully authenticated...
```

### 2.8 Add Remote and Push

```bash
# Add remote
git remote add origin git@github.com:YOUR_USERNAME/ai-employee-vault-sync.git

# Create initial commit
git add -A
git commit -m "Initial vault structure - Phase 4 Platinum Tier"

# Push to GitHub
git push -u origin main
```

---

## Step 3: Setup on Cloud VM

### 3.1 SSH into Cloud VM

```bash
ssh ubuntu@YOUR_CLOUD_IP
# Or: ssh -i ~/.ssh/id_ed25519 ubuntu@YOUR_CLOUD_IP
```

### 3.2 Install Git (if not installed)

```bash
sudo apt update
sudo apt install -y git
```

### 3.3 Generate SSH Key on Cloud

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "cloud-vm-sync-2026" -f ~/.ssh/id_ed25519_cloud

# Copy public key
cat ~/.ssh/id_ed25519_cloud.pub
```

### 3.4 Add Cloud SSH Key to GitHub

1. Copy the output of `cat ~/.ssh/id_ed25519_cloud.pub`
2. Go to: https://github.com/settings/ssh/new
3. Paste public key
4. Title: `Cloud VM Sync`
5. Click **Add SSH key**

### 3.5 Clone Vault Repository

```bash
# Clone repository
cd ~
git clone git@github.com:YOUR_USERNAME/ai-employee-vault-sync.git vault

# Verify
cd vault
ls -la
```

### 3.6 Configure Cloud-Specific Settings

```bash
# Set git config
git config user.email "cloud@ai-employee"
git config user.name "Cloud Agent"
```

---

## Step 4: Automate Sync on Cloud

### 4.1 Create Sync Daemon Script

Create `~/sync-cloud.sh`:

```bash
#!/bin/bash
set -e

VAULT_DIR=~/vault
cd "$VAULT_DIR" || exit 1

# Log file
LOG_FILE=~/vault-sync-cloud.log
echo "=== Cloud Sync Started: $(date) ===" >> "$LOG_FILE"

# 1. Pull latest changes from GitHub
echo "Pulling from GitHub..." >> "$LOG_FILE"
if git pull origin main --quiet >> "$LOG_FILE" 2>&1; then
    echo "Pull successful" >> "$LOG_FILE"
else
    echo "ERROR: Pull failed" >> "$LOG_FILE"
    exit 1
fi

# 2. Run cloud agent tasks (if configured)
# python3 /opt/ai-employee/orchestrator.py --mode cloud
# sleep 30

# 3. Stage all changes
echo "Staging changes..." >> "$LOG_FILE"
git add -A

# 4. Check if there are changes to commit
if git diff --cached --quiet && git diff --quiet; then
    echo "No changes to commit" >> "$LOG_FILE"
    exit 0
fi

# 5. Verify no secrets staged
if git diff --cached --name-only | grep -qE '\.(env|session|token|cred|key)$'; then
    echo "ERROR: Secret files staged! Aborting commit." >> "$LOG_FILE"
    git diff --cached --name-only | grep -E '\.(env|session|token|cred|key)$' >> "$LOG_FILE"
    exit 1
fi

# 6. Commit changes
echo "Committing changes..." >> "$LOG_FILE"
git commit -m "Cloud updates $(date '+%Y-%m-%d %H:%M:%S UTC')"

# 7. Push to GitHub
echo "Pushing to GitHub..." >> "$LOG_FILE"
if git push origin main --quiet >> "$LOG_FILE" 2>&1; then
    echo "Push successful" >> "$LOG_FILE"
else
    echo "ERROR: Push failed" >> "$LOG_FILE"
    exit 1
fi

echo "=== Cloud Sync Complete: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
```

### 4.2 Make Script Executable

```bash
chmod +x ~/sync-cloud.sh
```

### 4.3 Add to Cron

```bash
# Edit crontab
crontab -e

# Add this line (sync every 5 minutes)
*/5 * * * * ~/sync-cloud.sh

# Or sync every 30 seconds (more frequent):
# * * * * * ~/sync-cloud.sh
# sleep 30; ~/sync-cloud.sh
```

---

## Step 5: Automate Sync on Local

### 5.1 Create Local Sync Script

Create `~/AI_Employee_Vault/sync-local.sh`:

```bash
#!/bin/bash
set -e

VAULT_DIR=~/AI_Employee_Vault
cd "$VAULT_DIR" || exit 1

echo "=== Local Sync Started: $(date) ===" >> ~/vault-sync-local.log

# 1. Pull from GitHub
echo "Pulling from GitHub..." >> ~/vault-sync-local.log
if git pull origin main --quiet >> ~/vault-sync-local.log 2>&1; then
    echo "Pull successful" >> ~/vault-sync-local.log
else
    echo "ERROR: Pull failed" >> ~/vault-sync-local.log
    # Check for conflicts
    if git status | grep -q "both modified"; then
        echo "Merge conflict detected!" >> ~/vault-sync-local.log
        echo "Conflict logged to /Errors/sync/" >> ~/vault-sync-local.log
        mkdir -p ../Errors/sync
        git status > "../Errors/sync/conflict-$(date +%Y%m%d-%H%M%S).log"
    fi
    exit 1
fi

# 2. Merge Cloud updates into Dashboard.md (single-writer rule)
if [ -d "Updates" ] && [ "$(ls -A Updates/*.md 2>/dev/null)" ]; then
    echo "Merging cloud updates into Dashboard.md..." >> ~/vault-sync-local.log

    # Append updates to Dashboard.md
    for update_file in Updates/*.md; do
        echo "" >> Dashboard.md
        cat "$update_file" >> Dashboard.md
        rm "$update_file"  # Clean up after merge
    done

    git add Dashboard.md
    echo "Updates merged" >> ~/vault-sync-local.log
fi

# 3. Stage local changes
git add -A

# 4. Check if there are changes to commit
if git diff --cached --quiet && git diff --quiet; then
    echo "No local changes to commit" >> ~/vault-sync-local.log
    exit 0
fi

# 5. Verify no secrets staged (security check)
if git diff --cached --name-only | grep -qE '\.(env|session|token|cred|key)$'; then
    echo "ERROR: Secret files staged! Aborting commit." >> ~/vault-sync-local.log
    exit 1
fi

# 6. Commit local changes
git commit -m "Local updates + merged cloud signals $(date '+%Y-%m-%d %H:%M:%S')"

# 7. Push to GitHub
echo "Pushing to GitHub..." >> ~/vault-sync-local.log
if git push origin main --quiet >> ~/vault-sync-local.log 2>&1; then
    echo "Push successful" >> ~/vault-sync-local.log
else
    echo "ERROR: Push failed" >> ~/vault-sync-local.log
    exit 1
fi

echo "=== Local Sync Complete: $(date) ===" >> ~/vault-sync-local.log
echo "" >> ~/vault-sync-local.log
```

### 5.2 Make Script Executable

```bash
chmod +x ~/AI_Employee_Vault/sync-local.sh
```

### 5.3 Add to Cron (Linux/macOS)

```bash
# Edit crontab
crontab -e

# Sync every 5 minutes
*/5 * * * * ~/AI_Employee_Vault/sync-local.sh >> ~/vault-sync-local.log 2>&1
```

### 5.4 Windows Task Scheduler

Create `sync-local.bat`:

```batch
@echo off
cd /d C:\Users\YourUsername\AI_Employee_Vault
git pull origin main
git add -A
git commit -m "Local updates %date% %time%"
git push origin main
```

Then:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Every 5 minutes
4. Action: Start a program
5. Program: `C:\Users\YourUsername\AI_Employee_Vault\sync-local.bat`

---

## Step 6: Enforce Project Rules

### 6.1 Claim-by-Move Verification

Add to both sync scripts (before commit):

```bash
# Verify claim-by-move: Check In_Progress folders
if ls In_Progress/*/*.md >/dev/null 2>&1; then
    echo "Claimed tasks exist in In_Progress/ - OK" >> "$LOG_FILE"
else
    echo "Warning: No active claims found" >> "$LOG_FILE"
fi
```

### 6.2 Single-Writer Dashboard.md Rule

Add to **cloud sync script only** (before commit):

```bash
# BLOCK cloud from modifying Dashboard.md (single-writer rule)
if git diff --cached --name-only | grep -q "Dashboard.md"; then
    echo "ERROR: Cloud attempted to modify Dashboard.md!" >> "$LOG_FILE"
    echo "Dashboard.md is single-writer (Local only). Blocking commit." >> "$LOG_FILE"
    git reset HEAD Dashboard.md
    exit 1
fi
```

### 6.3 Pre-Sync Security Audit

Create `phase-4/vault/security-audit.sh`:

```bash
#!/bin/bash
# Pre-sync security audit - run before git push

echo "Running security audit..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only)

# Check for secret file patterns
SECRET_PATTERNS=(
    "\.env$"
    "\.env\."
    "\.session$"
    "\.token$"
    "\.cred$"
    "\.key$"
    "\.pem$"
    "\.cert$"
    "secrets/"
    "creds/"
    "tokens/"
)

# Check each staged file
for file in $STAGED_FILES; do
    for pattern in "${SECRET_PATTERNS[@]}"; do
        if echo "$file" | grep -qE "$pattern"; then
            echo "SECURITY ALERT: Secret file staged: $file"
            echo "Blocking git push!"
            exit 1
        fi
    done
done

echo "Security audit passed - No secrets detected"
exit 0
```

### 6.4 Integrate Security Audit

Add to both sync scripts (before git push):

```bash
# Run security audit
if bash phase-4/vault/security-audit.sh; then
    echo "Security audit passed" >> "$LOG_FILE"
else
    echo "ERROR: Security audit failed!" >> "$LOG_FILE"
    exit 1
fi
```

---

## Step 7: Test Sync Setup

### 7.1 Test Cloud → Local Sync

1. **On Cloud**:
   ```bash
   cd ~/vault
   echo "# Test signal from cloud" > Updates/test-signal.md
   ~/sync-cloud.sh
   ```

2. **On Local**:
   ```bash
   cd ~/AI_Employee_Vault
   bash sync-local.sh
   cat Updates/test-signal.md
   # Should see: # Test signal from cloud
   ```

### 7.2 Test Local → Cloud Sync

1. **On Local**:
   ```bash
   cd ~/AI_Employee_Vault
   echo "# Test task from local" > Needs_Action/test-task.md
   bash sync-local.sh
   ```

2. **On Cloud**:
   ```bash
   cd ~/vault
   ~/sync-cloud.sh
   cat Needs_Action/test-task.md
   # Should see: # Test task from local
   ```

### 7.3 Test Claim-by-Move

```bash
# On Local: Create test task
echo "# Claim test" > Needs_Action/claim-test.md

# Start both agents (cloud and local)
# They will both try to claim the task

# Verify only one has it:
# - If In_Progress/cloud/claim-test.md exists → Cloud claimed
# - If In_Progress/local/claim-test.md exists → Local claimed
# - Should NEVER be in both folders
```

### 7.4 Test Secrets Isolation

```bash
# Try to add a secret file
echo "SECRET_KEY=abc123" > .env
git add .env
git commit -m "Test secret"

# Should be BLOCKED by pre-sync audit
# Output: SECURITY ALERT: Secret file staged: .env
```

---

## Step 8: Sync Monitoring

### 8.1 Check Sync Logs

**Cloud**:
```bash
tail -f ~/vault-sync-cloud.log
```

**Local**:
```bash
tail -f ~/vault-sync-local.log
```

### 8.2 Check Git Status

**Cloud**:
```bash
cd ~/vault
git status
git log --oneline -5
```

**Local**:
```bash
cd ~/AI_Employee_Vault
git status
git log --oneline -5
```

### 8.3 Monitor Sync Intervals

Check cron logs:
```bash
# Cloud
sudo tail -f /var/log/syslog | grep CRON

# Local (macOS)
log show --predicate 'process == "cron"' --last 1h

# Local (Linux)
sudo tail -f /var/log/cron.log
```

---

## Troubleshooting

### Issue: Git Push Fails - "Permission Denied"

**Solution**: Verify SSH key is added to GitHub
```bash
ssh -T git@github.com
# Should authenticate successfully
```

### Issue: Sync Conflicts

**Solution**: Manual resolution required
```bash
# Check for conflicts
git status | grep "both modified"

# Resolve conflicts manually
vim <conflicted-file>

# Mark as resolved
git add <conflicted-file>
git commit -m "Resolved merge conflict"
```

### Issue: Secrets Detected in Vault

**Solution**: Remove from Git tracking
```bash
# Remove file from Git (keep local copy)
git rm --cached .env

# Add to .gitignore
echo ".env" >> .gitignore

# Commit
git add .gitignore
git commit -m "Remove .env from tracking"
git push
```

### Issue: Dashboard.md Conflict

**Solution**: Ensure cloud never modifies Dashboard.md
- Check cloud sync logs for "ERROR: Cloud attempted to modify Dashboard.md"
- Verify single-writer rule in cloud sync script

---

## Security Best Practices

1. **Always use SSH keys** (never HTTPS with passwords in scripts)
2. **Keep .gitignore updated** with all secret patterns
3. **Run security audit** before every git push
4. **Review sync logs regularly** for security alerts
5. **Rotate SSH keys** every 90 days
6. **Use private GitHub repositories** only
7. **Never commit .env files**, even with dummy data
8. **Audit Git history** for accidental secrets:
   ```bash
   git log --all --full-history --source -- "*env*" "*secret*"
   ```

---

## Summary

✅ **Setup Complete**:
- Private GitHub repository created
- Local vault initialized and pushed
- Cloud VM cloned repository
- Bidirectional sync scripts created
- Security audit integrated
- Project rules enforced (claim-by-move, single-writer Dashboard.md)

**Next Steps**:
1. Run test syncs (cloud → local, local → cloud)
2. Verify claim-by-move coordination
3. Confirm secrets isolation
4. Deploy cloud agent services
5. Monitor sync logs for first 24 hours

**Sync Status**: Ready for Production

---

**Last Updated**: 2026-02-21
**Phase**: 4 - Platinum Tier
**Component**: Vault Synchronization
