# Implementation Plan: Silver Tier - Functional Assistant

**Feature**: 002-silver-tier
**Phase**: 2 (Silver Tier)
**Builds On**: 001-bronze-tier (Phase 1)
**Created**: 2025-02-20
**Status**: Draft

---

## Technical Context

### Architecture Overview

Phase 2 extends the Bronze Tier foundation with:
- **Multi-watcher perception** (2+ concurrent watchers)
- **Human-in-the-loop approval** workflow
- **MCP server integration** for external actions
- **Reasoning loop** with Plan.md creation
- **Scheduled execution** for 24/7 operation

### Technology Stack

**Core Technologies** (inherited from Phase 1):
- **Language**: Python 3.11+
- **Vault**: Obsidian markdown with YAML frontmatter
- **Watchers**: Watchdog (filesystem), Google API (Gmail), Playwright (WhatsApp - optional)
- **Agent Skills**: Reusable .md files for AI logic patterns

**New for Phase 2**:
- **MCP Servers**: Model Context Protocol servers for external actions
  - `mcp_email`: Email sending capability
  - `mcp_social_linkedin`: LinkedIn posting capability
- **Scheduling**: cron (Linux) or Task Scheduler (Windows)
- **Reasoning**: Ralph Wiggum loop pattern (Stop hook iteration)

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Second Watcher** | Gmail Watcher | Most business-relevant, good API support, complements filesystem watcher |
| **MCP Priority** | Email first, LinkedIn second | Email is universal, LinkedIn has specific business requirement |
| **Scheduling Platform** | Windows Task Scheduler | Project running on Windows (per Phase 1) |
| **Approval Detection** | File polling (every 30s) | Simple, no complex file system watching needed |
| **Plan Iteration** | Stop hook pattern | Proven pattern from Ralph Wiggum skill |

### Dependencies

**Phase 1 Deliverables** (must remain intact):
- ✅ AI_Employee_Vault structure
- ✅ Dashboard.md and Company_Handbook.md
- ✅ FilesystemWatcher implementation
- ✅ Claude Code read/write capability
- ✅ /Needs_Action/, /Done/, /Plans/, /Pending_Approval/ folders

**New Dependencies**:
- Gmail API credentials (client_id, client_secret, refresh_token) - **user must provide**
- MCP servers installed and configured locally
- Python libraries: google-auth, google-api-python-client, google-auth-oauthlib
- Playwright (if WhatsApp watcher added): playwright, pyplaywright

---

## Constitution Check

### Pre-Design Compliance

**GATE: All requirements MUST comply with constitution principles**

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Document Adherence** | ✅ PASS | Only Silver Tier features specified (no Gold/Platinum) |
| **II. Privacy & Security First** | ✅ PASS | Secrets stay local-only (.env files), no credentials in vault |
| **III. Human-in-the-Loop** | ✅ PASS | /Pending_Approval/ workflow mandatory for sensitive actions |
| **IV. MCP Server Pattern** | ✅ PASS | External actions (email, LinkedIn) via MCP only |
| **V. Ralph Wiggum Loop** | ✅ PASS | Iterative reasoning uses Stop hook pattern |
| **VI. Watcher-Triggered** | ✅ PASS | All perception starts with file drops in /Needs_Action/ |
| **VII. Vault-Only Read/Write** | ✅ PASS | Claude reads/writes only to vault files |
| **VIII. Incremental Phase Execution** | ✅ PASS | Phase 1 untouched, Phase 2 in /phase-2/ only |
| **IX. Agent Skills Implementation** | ✅ PASS | All new AI logic via Agent Skills only |

**Gate Evaluation**: ✅ **ALL PASS** - Proceed to design

---

## Phase 0: Research & Technical Decisions

### Research Tasks

#### R1: Second Watcher Selection

**Question**: Which watcher should be added alongside FilesystemWatcher?

**Options Considered**:
1. **Gmail Watcher** ✅ **CHOSEN**
   - Pros: Business-relevant, good API support, high-value content
   - Cons: Requires OAuth setup, credentials management
   - Agent Skill: `gmail_watcher.md`
2. **WhatsApp Watcher**
   - Pros: Real-time messaging, high engagement
   - Cons: Requires Playwright, more complex setup
   - Agent Skill: `whatsapp_watcher.md`
3. **Finance Watcher**
   - Pros: Transaction monitoring, business-critical
   - Cons: Requires bank/CSV access, privacy concerns
   - Agent Skill: `finance_watcher.md`

