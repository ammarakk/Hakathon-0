#!/bin/bash
# Local Vault Sync Script for Phase 4 - Platinum Tier
# Purpose: Pull cloud updates, merge into Dashboard.md, push local changes
# Usage: Run via cron or manually

set -e

echo "=== Local Vault Sync Started: $(date) ===" >> ~/vault-sync-local.log

VAULT_DIR="$HOME/AI_Employee_Vault"

# Change to vault directory
cd "$VAULT_DIR" || exit 1

# =============================================================================
# 1. Pull from GitHub
# =============================================================================
echo "Pulling from GitHub..." >> ~/vault-sync-local.log
if git pull origin main --quiet >> ~/vault-sync-local.log 2>&1; then
    echo "✓ Pull successful" >> ~/vault-sync-local.log
else
    echo "✗ ERROR: Pull failed" >> ~/vault-sync-local.log

    # Check for conflicts
    if git status | grep -q "both modified"; then
        echo "✗ Merge conflict detected!" >> ~/vault-sync-local.log
        mkdir -p "$VAULT_DIR/Errors/sync"
        git status > "$VAULT_DIR/Errors/sync/conflict-$(date +%Y%m%d-%H%M%S).log"
        exit 1
    fi
fi

# =============================================================================
# 2. Merge Cloud updates into Dashboard.md
# =============================================================================
if [ -d "Updates" ] && [ "$(ls -A Updates/*.md 2>/dev/null)" ]; then
    echo "Merging cloud updates..." >> ~/vault-sync-local.log

    # Backup current Dashboard.md
    cp Dashboard.md "Dashboard.md.backup-$(date +%Y%m%d-%H%M%S)"

    # Append all update files to Dashboard.md
    for update_file in Updates/*.md; do
        if [ -f "$update_file" ]; then
            echo "" >> Dashboard.md
            echo "---" >> Dashboard.md
            cat "$update_file" >> Dashboard.md

            # Remove merged update file
            rm "$update_file"
        fi
    done

    # Stage Dashboard.md update
    git add Dashboard.md
    echo "✓ Updates merged into Dashboard.md" >> ~/vault-sync-local.log
fi

# =============================================================================
# 3. Stage local changes
# =============================================================================
git add -A

# =============================================================================
# 4. Check if there are changes to commit
# =============================================================================
if git diff --cached --quiet && git diff --quiet; then
    echo "No local changes to commit" >> ~/vault-sync-local.log
    exit 0
fi

# =============================================================================
# 5. Commit local changes
# =============================================================================
git commit -m "Local updates + merged cloud signals $(date '+%Y-%m-%d %H:%M:%S')"

# =============================================================================
# 6. Push to GitHub
# =============================================================================
echo "Pushing to GitHub..." >> ~/vault-sync-local.log
if git push origin main --quiet >> ~/vault-sync-local.log 2>&1; then
    echo "✓ Push successful" >> ~/vault-sync-local.log
else
    echo "✗ ERROR: Push failed" >> ~/vault-sync-local.log
    exit 1
fi

echo "=== Local Sync Complete: $(date) ===" >> ~/vault-sync-local.log
echo "" >> ~/vault-sync-local.log
