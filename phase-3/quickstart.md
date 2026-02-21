# Quick Start Guide: Gold Tier - Autonomous Employee

**Feature**: 003-gold-tier
**Phase**: 3 (Gold Tier)
**Estimated Setup Time**: 2-3 hours

---

## Overview

This guide will walk you through setting up the Gold Tier - Autonomous Employee, which adds:

- **Cross-domain integration** (Personal + Business tasks in unified plans)
- **Odoo accounting system** (self-hosted, local)
- **Multi-platform social media** (LinkedIn + Facebook/Instagram + Twitter/X)
- **Weekly CEO Briefing** (automated Monday Morning reports)
- **Error recovery** (graceful degradation when components fail)
- **Comprehensive audit logging** (complete trail of all actions)

**Prerequisites**:
- ✅ Phase 1 (Bronze Tier) completed
- ✅ Phase 2 (Silver Tier) completed
- Windows 10/11 machine
- Python 3.11+ installed
- Admin rights (for Odoo installation)

---

## Step 1: Install Odoo Community Edition (30 minutes)

### 1.1 Download Odoo

1. Visit: https://www.odoo.com/page/download
2. Select: **Odoo 19+ for Windows**
3. Download: **Odoo Community Edition** (NOT Enterprise)
4. Save installer to Downloads folder

### 1.2 Run Installer

1. Double-click `odoo_19.0.latest.exe` (or similar)
2. Click **Next** through installation wizard
3. Choose installation path (default: `C:\Program Files (x86)\Odoo`)
4. Wait for installation to complete (~5 minutes)

### 1.3 Initial Configuration

1. Browser opens to: http://localhost:8069
2. Click **Create Database**
3. Fill in form:
   - **Master Password**: Create strong password (store securely!)
   - **Database Name**: `ai_employee_business`
   - **Email**: admin@example.com
   - **Password**: Create admin password
   - **Phone**: (optional)
   - **Language**: English (US)
4. Click **Create Database**
5. Wait 1-2 minutes for database initialization

### 1.4 Enable Required Modules

1. Login with admin credentials
2. Click **Apps** menu (top left)
3. Search for and install these modules (one at a time):
   - **Invoicing** (or "Accounting")
   - **Contacts**
   - **Products** (usually installed by default)
4. Wait for each module to install

### 1.5 Create Test Data

1. Go to **Contacts** → **Create**
2. Create 3 customers:
   - **ABC Corp**: contact@abccorp.com
   - **XYZ Ltd**: info@xyzltd.com
   - **Startup Co**: hello@startupco.com
3. Go to **Products** → **Create**
4. Create 3 products/services:
   - **Consulting Services**: $100/hour
   - **Software Development**: $150/hour
   - **Technical Support**: $75/hour
5. Go to **Invoicing** → **Customers** → **Invoices** → **Create**
6. Create 2 draft invoices (do NOT post/validate yet):
   - Invoice #1 for ABC Corp ($1,000)
   - Invoice #2 for XYZ Ltd ($1,500)

### 1.6 Verify Odoo Setup

✅ **Success Criteria**:
- Odoo accessible at http://localhost:8069
- Can login with admin credentials
- 3 customers visible in Contacts
- 3 products visible in Products
- 2 draft invoices visible in Invoicing

---

## Step 2: Configure Social Platform Developer Accounts (45 minutes)

### 2.1 Facebook/Instagram Setup

#### Create Meta Developer Account

1. Visit: https://developers.facebook.com
2. Click **Get Started** → **Create Account**
3. Register with your Facebook account
4. Verify email address

#### Create Facebook App

1. Go to: https://developers.facebook.com/apps
2. Click **Create App** → **Business** type
3. Fill in:
   - **App Name**: AI Employee Social
   - **Contact Email**: your email
4. Click **Create App**
5. Add **Product**: **Facebook Login** (for testing)
6. Note: **App ID** and **App Secret** (from Settings → Basic)

#### Generate Page Access Token

