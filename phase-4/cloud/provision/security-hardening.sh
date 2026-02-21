#!/bin/bash
# Security Hardening for Phase 4 - Platinum Tier Cloud VM
# Platform: Ubuntu 22.04 LTS
# Purpose: Configure firewall, SSH hardening, fail2ban, and system security

set -e

echo "=== Security Hardening - Phase 4 Cloud VM ==="
echo ""

LOG_FILE="/var/log/security-hardening.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# ==============================================================================
# Step 1: Configure UFW Firewall
# ==============================================================================
log "Step 1: Configuring UFW Firewall"

# Reset to default
sudo ufw --force reset >> "$LOG_FILE" 2>&1

# Set default policies
sudo ufw default deny incoming >> "$LOG_FILE" 2>&1
sudo ufw default allow outgoing >> "$LOG_FILE" 2>&1

# Allow SSH (from anywhere for now, restrict later)
log "  Allowing SSH (port 22)..."
sudo ufw allow 22/tcp >> "$LOG_FILE" 2>&1

# Allow HTTP
log "  Allowing HTTP (port 80)..."
sudo ufw allow 80/tcp >> "$LOG_FILE" 2>&1

# Allow HTTPS
log "  Allowing HTTPS (port 443)..."
sudo ufw allow 443/tcp >> "$LOG_FILE" 2>&1

# Allow Health Endpoint
log "  Allowing Health Endpoint (port 8080)..."
sudo ufw allow 8080/tcp >> "$LOG_FILE" 2>&1

# Allow Odoo (restrict to your IP in production)
log "  Allowing Odoo (port 8069)..."
sudo ufw allow 8069/tcp >> "$LOG_FILE" 2>&1

# Enable firewall
log "  Enabling UFW firewall..."
sudo ufw --force enable >> "$LOG_FILE" 2>&1

log "  ✓ Firewall configured and enabled"

# ==============================================================================
# Step 2: SSH Hardening
# ==============================================================================
log "Step 2: Hardening SSH Configuration"

SSH_CONFIG="/etc/ssh/sshd_config"

# Backup original config
sudo cp "$SSH_CONFIG" "${SSH_CONFIG}.bak"

log "  Configuring SSH security settings..."

# Disable root login
sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' "$SSH_CONFIG"

# Disable password authentication (key-only)
sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' "$SSH_CONFIG"

# Disable X11 forwarding
sudo sed -i 's/^X11Forwarding.*/X11Forwarding no/' "$SSH_CONFIG"

# Set MaxAuthTries
sudo sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' "$SSH_CONFIG"

# Set LoginGraceTime
sudo sed -i 's/^#*LoginGraceTime.*/LoginGraceTime 60/' "$SSH_CONFIG"

# Set ClientAliveInterval
echo "" | sudo tee -a "$SSH_CONFIG" > /dev/null
echo "# Security hardening (Phase 4)" | sudo tee -a "$SSH_CONFIG" > /dev/null
echo "ClientAliveInterval 300" | sudo tee -a "$SSH_CONFIG" > /dev/null
echo "ClientAliveCountMax 2" | sudo tee -a "$SSH_CONFIG" > /dev/null
echo "AllowUsers ai-employee ubuntu" | sudo tee -a "$SSH_CONFIG" > /dev/null

# Test SSH config
log "  Testing SSH configuration..."
if sudo sshd -t 2>&1; then
    log "  ✓ SSH configuration valid"
    sudo systemctl reload sshd >> "$LOG_FILE" 2>&1
    log "  ✓ SSH reloaded with hardening"
else
    log "  ✗ SSH configuration has errors, reverting"
    sudo mv "${SSH_CONFIG}.bak" "$SSH_CONFIG"
    exit 1
fi

# ==============================================================================
# Step 3: Configure Fail2ban
# ==============================================================================
log "Step 3: Configuring Fail2ban"

JAIL_LOCAL="/etc/fail2ban/jail.local"

if [ ! -f "$JAIL_LOCAL" ]; then
    sudo cp /etc/fail2ban/jail.conf "$JAIL_LOCAL"
fi

log "  Configuring SSH protection in Fail2ban..."

# Configure SSH jail
sudo tee -a "$JAIL_LOCAL" > /dev/null <<'EOF'

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
findtime = 600
bantime = 3600
EOF

