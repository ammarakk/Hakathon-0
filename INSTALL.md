# AI Employee - Installation Guide
## 🚀 Complete Setup Instructions for Cloud & Local Deployment

**Version**: 4.0.0 (Platinum Tier)
**Estimated Setup Time**: 2-3 hours

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Local Setup (30 Minutes)](#local-setup-30-minutes)
4. [Cloud Deployment (2 Hours)](#cloud-deployment-2-hours)
5. [Post-Installation](#post-installation)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts

- **GitHub Account**: For vault synchronization
- **Oracle Cloud Account**: For cloud VM (Always Free tier)
- **Domain Name**: For Odoo HTTPS (optional but recommended)

### Local Machine Requirements

- **OS**: Linux, macOS, or Windows with WSL2
- **Python**: 3.10 or higher
- **Node.js**: v24 or higher
- **Git**: Latest version
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 10GB free space

### Cloud VM Requirements

- **Provider**: Oracle Cloud (Always Free)
- **Specs**: 4 ARM CPUs, 24GB RAM (free tier)
- **OS**: Ubuntu 22.04 LTS

---

## Quick Start (5 Minutes)

This gets you running locally with basic functionality.

### Step 1: Clone Repository

```bash
git clone https://github.com/yourcompany/ai-employee.git
cd ai-employee
```

### Step 2: Create Vault Structure

```bash
# Create vault directory
mkdir -p AI_Employee_Vault

# Create folder structure
cd AI_Employee_Vault
mkdir -p Needs_Action/{email,social,accounting,personal}
mkdir -p In_Progress/{cloud-agent,local-agent}
mkdir -p Pending_Approval/{email,social,accounting}
mkdir -p Done/{email,social,accounting}
mkdir -p Updates Plans Rejected Logs
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp phase-4/local/config/local.env.example AI_Employee_Vault/.env

# Edit configuration
nano AI_Employee_Vault/.env
```

**Minimum Required Configuration**:
```bash
# Required
AGENT_ROLE=LOCAL
VAULT_PATH=/path/to/AI_Employee_Vault

# At least one MCP server
MCP_EMAIL_ENABLED=true
MCP_EMAIL_HOST=smtp.gmail.com
MCP_EMAIL_PORT=587
MCP_EMAIL_USER=your-email@gmail.com
# MCP_EMAIL_PASSWORD=generate-app-password
```

### Step 4: Install Dependencies

```bash
# Python dependencies
pip install flask pyyaml requests python-dotenv

# Or use requirements file (if available)
pip install -r requirements.txt
```

### Step 5: Test Basic Functionality

```bash
# Run platinum demo test
bash phase-4/tests/platinum-demo/test-offline-email.sh
```

**Expected Output**:
```
=== Platinum Tier Demo - Offline Email Flow ===
...
✓ Platinum demo complete
```

---

## Local Setup (30 Minutes)

Complete local setup with all features.

### Step 1: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install flask==3.0.0
pip install pyyaml==6.0.1
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install psutil==5.9.5
pip install watchdog==3.0.0
```

### Step 2: Install Node.js Dependencies

```bash
# For social media integrations
npm install

# Or install individual packages
npm install @mcp/email
npm install @mcp/social-linkedin
npm install @mcp/social-fb-ig
npm install @mcp/social-x
```

### Step 3: Setup Local Agent

```bash
# Run setup script
bash phase-4/local/agent/setup-local.sh

# Follow prompts:
# - Agent directory: ~/ai-employee
# - Vault path: ~/AI_Employee_Vault
# - Configuration: Use existing .env
```

**Setup Creates**:
- Virtual environment at `~/ai-employee/venv`
- Configuration at `~/ai-employee/phase-4/local/config/local.env`
- Orchestrator at `~/ai-employee/phase-4/local/agent/orchestrator.py`
- Sync script at `~/AI_Employee_Vault/sync-local.sh`

### Step 4: Configure Credentials

Edit `~/AI_Employee_Vault/.env`:

```bash
# ===== Email Configuration =====
MCP_EMAIL_ENABLED=true
MCP_EMAIL_HOST=smtp.gmail.com
MCP_EMAIL_PORT=587
MCP_EMAIL_USER=your-email@gmail.com
MCP_EMAIL_PASSWORD=your-app-password  # Generate: https://myaccount.google.com/apppasswords

# ===== Odoo Configuration =====
MCP_ODOO_ENABLED=true
MCP_ODOO_URL=https://odoo.yourdomain.com
MCP_ODOO_DB=odoo
MCP_ODOO_USER=admin
MCP_ODOO_PASSWORD=your-odoo-password

# ===== LinkedIn Configuration =====
MCP_SOCIAL_LINKEDIN_ENABLED=true
# Get from: https://www.linkedin.com/developers/
LINKEDIN_CLIENT_ID=your-client-id
LINKEDIN_CLIENT_SECRET=your-client-secret
LINKEDIN_ACCESS_TOKEN=your-access-token

# ===== Twitter/X Configuration =====
MCP_SOCIAL_X_ENABLED=true
# Get from: https://developer.twitter.com/
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret

# ===== Facebook/Instagram Configuration =====
MCP_SOCIAL_FB_IG_ENABLED=true
# Get from: https://developers.facebook.com/
FACEBOOK_PAGE_ACCESS_TOKEN=your-page-access-token
INSTAGRAM_BUSINESS_ID=your-business-id

# ===== WhatsApp Configuration =====
WHATSAPP_SESSION_PATH=~/.whatsapp/session.data

# ===== Banking Configuration =====
# BANK_API_KEY=your-bank-api-key
```

### Step 5: Setup Vault Sync

```bash
# Make sync script executable
chmod +x ~/AI_Employee_Vault/sync-local.sh

# Test sync script
bash ~/AI_Employee_Vault/sync-local.sh
```

### Step 6: Start Local Agent

```bash
# Activate virtual environment
source ~/ai-employee/venv/bin/activate

# Start orchestrator
python3 ~/ai-employee/phase-4/local/agent/orchestrator.py
```

**Expected Output**:
```
Local Orchestrator starting (ROLE: LOCAL)
Vault: ~/AI_Employee_Vault
Allowed Actions: ['approve', 'send', 'post', 'whatsapp', 'banking', 'execute']

Processing Pending_Approval/...
[No pending approvals]
```

### Step 7: Setup Cron (Optional)

For automatic sync:

```bash
# Edit crontab
crontab -e

# Add this line (sync every 5 minutes)
*/5 * * * * ~/AI_Employee_Vault/sync-local.sh >> ~/vault-sync-local.log 2>&1
```

---

## Cloud Deployment (2 Hours)

Production deployment on Oracle Cloud.

### Step 1: Create Oracle Cloud Account

1. Go to https://www.oracle.com/cloud/free/
2. Sign up for Always Free tier
3. Verify email address
4. Add payment method (required for verification, not charged)

**Free Tier Includes**:
- 2 AMD VMs (with conditions)
- 4 ARM VMs (up to 24GB RAM) - **Recommended**
- 200GB storage
- 10TB data transfer

### Step 2: Create Cloud VM

1. Login to Oracle Cloud Console
2. Go to **Compute** → **Instances**
3. Click **Create Instance**
4. Configure:
   - **Name**: ai-employee-cloud
   - **Shape**: VM.Standard.A1.Flex (ARM)
   - **OCPU**: 4 (free tier limit)
   - **Memory**: 24GB (free tier limit)
   - **Image**: Ubuntu 22.04 Minimal
   - **SSH Key**: Upload your public key
5. Click **Create**

**Wait 5-10 minutes** for VM to be provisioned.

### Step 3: Connect to VM

```bash
# Get VM public IP from Oracle Cloud Console
# Connect via SSH
ssh -i ~/.ssh/your-key.pem ubuntu@YOUR_VM_PUBLIC_IP

# Or if using SSH config:
ssh ai-employee-cloud
```

### Step 4: Run Setup Script

```bash
# Clone repository on VM
git clone https://github.com/yourcompany/ai-employee.git
cd ai-employee

# Run installation
sudo bash phase-4/cloud/provision/install-dependencies.sh
```

**This Installs**:
- Python 3.13
- Node.js v24
- PostgreSQL 14
- Nginx
- Git
- System tools

### Step 5: Security Hardening

```bash
# Run security hardening
sudo bash phase-4/cloud/provision/security-hardening.sh
```

**This Configures**:
- UFW firewall (ports: 22, 80, 443, 8080, 8069)
- SSH hardening (key-only, no root)
- Fail2ban (SSH protection)
- Automatic security updates

### Step 6: Setup Cloud Agent

```bash
# Run cloud agent setup
sudo bash phase-4/cloud/agent/setup-agent.sh
```

**This Creates**:
- ai-employee user
- Virtual environment at /opt/ai-employee/venv
- Configuration at /opt/ai-employee/phase-4/cloud/config/cloud.env
- Systemd services

### Step 7: Configure Cloud Environment

```bash
# Edit cloud configuration
sudo nano /opt/ai-employee/phase-4/cloud/config/cloud.env
```

**Cloud Configuration** (NO credentials):
```bash
AGENT_ROLE=CLOUD
AGENT_NAME=cloud
VAULT_PATH=/vault

# Watchers
GMAIL_WATCHER_ENABLED=true
FILESYSTEM_WATCHER_ENABLED=true

# Allowed actions (NO send/post/pay)
ALLOWED_ACTIONS=triage,draft,schedule,monitor

# Odoo (draft only)
ODOO_URL=http://localhost:8069
ODOO_MODE=draft

# Health server
HEALTH_PORT=8080
HEALTH_RATE_LIMIT=1

# Security
SECRET_CHECK_ENABLED=true
BLOCK_MODIFIES_DASHBOARD_MD=true
```

### Step 8: Deploy Odoo (Optional)

If using Odoo for accounting:

```bash
# Run Odoo installation
sudo bash phase-4/cloud/odoo/odoo-install.sh

# Setup HTTPS (requires domain)
sudo bash phase-4/cloud/odoo/nginx-ssl-setup.sh yourdomain.com admin@yourdomain.com
```

**This Deploys**:
- Odoo 16 Community
- PostgreSQL database
- Nginx reverse proxy
- Let's Encrypt SSL certificate
- Automated backups (daily, 7-day retention)

### Step 9: Setup Vault Sync

```bash
# Create vault directory
sudo mkdir -p /vault
sudo chown ai-employee:ai-employee /vault

# Initialize Git repository
cd /vault
git init

# Add remote (your private GitHub repository)
git remote add origin https://github.com/yourusername/ai-employee-vault.git

# Pull initial content
git pull origin main
```

### Step 10: Start Services

```bash
# Start health server
sudo systemctl start ai-employee-health
sudo systemctl enable ai-employee-health

# Start orchestrator
sudo systemctl start ai-employee-orchestrator
sudo systemctl enable ai-employee-orchestrator

# Start sync daemon
sudo systemctl start ai-employee-sync
sudo systemctl enable ai-employee-sync

# Start watchers (optional)
sudo systemctl start ai-employee-gmail-watcher
sudo systemctl enable ai-employee-gmail-watcher

# Start Odoo (if installed)
sudo systemctl start odoo
sudo systemctl enable odoo
```

### Step 11: Verify Deployment

```bash
# Check health endpoint
curl http://localhost:8080/health

# Expected output:
{
  "status": "healthy",
  "timestamp": "2026-02-21T10:30:00",
  "active_watchers": ["gmail", "filesystem"],
  "uptime_seconds": 60,
  "memory_usage": "256MB"
}

# Check service status
sudo systemctl status ai-employee-health
sudo systemctl status ai-employee-orchestrator
sudo systemctl status ai-employee-sync

# Check logs
sudo journalctl -u ai-employee-health -f
```

### Step 12: Configure External Monitoring (Optional)

**Using UptimeRobot** (free):
1. Go to https://uptimerobot.com/
2. Sign up for free account
3. Add monitor:
   - **Type**: HTTPS
   - **URL**: http://YOUR_VM_IP:8080/health
   - **Interval**: 5 minutes
4. Configure alerts (email, Slack, etc.)

---

## Post-Installation

### Step 1: Update Dashboard

Edit `AI_Employee_Vault/Dashboard.md`:

```markdown
# AI Employee Dashboard

**System Status**: Online
**Cloud**: ✅ Operational
**Local**: ✅ Operational

## Components

| Component | Status | Uptime |
|-----------|--------|--------|
| Cloud Agent | ✅ Healthy | 99.9% |
| Local Agent | ✅ Healthy | 100% |
| Odoo | ✅ Running | 99.5% |
| Vault Sync | ✅ Synced | Active |

## Recent Activity

- [2026-02-21] System deployed
- [2026-02-21] All tests passing
- [2026-02-21] Cloud agent operational
```

### Step 2: Run Verification Tests

```bash
# On local machine
bash phase-4/tests/platinum-demo/test-offline-email.sh
bash phase-4/tests/integration/test-domain-split.sh
bash phase-4/tests/integration/test-vault-sync.sh
bash phase-4/tests/security/test-secrets-isolation.sh
```

### Step 3: Setup Backup (Odoo)

If using Odoo:

```bash
# Verify backup script
sudo cat /opt/ai-employee/phase-4/cloud/odoo/backup-script.sh

# Check cron job
sudo crontab -l | grep odoo

# Expected: Daily backup at 2 AM
0 2 * * * /opt/ai-employee/phase-4/cloud/odoo/backup-script.sh
```

### Step 4: Configure Domain (Optional)

For Odoo HTTPS:

```bash
# Update DNS
# Add A record: odoo.yourdomain.com → YOUR_VM_PUBLIC_IP

# Verify SSL
curl https://odoo.yourdomain.com
```

---

## Verification

### Health Checks

```bash
# Cloud health
curl http://YOUR_VM_IP:8080/health

# Odoo health
curl http://YOUR_VM_IP:8069
curl https://odoo.yourdomain.com

# Local agent
ps aux | grep orchestrator
```

### Log Checks

```bash
# Cloud logs
sudo journalctl -u ai-employee-health -n 50
sudo journalctl -u ai-employee-orchestrator -n 50
sudo journalctl -u ai-employee-sync -n 50

# Local logs
tail -f ~/ai-employee/agent.log
tail -f ~/vault-sync-local.log

# Odoo logs
sudo tail -f /var/log/odoo/odoo.log
```

### Sync Verification

```bash
# On cloud
cd /vault
git status
git log -1

# On local
cd ~/AI_Employee_Vault
git status
git log -1
```

---

## Troubleshooting

### Issue: Health Server Not Responding

**Solution**:
```bash
# Check service
sudo systemctl status ai-employee-health

# Restart service
sudo systemctl restart ai-employee-health

# Check logs
sudo journalctl -u ai-employee-health -n 100

# Verify port not in use
sudo netstat -tlnp | grep 8080
```

### Issue: Sync Daemon Failures

**Solution**:
```bash
# Check sync log
tail -f /var/log/ai-employee/sync.log

# Check Git conflicts
cd /vault
git status

# Resolve conflicts
git pull origin main
# Manual resolution
git add .
git commit -m "Resolved conflicts"
git push origin main
```

### Issue: Odoo Not Starting

**Solution**:
```bash
# Check Odoo status
sudo systemctl status odoo

# Check PostgreSQL
sudo systemctl status postgresql

# Check Odoo logs
sudo tail -f /var/log/odoo/odoo.log

# Run health check
sudo bash /opt/ai-employee/phase-4/cloud/odoo/health-check.sh
```

### Issue: Secrets Detected

**Solution**:
```bash
# Run security audit
bash /opt/ai-employee/phase-4/vault/security-audit.sh

# Find secret files
cd /vault
find . -name "*.env" -o -name "*.session"

# Remove from Git
git rm --cached path/to/secret
git commit -m "Remove secret"
```

---

## Next Steps

1. **Configure Credentials**: Add your API keys to `.env`
2. **Test Workflows**: Run demo scripts
3. **Monitor Logs**: Watch for 24-48 hours
4. **Scale**: Add more watchers as needed

---

## Support

- **Documentation**: See `docs/` directory
- **Issues**: https://github.com/yourcompany/ai-employee/issues
- **Email**: support@yourcompany.com

---

**Installation Complete! 🎉**

Your AI Employee is now ready to work 24/7 for your business.
