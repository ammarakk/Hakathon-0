# Quick Start Guide: Phase 2 (Silver Tier)

**Last Updated**: 2025-02-20
**Estimated Time**: 2-3 hours for setup

---

## Prerequisites

- ✅ Phase 1 (Bronze Tier) complete and verified
- Python 3.11+ installed
- Node.js installed (for MCP servers)
- Gmail account (for Gmail watcher)
- Windows Task Scheduler access (for scheduling)

---

## Step 1: Gmail API Setup (30 minutes)

### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "AI Employee - Phase 2"
3. Enable Gmail API:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

### 1.2 Create OAuth 2.0 Credentials

1. Navigate to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "AI Employee Gmail Watcher"
5. Download credentials JSON
6. Save to: `phase-2/secrets/gmail_credentials.json` (NEVER commit this)

### 1.3 Test OAuth Flow

```bash
cd phase-2/code
python test_gmail_auth.py
```

Follow browser authorization flow.

---

## Step 2: Install MCP Servers (15 minutes)

### 2.1 Install MCP Email Server

```bash
npm install -g @modelcontextprotocol/server-email
mcp-email --version
```

### 2.2 Install MCP LinkedIn Server (Optional)

```bash
npm install -g @modelcontextprotocol/server-social-linkedin
mcp-social-linkedin --version
```

### 2.3 Verify Installation

```bash
# Start MCP Email server (test mode)
mcp-email --port 3000 --test-mode

# In another terminal, test connection
curl http://localhost:3000/health
```

---

## Step 3: Configure Environment (10 minutes)

### 3.1 Create Environment File

Create `phase-2/.env`:

```env
# Gmail API
GMAIL_CREDENTIALS_PATH=phase-2/secrets/gmail_credentials.json
GMAIL_TOKEN_PATH=phase-2/secrets/gmail_token.json

# MCP Servers
MCP_EMAIL_HOST=localhost
MCP_EMAIL_PORT=3000
MCP_LINKEDIN_HOST=localhost
MCP_LINKEDIN_PORT=3001

# Polling Intervals (seconds)
WATCHER_CHECK_INTERVAL=30
APPROVAL_POLL_INTERVAL=30
PLAN_ITERATION_INTERVAL=60
```

### 3.2 Create Secrets Directory

```bash
mkdir -p phase-2/secrets
echo "phase-2/secrets/" >> .gitignore
```

---

## Step 4: Implement Gmail Watcher (45 minutes)

### 4.1 Create Gmail Watcher

Reference: `.claude/commands/gmail_watcher.md`

Create `phase-2/code/gmail_watcher.py`:

```python
#!/usr/bin/env python3
"""
Gmail Watcher - Monitor Gmail for important emails
Based on gmail_watcher.md Agent Skill
"""
from base_watcher import BaseWatcher
import google.auth
from googleapiclient.discovery import build
# ... (implementation per Agent Skill)

async def check(self):
    # Fetch emails from Gmail API
    # Filter by "important" label
    # Return list of email items
    pass

async def process_item(self, item):
    # Extract email content
    # Determine action type
    # Set sensitivity level
    pass

async def create_action_file(self, item):
    # Create .md file in /Needs_Action/
    # Include YAML frontmatter
    pass
```

### 4.2 Test Gmail Watcher

```bash
cd phase-2/code
python gmail_watcher.py --test
```

### 4.3 Verify Multi-Watcher Setup

```bash
# Terminal 1: Filesystem Watcher (from Phase 1)
cd phase-1/code
python filesystem_watcher.py

# Terminal 2: Gmail Watcher
cd phase-2/code
python gmail_watcher.py

# Terminal 3: Trigger test events
# Drop file in test_drop_folder
# Send test email to yourself

# Verify both create files in /Needs_Action/
ls -la ../../AI_Employee_Vault/Needs_Action/
```

---

## Step 5: Implement Approval Workflow (45 minutes)

### 5.1 Create Approval Poller

Create `phase-2/code/approval_poller.py`:

```python
#!/usr/bin/env python3
"""
Approval Poller - Check /Pending_Approval/ for human decisions
"""
import time
from pathlib import Path

PENDING_APPROVAL = Path("AI_Employee_Vault/Pending_Approval")

def check_approvals():
    for file in PENDING_APPROVAL.glob("*.md"):
        content = file.read_text()
        if "[x] Approved" in content:
            execute_approval(file)
        elif "[x] Rejected" in content:
            handle_rejection(file)

def execute_approval(file):
    # Parse approval type
    # Call appropriate MCP server
    # Move file to /Done/
    pass

while True:
    check_approvals()
    time.sleep(30)  # Poll every 30 seconds
```

