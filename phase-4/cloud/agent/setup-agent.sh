#!/bin/bash
# Cloud Agent Setup Script for Phase 4 - Platinum Tier
# Purpose: Deploy cloud agent with Python venv, dependencies, and systemd services

set -e

echo "=== Cloud Agent Setup - Phase 4 Platinum Tier ==="
echo ""

# Configuration
AGENT_USER="ai-employee"
AGENT_DIR="/opt/ai-employee"
VAULT_PATH="/vault"
PYTHON_VERSION="python3.10"

LOG_FILE="/var/log/ai-employee/setup.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $*"
    exit 1
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root or with sudo"
    exit 1
fi

# ==============================================================================
# Step 1: Create agent user
# ==============================================================================
log "Step 1: Creating agent user..."

if ! id "$AGENT_USER" &>/dev/null; then
    useradd --system \
        --shell /bin/bash \
        --home $AGENT_DIR \
        --comment "AI Employee Agent" \
        $AGENT_USER
    log "  ✓ User '$AGENT_USER' created"
else
    log "  ✓ User '$AGENT_USER' already exists"
fi

# ==============================================================================
# Step 2: Create directory structure
# ==============================================================================
log "Step 2: Creating directory structure..."

mkdir -p $AGENT_DIR
mkdir -p $VAULT_PATH
mkdir -p /var/log/ai-employee

# Copy phase-4 files
if [ -d "phase-4" ]; then
    log "  Copying Phase 4 files to $AGENT_DIR..."
    cp -r phase-4 $AGENT_DIR/
    chown -R $AGENT_USER:$AGENT_USER $AGENT_DIR/phase-4
    log "  ✓ Phase 4 files copied"
fi

# ==============================================================================
# Step 3: Create Python virtual environment
# ==============================================================================
log "Step 3: Setting up Python virtual environment..."

log "  Creating Python venv at $AGENT_DIR/venv..."
sudo -u $AGENT_USER python3 -m venv $AGENT_DIR/venv >> "$LOG_FILE" 2>&1

# Upgrade pip
log "  Upgrading pip..."
sudo -u $AGENT_USER $AGENT_DIR/venv/bin/pip install --upgrade pip >> "$LOG_FILE" 2>&1

# Install Python dependencies
log "  Installing Python dependencies..."
REQUIREMENTS_FILE="$AGENT_DIR/phase-4/cloud/requirements.txt"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    log "  Creating requirements.txt..."
    cat > "$REQUIREMENTS_FILE" <<'EOF'
# Phase 4 Cloud Agent Requirements

# Web Framework
flask==3.0.0
gunicorn==21.2.0

# Watchdogs
watchdog==3.0.0

# Email
gmail-api==0.7.1
google-api-python-client==2.100.0

# Utilities
pyyaml==6.0.1
requests==2.31.0
python-dotenv==1.0.0

# System monitoring
psutil==5.9.5
EOF
fi

sudo -u $AGENT_USER $AGENT_DIR/venv/bin/pip install -r "$REQUIREMENTS_FILE" >> "$LOG_FILE" 2>&1

log "  ✓ Python dependencies installed"

# ==============================================================================
# Step 4: Create configuration files
# ==============================================================================
log "Step 4: Creating configuration files..."

CLOUD_ENV="$AGENT_DIR/phase-4/cloud/config/cloud.env"

if [ ! -f "$CLOUD_ENV" ]; then
    log "  Creating cloud.env from template..."
    cp "$CLOUD_ENV.example" "$CLOUD_ENV" 2>/dev/null || cat > "$CLOUD_ENV" <<'EOF'
# Cloud Agent Configuration
AGENT_ROLE=CLOUD
AGENT_NAME=cloud
VAULT_PATH=/vault

# Watcher Configuration
WATCHER_INTERVAL=30
GMAIL_WATCHER_ENABLED=true
FILESYSTEM_WATCHER_ENABLED=true

# Allowed Actions
ALLOWED_ACTIONS=triage,draft,schedule,monitor

# Health Server
HEALTH_PORT=8080
HEALTH_RATE_LIMIT=1

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai-employee/agent.log
EOF
fi

chmod 600 "$CLOUD_ENV"
chown $AGENT_USER:$AGENT_USER "$CLOUD_ENV"

log "  ✓ Cloud configuration created"

# ==============================================================================
# Step 5: Setup systemd services
# ==============================================================================
log "Step 5: Installing systemd services..."

