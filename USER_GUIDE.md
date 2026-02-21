# AI Employee - User Guide
## 📖 Complete Guide for Using Your AI Employee

**Version**: 4.0.0 (Platinum Tier)

---

## 🎯 Welcome to AI Employee

AI Employee is your autonomous digital workforce that works 24/7 to handle business operations. This guide will help you understand how to interact with your AI Employee effectively.

---

## 📚 Table of Contents

1. [Understanding Your AI Employee](#understanding-your-ai-employee)
2. [Quick Start](#quick-start)
3. [Daily Operations](#daily-operations)
4. [Workflows](#workflows)
5. [Monitoring & Oversight](#monitoring--oversight)
6. [Best Practices](#best-practices)
7. [FAQ](#faq)

---

## Understanding Your AI Employee

### What Your AI Employee Does

**📧 Email Management**
- Monitors your Gmail 24/7
- Identifies important emails
- Drafts intelligent responses
- Waits for your approval before sending

**📱 Social Media Management**
- Creates posts for LinkedIn, Twitter/X, Facebook/Instagram
- Schedules content for optimal times
- Engages with your audience
- Requires approval before publishing

**💰 Accounting & Invoicing**
- Drafts invoices in Odoo
- Records transactions
- Tracks expenses
- Posts approved invoices to accounting system

**📊 Business Intelligence**
- Generates Monday morning CEO briefings
- Analyzes revenue trends
- Identifies bottlenecks
- Provides recommendations

### How It Works

```
Your Email → Cloud Agent Detects → Drafts Response → You Approve → Local Agent Sends
```

**Key Principles**:
1. **Cloud Agent** (Always-on): Monitors, drafts, schedules
2. **Local Agent** (Executive): Approves, sends, posts with credentials
3. **Vault**: All coordination through files
4. **You**: Always in control with approval power

---

## Quick Start

### First-Time Setup (5 Minutes)

#### 1. Check Your Dashboard

Open `AI_Employee_Vault/Dashboard.md` to see:
- System status
- Active tasks
- Completed work
- Component health

#### 2. Review Pending Approvals

Check `AI_Employee_Vault/Pending_Approval/` for items needing your attention:

```bash
cd AI_Employee_Vault
ls -la Pending_Approval/
```

#### 3. Approve or Reject

Open any pending file:
- Add `APPROVED` to approve
- Add `REJECTED` to reject

**Example**:
```markdown
# Email Response Draft

**Subject**: Re: Project Proposal

[Response content here...]

---
**STATUS**: PENDING APPROVAL

**Your Decision**: Add "APPROVED" or "REJECTED" here
```

Your action:
```markdown
**Your Decision**: APPROVED
```

#### 4. Watch Processing

After approval, the Local Agent will:
1. Detect your approval
2. Execute the action (send email, post to social media, etc.)
3. Move file to `Done/`
4. Log the action

---

## Daily Operations

### Morning Routine (5 Minutes)

#### 1. Check Dashboard
```bash
# Open dashboard
cat AI_Employee_Vault/Dashboard.md

# Or open in editor
nano AI_Employee_Vault/Dashboard.md
```

**Look for**:
- ❌ Errors or warnings
- 📧 New emails processed
- 📊 Reports generated
- 🔧 System status

#### 2. Review Overnight Work
```bash
# Check Done folder for completed work
ls -la AI_Employee_Vault/Done/

# Check Logs folder for any issues
ls -la AI_Employee_Vault/Logs/
```

#### 3. Process Approvals
```bash
# Check pending approvals
ls -la AI_Employee_Vault/Pending_Approval/

# Open each pending file
```

**Process each**:
- Review the draft/content
- Add `APPROVED` or `REJECTED`
- Save and close
- Local Agent will handle the rest

### Throughout the Day

#### Create New Tasks

**To Process Email**:
```bash
# Move email to Needs_Action
cp email_message.txt AI_Employee_Vault/Needs_Action/email/

# Cloud agent will pick it up
```

**To Create Social Post**:
```bash
# Create post file
cat > AI_Employee_Vault/Needs_Action/social/new-product.md <<EOF
# Social Post: New Product Launch

**Platform**: LinkedIn
**Content**: Excited to announce our new product...
**Schedule**: 2026-02-22 10:00 AM

---

[Full post content here]
EOF

# Cloud agent will format and draft
```

**To Create Invoice**:
```bash
# Create invoice file
cat > AI_Employee_Vault/Needs_Action/accounting/invoice-client-x.md <<EOF
# Invoice: Client X Project

**Client**: Client X
**Amount**: $5000
**Due Date**: 2026-03-01
**Line Items**:
- Project Phase 1: $3000
- Project Phase 2: $2000
EOF

# Cloud agent will create Odoo draft
```

#### Check Progress

```bash
# Check in-progress tasks
ls -la AI_Employee_Vault/In_Progress/

# Check updates from cloud
ls -la AI_Employee_Vault/Updates/
```

### Evening Routine (2 Minutes)

#### 1. Review Summary
```bash
# Check dashboard for daily summary
cat AI_Employee_Vault/Dashboard.md | grep "Today"
```

#### 2. Verify Sync
```bash
# Check vault sync
tail -20 ~/vault-sync-local.log
```

---

## Workflows

### Email Processing Workflow

**Scenario**: Client sends urgent email requesting proposal revision

**Step 1**: Email arrives
- Cloud Gmail Watcher detects new email
- Creates file in `Needs_Action/email/`

**Step 2**: Cloud processes
- Cloud agent claims task (moves to `In_Progress/cloud-agent/`)
- Drafts response
- Creates approval file in `Pending_Approval/email/`
- Releases claim

**Step 3**: You approve
- Open approval file
- Review draft
- Add `APPROVED`
- Save file

**Step 4**: Local executes
- Local agent detects approval
- Sends email via SMTP
- Moves to `Done/email/`
- Logs to Dashboard

**Time**: ~2 minutes (cloud drafting) + ~1 minute (your approval) + ~10 seconds (sending)

### Social Media Posting Workflow

**Scenario**: Post company announcement on LinkedIn

**Step 1**: Create post request
```bash
cat > AI_Employee_Vault/Needs_Action/social/company-announcement.md <<EOF
# Social Post: Company Announcement

**Platform**: LinkedIn
**Type**: Announcement
**Schedule**: Tomorrow 9:00 AM

**Content**:
We're thrilled to announce...

**Hashtags**: #company #announcement #growth
EOF
```

**Step 2**: Cloud formats
- Cloud agent detects request
- Formats for LinkedIn (character limit, hashtags, mentions)
- Optimizes posting time
- Creates approval file

**Step 3**: You approve
- Review formatted post
- Add `APPROVED`
- Save file

**Step 4**: Local posts
- Local agent detects approval
- Posts to LinkedIn via API
- Moves to `Done/social/`
- Logs post URL and engagement

### Invoice Creation Workflow

**Scenario**: Create invoice for completed project

**Step 1**: Create invoice request
```bash
cat > AI_Employee_Vault/Needs_Action/accounting/project-invoice.md <<EOF
# Invoice: Website Development Project

**Client**: ABC Corp
**Project**: Website Redesign
**Amount**: $7500
**Due**: Net 30

**Items**:
- Design: $2500
- Development: $4000
- Testing: $1000
EOF
```

**Step 2**: Cloud drafts
- Cloud agent creates Odoo invoice draft
- Assigns invoice number
- Calculates tax
- Creates approval file

**Step 3**: You approve
- Review invoice details
- Add `APPROVED`
- Save file

**Step 4**: Local posts
- Local agent posts invoice to Odoo
- Sends invoice email to client
- Records transaction
- Moves to `Done/accounting/`

---

## Monitoring & Oversight

### Health Monitoring

**Check System Health**:
```bash
# Cloud health
curl http://YOUR_CLOUD_IP:8080/health

# Local agent
ps aux | grep orchestrator

# Sync status
cd ~/AI_Employee_Vault
git status
```

### Review Dashboard

**Dashboard Sections**:
1. **System Status**: Overall health
2. **Component Status**: Cloud, Local, Odoo, Sync
3. **Active Tasks**: Currently in progress
4. **Completed Work**: Recent completions
5. **Pending Approvals**: Awaiting your decision
6. **Errors & Warnings**: Issues needing attention

### Audit Trail

**All Actions Are Logged**:
- Email sent → `Done/email/sent-*.md`
- Social post → `Done/social/posted-*.md`
- Invoice created → `Done/accounting/invoice-*.md`
- Every log includes:
  - Timestamp
  - Agent (cloud/local)
  - Action taken
  - Result

**Review Recent Activity**:
```bash
# Today's completed work
find AI_Employee_Vault/Done/ -type f -mtime -1

# Check logs
tail -50 ~/ai-employee/agent.log
```

---

## Best Practices

### 1. Regular Approval Checks

**Check 3x daily**:
- Morning (overnight processing)
- Midday (new items)
- Evening (before signing off)

**Time investment**: 5 minutes per check

### 2. Clear Instructions

When creating tasks, be specific:

**✅ Good**:
```markdown
# Email Response: Project Timeline

**To**: client@company.com
**Subject**: Re: Project Timeline

**Key Points**:
- Phase 1: Complete by March 1
- Phase 2: Starts March 2
- Budget: Within original scope
```

**❌ Vague**:
```markdown
# Email: Respond to client about project
```

### 3. Use Approvals Effectively

**Always review**:
- Email drafts for tone and accuracy
- Social posts for brand consistency
- Invoices for correct amounts

**Don't auto-approve**: Take time to review

### 4. Monitor System Health

**Daily checks**:
- Dashboard status
- Pending approvals
- Error logs

**Weekly reviews**:
- Completed work summary
- System performance
- Optimization opportunities

### 5. Provide Feedback

**If drafts are off**:
- Add feedback to approval file
- Cloud agent learns preferences

**Example**:
```markdown
**Feedback**: Make response more formal. Use "Dear Mr. Smith" instead of "Hi"
```

---

## FAQ

### Q: How quickly does my AI Employee respond?

**A**:
- Email drafting: ~2 minutes (cloud processing)
- After your approval: ~10 seconds (local sending)
- Social posting: ~30 seconds
- Invoice creation: ~1 minute

### Q: What happens if I'm offline?

**A**: Cloud agent continues working:
- Monitors email
- Creates drafts
- Queues approvals for when you return

No actions are taken without your approval.

### Q: Is my data secure?

**A**: Yes, multi-layered security:
- **No secrets on cloud**: No API keys, tokens, or passwords
- **Git sync**: Only markdown files, no credentials
- **Pre-sync audit**: Blocks secrets from being committed
- **Local storage**: All sensitive data on your machine only

### Q: Can I customize workflows?

**A**: Yes, several ways:
- Edit task templates
- Add custom approval criteria
- Modify scheduling preferences
- Configure notification settings

### Q: What if my AI Employee makes a mistake?

**A**:
- **Cloud mistakes**: Caught in approval phase
- **Local mistakes**: Logged to `Errors/` folder
- **Recovery**: Reject approval, provide feedback, retry

### Q: How do I scale up?

**A**:
- Add more watchers (finance, support, etc.)
- Connect more MCP servers
- Add team members with approval authority
- Scale cloud resources (Oracle Cloud allows upgrades)

### Q: Can I integrate with other tools?

**A**: Yes, through MCP (Model Context Protocol):
- Email servers (Gmail, Outlook, etc.)
- Accounting (Odoo, QuickBooks, Xero)
- CRM (Salesforce, HubSpot)
- Project management (Jira, Asana, Trello)

### Q: What's the cost?

**A**:
- **Oracle Cloud**: Always Free tier (4 ARM CPUs, 24GB RAM)
- **GitHub**: Free for private repositories
- **Domain**: ~$10/year (optional)
- **Total**: ~$10/year or less

---

## Advanced Usage

### Custom Watchers

Create domain-specific watchers:

```bash
# Finance watcher
cp phase-4/.claude/commands/finance_watcher.md ~/.claude/commands/

# WhatsApp watcher
cp phase-4/.claude/commands/whatsapp_watcher.md ~/.claude/commands/
```

### Custom MCP Servers

Add integrations:

```bash
# Install MCP server
npm install @mcp/custom-integration

# Configure in .env
MCP_CUSTOM_ENABLED=true
MCP_CUSTOM_API_KEY=your-key
```

### Scheduled Reports

Automate CEO briefings:

```bash
# Add to cron
0 9 * * 1 ~/ai-employee/scripts/weekly-briefing.sh
```

---

## Support

### Documentation
- Full documentation: `docs/`
- API reference: `docs/api.md`
- Architecture: `docs/architecture.md`

### Getting Help
- Issues: https://github.com/yourcompany/ai-employee/issues
- Email: support@yourcompany.com
- Community: https://github.com/yourcompany/ai-employee/discussions

---

## Summary

Your AI Employee is designed to:
- ✅ Work 24/7 without interruption
- ✅ Handle repetitive tasks automatically
- ✅ Always seek your approval for important actions
- ✅ Learn your preferences over time
- ✅ Scale with your business

**Your role**:
1. Review drafts (~5 minutes, 3x daily)
2. Approve or reject actions
3. Provide feedback for improvement
4. Monitor system health

**Time investment**: ~15 minutes per day

**Productivity gain**: ~10-20 hours per week saved

---

**Enjoy your AI Employee! 🎉**

*For technical support, contact: support@yourcompany.com*
