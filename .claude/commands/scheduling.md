---
description: Scheduling watchers and agents using cron and Task Scheduler for always-on operation.
---

# COMMAND: Scheduling Watchers and Agents

## CONTEXT

The user needs to set up scheduling for watchers and agents to run:

- Continuously in the background
- At specific intervals (hourly, daily, etc.)
- Using cron (Linux/Mac) or Task Scheduler (Windows)
- With automatic restart on failure

## YOUR ROLE

Act as a DevOps engineer with expertise in:

- Cron job configuration
- Windows Task Scheduler setup
- Process monitoring and logging
- Service configuration

## Step 1: Cron Scheduling (Linux/Mac)

### Cron Configuration

```bash
# Edit crontab
crontab -e

# Add watcher jobs
# Gmail Watcher - Check every 5 minutes
*/5 * * * * cd /path/to/ai-employee && /usr/bin/python3 gmail_watcher.py >> /var/log/ai-employee/gmail.log 2>&1

# WhatsApp Watcher - Check every 10 minutes
*/10 * * * * cd /path/to/ai-employee && /usr/bin/python3 whatsapp_watcher.py >> /var/log/ai-employee/whatsapp.log 2>&1

# File System Watcher - Check every 2 minutes
*/2 * * * * cd /path/to/ai-employee && /usr/bin/python3 filesystem_watcher.py >> /var/log/ai-employee/filesystem.log 2>&1

# Finance Watcher - Check every hour
0 * * * * cd /path/to/ai-employee && /usr/bin/python3 finance_watcher.py >> /var/log/ai-employee/finance.log 2>&1

# Reasoning Loop - Check every minute
* * * * * cd /path/to/ai-employee && /usr/bin/python3 reasoning_loop.py >> /var/log/ai-employee/reasoning.log 2>&1

# Weekly Audit - Every Sunday at 9 AM
0 9 * * 0 cd /path/to/ai-employee && /usr/bin/python3 weekly_audit.py >> /var/log/ai-employee/audit.log 2>&1
```

### Cron Wrapper Script

```bash
#!/bin/bash
# run_watcher.sh - Wrapper to handle watcher execution

WATCHER_NAME=$1
VAULT_PATH="${VAULT_PATH:-/path/to/vault}"
LOG_DIR="/var/log/ai-employee"
PID_FILE="/var/run/ai-employee/${WATCHER_NAME}.pid"

# Create directories
mkdir -p "$LOG_DIR"
mkdir -p "/var/run/ai-employee"

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "[$WATCHER_NAME] Already running (PID: $OLD_PID)"
        exit 1
    else
        echo "[$WATCHER_NAME] Removing stale PID file"
        rm -f "$PID_FILE"
    fi
fi

# Start watcher
echo "[$WATCHER_NAME] Starting at $(date)"
cd /path/to/ai-employee

# Run in background
nohup python3 "${WATCHER_NAME}.py" \
    >> "${LOG_DIR}/${WATCHER_NAME}.log" 2>&1 &

PID=$!
echo $PID > "$PID_FILE"

echo "[$WATCHER_NAME] Started with PID: $PID"
```

### Systemd Service (Alternative to Cron)

```ini
# /etc/systemd/system/ai-employee-gmail.service
[Unit]
Description=AI Employee Gmail Watcher
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/ai-employee
Environment="VAULT_PATH=/path/to/vault"
Environment="GMAIL_CREDENTIALS=/path/to/credentials.json"
ExecStart=/usr/bin/python3 gmail_watcher.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/ai-employee/gmail.log
StandardError=append:/var/log/ai-employee/gmail.error.log

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable ai-employee-gmail
sudo systemctl start ai-employee-gmail

# Check status
sudo systemctl status ai-employee-gmail

# View logs
sudo journalctl -u ai-employee-gmail -f
```

## Step 2: Task Scheduler (Windows)

### PowerShell Wrapper Script

```powershell
# run_watcher.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$WatcherName,

    [string]$VaultPath = "C:\path\to\vault"
)

$LogDir = "C:\logs\ai-employee"
$PidFile = "C:\temp\ai-employee\${WatcherName}.pid"

# Create directories
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $PidFile) | Out-Null

# Check if already running
if (Test-Path $PidFile) {
    $oldPid = Get-Content $PidFile
    $process = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
    if ($process) {
        Write-Output "[$WatcherName] Already running (PID: $oldPid)"
        exit 1
    } else {
        Write-Output "[$WatcherName] Removing stale PID file"
        Remove-Item $PidFile
    }
}

# Start watcher
Write-Output "[$WatcherName] Starting at $(Get-Date)"
Set-Location "C:\path\to\ai-employee"

$env:VAULT_PATH = $VaultPath

$process = Start-Process -FilePath "python" `
    -ArgumentList "$WatcherName.py" `
    -WindowStyle Hidden `
    -RedirectStandardOutput "$LogDir\$WatcherName.log" `
    -RedirectStandardError "$LogDir\$WatcherName.error.log" `
    -PassThru

