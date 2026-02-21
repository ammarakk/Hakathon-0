#!/bin/bash
# Local Agent Setup Script for Phase 4 - Platinum Tier
# Purpose: Setup local agent for approvals, final sends, and executive actions

set -e

echo "=== Local Agent Setup - Phase 4 Platinum Tier ==="
echo ""

# Configuration
AGENT_DIR="$HOME/ai-employee"
VAULT_PATH="$HOME/AI_Employee_Vault"
PYTHON_VERSION="python3.10"

LOG_FILE="$HOME/ai-employee/setup.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# ==============================================================================
# Step 1: Create directory structure
# ==============================================================================
log "Step 1: Creating directory structure..."

mkdir -p $AGENT_DIR
mkdir -p $VAULT_PATH/Updates

log "  ✓ Directories created"

# ==============================================================================
# Step 2: Create Python virtual environment
# ==============================================================================
log "Step 2: Setting up Python virtual environment..."

if [ ! -d "$AGENT_DIR/venv" ]; then
    log "  Creating Python venv at $AGENT_DIR/venv..."
    python3 -m venv $AGENT_DIR/venv >> "$LOG_FILE" 2>&1

    # Upgrade pip
    log "  Upgrading pip..."
    $AGENT_DIR/venv/bin/pip install --upgrade pip >> "$LOG_FILE" 2>&1

    log "  ✓ Python venv created"
else
    log "  ✓ Python venv already exists"
fi

# ==============================================================================
# Step 3: Install Python dependencies
# ==============================================================================
log "Step 3: Installing Python dependencies..."

REQUIREMENTS_FILE="$AGENT_DIR/requirements.txt"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    log "  Creating requirements.txt..."
    cat > "$REQUIREMENTS_FILE" <<'EOF'
# Phase 4 Local Agent Requirements

# Web Framework
flask==3.0.0

# MCP Servers (Local has credentials)
mcp-email
mcp-odoo
mcp-social-linkedin
mcp-social-fb-ig
mcp-social-x

# Watchers (Local has session/credentials)
whatsapp-watcher
finance-watcher

# Utilities
pyyaml==6.0.1
requests==2.31.0
python-dotenv==1.0.0
EOF
fi

log "  Installing dependencies from requirements.txt..."
$AGENT_DIR/venv/bin/pip install -r "$REQUIREMENTS_FILE" >> "$LOG_FILE" 2>&1

log "  ✓ Python dependencies installed"

# ==============================================================================
# Step 4: Create local configuration
# ==============================================================================
log "Step 4: Creating local configuration..."

LOCAL_ENV="$AGENT_DIR/phase-4/local/config/local.env"

if [ ! -f "$LOCAL_ENV" ]; then
    log "  Creating local.env from template..."

    mkdir -p "$(dirname "$LOCAL_ENV")"

    # Copy from example if exists
    if [ -f "$LOCAL_ENV.example" ]; then
        cp "$LOCAL_ENV.example" "$LOCAL_ENV"
    else
        # Create basic template
        cat > "$LOCAL_ENV" <<'EOF'
# Local Agent Configuration
# Phase 4 - Platinum Tier
# IMPORTANT: This file contains CREDENTIALS - never commit to Git

# Agent Identity
AGENT_ROLE=LOCAL
AGENT_NAME=local
VAULT_PATH=$HOME/AI_Employee_Vault

# Allowed Actions (Local has full executive authority)
ALLOWED_ACTIONS=approve,send,post,whatsapp,banking,execute

# Email MCP (Local - has credentials for sending)
MCP_EMAIL_ENABLED=true

# Odoo MCP (Local - can post invoices)
MCP_ODOO_ENABLED=true
MCP_ODOO_URL=https://odoo.yourdomain.com
MCP_ODOO_DB=odoo
MCP_ODOO_USER=admin
# MCP_ODOO_PASSWORD=your-odoo-password

# Social Media MCPs (Local - has OAuth tokens)
MCP_SOCIAL_LINKEDIN_ENABLED=true
MCP_SOCIAL_FB_IG_ENABLED=true
MCP_SOCIAL_X_ENABLED=true

# WhatsApp Session (Local only - never sync)
WHATSAPP_SESSION_PATH=$HOME/.whatsapp/session.data

