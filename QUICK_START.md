# Quick Start Guide
## 🚀 Get AI Employee Running in 5 Minutes

**Version**: 4.0.0 (Platinum Tier)

---

## Option 1: Local Demo (5 Minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/ammarakk/Hakathon-0.git
cd Hakathon-0
```

### Step 2: Run Demo
```bash
bash phase-4/tests/platinum-demo/test-offline-email.sh
```

### Step 3: View Results
```bash
cat AI_Employee_Vault/Demo_*/demo-log.txt
```

**✅ Done! You've seen AI Employee in action!**

---

## Option 2: Full Setup (30 Minutes)

### Step 1: Install Dependencies
```bash
# Python
python3 -m venv venv
source venv/bin/activate
pip install flask pyyaml requests python-dotenv

# Node.js (for social media)
npm install @mcp/email @mcp/social-linkedin
```

### Step 2: Create Vault
```bash
mkdir -p ~/AI_Employee_Vault
mkdir -p ~/AI_Employee_Vault/{Needs_Action,In_Progress,Pending_Approval,Done,Updates}
```

### Step 3: Configure Environment
```bash
# Copy template
cp phase-4/local/config/local.env.example ~/AI_Employee_Vault/.env

# Edit with your credentials
nano ~/AI_Employee_Vault/.env
```

**Minimum Configuration**:
```bash
AGENT_ROLE=LOCAL
VAULT_PATH=~/AI_Employee_Vault

# Add at least one:
MCP_EMAIL_ENABLED=true
MCP_EMAIL_HOST=smtp.gmail.com
MCP_EMAIL_PORT=587
MCP_EMAIL_USER=your-email@gmail.com
MCP_EMAIL_PASSWORD=your-app-password
```

### Step 4: Test All Features
```bash
# Run all tests
bash phase-4/tests/platinum-demo/test-offline-email.sh
bash phase-4/tests/integration/test-domain-split.sh
bash phase-4/tests/integration/test-vault-sync.sh
bash phase-4/tests/security/test-secrets-isolation.sh
```

**✅ Done! AI Employee is ready to work!**

---

## Option 3: Cloud Deployment (2 Hours)

### Step 1: Create Oracle Cloud Account
1. Go to: https://www.oracle.com/cloud/free/
2. Sign up (free tier)
3. Create VM (4 ARM CPUs, 24GB RAM)

### Step 2: Connect to VM
```bash
ssh ubuntu@YOUR_VM_PUBLIC_IP
```

### Step 3: Run Setup
```bash
git clone https://github.com/ammarakk/Hakathon-0.git
sudo bash phase-4/cloud/provision/install-dependencies.sh
sudo bash phase-4/cloud/agent/setup-agent.sh
```

### Step 4: Start Services
```bash
sudo systemctl start ai-employee-health
sudo systemctl start ai-employee-orchestrator
sudo systemctl start ai-employee-sync
```

### Step 5: Verify
```bash
curl http://localhost:8080/health
```

**✅ Done! AI Employee running 24/7 on cloud!**

---

## What's Next?

### After Setup

1. **Configure Credentials** (15 min)
   - Gmail app password
   - Social media tokens
   - Odoo password (optional)

2. **Create First Task** (1 min)
   ```bash
   # Create email task
   cat > ~/AI_Employee_Vault/Needs_Action/email/test.md <<EOF
   # Test Email

   Send to: client@example.com
   Subject: Testing AI Employee

   This is a test email.
   EOF
   ```

3. **Monitor Dashboard** (ongoing)
   ```bash
   cat ~/AI_Employee_Vault/Dashboard.md
   ```

4. **Approve Tasks** (as needed)
   - Open `Pending_Approval/` files
   - Add `APPROVED` or `REJECTED`
   - Local agent executes

---

## Common Tasks

### Check System Status
```bash
# Local
ps aux | grep orchestrator

# Cloud
curl http://YOUR_VM_IP:8080/health
sudo systemctl status ai-employee-health
```

### View Logs
```bash
# Local
tail -f ~/ai-employee/agent.log

# Cloud
sudo journalctl -u ai-employee-health -f
```

### Sync Vault
```bash
# Local
bash ~/AI_Employee_Vault/sync-local.sh

# Cloud (automatic via systemd)
# Or manual:
cd /vault
bash /opt/ai-employee/phase-4/cloud/agent/sync-daemon.sh
```

### Run Tests
```bash
# All tests
for test in phase-4/tests/**/*.sh; do bash "$test"; done

# Individual tests
bash phase-4/tests/platinum-demo/test-offline-email.sh
```

---

## Credential Setup

### Gmail
```
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to: App passwords
4. Generate: Mail + Other
5. Copy password to .env
```

### LinkedIn
```
1. Go to: https://www.linkedin.com/developers/
2. Create new app
3. Copy Client ID & Secret
4. Generate access token
5. Add to .env
```

### Twitter/X
```
1. Go to: https://developer.twitter.com/
2. Create new app
3. Copy API keys & tokens
4. Add to .env
```

---

## Troubleshooting

### Problem: Import errors
```bash
# Solution
source venv/bin/activate
pip install --upgrade pip
pip install flask pyyaml requests python-dotenv
```

### Problem: Permission denied
```bash
# Solution
chmod +x phase-4/tests/**/*.sh
chmod +x phase-4/cloud/agent/*.sh
```

### Problem: Health server not responding
```bash
# Solution
sudo systemctl restart ai-employee-health
sudo journalctl -u ai-employee-health -n 50
```

---

## Need More Help?

- **Full Setup Guide**: See ENV_SETUP.md
- **Installation Guide**: See INSTALL.md
- **User Guide**: See USER_GUIDE.md
- **Documentation**: See README.md

---

## Summary

| Option | Time | Result |
|--------|------|--------|
| Local Demo | 5 min | See system in action |
| Full Setup | 30 min | Ready to use locally |
| Cloud Deploy | 2 hours | 24/7 operations |

---

**Ready? Choose your option and get started! 🚀**

*For detailed instructions, see ENV_SETUP.md*
