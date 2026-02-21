---
description: Cloud VM deployment guide for 24/7 AI Employee operation.
---

# COMMAND: Cloud Deployment (Oracle/AWS)

## CONTEXT

Deploy the AI Employee system on a cloud VM for:

- 24/7 operation
- Remote monitoring
- Domain specialization (cloud vs local)
- Health monitoring

## YOUR ROLE

Act as a DevOps engineer with expertise in:

- Cloud VM provisioning
- Service deployment
- Remote monitoring
- Security best practices

## IMPLEMENTATION

### 1. Oracle Cloud Free Tier Setup

```bash
# Create VM instance
# - Oracle Cloud Always Free: 2 AMD VMs, 24GB RAM each
# - Ubuntu 22.04 LTS recommended

# SSH into instance
ssh -i ~/.ssh/oci_key ubuntu@your-vm-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Clone repository
git clone https://github.com/your-repo/ai-employee.git
cd ai-employee

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# .env file (NEVER commit this)
cat > .env << EOF
# Vault path
VAULT_PATH=/home/ubuntu/ai-employee/vault

# Gmail credentials
GMAIL_CREDENTIALS=/home/ubuntu/ai-employee/credentials/gmail.json

# WhatsApp session
WHATSAPP_SESSION=/home/ubuntu/ai-employee/.whatsapp_session

# SMTP settings (for email sending)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Odoo settings
ODOO_URL=http://your-odoo-server:8069
ODOO_DB=odoo
ODOO_USER=admin
ODOO_PASSWORD=admin

# Social media tokens
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_ACCESS_TOKEN=your_token

# Twitter credentials
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_access_secret
EOF

# Secure the file
chmod 600 .env
```

### 3. Systemd Service Configuration

```ini
# /etc/systemd/system/ai-employee-gmail.service
[Unit]
Description=AI Employee Gmail Watcher
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-employee
Environment="PATH=/home/ubuntu/ai-employee/venv/bin"
EnvironmentFile=/home/ubuntu/ai-employee/.env
ExecStart=/home/ubuntu/ai-employee/venv/bin/python gmail_watcher.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/ai-employee/gmail.log
StandardError=append:/var/log/ai-employee/gmail.error.log

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/ai-employee
sudo chown ubuntu:ubuntu /var/log/ai-employee

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable ai-employee-gmail
sudo systemctl start ai-employee-gmail

# Check status
sudo systemctl status ai-employee-gmail
```

### 4. Domain Specialization

```python
# cloud_owner.py - Cloud-owned operations

CLOUD_OWNED_TASKS = {
    'watchers': [
        'gmail_watcher',
        'filesystem_watcher',
        'finance_watcher',
    ],
    'processing': [
        'reasoning_loop',
        'weekly_audit',
    ],
    'reporting': [
        'ceo_briefing',
        'audit_summary',
    ],
}

LOCAL_OWNED_TASKS = {
    'sensitive_actions': [
        'whatsapp_watcher',  # Requires local session
        'payment_approvals',  # Requires local confirmation
    ],
    'human_interaction': [
        'pending_approvals',
        'dashboard_updates',
    ],
}


def is_cloud_owned(task: str) -> bool:
    """Check if task should run on cloud."""
    for tasks in CLOUD_OWNED_TASKS.values():
        if task in tasks:
            return True
    return False


def is_local_owned(task: str) -> bool:
    """Check if task should run locally."""
    for tasks in LOCAL_OWNED_TASKS.values():
        if task in tasks:
            return True
    return False
```

### 5. Health Monitoring

```python
# health_check.py

import asyncio
import os
from pathlib import Path
from datetime import datetime


async def check_health():
    """Check system health."""
    checks = {
        'vault_exists': Path(os.getenv('VAULT_PATH')).exists(),
        'services_running': check_services(),
        'disk_space': check_disk_space(),
        'memory_usage': check_memory(),
    }

    return all(checks.values()), checks


def check_services():
    """Check if critical services are running."""
    import subprocess
    result = subprocess.run(
        ['systemctl', 'is-active', 'ai-employee-gmail'],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def check_disk_space():
    """Check available disk space."""
    import shutil
    usage = shutil.disk_usage('/')
    return usage.free > 1_000_000_000  # At least 1GB free


def check_memory():
    """Check memory usage."""
    import psutil
    return psutil.virtual_memory().percent < 80


# Expose health endpoint
from aiohttp import web

async def health_handler(request):
    """Health check endpoint."""
    healthy, checks = await check_health()
    status = 200 if healthy else 503
    return web.json_response({'healthy': healthy, 'checks': checks}, status=status)


app = web.Application()
app.router.add_get('/health', health_handler)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
```

### 6. Sync Configuration

```bash
# Install Syncthing for vault sync
sudo apt install -y syncthing

# Configure Syncthing
# - GUI: http://localhost:8384
# - Add folder: /home/ubuntu/ai-employee/vault
# - Share ID with local machine

# Or use Git for sync
cd /home/ubuntu/ai-employee
git config user.name "AI Employee Cloud"
git config user.email "cloud@ai-employee"
```

## ACCEPTANCE CRITERIA

- VM runs 24/7 with automatic restart
- Cloud watchers operate independently
- Local operations remain secure
- Health monitoring enabled
- Vault sync configured

## FOLLOW-UPS

- Set up automated backups
- Configure alerting for failures
- Create deployment scripts
- Add monitoring dashboard
