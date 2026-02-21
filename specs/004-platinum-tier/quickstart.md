# Phase 4 Quickstart Guide

**Phase**: 4 - Platinum Tier (Always-On Cloud + Local Executive)
**Last Updated**: 2026-02-21
**Estimated Setup Time**: 2-3 hours

---

## Prerequisites

### Required Accounts

1. **Oracle Cloud Account** (Free)
   - Sign up at: https://www.oracle.com/cloud/free/
   - Requires credit card (verification only, no charges for Always Free)

2. **GitHub or GitLab Account** (Free)
   - For vault Git repository hosting

3. **Domain Name** (Optional but recommended)
   - For Odoo HTTPS (e.g., `odoo.yourdomain.com`)
   - Can use Oracle Cloud free subdomain or IP address for testing

### Required Tools

**On Local Machine**:
- Python 3.10+
- Git 2.34+
- SSH client
- Claude Code with Agent Skills (Phases 1-3 installed)

**On Cloud VM** (installed by scripts):
- Ubuntu 22.04 LTS
- Python 3.10+
- Git 2.34+
- PostgreSQL 14
- Nginx 1.18+
- Odoo 16 Community

---

## Step 1: Cloud VM Provisioning (20 minutes)

### 1.1 Create Oracle Cloud VM

1. Log in to Oracle Cloud Console
2. Navigate to: **Compute → Instances → Create Instance**
3. Configure:
   - **Name**: `ai-employee-cloud`
   - **Shape**: `VM.Standard.E4.Flex` (Always Free)
     - OCPUs: 4 (Always Free limit)
     - Memory: 24 GB (Always Free limit)
   - **Image**: `Ubuntu 22.04 Minimal`
   - **SSH Key**: Upload your public SSH key
4. Create instance

### 1.2 Configure Networking

1. Go to: **Virtual Cloud Network → Security Lists**
2. Add Ingress Rules:
   ```
   Port 22   (SSH)        - Your IP
   Port 80   (HTTP)       - 0.0.0.0/0
   Port 443  (HTTPS)      - 0.0.0.0/0
   Port 8080 (Health)     - 0.0.0.0/0
   Port 8069 (Odoo)       - 0.0.0.0/0 (local only)
   ```

### 1.3 SSH into VM

```bash
ssh -i ~/.ssh/your_key ubuntu@<your-vm-public-ip>
```

---

## Step 2: Install Dependencies (15 minutes)

### 2.1 Run Setup Script

```bash
# Clone Phase 4 scripts
git clone <your-repo> /tmp/phase-4
cd /tmp/phase-4/cloud/provision

# Run dependency installation
sudo bash install-dependencies.sh
```

### 2.2 Manual Installation (if script fails)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install -y python3.10 python3-pip python3-venv

# Install Git
sudo apt install -y git

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Nginx
sudo apt install -y nginx

# Install certbot (for Let's Encrypt)
sudo apt install -y certbot python3-certbot-nginx

# Install fail2ban (security)
sudo apt install -y fail2ban
```

---

## Step 3: Deploy Odoo on Cloud (30 minutes)

### 3.1 Install Odoo

```bash
cd /tmp/phase-4/cloud/odoo
sudo bash odoo-install.sh
```

**Manual Installation** (if script fails):

```bash
# Create Odoo user
sudo useradd -m -d /opt/odoo -U -r -s /bin/bash odoo

# Install Python dependencies
sudo apt install -y python3-pip python3-dev python3-wheel \
    libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libpq-dev libjpeg-dev

# Clone Odoo 16
sudo -u odoo git clone --depth 1 --branch 16.0 https://github.com/odoo/odoo /opt/odoo/odoo

# Install Python requirements
sudo -u odoo pip3 install -r /opt/odoo/odoo/requirements.txt

# Create PostgreSQL database
sudo -u postgres createdb odoo