1. Create or use existing Facebook Page (for business)
2. Go to: **Tools & Support** → **Graph API Explorer**
3. Select your App from dropdown
4. Generate Page Access Token:
   - Select **Page** from dropdown
   - Select your page
   - Permissions: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`
5. Copy **Page Access Token** (long string)
6. Note **Page ID** (from Page Settings → About)

#### Connect Instagram Business Account

1. Go to your Facebook Page
2. Click **Settings** → **Instagram**
3. Click **Connect Account**
4. Login to Instagram business account
5. Note **Instagram Business Account ID** (from Instagram Creator Studio)

### 2.2 Twitter/X Setup

#### Create X Developer Account

1. Visit: https://developer.twitter.com
2. Click **Sign up for Free Account**
3. Register with your X (Twitter) account
4. Verify email address

#### Create X App

1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Click **Create Project** → **Create an App**
3. Fill in:
   - **App name**: AI Employee Social
   - **Description**: Automated social posting
   - **Use case**: Posting tweets from business automation
4. Click **Next** → **Create App**
5. Go to **Settings** → **Authentication**
6. Copy **Bearer Token** (generate if not present)

### 2.3 Verify Social Setup

✅ **Success Criteria**:
- Facebook Page Access Token obtained
- Facebook Page ID noted
- Instagram Business Account ID noted
- Twitter/X Bearer Token obtained

---

## Step 3: Install and Configure MCP Servers (30 minutes)

### 3.1 Install Odoo MCP Server

```bash
npm install -g @modelcontextprotocol/server-odoo
```

### 3.2 Install Social Platform MCP Servers

```bash
npm install -g @modelcontextprotocol/server-social-fb-ig
npm install -g @modelcontextprotocol/server-social-x
```

### 3.3 Create Credentials Files

Create folder:
```bash
mkdir phase-3/secrets
```

#### Odoo Credentials

Create `phase-3/secrets/.odoo_credentials`:
```env
ODOO_URL=http://localhost:8069
ODOO_DB=ai_employee_business
ODOO_USER=admin
ODOO_PASSWORD=your_admin_password_here
```

#### Facebook/Instagram Credentials

Create `phase-3/secrets/.fb_credentials`:
```env
FB_PAGE_ACCESS_TOKEN=your_long_page_access_token_here
FB_PAGE_ID=your_page_id_here
IG_BUSINESS_ACCOUNT_ID=your_ig_account_id_here
```

#### Twitter/X Credentials

Create `phase-3/secrets/.x_credentials`:
```env
X_BEARER_TOKEN=your_bearer_token_here
```

### 3.4 Configure MCP Servers in Claude Code

1. Open Claude Code Settings
2. Go to **MCP Servers** section
3. Add each server configuration (refer to MCP documentation for exact format)
4. Test each MCP connection

---

## Step 4: Update Vault Structure (20 minutes)

### 4.1 Update Dashboard.md

Open `AI_Employee_Vault/Dashboard.md` and add sections:

```markdown
## Gold Tier Status

### Cross-Domain Overview

| Domain | Pending Items | Priority |
|--------|---------------|----------|
| Personal | 2 | Medium |
| Business | 5 | High |

### Active Cross-Domain Plans

| Plan ID | Domains | Tasks | Progress | Status |
|---------|---------|-------|----------|--------|
| PLAN-2025-003 | Personal, Business | 6 | 4/6 (66%) | In Progress |

### Latest CEO Briefing

**Date**: Monday, February 8, 2026
**Revenue MTD**: $12,500.00
**Outstanding Invoices**: 3
**Link**: [[CEO_Briefings/Briefing_2026-02-08]]
```

### 4.2 Update Company_Handbook.md

Open `AI_Employee_Vault/Company_Handbook.md` and add rules:

```markdown
## Cross-Domain Rules

### Unified Task Management

- Personal and business items processed in unified reasoning loop
- Tasks labeled with domain: [Personal] or [Business]
- Business tasks prioritized by default (client deadlines, payments)

### Odoo Accounting

- All invoices created as drafts in Odoo
- Draft invoices require /Pending_Approval/ before posting
- Payments >$500 require explicit human approval

### Social Media Posting

- All social posts (LinkedIn, FB, IG, X) require approval
- Platform-specific formatting applied automatically
- Posts generated from business events (completed projects, testimonials)

### Error Handling