SERVICES_DIR="$AGENT_DIR/phase-4/cloud/agent/systemd-units"

if [ -d "$SERVICES_DIR" ]; then
    for service in "$SERVICES_DIR"/*.service; do
        if [ -f "$service" ]; then
            SERVICE_NAME=$(basename "$service")
            log "  Installing $SERVICE_NAME..."
            cp "$service" /etc/systemd/system/
            systemctl daemon-reload >> "$LOG_FILE" 2>&1
            systemctl enable "${SERVICE_NAME%.service}" >> "$LOG_FILE" 2>&1
            log "    ✓ ${SERVICE_NAME%.service} enabled"
        fi
    done
fi

log "  ✓ Systemd services installed"

# ==============================================================================
# Step 6: Setup sync daemon
# ==============================================================================
log "Step 6: Installing vault sync daemon..."

SYNC_DAEMON="$AGENT_DIR/phase-4/cloud/agent/sync-daemon.sh"

if [ -f "$SYNC_DAEMON" ]; then
    # Make executable
    chmod +x "$SYNC_DAEMON"

    # Create systemd service for sync daemon
    cat > /etc/systemd/system/ai-employee-sync.service <<EOF
[Unit]
Description=AI Employee Vault Sync Daemon
Documentation=https://github.com/your-username/ai-employee
After=network.target

[Service]
Type=simple
User=$AGENT_USER
Group=$AGENT_USER
WorkingDirectory=$VAULT_PATH
Environment="PATH=$AGENT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$SYNC_DAEMON
Restart=always
RestartSec=60
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ai-employee-sync

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload >> "$LOG_FILE" 2>&1
    systemctl enable ai-employee-sync >> "$LOG_FILE" 2>&1
    log "  ✓ Sync daemon installed as systemd service"
else
    log "  Warning: sync-daemon.sh not found, skipping"
fi

# ==============================================================================
# Step 7: Setup security audit
# ==============================================================================
log "Step 7: Installing security audit script..."

SECURITY_AUDIT="$AGENT_DIR/phase-4/vault/security-audit.sh"

if [ -f "$SECURITY_AUDIT" ]; then
    chmod +x "$SECURITY_AUDIT"
    log "  ✓ Security audit script installed (executable)"
else
    log "  Warning: security-audit.sh not found, skipping"
fi

# ==============================================================================
# Step 8: Create log directory and permissions
# ==============================================================================
log "Step 8: Setting up logging..."

# Create log directory
mkdir -p /var/log/ai-employee
chown $AGENT_USER:$AGENT_USER /var/log/ai-employee

# Configure logrotate
cat > /etc/logrotate.d/ai-employee <<EOF
# AI Employee Logs
/var/log/ai-employee/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 0640 $AGENT_USER $AGENT_USER
    sharedscripts
    postrotate
        systemctl reload ai-employee-orchestrator > /dev/null 2>&1 || true
    endscript
}
EOF

log "  ✓ Logging configured"

# ==============================================================================
# Step 9: Display summary
# ==============================================================================
echo ""
echo "=== Cloud Agent Setup Complete ==="
echo ""
echo "Agent User: $AGENT_USER"
echo "Agent Directory: $AGENT_DIR"
echo "Vault Path: $VAULT_PATH"
echo ""
echo "Python Venv: $AGENT_DIR/venv"
echo "Python Version: $(python3 --version)"
echo ""
echo "Systemd Services:"
systemctl list-units | grep ai-employee | grep -v "not-found" || echo "  (No services found - may need manual start)"
echo ""
echo "Configuration Files:"
echo "  Cloud Config: $CLOUD_ENV"
echo "  Sync Daemon: $SYNC_DAEMON"
echo "  Security Audit: $SECURITY_AUDIT"
echo ""
echo "Next Steps:"
echo "  1. Start health server:"
echo "     systemctl start ai-employee-health"
echo ""
echo "  2. Start orchestrator:"
echo "     systemctl start ai-employee-orchestrator"
echo ""
echo "  3. Start sync daemon:"
echo "     systemctl start ai-employee-sync"
echo ""
echo "  4. Check health status:"
echo "     curl http://localhost:8080/health"
echo ""
echo "  5. View logs:"
echo "     journalctl -u ai-employee-health -f"
echo "     tail -f /var/log/ai-employee/agent.log"
echo ""
echo "Setup log: $LOG_FILE"
echo ""
echo "✓ Cloud Agent Setup Complete"
echo ""
