#!/bin/bash
# Odoo 16 Community Installation Script for Phase 4 - Platinum Tier
# Purpose: Deploy Odoo on Cloud VM with PostgreSQL, Nginx, and HTTPS
# Platform: Ubuntu 22.04 LTS
# Odoo Version: 16.0
# PostgreSQL Version: 14

set -e

echo "=== Odoo 16 Installation - Phase 4 Platinum Tier ==="
echo ""

# Configuration
ODOO_USER="odoo"
ODOO_INSTALL_DIR="/opt/odoo"
ODOO_VERSION="16.0"
ODOO_DB_NAME="odoo"
ODOO_DB_USER="odoo"
ODOO_DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
ODOO_ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
LOG_FILE="/var/log/odoo-install.log"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $*"
    exit 1
}

# System update
log "Step 1: Updating system packages..."
sudo apt update >> "$LOG_FILE" 2>&1
sudo apt upgrade -y >> "$LOG_FILE" 2>&1

# Install Python dependencies
log "Step 2: Installing Python dependencies..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libtiff5-dev \
    libjpeg8-dev \
    libopenjp2-7-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    libpq-dev \
    >> "$LOG_FILE" 2>&1

# Install PostgreSQL
log "Step 3: Installing PostgreSQL 14..."
sudo apt install -y postgresql postgresql-contrib >> "$LOG_FILE" 2>&1

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create Odoo database user
log "Step 4: Creating PostgreSQL user and database..."
sudo -u postgres createuser -s $ODOO_DB_USER >> "$LOG_FILE" 2>&1
sudo -u postgres psql -c "ALTER USER $ODOO_DB_USER WITH PASSWORD '$ODOO_DB_PASSWORD';" >> "$LOG_FILE" 2>&1
sudo -u postgres createdb $ODOO_DB_NAME -O $ODOO_DB_USER >> "$LOG_FILE" 2>&1

# Create Odoo user
log "Step 5: Creating Odoo system user..."
if ! id "$ODOO_USER" &>/dev/null; then
    sudo adduser --system --quiet --shell=/bin/bash --home=$ODOO_INSTALL_DIR --gecos 'Odoo' $ODOO_USER
    sudo mkdir -p $ODOO_INSTALL_DIR
    sudo chown $ODOO_USER:$ODOO_USER $ODOO_INSTALL_DIR
fi

# Install Python 3 venv
log "Step 6: Setting up Python virtual environment..."
sudo -u $ODOO_USER python3 -m venv $ODOO_INSTALL_DIR/venv >> "$LOG_FILE" 2>&1

# Clone Odoo from GitHub
log "Step 7: Cloning Odoo $ODOO_VERSION..."
if [ ! -d "$ODOO_INSTALL_DIR/odoo" ]; then
    sudo -u $ODOO_USER git clone --depth 1 --branch $ODOO_VERSION https://github.com/odoo/odoo $ODOO_INSTALL_DIR/odoo >> "$LOG_FILE" 2>&1
fi

# Install Python requirements
log "Step 8: Installing Odoo Python requirements..."
sudo -u $ODOO_USER $ODOO_INSTALL_DIR/venv/bin/pip install -r $ODOO_INSTALL_DIR/odoo/requirements.txt >> "$LOG_FILE" 2>&1

# Create Odoo configuration file
log "Step 9: Creating Odoo configuration..."
sudo tee /etc/odoo.conf > /dev/null <<EOF
[options]
admin_passwd = $ODOO_ADMIN_PASSWORD
db_host = localhost
db_port = 5432
db_user = $ODOO_DB_USER
db_password = $ODOO_DB_PASSWORD
dbfilter = ^$ODOO_DB_NAME$
addons_path = $ODOO_INSTALL_DIR/odoo/addons
data_dir = /var/lib/odoo
logfile = /var/log/odoo/odoo.log
log_level = info
http_port = 8069
proxymode = True
EOF

sudo chown $ODOO_USER:$ODOO_USER /etc/odoo.conf
sudo chmod 640 /etc/odoo.conf

# Create data directory
log "Step 10: Creating Odoo data directory..."
sudo mkdir -p /var/lib/odoo
sudo chown $ODOO_USER:$ODOO_USER /var/lib/odoo

# Create log directory
sudo mkdir -p /var/log/odoo
sudo chown $ODOO_USER:$ODOO_USER /var/log/odoo

# Create systemd service
log "Step 11: Creating systemd service for Odoo..."
sudo tee /etc/systemd/system/odoo.service > /dev/null <<EOF
[Unit]
Description=Odoo 16 Open Source ERP
Documentation=https://github.com/odoo/odoo
After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo
User=odoo
Group=odoo
WorkingDirectory=$ODOO_INSTALL_DIR/odoo
Environment="PATH=$ODOO_INSTALL_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$ODOO_INSTALL_DIR/venv/bin/python $ODOO_INSTALL_DIR/odoo/odoo-bin -c /etc/odoo.conf
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Save credentials for reference
log "Step 12: Saving credentials..."
sudo tee /opt/odoo-credentials.txt > /dev/null <<EOF
Odoo Installation Credentials - $(date)
========================================
Database: $ODOO_DB_NAME
Database User: $ODOO_DB_USER
Database Password: $ODOO_DB_PASSWORD
Admin Password: $ODOO_ADMIN_PASSWORD
========================================
IMPORTANT: Save these credentials securely!
EOF
sudo chmod 600 /opt/odoo-credentials.txt

# Reload systemd and start Odoo
log "Step 13: Starting Odoo service..."
sudo systemctl daemon-reload >> "$LOG_FILE" 2>&1
sudo systemctl enable odoo >> "$LOG_FILE" 2>&1
sudo systemctl start odoo >> "$LOG_FILE" 2>&1

# Wait for Odoo to start
log "Waiting for Odoo to start..."
sleep 10

# Check if Odoo is running
if systemctl is-active --quiet odoo; then
    log "✓ Odoo service started successfully"
else
    error_exit "Odoo service failed to start. Check logs: journalctl -u odoo"
fi

# Test Odoo connection
log "Testing Odoo connection on port 8069..."
if curl -s http://localhost:8069 > /dev/null; then
    log "✓ Odoo is responding on http://localhost:8069"
else
    log "Warning: Odoo not responding yet. Check logs: tail -f /var/log/odoo/odoo.log"
fi

# Display completion message
echo ""
echo "=== Odoo 16 Installation Complete ==="
echo ""
echo "Odoo URL: http://localhost:8069"
echo "Database: $ODOO_DB_NAME"
echo "Database User: $ODOO_DB_USER"
echo ""
echo "IMPORTANT: Save these credentials:"
echo "  Database Password: $ODOO_DB_PASSWORD"
echo "  Admin Password: $ODOO_ADMIN_PASSWORD"
echo ""
echo "Credentials saved to: /opt/odoo-credentials.txt"
echo ""
echo "Next Steps:"
echo "  1. Access Odoo: http://localhost:8069"
echo "  2. Create database with admin user"
echo "  3. Install required modules"
echo "  4. Run: bash nginx-ssl-setup.sh to enable HTTPS"
echo ""
echo "Logs:"
echo "  Installation: $LOG_FILE"
echo "  Odoo: tail -f /var/log/odoo/odoo.log"
echo "  Service: journalctl -u odoo -f"
echo ""