- System continues operating if one component fails
- All errors logged to /Logs/errors.md
- Critical components (watchers) restart automatically
```

### 4.3 Create New Folders

```bash
mkdir AI_Employee_Vault/CEO_Briefings
mkdir AI_Employee_Vault/Accounting/Odoo
```

---

## Step 5: Test Cross-Domain Integration (15 minutes)

### 5.1 Create Test Scenarios

**Scenario 1: Personal + Business Items**

1. Create test file in dropbox directory: `test_personal_message.txt`
   - Content: "Call mom about weekend plans"
2. Create test email to yourself with subject: "Project completed - send invoice"

### 5.2 Verify Unified Plan Creation

1. Wait for watchers to create ActionItems in /Needs_Action/
2. Trigger Claude reasoning (manual or scheduled)
3. Verify Plan.md created with:
   - Task: [Personal] Call mom
   - Task: [Business] Create invoice
   - Tasks labeled with domains
   - Business task prioritized first

### 5.3 Verify Odoo Draft Creation

1. If invoice task created, check that:
   - Odoo draft invoice created via MCP
   - Approval request in /Pending_Approval/
   - Draft details in vault file

### 5.4 Verify Social Post Creation

1. Manually create ActionItem for business event:
   - File: `/Needs_Action/test_business_event.md`
   - Content: "Project for ABC Corp completed successfully"
2. Trigger Claude reasoning
3. Verify social post drafts created for:
   - LinkedIn
   - Facebook
   - Twitter/X
   - Instagram (if image provided)

---

## Step 6: Test Weekly CEO Briefing (10 minutes)

### 6.1 Manual Trigger

Run the briefing generator:
```bash
python phase-3/code/generate_ceo_briefing.py
```

### 6.2 Verify Briefing Content

Check that `CEO_Briefing_YYYY-MM-DD.md` contains:
- ✅ Revenue Summary (from Odoo)
- ✅ Pending Items count
- ✅ Bottlenecks list
- ✅ Recommendations (actionable, prioritized)

### 6.3 Schedule Automatic Briefing

Open Windows Task Scheduler:
```
Trigger: Create Basic Task → Name: "AI Employee - Weekly CEO Briefing"
Trigger: Weekly, Monday, 8:00 AM
Action: Start a program
Program: python
Arguments: C:\Users\User\Desktop\hakathon-00\phase-3\code\generate_ceo_briefing.py
```

---

## Step 7: Test Error Recovery (10 minutes)

### 7.1 Simulate MCP Failure

1. Stop Odoo (close Odoo service or window)
2. Trigger action requiring Odoo (e.g., create invoice)
3. Verify:
   - Error logged to `/Logs/errors.md`
   - Other components still working
   - Dashboard.md shows "Error: Odoo unavailable"

### 7.2 Verify Recovery

1. Restart Odoo
2. Trigger retry of failed action
3. Verify action completes successfully
4. Check error log shows "resolved: true"

---

## Verification Checklist

Complete all items to verify Gold Tier setup:

### Odoo Setup
- [ ] Odoo running at http://localhost:8069
- [ ] Admin database created
- [ ] Modules enabled (Invoicing, Contacts, Products)
- [ ] 3 customers created
- [ ] 3 products created
- [ ] 2 draft invoices created

### Social Platforms
- [ ] Facebook Page Access Token obtained
- [ ] Instagram Business Account connected
- [ ] Twitter/X Bearer Token obtained
- [ ] All 3 social MCP servers installed

### MCP Servers
- [ ] mcp-odoo configured and tested
- [ ] mcp-social-fb-ig configured and tested
- [ ] mcp-social-x configured and tested
- [ ] mcp-email (from Phase 2) still running
- [ ] mcp-social-linkedin (from Phase 2) still running

### Vault Structure
- [ ] Dashboard.md updated with Gold sections
- [ ] Company_Handbook.md updated with cross-domain rules
- [ ] /CEO_Briefings/ folder created
- [ ] /Accounting/Odoo/ folder created

### Cross-Domain Integration
- [ ] Test scenario creates unified Plan.md
- [ ] Tasks labeled [Personal] and [Business]
- [ ] Business tasks prioritized first

### Odoo Integration
- [ ] Draft invoice created from /Needs_Action/
- [ ] Approval workflow tested
- [ ] Invoice posted to Odoo after approval

### Social Media Integration
- [ ] Social post drafts created for all platforms
- [ ] Approval workflow tested
- [ ] Posts successfully published

### CEO Briefing
- [ ] Briefing generated with all sections
- [ ] Revenue summary from Odoo data
- [ ] Recommendations actionable

### Error Recovery
- [ ] Error logged when component fails
- [ ] System continues operating
- [ ] Recovery successful when component restored

### Audit Logging
- [ ] /Logs/audit-YYYY-MM-DD.md created
- [ ] Entries for 5+ event types
- [ ] All actions logged

---

## Troubleshooting

### Odoo Won't Start

**Problem**: Odoo service not running
**Solution**:
1. Check Windows Services for "Odoo"
2. Manually start service
3. Or run Odoo from Start Menu

### MCP Server Not Found

**Problem**: npm install fails for MCP server
**Solution**:
1. Check Node.js installed: `node --version`
2. Update npm: `npm install -g npm@latest`
3. Try install with verbose: `npm install -g @modelcontextprotocol/server-odoo --verbose`

### Social API Authentication Failed

**Problem**: 401 Unauthorized error when posting
**Solution**:
1. Check access token not expired
2. Regenerate tokens if needed
3. Verify correct permissions granted

### Plan.md Not Created

**Problem**: Claude not creating unified plans
**Solution**:
1. Check watchers running (Gmail, Filesystem)
2. Verify /Needs_Action/ has items
3. Manually trigger Claude reasoning
4. Check Claude Code logs for errors

### Briefing Missing Revenue Data

**Problem**: CEO Briefing shows $0 revenue
**Solution**:
1. Verify Odoo contains posted invoices
2. Check MCP connection to Odoo
3. Run test query: `python phase-3/code/test_odoo_mcp.py`

---

## Next Steps

After completing this guide:

1. **Verify all 12 Gold Tier success criteria** (see spec.md)
2. **Run end-to-end test** (see verification.md)
3. **Document any issues encountered** (for architecture.md lessons learned)
4. **Proceed to `/sp.tasks`** for detailed implementation tasks

---

**Estimated Total Time**: 2-3 hours
**Difficulty**: Intermediate
**Prerequisites**: Phase 1 + Phase 2 completed

**Support**: Refer to research.md for technical decisions, plan.md for architecture details