# Configure Odoo
sudo cp /opt/odoo/odoo/debian/odoo.conf /etc/odoo.conf
sudo chown odoo:odoo /etc/odoo.conf
```

### 3.2 Configure Nginx + HTTPS

```bash
sudo bash nginx-ssl-setup.sh your-domain.com
```

**Manual Configuration**:

```bash
# Configure Nginx reverse proxy
sudo tee /etc/nginx/sites-available/odoo <<EOF
server {
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Restart Nginx
sudo systemctl restart nginx
```

### 3.3 Setup Backups

```bash
# Add to crontab
crontab -e

# Add line (daily at 2 AM):
0 2 * * * /opt/phase-4/cloud/odoo/backup-script.sh
```

---

## Step 4: Setup Vault Sync (20 minutes)

### 4.1 Initialize Git Repository

**On Cloud VM**:

```bash
# Create vault directory
sudo mkdir -p /vault
sudo chown ubuntu:ubuntu /vault

# Initialize Git repo
cd /vault
git init
git config user.email "cloud@ai-employee"
git config user.name "Cloud Agent"

# Create .gitignore
cat > .gitignore <<'EOF'
.env
.env.*
*.session
*.token
*.cred
*.credentials
.claude/
node_modules/
__pycache__/
*.pyc
EOF
```

**On Local Machine**:

```bash
# Create vault directory (if not exists)
mkdir -p AI_Employee_Vault
cd AI_Employee_Vault

# Initialize Git repo
git init
git config user.email "local@ai-employee"
git config user.name "Local Agent"

# Create same .gitignore
cat > .gitignore <<'EOF'
.env
.env.*
*.session
*.token
*.cred
*.credentials
.claude/
node_modules/
__pycache__/
*.pyc
EOF
```

### 4.2 Create GitHub Repository

```bash
# On GitHub, create new repository: ai-employee-vault

# Add remote (on cloud)
cd /vault
git remote add origin git@github.com:your-username/ai-employee-vault.git

# Add remote (on local)
cd AI_Employee_Vault
git remote add origin git@github.com:your-username/ai-employee-vault.git
```

### 4.3 Setup SSH Keys

**On Cloud VM**:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "cloud@ai-employee" -f ~/.ssh/id_ed25519 -N ""

# Add to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy output to GitHub: Settings → SSH Keys → New SSH Key
```

**On Local Machine**:

```bash
# Use existing SSH key or generate new one
ssh-keygen -t ed25519 -C "local@ai-employee"
# Add to GitHub (same key or different)
```

### 4.4 Initial Commit

**On Cloud VM**:

```bash
cd /vault
git add .
git commit -m "Initial vault structure (cloud)"
git push -u origin main
```

---

## Step 5: Deploy Cloud Agent (25 minutes)

### 5.1 Setup Agent Code

```bash
# On cloud VM
cd /tmp/phase-4/cloud/agent
bash setup-agent.sh
```

**Manual Setup**:

```bash
# Create agent directory
sudo mkdir -p /opt/ai-employee
sudo chown ubuntu:ubuntu /opt/ai-employee

# Clone repository
cd /opt/ai-employee
git clone <your-repo> .

# Create Python venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5.2 Configure Cloud Environment

```bash
# Create .env file
cat > /opt/ai-employee/.env <<'EOF'
# Agent Configuration
AGENT_ROLE=CLOUD
AGENT_NAME=cloud
VAULT_PATH=/vault

# Watcher Configuration
WATCHER_INTERVAL=30
GMAIL_WATCHER_ENABLED=true
FILESYSTEM_WATCHER_ENABLED=true

# Odoo Configuration
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USER=admin
ODOO_PASSWORD=<change-me>

# Sync Configuration
SYNC_INTERVAL=30
GIT_REPO_PATH=/vault
GIT_BRANCH=main

# Health Server
HEALTH_PORT=8080
HEALTH_RATE_LIMIT=1

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai-employee/agent.log
EOF

# Secure .env
chmod 600 /opt/ai-employee/.env
```

### 5.3 Setup Systemd Services

```bash
# Copy service files
sudo cp /opt/ai-employee/cloud/agent/systemd-units/*.service /etc/systemd/system/

# Enable services
sudo systemctl enable ai-employee-orchestrator
sudo systemctl enable ai-employee-gmail-watcher
sudo systemctl enable ai-employee-filesystem-watcher
sudo systemctl enable ai-employee-health

# Start services
sudo systemctl start ai-employee-orchestrator
sudo systemctl start ai-employee-gmail-watcher
sudo systemctl start ai-employee-filesystem-watcher
sudo systemctl start ai-employee-health
```

### 5.4 Verify Deployment

```bash
# Check service status
sudo systemctl status ai-employee-*

# Check health endpoint
curl http://localhost:8080/health

# Expected output:
# {"status":"healthy","timestamp":"2026-02-21T10:30:00Z",...}
```

---

## Step 6: Setup Local Agent (20 minutes)

### 6.1 Install Dependencies

```bash
# On local machine (Windows/Mac/Linux)
cd phase-4/local/agent
bash setup-local.sh
```

**Manual Setup**:

```bash
# Create local directory
mkdir -p ~/ai-employee
cd ~/ai-employee

# Clone repository
git clone <your-repo> .

# Create Python venv
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### 6.2 Configure Local Environment

```bash
# Create .env file
cat > ~/ai-employee/.env <<'EOF'
# Agent Configuration
AGENT_ROLE=LOCAL
AGENT_NAME=local
VAULT_PATH=~/AI_Employee_Vault

# Watcher Configuration
WHATSAPP_WATCHER_ENABLED=true
FINANCE_WATCHER_ENABLED=true

# MCP Servers (with credentials)
MCP_EMAIL_ENABLED=true
MCP_ODOO_URL=https://your-domain.com
MCP_ODOO_DB=odoo
MCP_ODOO_USER=admin
MCP_ODOO_PASSWORD=<your-password>

# Social Media (optional)
MCP_SOCIAL_LINKEDIN_ENABLED=true
MCP_SOCIAL_FB_IG_ENABLED=true
MCP_SOCIAL_X_ENABLED=true

# Sync Configuration
SYNC_INTERVAL=30
GIT_REPO_PATH=~/AI_Employee_Vault
GIT_BRANCH=main

# Logging
LOG_LEVEL=INFO
LOG_FILE=~/ai-employee/agent.log
EOF

# Secure .env
chmod 600 ~/ai-employee/.env
```

### 6.3 Start Local Agent

```bash
# Activate venv
source ~/ai-employee/venv/bin/activate

# Run orchestrator
python ~/ai-employee/orchestrator.py
```

---

## Step 7: Verification (15 minutes)

### 7.1 Test Vault Sync

```bash
# On cloud: create test file
ssh ubuntu@<vm-ip> "echo 'test-from-cloud' > /vault/Needs_Action/test.md"

# On cloud: push
ssh ubuntu@<vm-ip> "cd /vault && git add . && git commit -m 'Test' && git push"

# On local: pull
cd ~/AI_Employee_Vault
git pull

# Verify file exists
cat Needs_Action/test.md
```

### 7.2 Test Health Monitoring

```bash
# Check health endpoint
curl https://your-vm-ip:8080/health

# Expected output:
# {"status":"healthy","active_watchers":["gmail_watcher","filesystem_watcher"],...}
```

### 7.3 Test Claim-by-Move

```bash
# Create test task
echo "# Test Task" > ~/AI_Employee_Vault/Needs_Action/test-claim.md

# Start local agent
python ~/ai-employee/orchestrator.py &

# Check if claimed
ls ~/AI_Employee_Vault/In_Progress/local/test-claim.md

# Expected: file moved from Needs_Action to In_Progress/local/
```

### 7.4 Test Secrets Isolation

```bash
# On cloud: scan for secrets
ssh ubuntu@<vm-ip> "find /vault -name '*.env' -o -name '*.token' -o -name '*.session'"

# Expected: No results (secrets not synced)
```

### 7.5 Run Platinum Demo

```bash
cd phase-4/tests/platinum-demo
bash test-offline-email.sh
```

---

## Troubleshooting

### Cloud VM Issues

**Problem**: Cannot SSH into VM
- **Solution**: Check security list rules in Oracle Cloud Console

**Problem**: Odoo not accessible
- **Solution**: Check Nginx status: `sudo systemctl status nginx`
- **Solution**: Check Odoo status: `sudo systemctl status odoo`

### Sync Issues

**Problem**: Git push fails
- **Solution**: Check SSH key: `ssh -T git@github.com`
- **Solution**: Pull first: `git pull origin main`

**Problem**: Sync conflicts
- **Solution**: Stop agents, resolve manually, restart

### Agent Issues

**Problem**: Service not starting
- **Solution**: Check logs: `sudo journalctl -u ai-employee-orchestrator`
- **Solution**: Check .env file permissions: `chmod 600 .env`

---

## Next Steps

1. **Monitor Health**: Check UptimeRobot dashboard for uptime
2. **Review Logs**: Check `/var/log/ai-employee/` on cloud
3. **Run Demo**: Execute platinum demo scenario
4. **Configure Watchers**: Set up Gmail API, webhook URLs
5. **Customize Skills**: Adjust Agent Skills for your business

---

## Summary

✅ Cloud VM provisioned (Oracle Always Free)
✅ Odoo deployed with HTTPS
✅ Vault sync configured (Git)
✅ Cloud agent running (systemd)
✅ Local agent configured
✅ Health monitoring active
✅ All tests passing

**Phase 4 Platinum Tier achieved!**

For detailed documentation, see:
- `cloud-deployment.md` - Full deployment guide
- `troubleshooting.md` - Common issues and solutions
- `migration-guide.md` - Phase 3 to Phase 4 migration