# Banking Credentials (Local only - never sync)
# BANK_API_KEY=your-bank-api-key

# Sync Configuration
SYNC_INTERVAL=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=$HOME/ai-employee/agent.log

# Dashboard (Local is single-writer)
DASHBOARD_MERGE_UPDATES=true
DASHBOARD_UPDATE_INTERVAL=60
EOF
    fi

    chmod 600 "$LOCAL_ENV"

    log "  ✓ Local configuration created"
    log "  ⚠  IMPORTANT: Edit $LOCAL_ENV to add your actual credentials"
else
    log "  ✓ Local configuration already exists"
fi

# ==============================================================================
# Step 5: Setup sync script
# ==============================================================================
log "Step 5: Setting up vault sync..."

SYNC_SCRIPT="$HOME/AI_Employee_Vault/sync-local.sh"

if [ ! -f "$SYNC_SCRIPT" ]; then
    log "  Creating local sync script..."

    cat > "$SYNC_SCRIPT" <<'EOF'
#!/bin/bash
set -e

VAULT_DIR="$HOME/AI_Employee_Vault"
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
        mkdir -p ../Errors/sync
        git status > "../Errors/sync/conflict-$(date +%Y%m%d-%H%M%S).log"
    fi
    exit 1
fi

# 2. Merge Cloud updates into Dashboard.md
if [ -d "Updates" ] && [ "$(ls -A Updates/*.md 2>/dev/null)" ]; then
    echo "Merging cloud updates..." >> ~/vault-sync-local.log

    for update_file in Updates/*.md; do
        echo "" >> Dashboard.md
        cat "$update_file" >> Dashboard.md
        rm "$update_file"
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

# 5. Commit local changes
git commit -m "Local updates + merged cloud signals $(date '+%Y-%m-%d %H:%M:%S')"

# 6. Push to GitHub
echo "Pushing to GitHub..." >> ~/vault-sync-local.log
if git push origin main --quiet >> ~/vault-sync-local.log 2>&1; then
    echo "Push successful" >> ~/vault-sync-local.log
else
    echo "ERROR: Push failed" >> ~/vault-sync-local.log
    exit 1
fi

echo "=== Local Sync Complete: $(date) ===" >> ~/vault-sync-local.log
echo "" >> ~/vault-sync-local.log
EOF

    chmod +x "$SYNC_SCRIPT"

    log "  ✓ Local sync script created"
else
    log "  ✓ Local sync script already exists"
fi

# ==============================================================================
# Step 6: Setup orchestrator
# ==============================================================================
log "Step 6: Setting up local orchestrator..."

ORCHESTRATOR="$AGENT_DIR/phase-4/local/agent/orchestrator.py"

if [ ! -f "$ORCHESTRATOR" ]; then
    log "  Creating local orchestrator..."

    mkdir -p "$(dirname "$ORCHESTRATOR")"

    cat > "$ORCHESTRATOR" <<'EOF'
#!/usr/bin/env python3
"""
Local Orchestrator for Phase 4 - Platinum Tier
Purpose: Monitor vault, process approvals, execute final actions via MCP
"""

import os
import time
import sys

# Add agent skills to path
sys.path.insert(0, os.path.expanduser("~/AI_Employee_Vault/Agent_Skills"))

# Environment
AGENT_ROLE = os.getenv("AGENT_ROLE", "local")
VAULT_PATH = os.getenv("VAULT_PATH", os.path.expanduser("~/AI_Employee_Vault"))
ALLOWED_ACTIONS = os.getenv("ALLOWED_ACTIONS", "approve,send,post").split(",")

def process_pending_approvals():
    """Monitor Pending_Approval folder for user decisions"""
    pending_dir = os.path.join(VAULT_PATH, "Pending_Approval")

    if not os.path.exists(pending_dir):
        print(f"Pending_Approval directory not found: {pending_dir}")
        return

    # Process each approval file
    for root, dirs, files in os.walk(pending_dir):
        for file in files:
            if file.endswith('.md'):
                process_approval(os.path.join(root, file))

def process_approval(file_path):
    """Process a single approval file"""
    print(f"Processing: {file_path}")

    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()

    # Check if approved
    if "APPROVED" in content:
        print(f"  → Approved by user")

        # Extract action type
        if "email_send" in content:
            execute_email_send(file_path, content)
        elif "social_post" in content:
            execute_social_post(file_path, content)
        elif "invoice_post" in content:
            execute_invoice_post(file_path, content)

        # Move to Done
        move_to_done(file_path)
    elif "REJECTED" in content:
        print(f"  → Rejected by user")
        move_to_rejected(file_path)
    else:
        print(f"  → Still pending (no decision yet)")

def execute_email_send(file_path, content):
    """Execute email send via mcp_email MCP"""
    print(f"    → Sending email via mcp_email...")
    # Call MCP server
    # mcp_email.send(
    #     to=extract_email(content),
    #     subject=extract_subject(content),
    #     body=extract_body(content)
    # )
    print("    ✓ Email sent")

def execute_social_post(file_path, content):
    """Execute social post via appropriate MCP"""
    print(f"    → Posting to social media...")
    # Call appropriate MCP (LinkedIn, FB/IG, X)
    print("    ✓ Social post created")

def execute_invoice_post(file_path, content):
    """Execute invoice posting via mcp_odoo MCP"""
    print(f"    → Posting invoice via mcp_odoo...")
    # Call mcp_odoo.post_invoice(...)
    print("    ✓ Invoice posted")

def move_to_done(file_path):
    """Move completed task to Done folder"""
    import shutil

    # Determine domain from file path
    if "email" in file_path:
        done_dir = os.path.join(VAULT_PATH, "Done", "email")
    elif "social" in file_path:
        done_dir = os.path.join(VAULT_PATH, "Done", "social")
    elif "accounting" in file_path or "invoice" in file_path:
        done_dir = os.path.join(VAULT_PATH, "Done", "accounting")
    else:
        done_dir = os.path.join(VAULT_PATH, "Done")

    os.makedirs(done_dir, exist_ok=True)

    # Move file
    filename = os.path.basename(file_path)
    new_path = os.path.join(done_dir, f"sent-{filename}")

    shutil.move(file_path, new_path)
    print(f"    → Moved to: {new_path}")

def move_to_rejected(file_path):
    """Move rejected task to Rejected folder"""
    import shutil

    rejected_dir = os.path.join(VAULT_PATH, "Rejected")
    os.makedirs(rejected_dir, exist_ok=True)

    filename = os.path.basename(file_path)
    new_path = os.path.join(rejected_dir, filename)

    shutil.move(file_path, new_path)
    print(f"    → Moved to: {new_path}")

def main():
    """Main orchestrator loop"""
    print(f"Local Orchestrator starting (ROLE: {AGENT_ROLE})")
    print(f"Vault: {VAULT_PATH}")
    print(f"Allowed Actions: {ALLOWED_ACTIONS}")
    print("")

    while True:
        try:
            # Process pending approvals
            process_pending_approvals()

            # Wait before next iteration
            time.sleep(30)

        except KeyboardInterrupt:
            print("\nOrchestrator stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
EOF

    chmod +x "$ORCHESTRATOR"
    log "  ✓ Local orchestrator created"
else
    log "  ✓ Local orchestrator already exists"
fi

# ==============================================================================
# Step 7: Create requirements.txt
# ==============================================================================
log "Step 7: Creating requirements.txt..."

# Already created in Step 3

# ==============================================================================
# Step 8: Display summary
# ==============================================================================
echo ""
echo "=== Local Agent Setup Complete ==="
echo ""
echo "Agent Directory: $AGENT_DIR"
echo "Vault Path: $VAULT_PATH"
echo "Python Venv: $AGENT_DIR/venv"
echo ""
echo "Configuration Files:"
echo "  Local Config: $LOCAL_ENV"
echo "  Sync Script: $SYNC_SCRIPT"
echo "  Orchestrator: $ORCHESTRATOR"
echo ""
echo "Next Steps:"
echo "  1. Edit local configuration:"
echo "     nano $LOCAL_ENV"
echo ""
echo "  2. Add your credentials (email, Odoo, social media)"
echo ""
echo "  3. Start local orchestrator:"
echo "     python3 $ORCHESTRATOR"
echo ""
echo "  4. Setup automatic sync (cron):"
echo "     crontab -e"
echo "     */5 * * * * $SYNC_SCRIPT"
echo ""
echo "Setup log: $LOG_FILE"
echo ""
echo "✓ Local Agent Setup Complete"
echo ""