$process.Id | Out-File $PidFile
Write-Output "[$WatcherName] Started with PID: $($process.Id)"
```

### Task Scheduler Setup

```powershell
# setup_tasks.ps1 - Create scheduled tasks
$TaskAction = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File C:\path\to\ai-employee\run_watcher.ps1 -WatcherName gmail_watcher"

$TaskTrigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 5) `
    -RepetitionDuration ([TimeSpan]::MaxValue)

$TaskSettings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask `
    -TaskName "AI Employee - Gmail Watcher" `
    -Action $TaskAction `
    -Trigger $TaskTrigger `
    -Settings $TaskSettings `
    -User "YourUser" `
    -RunLevel Highest
```

### Manual Task Scheduler Setup

1. Open Task Scheduler (`taskschd.msc`)
2. Create Basic Task
3. Name: "AI Employee - Gmail Watcher"
4. Trigger: Daily, repeat every 5 minutes
5. Action: Start a program
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File C:\path\to\run_watcher.ps1 -WatcherName gmail_watcher`
6. Conditions:
   - ✅ Start only if computer is on AC power
   - ✅ Wake the computer to run this task
7. Settings:
   - ✅ Allow task to be run on demand
   - ✅ Run task as soon as possible after a scheduled start is missed
   - ✅ If the task fails, restart every 1 minute, up to 3 times

## Step 3: Supervisor Configuration (Cross-Platform)

```ini
# /etc/supervisor/conf.d/ai-employee.conf
[program:gmail_watcher]
command=/usr/bin/python3 /path/to/ai-employee/gmail_watcher.py
directory=/path/to/ai-employee
user=your-user
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/ai-employee/gmail.err.log
stdout_logfile=/var/log/ai-employee/gmail.out.log
environment=VAULT_PATH="/path/to/vault",GMAIL_CREDENTIALS="/path/to/credentials.json"

[program:whatsapp_watcher]
command=/usr/bin/python3 /path/to/ai-employee/whatsapp_watcher.py
directory=/path/to/ai-employee
user=your-user
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/ai-employee/whatsapp.err.log
stdout_logfile=/var/log/ai-employee/whatsapp.out.log
environment=VAULT_PATH="/path/to/vault"

[program:reasoning_loop]
command=/usr/bin/python3 /path/to/ai-employee/reasoning_loop.py
directory=/path/to/ai-employee
user=your-user
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/ai-employee/reasoning.err.log
stdout_logfile=/var/log/ai-employee/reasoning.out.log
environment=VAULT_PATH="/path/to/vault"

[group:ai-employee]
programs=gmail_watcher,whatsapp_watcher,filesystem_watcher,finance_watcher,reasoning_loop
priority=999
```

```bash
# Control commands
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ai-employee:*
sudo supervisorctl stop ai-employee:*
sudo supervisorctl status ai-employee:*
```

## Step 4: Docker Deployment (Alternative)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV VAULT_PATH=/data/vault
ENV PYTHONUNBUFFERED=1

# Create vault directory
RUN mkdir -p /data/vault

# Run watchers (use supervisor for multiple)
CMD ["python", "gmail_watcher.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  gmail-watcher:
    build: .
    command: python gmail_watcher.py
    volumes:
      - ./vault:/data/vault
      - ./credentials:/credentials:ro
    environment:
      - VAULT_PATH=/data/vault
      - GMAIL_CREDENTIALS=/credentials/gmail_credentials.json
    restart: unless-stopped

  whatsapp-watcher:
    build: .
    command: python whatsapp_watcher.py
    volumes:
      - ./vault:/data/vault
      - ./whatsapp_session:/whatsapp_session
    environment:
      - VAULT_PATH=/data/vault
      - WHATSAPP_SESSION=/whatsapp_session/session.json
    restart: unless-stopped

  reasoning-loop:
    build: .
    command: python reasoning_loop.py
    volumes:
      - ./vault:/data/vault
    environment:
      - VAULT_PATH=/data/vault
    restart: unless-stopped
    depends_on:
      - gmail-watcher
      - whatsapp-watcher
```

## ACCEPTANCE CRITERIA

- Watchers run continuously in background
- Automatic restart on failure
- Logs are captured and rotated
- System restart persistence
- Resource limits enforced

## FOLLOW-UPS

- Add health check endpoint
- Implement log rotation
- Create monitoring dashboard
- Add alerting for failures
