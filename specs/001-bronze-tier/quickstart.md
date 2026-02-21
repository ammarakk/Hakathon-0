# Quick Start Guide: Phase 1 Bronze Tier

**Last Updated**: 2025-02-20
**Estimated Time**: 1-2 hours

## Prerequisites

- Python 3.11+ installed
- Obsidian installed
- Claude Code accessible
- Terminal access

## Step 1: Create Vault Structure (5 minutes)

```bash
# Create vault directory
mkdir -p AI_Employee_Vault
cd AI_Employee_Vault

# Create folders
mkdir -p Needs_Action Done Agent_Skills Logs Accounting Plans Pending_Approval In_Progress Updates
```

## Step 2: Create Dashboard.md (5 minutes)

Create `AI_Employee_Vault/Dashboard.md`:

```markdown
# AI Employee Dashboard

## Bank Summary

| Account | Balance | Last Updated |
|---------|---------|--------------|
| Checking | $0.00 | - |
| Savings | $0.00 | - |

## Pending Messages

| Source | Count | Last Checked |
|--------|-------|--------------|
| Gmail | 0 | - |
| WhatsApp | 0 | - |

## Active Projects

| Project | Status | Last Activity |
|----------|--------|---------------|
| - | - | - |

---

*Last updated: 2025-02-20*
```

## Step 3: Create Company_Handbook.md (5 minutes)

Create `AI_Employee_Vault/Company_Handbook.md`:

```markdown
# Company Handbook

## Rules of Engagement

### Communication Style
- Be polite in all communications
- Use professional yet friendly tone
- Be concise but thorough
- Avoid jargon unless necessary

### Approval Thresholds
- **Payments >$500**: Require human approval
- **Email sends**: Require human review
- **Social media posts**: Require human approval
- **File deletions**: Require human confirmation

### Workflow
1. Watchers detect items → create files in /Needs_Action/
2. Process items systematically
3. Move completed items to /Done/
4. Archive processed items regularly

### Privacy & Security
- Never share credentials
- Keep .env files local-only
- Don't log sensitive information
- Ask for approval on uncertain actions

---

*Version: 1.0 - Bronze Tier*
```

## Step 4: Set Up Filesystem Watcher (15 minutes)

### Install Dependencies

```bash
pip install watchdog
```

### Create Watcher Script

Create `phase-1/code/filesystem_watcher.py` (use implementation from `filesystem_watcher.md` Agent Skill).

### Create Test Configuration

Create `phase-1/code/test_config.py`:

```python
from pathlib import Path

VAULT_PATH = Path("/path/to/AI_Employee_Vault")
WATCH_DIRECTORY = Path("/path/to/watch/folder")  # Change this!
CHECK_INTERVAL = 60  # seconds
```

## Step 5: Test Watcher (10 minutes)

### Terminal 1: Start Watcher

```bash
cd phase-1/code
python filesystem_watcher.py
```

### Terminal 2: Trigger File Drop

```bash
# Drop a test file in the monitored folder
echo "Test content" > /path/to/watch/folder/testfile.txt
```

### Verify

Check `/Needs_Action/` for new file:
```bash
ls -la AI_Employee_Vault/Needs_Action/
```

Expected: A new `.md` file with file metadata and content.

## Step 6: Test Claude Code Integration (15 minutes)

### Start Claude Code

```bash
# From vault root
cd AI_Employee_Vault
claude .
```

### Test Command to Claude

```
Please read the file in Needs_Action/ that was just created by the watcher,
understand its content, and write a summary response to Done/test_response.md
```

### Verify

Check `/Done/` for response file:
```bash
ls -la AI_Employee_Vault/Done/
```

## Step 7: Verify in Obsidian (5 minutes)

1. Open Obsidian
2. Open vault: `AI_Employee_Vault`
3. Verify files visible:
   - Dashboard.md ✓
   - Company_Handbook.md ✓
   - Needs_Action/ (with watcher-created file) ✓
   - Done/ (with Claude response) ✓

## Troubleshooting

**Watcher not creating files?**
- Check vault path in test_config.py
- Verify monitored directory exists
- Check terminal for error messages

**Claude cannot read vault?**
- Verify Claude is running from vault root
- Check file permissions
- Ensure files are valid markdown

**Obsidian not showing files?**
- Verify vault path in Obsidian settings
- Check that .md files exist
- Try reopening vault

## Success Criteria

✅ All folders created
✅ Dashboard.md exists with placeholders
✅ Company_Handbook.md exists with Rules of Engagement
✅ Watcher runs and creates file in /Needs_Action/
✅ Claude reads file and writes to /Done/
✅ All files visible in Obsidian

## Next Steps

After successful completion:
1. Document results in `phase-1/test-log.md`
2. Run `/sp.tasks` to create detailed task list
3. Begin implementation
