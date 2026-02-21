#!/bin/bash
# Install Dependencies for Phase 4 - Platinum Tier Cloud VM
# Platform: Ubuntu 22.04 LTS
# Purpose: Install Python, Git, PostgreSQL, Nginx, and other required packages

set -e

echo "=== Installing Phase 4 Dependencies ==="
echo "Platform: Ubuntu 22.04 LTS"
echo ""

LOG_FILE="/var/log/phase-4-install.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Update system
log "Step 1: Updating system packages..."
sudo apt update >> "$LOG_FILE" 2>&1
sudo apt upgrade -y >> "$LOG_FILE" 2>&1

# Install essential build tools
log "Step 2: Installing build tools..."
sudo apt install -y \
    build-essential \
    curl \
    wget \
    git \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    >> "$LOG_FILE" 2>&1

# Install Python 3.10+ with pip
log "Step 3: Installing Python 3..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    python3-setuptools \
    >> "$LOG_FILE" 2>&1

# Verify Python version
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
log "  Python version: $PYTHON_VERSION"

# Install Git
log "Step 4: Installing Git..."
sudo apt install -y git >> "$LOG_FILE" 2>&1
GIT_VERSION=$(git --version)
log "  $GIT_VERSION"

# Install PostgreSQL 14
log "Step 5: Installing PostgreSQL 14..."
sudo apt install -y \
    postgresql \
    postgresql-contrib \
    postgresql-server-dev-all \
    >> "$LOG_FILE" 2>&1

# Start PostgreSQL
sudo systemctl start postgresql >> "$LOG_FILE" 2>&1
sudo systemctl enable postgresql >> "$LOG_FILE" 2>&1

# Verify PostgreSQL
PG_VERSION=$(psql --version | awk '{print $3}')
log "  PostgreSQL: $PG_VERSION"

# Install Nginx
log "Step 6: Installing Nginx..."
sudo apt install -y nginx >> "$LOG_FILE" 2>&1
NGINX_VERSION=$(nginx -v 2>&1 | grep -oP '\d+\.\d+\.\d+')
log "  Nginx: $NGINX_VERSION"

# Install certbot for Let's Encrypt SSL
log "Step 7: Installing certbot (Let's Encrypt)..."
sudo apt install -y \
    certbot \
    python3-certbot-nginx \
    >> "$LOG_FILE" 2>&1

# Install additional Python packages
log "Step 8: Installing additional Python packages..."
sudo apt install -y \
    python3-psycopg2 \
    python3-pycurl \
    python3-yaml \
    python3-requests \
    python3-flask \
    >> "$LOG_FILE" 2>&1

# Install Supervisor (for process management)
log "Step 9: Installing Supervisor..."
sudo apt install -y supervisor >> "$LOG_FILE" 2>&1
sudo systemctl start supervisor >> "$LOG_FILE" 2>&1
sudo systemctl enable supervisor >> "$LOG_FILE" 2>&1

# Install useful utilities
log "Step 10: Installing utilities..."
sudo apt install -y \
    htop \
    tmux \
    vim \
    nano \
    tree \
    jq \
    fail2ban \
    ufw \
    >> "$LOG_FILE" 2>&1

# Configure firewall (UFW)
log "Step 11: Configuring firewall (UFW)..."

# Reset UFW to default
sudo ufw --force reset >> "$LOG_FILE" 2>&1

# Allow SSH
sudo ufw allow 22/tcp >> "$LOG_FILE" 2>&1

# Allow HTTP
sudo ufw allow 80/tcp >> "$LOG_FILE" 2>&1

# Allow HTTPS
sudo ufw allow 443/tcp >> "$LOG_FILE" 2>&1

# Allow Health Endpoint
sudo ufw allow 8080/tcp >> "$LOG_FILE" 2>&1

# Allow Odoo (restrict to local if needed)
sudo ufw allow 8069/tcp >> "$LOG_FILE" 2>&1

# Enable firewall
sudo ufw --force enable >> "$LOG_FILE" 2>&1

log "  ✓ Firewall configured and enabled"

# Install Fail2ban
log "Step 12: Configuring Fail2ban..."
sudo systemctl start fail2ban >> "$LOG_FILE" 2>&1
sudo systemctl enable fail2ban >> "$LOG_FILE" 2>&1
log "  ✓ Fail2ban started"

# Create ai-employee user if doesn't exist
log "Step 13: Creating ai-employee user..."
if ! id ai-employee &>/dev/null; then
    sudo adduser --system --shell /bin/bash ai-employee
    sudo usermod -aG sudo ai-employee
    log "  ✓ User 'ai-employee' created"
else
    log "  ✓ User 'ai-employee' already exists"
fi

# Create directories
log "Step 14: Creating required directories..."
sudo mkdir -p /opt/ai-employee
sudo mkdir -p /var/log/ai-employee
sudo mkdir -p /vault
sudo chown -R ai-employee:ai-employee /opt/ai-employee
sudo chown -R ai-employee:ai-employee /var/log/ai-employee
sudo chown ai-employee:ai-employee /vault
log "  ✓ Directories created"

# Display completion message
echo ""
echo "=== Dependency Installation Complete ==="
echo ""
echo "Installed Software:"
echo "  Python:    $PYTHON_VERSION"
echo "  Git:       $GIT_VERSION"
echo "  PostgreSQL: $PG_VERSION"
echo "  Nginx:     $NGINX_VERSION"
echo "  Certbot:   Installed"
echo "  Supervisor: Installed"
echo "  Fail2ban:  Installed"
echo ""
echo "Firewall Rules:"
sudo ufw status verbose
echo ""
echo "System Users:"
echo "  ai-employee: Created (system user)"
echo ""
echo "Directories:"
echo "  /opt/ai-employee  (application code)"
echo "  /var/log/ai-employee (logs)"
echo "  /vault             (vault files)"
echo ""
echo "Next Steps:"
echo "  1. Run: bash oracle-cloud-setup.sh (for cloud provisioning)"
echo "  2. Run: bash odoo-install.sh (for Odoo deployment)"
echo "  3. Run: bash nginx-ssl-setup.sh your-domain.com (for HTTPS)"
echo "  4. Run: bash setup-agent.sh (to deploy cloud agent)"
echo ""
echo "Installation log: $LOG_FILE"
echo ""
