# Feature Specification: Bronze Tier - Foundation (Phase 1)

**Feature Branch**: `001-bronze-tier`
**Created**: 2025-02-20
**Status**: Draft
**Input**: Phase 1 specification from hackathon blueprint

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Vault Setup and Access (Priority: P1)

As a personal user, I want an Obsidian vault that serves as my AI Employee's central dashboard and memory, so that I can visually track my digital affairs and have a human-readable interface for all system activity.

**Why this priority**: The vault is the foundation of the entire system. Without it, no other components can function. It provides visibility, control, and accessibility to all AI Employee operations.

**Independent Test**: Can be tested by opening the vault in Obsidian and verifying Dashboard.md and Company_Handbook.md exist and display correctly with basic structure.

**Acceptance Scenarios**:

1. **Given** a newly created vault directory, **When** I open it in Obsidian, **Then** I see Dashboard.md with placeholder sections for bank balance, pending messages, and active projects
2. **Given** the vault contains Company_Handbook.md, **When** I open it, **Then** I see "Rules of Engagement" including politeness guidelines and approval thresholds (payments >$500)
3. **Given** the vault structure, **When** I navigate the folder tree, **Then** I see all required folders: /Needs_Action/, /Done/, /Agent_Skills/, /Logs/, /Accounting/

---

### User Story 2 - Watcher Monitoring (Priority: P1)

As a user, I want a watcher script that monitors either my Gmail or filesystem, so that new items (emails or file drops) are automatically detected and recorded without manual intervention.

**Why this priority**: Watchers provide the "perception" layer of the AI Employee. Without automated detection, the system cannot respond to external events. This is the minimum viable perception capability.

**Independent Test**: Can be tested by running the chosen watcher (Gmail or filesystem) in a terminal, triggering a new event (receiving an email or dropping a file), and verifying a corresponding .md file appears in /Needs_Action/.

**Acceptance Scenarios**:

1. **Given** the Gmail watcher is running with valid credentials, **When** an unread important email arrives, **Then** a formatted .md file appears in /Needs_Action/ with email headers, snippet, and suggested actions
2. **Given** the filesystem watcher is running, **When** a file is dropped into the monitored directory, **Then** the file is copied to /Needs_Action/files/ with a companion .md metadata file
3. **Given** either watcher is running, **When** no new items are detected, **Then** the watcher continues running without errors and logs "no new items" status

---

### User Story 3 - Claude Code Integration (Priority: P1)

As a user, I want Claude Code to be able to read and write files in the vault, so that the AI can process watcher-detected items and create responses or take actions.

**Why this priority**: Reading and writing to the vault is how Claude Code interacts with the system. Without this capability, watchers cannot trigger AI reasoning or actions.

**Independent Test**: Can be tested by manually running Claude Code with vault context, having it read a file from /Needs_Action/, and verifying it can write a response file to /Done/ with correct formatting.

**Acceptance Scenarios**:

1. **Given** a watcher-created .md file exists in /Needs_Action/, **When** I invoke Claude Code with vault context, **Then** Claude can read and parse the file content
2. **Given** Claude Code has processed an item, **When** it creates a response, **Then** a properly formatted .md file appears in /Done/ with action taken or notes added
3. **Given** Claude Code is operating, **When** it needs to reference AI logic, **Then** it uses only the pre-created Agent Skills from Agent_Skills/ folder

---

### Edge Cases

- What happens when the watcher loses network connectivity (Gmail) or the watched directory is deleted (filesystem)?
- How does the system handle malformed email content or corrupted files?
- What happens when /Needs_Action/ becomes extremely large (thousands of items)?
- How does Claude Code handle conflicting or duplicate items?
- What happens when vault files are manually edited while watchers are running?

## Requirements *(mandatory)*

### Constitutional Constraints
**GATE: All requirements MUST comply with constitution principles**

- [x] Document Adherence: Only Bronze Tier features from hackathon blueprint are included
- [x] Privacy & Security: No secrets (.env, tokens, credentials) stored in vault files
- [ ] Human-in-the-Loop: Not required in Bronze phase (deferred to Silver+)
- [ ] MCP Pattern: Not required in Bronze phase (deferred to Silver+)
- [x] Vault Structure: All files stay within defined folder structure (/phase-1/ for phase work, global folders for vault)
- [x] Agent Skills: All AI functionality implemented via Agent Skills only

### Functional Requirements

