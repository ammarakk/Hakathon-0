#!/bin/bash
# Cloud Sync Daemon for Phase 4 - Platinum Tier
# Purpose: Synchronize vault between Cloud VM and GitHub repository
# Interval: 30 seconds (configurable)
# Security: Pre-sync audit to prevent secrets from being committed

set -e

# Configuration
VAULT_DIR="/vault"
SYNC_INTERVAL=30  # seconds
GIT_BRANCH="main"
GIT_REMOTE="origin"
LOG_FILE="/var/log/ai-employee/sync-daemon.log"
SECURITY_AUDIT_SCRIPT="/opt/ai-employee/phase-4/vault/security-audit.sh"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $*"
    exit 1
}

# Main sync loop
sync_loop() {
    log "=== Cloud Sync Daemon Started ==="
    log "Vault: $VAULT_DIR"
    log "Sync Interval: $SYNC_INTERVAL seconds"
    log "Git Branch: $GIT_BRANCH"
    log "Remote: $GIT_REMOTE"
    log ""

    while true; do
        log "Starting sync cycle..."

        # Change to vault directory
        cd "$VAULT_DIR" || error_exit "Cannot access vault directory: $VAULT_DIR"

        # 1. Pull latest changes from GitHub
        log "Pulling from $GIT_REMOTE $GIT_BRANCH..."
        if git pull "$GIT_REMOTE" "$GIT_BRANCH" --quiet >> "$LOG_FILE" 2>&1; then
            log "Pull successful"
        else
            # Check if it's a conflict
            if git status | grep -q "both modified"; then
                log "ERROR: Merge conflict detected!"
                log "Logging conflict to /Errors/sync/"

                # Create conflict log
                mkdir -p Errors/sync
                {
                    echo "Merge Conflict detected at $(date)"
                    echo ""
                    git status
                    echo ""
                    echo "Files in conflict:"
                    git diff --name-only --diff-filter=U
                } > "Errors/sync/conflict-$(date +%Y%m%d-%H%M%S).log"

                # Stop further processing until conflict resolved
                log "Stopping sync daemon - conflict requires manual resolution"
                log "After resolving conflicts, restart sync daemon"
                exit 1
            else
                log "ERROR: Pull failed (no conflict detected)"
                log "Possible network issue - will retry on next cycle"
            fi
        fi

        # 2. Run cloud agent tasks (if any)
        # This is where the cloud orchestrator would run
        # For now, we just wait a bit to simulate processing
        sleep 5

        # 3. Stage all changes
        log "Staging changes..."
        git add -A >> "$LOG_FILE" 2>&1

        # 4. Check if there are changes to commit
        if git diff --cached --quiet && git diff --quiet; then
            log "No changes to commit"
        else
            # 5. Verify no secrets staged (security audit)
            log "Running security audit..."
            if [ -f "$SECURITY_AUDIT_SCRIPT" ]; then
                if bash "$SECURITY_AUDIT_SCRIPT" >> "$LOG_FILE" 2>&1; then
                    log "Security audit passed"
                else
                    log "ERROR: Security audit failed!"
                    log "Secrets detected in staged files. Aborting commit."
                    log "Blocking git push for security reasons."
                    exit 1
                fi
            else
                log "Warning: Security audit script not found, skipping..."
            fi

            # 6. BLOCK if Dashboard.md is being modified (single-writer rule)
            if git diff --cached --name-only | grep -q "Dashboard.md"; then
                log "ERROR: Cloud attempted to modify Dashboard.md!"
                log "Dashboard.md is single-writer (Local only). Blocking commit."
                git reset HEAD Dashboard.md
                exit 1
            fi

            # 7. Commit changes
            log "Committing changes..."
            git commit -m "Cloud updates $(date '+%Y-%m-%d %H:%M:%S UTC')" >> "$LOG_FILE" 2>&1

            # 8. Push to GitHub
            log "Pushing to $GIT_REMOTE $GIT_BRANCH..."
            if git push "$GIT_REMOTE" "$GIT_BRANCH" --quiet >> "$LOG_FILE" 2>&1; then
                log "Push successful"
            else
                # Check if push failed due to remote divergence
                log "ERROR: Push failed - remote may have diverged"
                log "Will retry on next cycle after pull"
            fi
        fi

        log "Sync cycle complete"
        log "Sleeping for $SYNC_INTERVAL seconds..."
        log ""

        # Wait for next interval
        sleep "$SYNC_INTERVAL"
    done
}

# Signal handlers
cleanup() {
    log "=== Cloud Sync Daemon Stopped ==="
    exit 0
}

trap cleanup SIGTERM SIGINT

# Main entry point
main() {
    # Verify we're in the right directory
    if [ ! -d "$VAULT_DIR" ]; then
        echo "Error: Vault directory not found: $VAULT_DIR"
        exit 1
    fi

    # Verify Git repository is initialized
    if [ ! -d "$VAULT_DIR/.git" ]; then
        echo "Error: Git repository not initialized in $VAULT_DIR"
        echo "Run: cd $VAULT_DIR && git init"
        exit 1
    fi

    # Check if security audit script exists
    if [ ! -f "$SECURITY_AUDIT_SCRIPT" ]; then
        echo "Warning: Security audit script not found: $SECURITY_AUDIT_SCRIPT"
        echo "Sync will proceed without security checks (NOT RECOMMENDED)"
    fi

    # Start sync loop
    sync_loop
}

# Run main function
main "$@"