# Start Fail2ban
sudo systemctl restart fail2ban >> "$LOG_FILE" 2>&1
sudo systemctl enable fail2ban >> "$LOG_FILE" 2>&1

log "  ✓ Fail2ban configured for SSH protection"

# ==============================================================================
# Step 4: System Security Updates
# ==============================================================================
log "Step 4: Configuring automatic security updates"

# Install unattended-upgrades
sudo apt install -y unattended-upgrades >> "$LOG_FILE" 2>&1

# Configure automatic updates
sudo dpkg-reconfigure -plow unattended-upgrades -y >> "$LOG_FILE" 2>&1

log "  ✓ Automatic security updates configured"

# ==============================================================================
# Step 5: Secure Shared Memory
# ==============================================================================
log "Step 5: Securing shared memory (kernel parameters)"

# Add to sysctl.conf
SYSCTL_FILE="/etc/sysctl.d/99-security.conf"

sudo tee "$SYSCTL_FILE" > /dev/null <<'EOF'
# Phase 4 Security Hardening
# ASLR
kernel.randomize_va_space = 2
kernel.randomize_va_space = 1

# Prevent kernel pointer overwrite
kernel.kptr_restrict = 1

# Restrict access to kernel logs
kernel.dmesg_restrict = 1

# Protect against symlink attacks
fs.protected_hardlinks = 1
fs.protected_symlinks = 1

# IP spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP broadcasts
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Ignore bogus ICMP errors
net.ipv4.icmp_ignore_bogus_error_responses = 1
EOF

# Apply sysctl settings
sudo sysctl -p "$SYSCTL_FILE" >> "$LOG_FILE" 2>&1

log "  ✓ Kernel security parameters applied"

# ==============================================================================
# Step 6: Restrict File Permissions
# ==============================================================================
log "Step 6: Setting restrictive umask"

# Set umask in /etc/profile
sudo tee -a /etc/profile > /dev/null <<'EOF'

# Phase 4 Security: Restrictive umask
umask 027
EOF

log "  ✓ Umask set to 027 (group/other read-only)"

# ==============================================================================
# Step 7: Install and Configure chkrootkit
# ==============================================================================
log "Step 7: Installing rootkit checker..."

sudo apt install -y chkrootkit >> "$LOG_FILE" 2>&1

# Configure chkrootkit
sudo tee -a /etc/chkrootkit.conf > /dev/null <<'EOF'
RUN_DAILY="true"
DIFF_MODE="quiet"
QUICK_MODE="false"
EOF

log "  ✓ chkrootkit installed"

# ==============================================================================
# Step 8: Configure Log Rotation
# ==============================================================================
log "Step 8: Configuring log rotation"

LOGROTATE_FILE="/etc/logrotate.d/ai-employee"

sudo tee "$LOGROTATE_FILE" > /dev/null <<'EOF'
# Phase 4 Application Logs
/var/log/ai-employee/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 ai-employee ai-employee
    sharedscripts
    postrotate
        systemctl reload ai-employee-orchestrator > /dev/null 2>&1 || true
    endscript
}
EOF

log "  ✓ Log rotation configured"

# ==============================================================================
# SUMMARY
# ==============================================================================
echo ""
echo "=== Security Hardening Complete ==="
echo ""
echo "Configured Security Measures:"
echo "  ✓ UFW Firewall (ports: 22, 80, 443, 8080, 8069)"
echo "  ✓ SSH Hardening (key-only, root disabled)"
echo "  ✓ Fail2ban (SSH brute-force protection)"
echo "  ✓ Automatic security updates"
echo "  ✓ Kernel security parameters"
echo "  ✓ Restrictive umask (027)"
echo "  ✓ chkrootkit (rootkit detection)"
echo "  ✓ Log rotation configured"
echo ""
echo "Security Recommendations:"
echo "  1. Consider restricting SSH to specific IP addresses:"
echo "     sudo ufw allow from YOUR_IP/22 proto tcp"
echo ""
echo "  2. Review SSH logins regularly:"
echo "     sudo tail -f /var/log/auth.log"
echo ""
echo "  3. Run security audit weekly:"
echo "     sudo chkrootkit"
echo ""
echo "  4. Monitor Fail2ban status:"
echo "     sudo fail2ban-client status"
echo ""
echo "Security log: $LOG_FILE"
echo ""

# Display current firewall status
echo "Current Firewall Status:"
sudo ufw status verbose
echo ""