**Decision**: Gmail Watcher
**Rationale**: Best balance of business value and implementation feasibility. Most professionals use email for business communication. Good API support and clear Agent Skill pattern.

#### R2: MCP Server Selection Priority

**Question**: Which MCP server should be implemented first?

**Options Considered**:
1. **MCP Email** ✅ **CHOSEN FIRST**
   - Pros: Universal use case, simple API, high value
   - Cons: Requires SMTP configuration
   - Agent Skill: `mcp_email.md`
2. **MCP Social LinkedIn**
   - Pros: Business requirement (sales generation)
   - Cons: LinkedIn API complexity, rate limits
   - Agent Skill: `mcp_social_linkedin.md`

**Decision**: Implement MCP Email first, LinkedIn second
**Rationale**: Email is more universal and testable. LinkedIn posting can be added incrementally after email flow works.

#### R3: Approval Detection Mechanism

**Question**: How should the system detect human approval in /Pending_Approval/?

**Options Considered**:
1. **File Polling** ✅ **CHOSEN**
   - Pros: Simple, reliable, no complex watching
   - Cons: 30-second delay
2. **Filesystem Watcher**
   - Pros: Real-time detection
   - Cons: Adds another watcher, complexity
3. **Manual Trigger**
   - Pros: Full control
   - Cons: Not automated

**Decision**: File polling every 30 seconds
**Rationale**: Simplicity wins. 30-second delay is acceptable for approval workflow. Can be optimized later if needed.

#### R4: Plan Iteration Strategy

**Question**: How should Claude iterate through Plan.md tasks?

**Options Considered**:
1. **Ralph Wiggum Loop (Stop Hook)** ✅ **CHOSEN**
   - Pros: Proven pattern, clear completion detection
   - Cons: Requires Agent Skill integration
   - Agent Skill: `ralph_wiggum_loop.md`
2. **Simple Checkbox Iteration**
   - Pros: Simple to understand
   - Cons: No error handling, no Stop hook
3. **Recursive Task Decomposition**
   - Pros: Handles complex tasks
   - Cons: Over-engineering for Silver Tier

**Decision**: Ralph Wiggum Loop pattern
**Rationale**: Agent Skill already exists, proven pattern, handles errors and completion detection properly.

---

## Phase 1: Design & Contracts

### Data Model

#### Entities (Extended from Phase 1)

**ActionItem** (Bronze + Silver extensions)
```yaml
ActionItem:
  id: string (unique)
  timestamp: ISO-8601 datetime
  source: enum (gmail, filesystem, whatsapp, finance)
  priority: enum (low, medium, high)
  content: string
  # NEW for Silver
  sensitivity_level: enum (none, low, medium, high)
  requires_approval: boolean (derived from sensitivity)
  business_context: string (for LinkedIn posting)
```

**ApprovalRequest** (NEW for Silver)
```yaml
ApprovalRequest:
  id: string (unique)
  action_type: enum (email_send, linkedin_post, payment, other)
  draft_content: string
  created_at: ISO-8601 datetime
  approval_status: enum (pending, approved, rejected, cancelled)
  approved_at: ISO-8601 datetime (nullable)
  approved_by: string (user identifier)
  rejection_reason: string (nullable)
  action_reference: string (link to original ActionItem)
```

**Plan** (NEW for Silver)
```yaml
Plan:
  id: string (unique)
  title: string
  created_from: string (ActionItem reference)
  created_at: ISO-8601 datetime
  status: enum (in_progress, complete, failed, cancelled)
  tasks: array of Task
  completed_at: ISO-8601 datetime (nullable)
  summary: string (generated on completion)

Task:
  step_number: integer
  description: string
  status: enum (pending, in_progress, complete, failed)
  completed_at: ISO-8601 datetime (nullable)
  error_details: string (nullable)
  retry_count: integer (default 0)
```

**LinkedInPost** (NEW for Silver)
```yaml
LinkedInPost:
  id: string (unique)
  content: string
  hashtags: array of string
  business_context: string
  draft_created_at: ISO-8601 datetime
  approval_status: enum (pending, approved, rejected, posted, failed)
  approved_at: ISO-8601 datetime (nullable)
  posted_at: ISO-8601 datetime (nullable)
  post_url: string (LinkedIn URL after posting)
  approval_reference: string (link to ApprovalRequest)
```

