# Feature Specification: Silver Tier - Functional Assistant

**Feature Branch**: `002-silver-tier`
**Created**: 2025-02-20
**Status**: Draft
**Phase**: 2 (Silver Tier)
**Builds On**: Phase 1 (Bronze Tier - 001-bronze-tier)
**Input**: User description: "Phase 2 (Silver Tier: Functional Assistant) - Multi-watcher support, human-in-loop approval, MCP integration, reasoning loop, scheduling"

---

## Overview

Phase 2 delivers a **Functional Assistant** that extends the Bronze Tier foundation with:
- **Multiple Watchers** monitoring different sources (Gmail + Filesystem minimum)
- **Human-in-the-Loop** approval workflow for sensitive actions
- **MCP Server Integration** for external actions (email, LinkedIn posting)
- **Reasoning Loop** that creates and executes Plan.md files
- **Scheduling** for automated watcher execution

**Key Principle**: This phase is **strictly incremental** - all Bronze Tier features remain intact and functional. No Gold or Platinum features are included.

---

## User Scenarios & Testing

### User Story 1 - Multi-Source Monitoring (Priority: P1)

**Description**: The AI Employee monitors multiple sources simultaneously (Gmail and Filesystem) and creates actionable items in /Needs_Action/ for each detected event.

**Why this priority**: Expands perception capabilities beyond single-source monitoring, enabling the AI to detect more opportunities and tasks from different channels.

**Independent Test**: Can be tested by (1) starting both Gmail and Filesystem watchers, (2) triggering events in both sources (email + file drop), (3) verifying both create .md files in /Needs_Action/ with correct source metadata.

**Acceptance Scenarios**:

1. **Given** Gmail Watcher is running and a new important email arrives, **When** the watcher processes the inbox, **Then** an action file is created in /Needs_Action/ with source: gmail, subject, sender, and email body
2. **Given** Filesystem Watcher is running and a file is dropped in monitored folder, **When** the watcher detects the new file, **Then** an action file is created in /Needs_Action/ with source: filesystem, file path, and metadata
3. **Given** Both watchers are running simultaneously, **When** events occur in both sources, **Then** separate action files are created for each event with unique timestamps and correct source identification

---

### User Story 2 - Human Approval for Sensitive Actions (Priority: P1)

**Description**: Before executing sensitive actions (payments >$500, social media posts, email sends), the AI drafts the action, writes it to /Pending_Approval/, and waits for human approval before proceeding.

**Why this priority**: Critical for safety and trust - ensures humans maintain control over high-impact actions while AI handles routine tasks autonomously.

**Independent Test**: Can be tested by (1) triggering a sensitive action (e.g., drafting an email), (2) verifying approval request appears in /Pending_Approval/, (3) manually adding [x] Approved to the file, (4) verifying the action executes after approval.

**Acceptance Scenarios**:

1. **Given** Claude drafts an email to send, **When** the draft is complete, **Then** an approval request is written to /Pending_Approval/ with draft content and [ ] Approval checkbox
2. **Given** An approval request exists in /Pending_Approval/, **When** the user edits the file to add [x] Approved, **Then** the action (email send) is executed and file is moved to /Done/
3. **Given** An approval request exists, **When** the user adds [x] Rejected or deletes the file, **Then** the action is cancelled and a note is written to /Logs/
4. **Given** A social media post is drafted, **When** it contains business content, **Then** it goes through /Pending_Approval/ before MCP posts to LinkedIn

---

### User Story 3 - Automated LinkedIn Posting (Priority: P2)

**Description**: When business-related content is detected, the AI drafts a LinkedIn post, gets human approval, and posts it via MCP server to generate sales leads.

**Why this priority**: Enables business value generation through automated social media presence while maintaining human oversight.

**Independent Test**: Can be tested by (1) detecting a business trigger (e.g., new product file dropped), (2) verifying Claude drafts LinkedIn post in /Pending_Approval/, (3) approving the post, (4) verifying MCP server posts (or simulates post) to LinkedIn.

**Acceptance Scenarios**:

1. **Given** A business-related file is detected, **When** Claude processes it, **Then** a LinkedIn post draft is created with relevant hashtags and professional tone
2. **Given** A LinkedIn post draft exists in /Pending_Approval/, **When** the user approves it, **Then** the MCP server posts to LinkedIn and confirmation is written to /Done/
3. **Given** LinkedIn posting fails (API error), **When** the error occurs, **Then** error details are logged to /Logs/ and a retry option is offered