### 5.2 Test Approval Workflow

```bash
# Trigger action requiring approval (e.g., draft email)
# Verify file appears in /Pending_Approval/
# Edit file to add [x] Approved
# Run approval poller
# Verify action executes
```

---

## Step 6: Configure Scheduling (30 minutes)

### 6.1 Create Windows Task Scheduler Entries

```powershell
# Filesystem Watcher (every 5 minutes)
schtasks /create /tn "AI Employee - Filesystem Watcher" `
  /tr "python C:\Users\User\Desktop\hakathon-00\phase-1\code\filesystem_watcher.py" `
  /sc minute /mo 5

# Gmail Watcher (every 5 minutes)
schtasks /create /tn "AI Employee - Gmail Watcher" `
  /tr "python C:\Users\User\Desktop\hakathon-00\phase-2\code\gmail_watcher.py" `
  /sc minute /mo 5

# Approval Poller (every 30 seconds)
schtasks /create /tn "AI Employee - Approval Poller" `
  /tr "python C:\Users\User\Desktop\hakathon-00\phase-2\code\approval_poller.py" `
  /sc minute /mo 1
```

### 6.2 Verify Scheduling

```bash
# List scheduled tasks
schtasks /query | findstr "AI Employee"

# Test auto-start
# Restart computer
# Verify watchers start automatically
```

---

## Step 7: Test End-to-End (30 minutes)

### Test 1: Multi-Source Monitoring

1. Restart computer (verify watchers auto-start)
2. Send test email to yourself
3. Drop test file in `test_drop_folder`
4. Verify both create files in `/Needs_Action/`

### Test 2: Approval Workflow

1. Trigger action requiring approval
2. Verify approval request in `/Pending_Approval/`
3. Approve the action (add `[x] Approved`)
4. Verify action executes within 30 seconds

### Test 3: MCP Integration

1. Draft email requiring approval
2. Approve the draft
3. Verify email sent via MCP
4. Check email inbox (test account)

### Test 4: Dashboard Updates

1. Open `Dashboard.md` in Obsidian
2. Verify Silver sections display
3. Verify watcher status updates
4. Verify pending approvals shown

---

## Troubleshooting

### Gmail Watcher Not Working

**Problem**: No emails detected

**Solutions**:
1. Verify OAuth token is valid
2. Check Gmail API quota limits
3. Verify "important" label is set on test emails
4. Check watcher logs: `phase-2/logs/gmail_watcher.log`

### MCP Server Not Responding

**Problem**: Approval hangs after user approval

**Solutions**:
1. Verify MCP server is running: `ps aux | grep mcp`
2. Check MCP server logs
3. Verify port is correct (3000 for email)
4. Test MCP server manually: `curl http://localhost:3000/health`

### Approval Not Detected

**Problem**: Approval poller doesn't detect `[x] Approved`

**Solutions**:
1. Verify checkbox format: `[x] Approved` (not `[X]`)
2. Check poller is running: `ps aux | grep approval_poller`
3. Verify file path is correct: `AI_Employee_Vault/Pending_Approval/`
4. Check poller logs: `phase-2/logs/approval_poller.log`

### Watchers Not Starting on Schedule

**Problem**: Watchers don't auto-start after reboot

**Solutions**:
1. Verify Task Scheduler entries exist: `schtasks /query`
2. Check "Run whether user is logged on or not" is enabled
3. Verify account has permissions to run tasks
4. Check Task Scheduler logs: Event Viewer → Task Scheduler

---

## Success Criteria

✅ **Multi-watcher**: Gmail + Filesystem both creating files in `/Needs_Action/`
✅ **Approval workflow**: Sensitive actions create approval requests
✅ **MCP integration**: Approved emails sent via MCP
✅ **Scheduling**: Watchers auto-start on schedule
✅ **Dashboard**: Silver status sections visible in Obsidian

---

## Next Steps

After successful setup:

1. **Monitor**: Run for 24 hours and verify stability
2. **Adjust**: Tune polling intervals as needed
3. **Extend**: Add LinkedIn posting MCP (if not done yet)
4. **Document**: Create user guide for your specific setup
5. **Proceed**: Ready for Phase 3 (Gold Tier) after validation

---

## Support

- **Agent Skills Reference**: `.claude/commands/`
- **Constitution**: `.specify/memory/constitution.md`
- **Phase 2 Spec**: `specs/002-silver-tier/spec.md`
- **Phase 2 Plan**: `specs/002-silver-tier/plan.md`

---

**Quick Start Status**: ✅ Complete
**Last Updated**: 2025-02-20
