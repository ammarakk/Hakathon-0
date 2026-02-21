# AI Employee - Environment Setup Guide
## 🛠️ Complete Configuration for Cloud & Local Deployment

**Version**: 4.0.0 (Platinum Tier)
**Setup Time**: 30-45 minutes

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Environment Setup](#local-environment-setup)
3. [Cloud Environment Setup](#cloud-environment-setup)
4. [Vault Configuration](#vault-configuration)
5. [Credential Setup](#credential-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

**For Local Machine**:
- Python 3.10 or higher
- Node.js v24 or higher
- Git (latest version)
- Text editor (VS Code, Nano, etc.)
- SSH client (for cloud access)

**For Cloud VM**:
- Oracle Cloud account (Always Free tier)
- SSH key pair
- Domain name (optional but recommended)

### Accounts Needed

1. **GitHub Account**: For vault synchronization
2. **Oracle Cloud Account**: For cloud VM
3. **Gmail Account**: For email integration
4. **Social Media Accounts**:
   - LinkedIn (for business posting)
   - Twitter/X (for tweets)
   - Facebook/Instagram (for social posting)
5. **Odoo Account** (optional): For accounting integration

---

## Local Environment Setup

### Step 1: Create Project Directory

```bash
# Create main directory
mkdir -p ~/ai-employee
cd ~/ai-employee

# Clone repository (if not already done)
git clone https://github.com/ammarakk/Hakathon-0.git .
# OR if you have the code locally
cp -r /path/to/Hakathon-0/* ~/ai-employee/
```

### Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation
which python  # Should show: ~/ai-employee/venv/bin/python
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install flask==3.0.0
pip install pyyaml==6.0.1
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install psutil==5.9.5
pip install watchdog==3.0.0
pip install gunicorn==21.2.0

# Verify installation
pip list | grep -E "(flask|yaml|requests|dotenv)"
```

### Step 4: Install Node.js Dependencies

```bash
# Install MCP servers for social media
npm install @mcp/email
npm install @mcp/social-linkedin
npm install @mcp/social-fb-ig
npm install @mcp/social-x

# Or install all at once
npm install @mcp/email @mcp/social-linkedin @mcp/social-fb-ig @mcp/social-x

# Verify installation
npm list --depth=0
```

### Step 5: Create Environment File

```bash
# Copy environment template
cp phase-4/local/config/local.env.example ~/AI_Employee_Vault/.env

# Or create from scratch
cat > ~/AI_Employee_Vault/.env << 'EOF'
# AI Employee Local Environment Configuration
# Phase 4 - Platinum Tier

# ===== Agent Identity =====
AGENT_ROLE=LOCAL
AGENT_NAME=local
VAULT_PATH=~/AI_Employee_Vault

# ===== Allowed Actions =====
ALLOWED_ACTIONS=approve,send,post,whatsapp,banking,execute

# ===== Logging =====
LOG_LEVEL=INFO
LOG_FILE=~/ai-employee/agent.log

# ===== Sync Configuration =====
SYNC_INTERVAL=30
GIT_REPO_PATH=~/AI_Employee_Vault
GIT_BRANCH=main

# ===== Dashboard =====
DASHBOARD_MERGE_UPDATES=true
DASHBOARD_UPDATE_INTERVAL=60
EOF
```

---

## Cloud Environment Setup

### Step 1: Provision Oracle Cloud VM

1. **Login to Oracle Cloud Console**
   - Go to: https://console.oracle.com
   - Sign in to your account

2. **Create New Instance**
   - Navigate to: Compute → Instances
   - Click: "Create Instance"
   - Configure:
     ```
     Name: ai-employee-cloud
     Shape: VM.Standard.A1.Flex (ARM)
     OCPUs: 4
     Memory: 24 GB
     Image: Ubuntu 22.04 Minimal
     SSH Key: Upload your public key
     ```
   - Click: "Create"

3. **Wait for Provisioning** (5-10 minutes)

4. **Note Public IP Address** for next steps

### Step 2: Connect to Cloud VM

```bash
# From your local machine
ssh -i ~/.ssh/your-key.pem ubuntu@YOUR_VM_PUBLIC_IP

# Or add to SSH config
cat >> ~/.ssh/config << 'EOF'
Host ai-employee-cloud
    HostName YOUR_VM_PUBLIC_IP
    User ubuntu
    IdentityFile ~/.ssh/your-key.pem
EOF

# Connect easily
ssh ai-employee-cloud
```

### Step 3: Update and Upgrade System

```bash
# On cloud VM
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget vim nano htop
```

### Step 4: Clone Repository on Cloud

```bash
# Clone repository
cd ~
git clone https://github.com/ammarakk/Hakathon-0.git
cd Hakathon-0

# Verify files
ls -la phase-4/
```

### Step 5: Run Cloud Setup Script

```bash
# Run automated setup
sudo bash phase-4/cloud/provision/install-dependencies.sh

# This installs:
# - Python 3.13
# - Node.js v24
# - PostgreSQL 14
# - Nginx
# - Other dependencies
```

### Step 6: Create Cloud Environment File

```bash
# Copy template
sudo cp phase-4/cloud/config/cloud.env.example /opt/ai-employee/phase-4/cloud/config/cloud.env

# Edit configuration
sudo nano /opt/ai-employee/phase-4/cloud/config/cloud.env
```

**Cloud Environment Configuration**:
```bash
# Cloud Agent Configuration
AGENT_ROLE=CLOUD
AGENT_NAME=cloud
VAULT_PATH=/vault

# Watcher Configuration
WATCHER_INTERVAL=30
GMAIL_WATCHER_ENABLED=true
FILESYSTEM_WATCHER_ENABLED=true

# Allowed Actions (NO send/post/pay)
ALLOWED_ACTIONS=triage,draft,schedule,monitor

# Odoo Configuration (Cloud - draft only)
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USER=admin
ODOO_MODE=draft

# Health Server
HEALTH_PORT=8080
HEALTH_RATE_LIMIT=1

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai-employee/agent.log

# Security
SECRET_CHECK_ENABLED=true
BLOCK_MODIFIES_DASHBOARD_MD=true
```

### Step 7: Setup Vault Directory on Cloud

```bash
# Create vault directory
sudo mkdir -p /vault
sudo chown ai-employee:ai-employee /vault

# Initialize Git repository
cd /vault
git init
git config user.name "AI Employee Cloud"
git config user.email "cloud@ai-employee"

# Add remote (your private GitHub repository)
git remote add origin https://github.com/ammarakk/ai-employee-vault.git
```

### Step 8: Start Cloud Services

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

# Verify services
sudo systemctl status ai-employee-health
sudo systemctl status ai-employee-orchestrator
sudo systemctl status ai-employee-sync
```

---

## Vault Configuration

### Step 1: Initialize Local Vault

```bash
# On local machine
cd ~/AI_Employee_Vault

# Initialize Git repository
git init
git config user.name "AI Employee Local"
git config user.email "local@ai-employee"

# Create .gitignore
cat > .gitignore << 'EOF'
# Obsidian cache
.obsidian/
.obsidian.vimrc

# Python cache
__pycache__/
*.pyc
*.pyo

# Secrets - NEVER COMMIT
.env
*.env
secrets/
creds/
tokens/
WhatsApp/
banking/
*.session
*.token
*.key
*.pem
*.cert
*.cred

# Node modules
node_modules/

# Logs
*.log

# Temporary files
*.tmp
*.bak
.DS_Store
Thumbs.db

# Git
.git/
EOF

# Add and commit .gitignore
git add .gitignore
git commit -m "Add .gitignore to protect secrets"
```

### Step 2: Create Vault Folder Structure

```bash
# Create all required folders
cd ~/AI_Employee_Vault

mkdir -p Needs_Action/{email,social,accounting,personal,business}
mkdir -p In_Progress/{cloud-agent,local-agent}
mkdir -p Pending_Approval/{email,social,accounting}
mkdir -p Done/{email,social,accounting}
mkdir -p Updates
mkdir -p Plans
mkdir -p Rejected
mkdir -p Logs
mkdir -p Errors/{sync,processing}
```

### Step 3: Create Dashboard

```bash
# Create main dashboard
cat > ~/AI_Employee_Vault/Dashboard.md << 'EOF'
# AI Employee Dashboard

**System Status**: Online
**Last Updated**: $(date '+%Y-%m-%d %H:%M:%S')

---

## System Components

| Component | Status | Uptime |
|-----------|--------|--------|
| Cloud Agent | ✅ Healthy | - |
| Local Agent | ✅ Online | - |
| Vault Sync | ✅ Active | - |
| Odoo | ⚠️ Not configured | - |

---

## Recent Activity

- [$(date '+%Y-%m-%d')] System initialized
- [$(date '+%Y-%m-%d')] Environment configured
- [$(date '+%Y-%m-%d')] Ready for operations

---

## Tasks

### In Progress
- None

### Pending Approval
- None

### Completed Today
- System setup completed

---

## Updates

No recent updates from cloud agent.
EOF
```

### Step 4: Setup GitHub Repository for Vault

```bash
# On local machine
cd ~/AI_Employee_Vault

# Create GitHub repository (private)
# Go to: https://github.com/new
# Repository name: ai-employee-vault
# Make it PRIVATE
# Don't initialize with README

# Add remote
git remote add origin https://github.com/ammarakk/ai-employee-vault.git

# Push initial content
git add -A
git commit -m "Initial vault structure"
git push -u origin main
```

### Step 5: Setup Sync Scripts

**Local Sync Script** (already created):
```bash
# Make executable
chmod +x ~/AI_Employee_Vault/sync-local.sh

# Test sync
bash ~/AI_Employee_Vault/sync-local.sh
```

**Cloud Sync Script** (on cloud VM):
```bash
# On cloud VM
sudo chmod +x /opt/ai-employee/phase-4/cloud/agent/sync-daemon.sh

# Test sync
cd /vault
bash /opt/ai-employee/phase-4/cloud/agent/sync-daemon.sh
```

---

## Credential Setup

### Email Configuration (Gmail)

```bash
# Edit local environment
nano ~/AI_Employee_Vault/.env
```

**Add Email Configuration**:
```bash
# ===== Email MCP Configuration =====
MCP_EMAIL_ENABLED=true
MCP_EMAIL_HOST=smtp.gmail.com
MCP_EMAIL_PORT=587
MCP_EMAIL_USER=your-email@gmail.com
# Generate app password: https://myaccount.google.com/apppasswords
MCP_EMAIL_PASSWORD=your-app-password-here
```

**Generate Gmail App Password**:
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification (if not enabled)
3. Go to: App passwords
4. Select: Mail + Select app: Other
5. Generate: Copy password

### LinkedIn Configuration

```bash
# Add to .env
nano ~/AI_Employee_Vault/.env
```

**LinkedIn Configuration**:
```bash
# ===== LinkedIn Configuration =====
MCP_SOCIAL_LINKEDIN_ENABLED=true

# Get from: https://www.linkedin.com/developers/
LINKEDIN_CLIENT_ID=your-client-id
LINKEDIN_CLIENT_SECRET=your-client-secret
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
LINKEDIN_ACCESS_TOKEN=your-access-token
```

**Get LinkedIn Credentials**:
1. Go to: https://www.linkedin.com/developers/
2. Create new app
3. Copy Client ID and Secret
4. Generate access token

### Twitter/X Configuration

```bash
# Add to .env
nano ~/AI_Employee_Vault/.env
```

**Twitter/X Configuration**:
```bash
# ===== Twitter/X Configuration =====
MCP_SOCIAL_X_ENABLED=true

# Get from: https://developer.twitter.com/
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret
TWITTER_BEARER_TOKEN=your-bearer-token
```

**Get Twitter/X Credentials**:
1. Go to: https://developer.twitter.com/
2. Create new app
3. Copy API keys and tokens

### Facebook/Instagram Configuration

```bash
# Add to .env
nano ~/AI_Employee_Vault/.env
```

**Facebook/Instagram Configuration**:
```bash
# ===== Facebook/Instagram Configuration =====
MCP_SOCIAL_FB_IG_ENABLED=true

# Get from: https://developers.facebook.com/
FACEBOOK_PAGE_ID=your-page-id
FACEBOOK_PAGE_ACCESS_TOKEN=your-page-access-token
INSTAGRAM_BUSINESS_ID=your-instagram-business-id
```

**Get Facebook Credentials**:
1. Go to: https://developers.facebook.com/
2. Create new app
3. Add Facebook Login
4. Generate page access token

### Odoo Configuration (Optional)

```bash
# Add to .env
nano ~/AI_Employee_Vault/.env
```

**Odoo Configuration**:
```bash
# ===== Odoo Configuration =====
MCP_ODOO_ENABLED=true
MCP_ODOO_URL=https://odoo.yourdomain.com
MCP_ODOO_DB=odoo
MCP_ODOO_USER=admin
# Generate strong password
MCP_ODOO_PASSWORD=your-strong-odoo-password
MCP_ODOO_MODE=post
```

### WhatsApp Configuration (Optional)

```bash
# Add to .env
nano ~/AI_Employee_Vault/.env
```

**WhatsApp Configuration**:
```bash
# ===== WhatsApp Configuration =====
WHATSAPP_ENABLED=true
# WhatsApp session file (local only, never sync)
WHATSAPP_SESSION_PATH=~/.whatsapp/session.data
WHATSAPP_QR_CODE_PATH=~/.whatsapp/qr.png
```

### Banking Configuration (Optional)

```bash
# Add to .env (NEVER commit to Git)
nano ~/AI_Employee_Vault/.env
```

**Banking Configuration**:
```bash
# ===== Banking Configuration =====
# WARNING: Never commit these to Git!
# BANK_API_KEY=your-bank-api-key
# BANK_ACCOUNT_ID=your-account-id
# BANK_ROUTING_NUMBER=your-routing-number
```

---

## Verification

### Step 1: Test Local Environment

```bash
# Activate virtual environment
source ~/ai-employee/venv/bin/activate

# Test Python
python --version
# Should show: Python 3.10+

# Test imports
python -c "import flask, yaml, requests, dotenv"
# No errors = success

# Test environment
python -c "from dotenv import load_dotenv; load_dotenv('~/AI_Employee_Vault/.env'); import os; print('AGENT_ROLE:', os.getenv('AGENT_ROLE'))"
# Should print: AGENT_ROLE: LOCAL
```

### Step 2: Test Cloud Environment

```bash
# SSH into cloud
ssh ai-employee-cloud

# Test health endpoint
curl http://localhost:8080/health

# Expected output:
{
  "status": "healthy",
  "timestamp": "2026-02-21T10:30:00",
  "active_watchers": [],
  "uptime_seconds": 60,
  "memory_usage": "256MB"
}
```

### Step 3: Test Vault Sync

**On Local**:
```bash
cd ~/AI_Employee_Vault
echo "Test update $(date)" >> Updates/test.txt
git add Updates/test.txt
git commit -m "Test sync"
git push origin main
```

**On Cloud**:
```bash
cd /vault
git pull origin main
cat Updates/test.txt
# Should show: Test update [timestamp]
```

### Step 4: Run Test Suite

```bash
# On local machine
cd ~/ai-employee

# Run platinum demo
bash phase-4/tests/platinum-demo/test-offline-email.sh

# Run domain split test
bash phase-4/tests/integration/test-domain-split.sh

# Run vault sync test
bash phase-4/tests/integration/test-vault-sync.sh

# Run security test
bash phase-4/tests/security/test-secrets-isolation.sh
```

### Step 5: Verify All Components

**Checklist**:
```bash
# Local environment
✅ Python 3.10+ installed
✅ Virtual environment active
✅ All dependencies installed
✅ .env file configured
✅ Vault folder structure created
✅ Dashboard.md exists
✅ sync-local.sh executable

# Cloud environment
✅ Oracle Cloud VM running
✅ Health server responding
✅ Cloud agent configured
✅ Vault directory ready
✅ Services running
✅ Sync daemon active

# Integration
✅ Git sync working
✅ Credentials configured
✅ Test suite passing
✅ Dashboard updating
```

---

## Troubleshooting

### Issue: Python Version Too Old

**Problem**:
```bash
python --version
# Shows: Python 3.8 or older
```

**Solution**:
```bash
# Install Python 3.13
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv
```

### Issue: Virtual Environment Not Activating

**Problem**:
```bash
source venv/bin/activate
# Error: bash: venv/bin/activate: No such file or directory
```

**Solution**:
```bash
# Re-create virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Issue: Module Import Errors

**Problem**:
```bash
python -c "import flask"
# Error: ModuleNotFoundError: No module named 'flask'
```

**Solution**:
```bash
# Ensure venv is activated
source venv/bin/activate

# Re-install dependencies
pip install --upgrade pip
pip install flask pyyaml requests python-dotenv
```

### Issue: Cloud Health Server Not Responding

**Problem**:
```bash
curl http://localhost:8080/health
# Error: Connection refused
```

**Solution**:
```bash
# Check service status
sudo systemctl status ai-employee-health

# Start service
sudo systemctl start ai-employee-health

# Check logs
sudo journalctl -u ai-employee-health -n 50

# Restart service
sudo systemctl restart ai-employee-health
```

### Issue: Git Sync Failing

**Problem**:
```bash
git push origin main
# Error: Permission denied or authentication failed
```

**Solution**:
```bash
# Setup SSH keys
ssh-keygen -t ed25519 -C "your-email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/ssh/new

# Test connection
ssh -T git@github.com
```

### Issue: Environment Variables Not Loading

**Problem**:
```bash
python -c "from dotenv import load_dotenv; load_dotenv('.env'); import os; print(os.getenv('AGENT_ROLE'))"
# Prints: None
```

**Solution**:
```bash
# Check .env file exists
ls -la ~/AI_Employee_Vault/.env

# Check file permissions
chmod 600 ~/AI_Employee_Vault/.env

# Verify file format
cat ~/AI_Employee_Vault/.env | head -5

# Should show: AGENT_ROLE=LOCAL
```

### Issue: Port Already in Use

**Problem**:
```bash
# Starting health server fails
# Error: Port 8080 already in use
```

**Solution**:
```bash
# Find process using port
sudo lsof -i :8080

# Kill process
sudo kill -9 PID

# OR use different port
# Edit cloud.env
HEALTH_PORT=8081
```

---

## Next Steps

After environment setup is complete:

1. **Configure Credentials** (15 minutes)
   - Add Gmail app password
   - Setup social media tokens
   - Configure Odoo (if using)

2. **Run Test Suite** (10 minutes)
   - Verify all tests pass
   - Check health endpoints
   - Test vault sync

3. **Deploy to Cloud** (2 hours)
   - Follow INSTALL.md guide
   - Setup Oracle Cloud VM
   - Start all services

4. **Start Operations** (5 minutes)
   - Create first task
   - Test workflow
   - Monitor dashboard

---

## Summary

**Setup Complete When**:
- ✅ Local environment configured
- ✅ Cloud VM running
- ✅ All dependencies installed
- ✅ Credentials configured
- ✅ Vault sync working
- ✅ All tests passing
- ✅ Health endpoints responding

**Time Investment**: 30-45 minutes

**Maintenance**: 15 minutes/day (approvals + monitoring)

---

**Need Help?**
- Documentation: See README.md, INSTALL.md
- Issues: https://github.com/ammarakk/Hakathon-0/issues
- Support: support@yourcompany.com

---

**Environment Setup Complete! 🎉**

*Your AI Employee is ready to work!*