---

### User Story 4 - Reasoning Loop with Plan Creation (Priority: P1)

**Description**: When processing items from /Needs_Action/, Claude creates structured Plan.md files in /Plans/ with checkbox tasks, then iterates using Ralph Wiggum loop until all tasks complete.

**Why this priority**: Core intelligence capability - enables multi-step reasoning and task execution beyond simple single-action responses.

**Independent Test**: Can be tested by (1) placing a multi-step task in /Needs_Action/, (2) verifying Claude creates Plan.md with checkboxes in /Plans/, (3) completing tasks iteratively, (4) verifying final completion and archive to /Done/.

**Acceptance Scenarios**:

1. **Given** A complex task is in /Needs_Action/, **When** Claude begins processing, **Then** a Plan.md is created in /Plans/ with numbered checklist of sub-tasks
2. **Given** A Plan.md exists with incomplete tasks, **When** Claude runs the reasoning loop, **Then** it executes the next unchecked task and updates the checkbox
3. **Given** All Plan.md tasks are complete, **When** the final task finishes, **Then** the plan is marked complete, moved to /Done/, and a summary is written
4. **Given** A task fails during execution, **When** the error occurs, **Then** Claude logs the error, marks task as [ ] Failed with error details, and either retries or escalates

---

### User Story 5 - Scheduled Watcher Execution (Priority: P2)

**Description**: Watchers are scheduled to run automatically via cron (Linux) or Task Scheduler (Windows), ensuring continuous monitoring without manual intervention.

**Why this priority**: Enables 24/7 operation - the AI Employee works continuously without requiring manual watcher startup.

**Independent Test**: Can be tested by (1) creating a cron/Task Scheduler entry, (2) verifying watchers start at scheduled time, (3) triggering test events, (4) verifying action files are created.

**Acceptance Scenarios**:

1. **Given** A cron job or Task Scheduler entry is configured, **When** the scheduled time arrives, **Then** the watcher script starts automatically
2. **Given** Watchers are running via scheduler, **When** the system restarts, **Then** watchers are configured to auto-start (optional but recommended)
3. **Given** Multiple watchers are scheduled, **When** they run concurrently, **Then** all watchers function without conflicts

---

### User Story 6 - MCP Email Integration (Priority: P2)

**Description**: Claude drafts emails, gets human approval, and sends them via MCP email server, enabling external communication capabilities.

**Why this priority**: Enables the AI to handle outbound communication for routine tasks while maintaining human oversight.

**Independent Test**: Can be tested by (1) triggering an email draft, (2) verifying draft appears in /Pending_Approval/, (3) approving the draft, (4) verifying MCP sends email successfully.

**Acceptance Scenarios**:

1. **Given** An email needs to be sent, **When** Claude drafts it, **Then** the draft includes To, Subject, Body, and is written to /Pending_Approval/
2. **Given** An email draft is approved, **When** approval is detected, **Then** MCP server sends the email and writes confirmation to /Done/
3. **Given** Email sending fails, **When** the error occurs, **Then** error is logged and retry is attempted up to 3 times

---

### Edge Cases

- **What happens when** Gmail API credentials expire or are invalid?
  - **Expected**: Watcher logs error, continues checking, retries with backoff, notifies user via /Logs/
- **What happens when** multiple watchers detect events simultaneously?
  - **Expected**: Each watcher processes independently, creates separate action files with unique timestamps to avoid conflicts
- **What happens when** human never responds to approval request (e.g., user away)?
  - **Expected**: Approval request remains in /Pending_Approval/ indefinitely, Claude periodically checks but does not auto-approve
- **What happens when** Plan.md execution fails halfway through?
  - **Expected**: Failed task is marked with [ ] Failed and error details, Claude either retries or escalates based on error type
- **What happens when** MCP server is unreachable during email send?
  - **Expected**: Error is logged, email remains in /Pending_Approval/, retry scheduled for later
- **What happens when** /Needs_Action/ contains hundreds of items?
  - **Expected**: Claude processes items in priority order (high → medium → low), oldest first within priority
- **What happens when** scheduled watchers crash?
  - **Expected**: Error logged, scheduler restarts watcher on next cycle, optional alert to user

---

## Requirements

### Constitutional Constraints
**GATE: All requirements MUST comply with constitution principles**