**EmailDraft** (NEW for Silver)
```yaml
EmailDraft:
  id: string (unique)
  to: string (email address)
  subject: string
  body: string (HTML or plain text)
  attachments: array of string (file paths)
  draft_created_at: ISO-8601 datetime
  approval_status: enum (pending, approved, rejected, sent, failed)
  approved_at: ISO-8601 datetime (nullable)
  sent_at: ISO-8601 datetime (nullable)
  send_result: string (success/failure details)
  approval_reference: string (link to ApprovalRequest)
```

**WatcherSchedule** (NEW for Silver)
```yaml
WatcherSchedule:
  watcher_name: string
  schedule_type: enum (cron, task_scheduler)
  schedule_expression: string (cron format or Task Scheduler trigger)
  last_run: ISO-8601 datetime (nullable)
  next_run: ISO-8601 datetime (nullable)
  status: enum (active, inactive, failed)
  pid: integer (process ID if running, nullable)
  log_file: string (path to watcher log)
```

#### State Transitions

**ApprovalRequest State Machine**:
```
pending → approved (user adds [x] Approved)
pending → rejected (user adds [x] Rejected)
pending → cancelled (user deletes file)
approved → executed (action completed)
rejected → archived (moved to /Logs/)
```

**Plan State Machine**:
```
in_progress → complete (all tasks checked)
in_progress → failed (task failed with no retry)
in_progress → cancelled (user intervention)
complete → archived (moved to /Done/)
```

### File Format Contracts

#### Contract 1: ApprovalRequest File Format

**Location**: `/Pending_Approval/*.md`

**Purpose**: Request human approval for sensitive actions

**Specification**:
```markdown
---
type: approval_request
action_type: email_send | linkedin_post | payment | other
created_at: ISO-8601 datetime
priority: low | medium | high
status: pending
---

# Approval Required: {Action Title}

**Action Type**: {action_type}
**Created**: {created_at}
**Priority**: {priority}

## Draft Content

{Draft of the action to be approved}

- For email: To, Subject, Body
- For LinkedIn: Post content, hashtags
- For payment: Amount, recipient, reason

## Approval Required

- [ ] **Approve** - Execute this action
- [ ] **Reject** - Cancel this action (add reason below)

## Rejection Reason (if rejecting)

{Space for user to explain rejection}

---
*Waiting for approval since {created_at}*
*Reference: {original ActionItem ID}*
```

**Validation Rules**:
1. File MUST have YAML frontmatter
2. `action_type` MUST be one of: email_send, linkedin_post, payment, other
3. Both approval checkboxes MUST be unchecked initially
4. File MUST be readable in Obsidian

#### Contract 2: Plan File Format

**Location**: `/Plans/Plan_{id}_{timestamp}.md`

**Purpose**: Multi-step execution plan created by reasoning loop

**Specification**:
```markdown
---
type: plan
id: string
created_from: string (ActionItem ID)
created_at: ISO-8601 datetime
status: in_progress | complete | failed
---

# Plan: {Title}

**Created**: {created_at}
**Source**: {created_from ActionItem reference}
**Status**: {status}

## Overview

{Brief description of what this plan accomplishes}

## Tasks

- [ ] **Task 1**: {Description}
- [ ] **Task 2**: {Description}
- [ ] **Task 3**: {Description}
- [ ] ...

## Progress

**Completed**: {count}/{total} tasks
**Last Updated**: {timestamp}

## Notes

{Additional context or decisions made during execution}

---
*Created by Claude via Ralph Wiggum loop*
*Iteration: {current_iteration}*
```

**Validation Rules**:
1. File MUST have YAML frontmatter
2. At least 2 tasks MUST be defined
3. Each task MUST be a markdown checkbox
4. Status MUST update as tasks complete

#### Contract 3: LinkedInPost Draft Format

**Location**: `/Pending_Approval/linkedin_post_{id}.md`

**Purpose**: Draft LinkedIn post for approval

**Specification**:
```markdown
---
type: linkedin_post_draft
id: string
created_at: ISO-8601 datetime
business_context: string
status: pending
---

# LinkedIn Post Draft

**Business Context**: {business_context}
**Created**: {created_at}

## Post Content

{Main post content - professional tone, 2-3 paragraphs}

## Hashtags

{Comma-separated list of relevant hashtags}

## Preview

[Preview of how post will appear on LinkedIn]

## Approval

- [ ] **Approve** - Post to LinkedIn now
- [ ] **Reject** - Cancel this post

---
*Awaiting approval before posting via MCP*
*Reference: {original ActionItem ID}*
```