Vault Setup:
- **FR-001**: System MUST create an Obsidian-compatible vault with .md files
- **FR-002**: Dashboard.md MUST display placeholder sections for: bank balance, pending messages, active projects
- **FR-003**: Company_Handbook.md MUST contain "Rules of Engagement" with: politeness guidelines, approval threshold for payments >$500
- **FR-004**: System MUST create required folder structure: /Needs_Action/, /Done/, /Agent_Skills/, /Logs/, /Accounting/, /Plans/, /Pending_Approval/, /In_Progress/, /Updates/

Watcher Implementation (Choose ONE of following):
- **FR-005A**: GmailWatcher MUST connect to Gmail API using OAuth2 credentials stored locally (not in vault)
- **FR-005B**: FilesystemWatcher MUST monitor a specified directory using watchdog library
- **FR-006**: Chosen watcher MUST run continuously in background (terminal or daemon mode)
- **FR-007**: Watcher MUST create formatted .md files in /Needs_Action/ for each detected item
- **FR-008**: GmailWatcher-created files MUST include: email headers (From, To, Subject), snippet, suggested actions checkboxes
- **FR-009**: FilesystemWatcher-created files MUST include: original filename, file size, type, metadata, and copy of file in /Needs_Action/files/

Claude Code Integration:
- **FR-010**: Claude Code MUST be able to read .md files from /Needs_Action/
- **FR-011**: Claude Code MUST be able to write .md files to /Done/
- **FR-012**: All AI reasoning and decision logic MUST be invoked via Agent Skills (no inline prompts)
- **FR-013**: System MUST demonstrate end-to-end flow: watcher detects item → creates file → Claude reads → Claude writes response

### Key Entities

- **Vault Folder**: Root directory containing all AI Employee files and subfolders
- **Dashboard.md**: Human-readable summary showing current state (bank balance, pending messages, active projects)
- **Company_Handbook.md**: Rulebook containing engagement guidelines, approval thresholds, behavioral rules
- **Action Item**: .md file created by watcher representing a detected item (email, file drop) requiring processing
- **Agent Skill**: .md file in /Agent_Skills/ containing reusable AI logic/patterns

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Vault opens successfully in Obsidian with no errors
- **SC-002**: Dashboard.md displays all required sections (bank balance, pending messages, active projects)
- **SC-003**: Company_Handbook.md contains "Rules of Engagement" with politeness guidelines and >$500 approval threshold
- **SC-004**: Chosen watcher (Gmail OR filesystem) runs for 10+ minutes without crashing
- **SC-005**: Watcher detects at least 1 new item (email OR file drop) and creates corresponding .md file in /Needs_Action/
- **SC-006**: Created .md file in /Needs_Action/ contains all required metadata (headers, snippet, suggested actions for emails; filename, size, type for files)
- **SC-007**: Claude Code successfully reads the watcher-created file and responds with context-aware content
- **SC-008**: Claude Code writes a properly formatted .md file to /Done/ directory
- **SC-009**: All AI interactions use Agent Skills exclusively (no loose prompts or inline instructions)
- **SC-010**: Zero secrets (.env files, API tokens, credentials) present in vault files

## Assumptions

1. User has Python 3.11+ installed for watcher scripts
2. User has Obsidian installed for vault access
3. For GmailWatcher: user has Google Cloud project with Gmail API enabled and OAuth2 credentials
4. For FilesystemWatcher: user has a designated directory to monitor
5. User can run terminal commands to start watchers
6. Vault directory is on local filesystem (not network drive)
7. Claude Code is accessible and can be pointed to vault directory

## Constraints

1. **Scope**: Only Bronze Tier features - no scheduling, multi-watcher, social posting, Odoo, cloud deployment, Ralph Wiggum loop
2. **Phase Boundary**: All phase-specific work (specs, plans, code) stays in /phase-1/ folder
3. **No MCP Servers**: MCP servers are Silver+ feature - not used in Bronze
4. **No Human-in-Loop**: Approval workflow is Silver+ feature - not required in Bronze
5. **One Watcher Only**: Implement GmailWatcher OR FilesystemWatcher, not both
6. **Local-Only**: No cloud or remote operations in Bronze phase
7. **Agent Skills Only**: All AI logic must be in /Agent_Skills/ - no prompt engineering outside skills
8. **Privacy**: No credentials, tokens, or .env files in vault (must stay local-only)

## Out of Scope

The following features are explicitly EXCLUDED from Phase 1 (Bronze):

- WhatsApp watcher (Silver tier)
- Finance watcher (Gold tier)
- Social media posting (Gold tier)
- Odoo integration (Gold tier)
- Scheduling/cron jobs (Silver tier)
- Ralph Wiggum loop pattern (Silver tier)
- Human approval workflow (Silver tier)
- Cloud deployment (Platinum tier)
- Multi-watcher coordination (Silver tier)
- MCP server integration (Silver tier)