- [x] **Document Adherence**: Only Silver Tier features included (no Gold/Platinum scope creep)
- [x] **Privacy & Security**: Secrets (.env, tokens, sessions) stay local-only; drafts only until approved
- [x] **Human-in-the-Loop**: Sensitive actions require /Pending_Approval/ workflow (payments >$500, posts, emails)
- [x] **MCP Pattern**: External actions (email, LinkedIn) use connected MCP servers only
- [x] **Vault Structure**: All new files stay within defined folder structure (/phase-2/ for code, global folders for vault files)
- [x] **Agent Skills**: All AI functionality (reasoning, planning, content generation) implemented as Agent Skills

### Functional Requirements

#### Multi-Watcher Support
- **FR-001**: System MUST support at least two concurrent watchers (Gmail + Filesystem minimum)
- **FR-002**: Each watcher MUST create action files in /Needs_Action/ with unique source identification
- **FR-003**: Watchers MUST use only pre-created Agent Skills (gmail_watcher.md, filesystem_watcher.md, whatsapp_watcher.md, finance_watcher.md)
- **FR-004**: Action files from different sources MUST have distinguishable metadata (source, timestamp, unique IDs)

#### Human-in-the-Loop Approval
- **FR-005**: System MUST detect sensitive actions (payments >$500, social posts, emails with attachments)
- **FR-006**: For sensitive actions, System MUST write approval request to /Pending_Approval/*.md
- **FR-007**: Approval request MUST include [ ] Approval checkbox and draft/action details
- **FR-008**: System MUST pause execution until user adds [x] Approved (or rejects/cancels)
- **FR-009**: Upon approval, System MUST execute the action and move file to /Done/
- **FR-010**: Upon rejection, System MUST cancel action and log note to /Logs/

#### LinkedIn Posting
- **FR-011**: When business-related content detected, System MUST draft LinkedIn post via Agent Skill
- **FR-012**: LinkedIn draft MUST include relevant hashtags, professional tone, and business value proposition
- **FR-013**: LinkedIn post MUST go through /Pending_Approval/ before posting
- **FR-014**: Upon approval, System MUST post via MCP server (mcp-social-linkedin)
- **FR-015**: System MUST verify post success and write confirmation to /Done/

#### Reasoning Loop
- **FR-016**: When processing /Needs_Action/ items, System MUST create Plan.md in /Plans/
- **FR-017**: Plan.md MUST contain numbered checklist of tasks/steps to complete the item
- **FR-018**: System MUST use Ralph Wiggum loop pattern (ralph_wiggum_loop.md Agent Skill) to iterate through tasks
- **FR-019**: System MUST update Plan.md checkboxes as tasks complete
- **FR-020**: When all tasks complete, System MUST mark plan complete, move to /Done/, and write summary

#### MCP Email Integration
- **FR-021**: When email needs to be sent, System MUST draft email with To, Subject, Body
- **FR-022**: Email draft MUST go through /Pending_Approval/ workflow
- **FR-023**: Upon approval, System MUST send via MCP server (mcp-email)
- **FR-024**: System MUST handle send errors with retry (up to 3 attempts) and logging

#### Scheduling
- **FR-025**: System MUST support scheduled execution via cron (Linux) or Task Scheduler (Windows)
- **FR-026**: Schedule configuration MUST be stored in /phase-2/ directory (not in vault)
- **FR-027**: System MUST log watcher start/stop events to /Logs/
- **FR-028** [OPTIONAL]: System SHOULD auto-start watchers on system boot

#### Dashboard Updates
- **FR-029**: Dashboard.md MUST be updated to show Silver Tier status
- **FR-030**: Dashboard.md MUST display pending items from multiple watchers (count by source)
- **FR-031**: Dashboard.md MUST show active plans in /Plans/ (count and status)

### Key Entities

- **ActionItem** (extends Bronze): Represents detected item from any watcher source. Attributes: id, timestamp, source (gmail/filesystem/whatsapp/finance), priority, content, sensitivity_level (for approval routing)
- **ApprovalRequest**: Represents pending human approval. Attributes: id, action_type, draft_content, created_at, approval_status (pending/approved/rejected), approved_at, approved_by
- **Plan**: Represents multi-step execution plan created by reasoning loop. Attributes: id, title, created_from (reference to ActionItem), tasks (array of {step_number, description, status, completed_at}), status (in_progress/complete/failed)
- **WatcherSchedule**: Represents scheduled execution configuration. Attributes: watcher_name, schedule_type (cron/task_scheduler), schedule_expression, last_run, next_run, status (active/inactive)
- **LinkedInPost**: Represents drafted social media post. Attributes: id, content, hashtags, business_context, draft_created_at, approval_status, posted_at, post_url (after posting)
- **EmailDraft**: Represents drafted email. Attributes: id, to, subject, body, attachments (list), draft_created_at, approval_status, sent_at, send_result

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: At least two watchers run concurrently for 10+ minutes without crashing
- **SC-002**: Watchers create action files in /Needs_Action/ from different sources (minimum 2 unique sources)
- **SC-003**: 100% of sensitive actions (>=$500 payments, social posts, emails) create approval requests in /Pending_Approval/
- **SC-004**: 95% of approved actions execute successfully within 30 seconds of approval
- **SC-005**: Claude creates Plan.md files for complex tasks with 3+ sub-steps
- **SC-006**: Ralph Wiggum loop iterates through Plan.md tasks until completion (test with 5-step plan)
- **SC-007**: LinkedIn posting flow completes end-to-end (draft → approve → post → confirm) in under 2 minutes
- **SC-008**: MCP email server successfully sends approved emails with 99% delivery rate
- **SC-009**: Scheduled watchers start automatically at configured time (verify with 3 consecutive scheduled runs)
- **SC-010**: Dashboard.md displays real-time counts of pending items by source (updates within 60 seconds of new item)
- **SC-011**: Zero secrets in vault files (manual verification - no API keys, tokens, or passwords in .md files)
- **SC-012**: All AI functionality (reasoning, planning, content generation) uses Agent Skills exclusively (verified by code inspection)

### Quality Gates

- **Gate 1**: All Bronze Tier features remain functional (no regressions from Phase 1)
- **Gate 2**: No Gold or Platinum features implemented (Odoo, Facebook/Instagram/X, weekly audit, cloud sync, A2A messaging)
- **Gate 3**: Human approval workflow tested and verified for all sensitive action types
- **Gate 4**: MCP servers (email, LinkedIn) connected and functional

---

## Assumptions & Dependencies

### Assumptions

1. **Gmail API Access**: User has or will create Gmail API credentials (client_id, client_secret) for Gmail Watcher
2. **LinkedIn Account**: User has a LinkedIn account for business posting with appropriate permissions
3. **MCP Servers**: MCP servers (mcp-email, mcp-social-linkedin) are installed and configured locally
4. **Network Connectivity**: Stable internet connection for Gmail API and MCP server communication
5. **File System Access**: Watcher has read access to monitored directories
6. **Windows/Linux Environment**: Scheduling uses Task Scheduler (Windows) or cron (Linux) - assumption of single OS for Phase 2

### Dependencies

1. **Phase 1 (Bronze Tier)**: All Bronze deliverables must remain intact and functional
2. **Agent Skills**: gmail_watcher.md, filesystem_watcher.md, ralph_wiggum_loop.md, linked_in_posting.md, mcp_email.md, mcp_social_linkedin.md
3. **Python Libraries**: google-api-python-client (Gmail), watchdog (filesystem), existing MCP server libraries
4. **Obsidian**: Vault continues to be accessible in Obsidian for manual verification
5. **Claude Code**: Claude continues to have read/write access to vault

### Out of Scope (Gold/Platinum)

- ❌ Odoo accounting integration
- ❌ Facebook/Instagram/X social posting
- ❌ Weekly audit / CEO briefing
- ❌ Cloud deployment / VM
- ❌ Vault synchronization (Git/Syncthing)
- ❌ Direct agent-to-agent (A2A) messaging
- ❌ Multi-domain specialization (personal vs business domains)
- ❌ Advanced error recovery (beyond basic retry)

---

## Notes

**Incremental Development**: This specification builds strictly on Phase 1. All Phase 1 features (vault structure, FilesystemWatcher, Claude read/write) remain intact and functional.

**Testing Strategy**: Each User Story can be tested independently. Start with US1 (multi-watcher) to verify perception, then US2 (human approval) for safety, then US4 (reasoning loop) for intelligence, then US3/US5/US6 for specific integrations.

**Constitutional Compliance**: This specification has been validated against all 9 constitutional principles. No Gold or Platinum features are included.

**Next Steps**: After this spec is approved, proceed to `/sp.plan` to create detailed implementation plan with technical decisions, architecture, and data model.