**Validation Rules**:
1. Content MUST be professional tone
2. At least 3 hashtags MUST be included
3. Content length SHOULD be under 3000 characters (LinkedIn limit)
4. Approval checkboxes MUST be unchecked initially

#### Contract 4: EmailDraft Format

**Location**: `/Pending_Approval/email_draft_{id}.md`

**Purpose**: Draft email for approval

**Specification**:
```markdown
---
type: email_draft
id: string
created_at: ISO-8601 datetime
to: string (email address)
subject: string
status: pending
---

# Email Draft

**To**: {to}
**Subject**: {subject}
**Created**: {created_at}

## Body

{Email body content - HTML or plain text}

## Attachments

{List of attachments if any}

## Approval

- [ ] **Approve** - Send this email
- [ ] **Reject** - Cancel this email

---
*Awaiting approval before sending via MCP*
*Reference: {original ActionItem ID}*
```

**Validation Rules**:
1. `to` MUST be valid email format
2. `subject` MUST NOT be empty
3. `body` MUST NOT be empty
4. Approval checkboxes MUST be unchecked initially

### Quick Start Guide

**Purpose**: Step-by-step setup for Phase 2

#### Step 1: Prepare Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials JSON
6. Save to `phase-2/secrets/gmail_credentials.json` (NEVER commit this)

#### Step 2: Install MCP Servers

```bash
# Install MCP Email server
npm install -g @modelcontextprotocol/server-email

# Install MCP Social LinkedIn server
npm install -g @modelcontextprotocol/server-social-linkedin

# Verify installation
mcp-email --version
mcp-social-linkedin --version
```

#### Step 3: Configure Environment Variables

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

# Scheduling
WATCHER_CHECK_INTERVAL=30
APPROVAL_POLL_INTERVAL=30
```

#### Step 4: Set Up Gmail Watcher

```bash
cd phase-2/code
python gmail_watcher.py --test
```

Follow OAuth flow to authorize access.

#### Step 5: Test Multi-Watcher Setup

```bash
# Terminal 1: Filesystem Watcher
cd phase-1/code
python filesystem_watcher.py

# Terminal 2: Gmail Watcher
cd phase-2/code
python gmail_watcher.py

# Terminal 3: Trigger test events
# Drop file in test_drop_folder
# Send test email to yourself

# Verify both create files in /Needs_Action/
```

#### Step 6: Test Approval Workflow

```bash
# Trigger action requiring approval (e.g., draft email)
# Verify file appears in /Pending_Approval/
# Edit file to add [x] Approved
# Verify action executes (email sent)
```

#### Step 7: Configure Scheduling (Windows)

```powershell
# Create Task Scheduler entries
# 1. Filesystem Watcher
schtasks /create /tn "AI Employee - Filesystem Watcher" /tr "python C:\Users\User\Desktop\hakathon-00\phase-1\code\filesystem_watcher.py" /sc minute /mo 5

# 2. Gmail Watcher
schtasks /create /tn "AI Employee - Gmail Watcher" /tr "python C:\Users\User\Desktop\hakathon-00\phase-2\code\gmail_watcher.py" /sc minute /mo 5

# Verify tasks are scheduled
schtasks /query | findstr "AI Employee"
```

#### Step 8: Test End-to-End

1. Restart computer
2. Verify watchers start automatically
3. Send test email
4. Verify /Needs_Action/ file created
5. Verify Plan.md created by Claude
6. Verify approval workflow works
7. Verify email sent via MCP

---

## Implementation Roadmap

### Milestone 1: Vault Updates (Day 1)

**Tasks**:
1. Update Dashboard.md with Silver status sections
2. Add Silver rules to Company_Handbook.md
3. Create /phase-2/ directory structure

**Deliverables**:
- Updated Dashboard.md with multi-watcher status
- Updated Company_Handbook.md with approval workflow rules
- /phase-2/code/, /phase-2/secrets/, /phase-2/logs/ directories

### Milestone 2: Gmail Watcher Integration (Days 2-3)

**Tasks**:
1. Set up Gmail API credentials
2. Implement GmailWatcher based on `gmail_watcher.md` skill
3. Test email detection and action file creation
4. Verify concurrent operation with FilesystemWatcher

**Deliverables**:
- Working GmailWatcher implementation
- Test results showing both watchers creating files
- OAuth flow documentation

### Milestone 3: Approval Workflow (Days 4-5)

**Tasks**:
1. Implement approval request creation based on `human_in_loop.md` skill
2. Implement approval polling mechanism
3. Integrate with approval execution (MCP call)
4. Test full approval flow (draft → approve → execute)

**Deliverables**:
- Working approval workflow
- Test files showing before/after approval
- Approval polling script

### Milestone 4: MCP Integration (Days 6-7)

**Tasks**:
1. Install and configure MCP Email server
2. Implement Claude → MCP email integration
3. Test email sending with approval
4. (Optional) Install MCP LinkedIn server
5. (Optional) Test LinkedIn posting flow

**Deliverables**:
- Working MCP email integration
- Test email sent successfully
- (Optional) LinkedIn post draft and posting flow

### Milestone 5: Reasoning Loop (Days 8-9)

**Tasks**:
1. Implement Plan.md creation based on `ralph_wiggum_loop.md` skill
2. Implement task iteration logic
3. Test with multi-step task
4. Verify completion and archival

**Deliverables**:
- Working reasoning loop
- Sample Plan.md files
- Test results showing task completion

### Milestone 6: Scheduling (Days 10-11)

**Tasks**:
1. Create cron/Task Scheduler entries for watchers
2. Test auto-start on system boot
3. Verify watchers run continuously
4. Create approval polling schedule

**Deliverables**:
- Scheduled watcher execution
- Auto-start configuration
- Scheduling documentation

### Milestone 7: Integration & Verification (Days 12-13)

**Tasks**:
1. End-to-end testing of all features
2. Update Dashboard.md with real-time status
3. Create verification.md with test results
4. Document any issues and workarounds

**Deliverables**:
- Comprehensive verification document
- Updated Dashboard.md
- All success criteria validated

---

## Risk Analysis

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Gmail API rate limits** | Medium | Medium | Implement exponential backoff, batch processing |
| **MCP server instability** | Low | High | Add retry logic, fallback to manual execution |
| **OAuth token expiration** | Medium | Medium | Implement token refresh, error handling |
| **Concurrent watcher conflicts** | Low | Low | Use file locking, unique timestamps |
| **Scheduling permissions** | Medium | Medium | Provide alternative manual startup instructions |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **User approval timeout** | High | Low | No auto-approval, indefinite wait is acceptable |
| **Test account limitations** | Medium | Medium | Use test accounts for email/LinkedIn, document limitations |
| **Windows Task Scheduler issues** | Low | Medium | Provide cron alternative for Linux, manual startup fallback |

---

## Success Metrics

### Quantitative Metrics

- ✅ **2+ watchers** running concurrently for 10+ minutes
- ✅ **95%+** of sensitive actions create approval requests
- ✅ **<30 seconds** from approval to action execution
- ✅ **99%+** email delivery rate via MCP
- ✅ **100%** of watchers auto-start on schedule

### Qualitative Metrics

- ✅ **User trust**: Approval workflow provides clear visibility
- ✅ **Business value**: LinkedIn posting generates leads
- ✅ **Reliability**: System runs 24/7 without manual intervention
- ✅ **Maintainability**: All logic via Agent Skills, easy to modify

---

## Post-Design Constitution Check

**Re-evaluation after design complete**:

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Document Adherence** | ✅ PASS | No Gold/Platinum features in design |
| **II. Privacy & Security** | ✅ PASS | Credentials in /phase-2/secrets/, not in vault |
| **III. Human-in-the-Loop** | ✅ PASS | /Pending_Approval/ workflow designed |
| **IV. MCP Server Pattern** | ✅ PASS | Email/LinkedIn via MCP only |
| **V. Ralph Wiggum Loop** | ✅ PASS | Plan iteration uses Stop hook |
| **VI. Watcher-Triggered** | ✅ PASS | All starts with /Needs_Action/ |
| **VII. Vault-Only Read/Write** | ✅ PASS | Claude vault-only access maintained |
| **VIII. Incremental Phase Execution** | ✅ PASS | Phase 1 intact, Phase 2 in /phase-2/ |
| **IX. Agent Skills Implementation** | ✅ PASS | All new logic references skills |

**Final Gate Evaluation**: ✅ **ALL PASS** - Design approved for implementation

---

## Next Steps

1. ✅ **Specification Complete**: specs/002-silver-tier/spec.md
2. ✅ **Implementation Plan Complete**: specs/002-silver-tier/plan.md (this file)
3. ⏭️ **Tasks Generation**: Run `/sp.tasks` to create detailed task list
4. ⏭️ **Implementation**: Run `/sp.implement` to execute tasks

---

**Plan Status**: ✅ Ready for task generation
**Last Updated**: 2025-02-20
**Plan Version**: 1.0
