# Feature Specification: Phase 4 - Platinum Tier (Always-On Cloud + Local Executive)

**Feature Branch**: `004-platinum-tier`
**Created**: 2026-02-21
**Status**: Draft
**Input**: Phase 4: Platinum Tier - Always-On Cloud + Local Executive (Production-ish AI Employee)

---

## Overview

Phase 4 delivers the **Platinum Tier** - a production-ready, always-on AI Employee system that combines cloud-based 24/7 operation with local executive control. This phase builds strictly on Phases 1-3 (Bronze, Silver, Gold) and represents the final tier in the hackathon blueprint.

The system achieves cloud/local work-zone specialization: Cloud agents handle continuous monitoring, triage, and draft generation, while Local agents retain executive authority for approvals, sensitive operations, and final send/post actions. Communication flows through a synced vault with claim-by-move coordination rules.

---

## User Scenarios & Testing

### User Story 1 - Cloud 24/7 Email Triage (Priority: P1)

As a business owner, I want my AI Employee to continuously monitor incoming emails even when my local machine is offline, so that time-sensitive communications are never missed and draft responses are ready for my review.

**Why this priority**: This is the core value proposition of Platinum Tier - continuous availability. Without 24/7 operation, the system provides no improvement over Phase 3.

**Independent Test**: Deploy cloud agent with Gmail watcher. Turn off local machine. Send test email. Verify cloud agent processes email and creates draft response in vault. Turn on local machine and verify draft appears in Pending_Approval.

**Acceptance Scenarios**:

1. **Given** Cloud agent is running and local machine is offline, **When** an important email arrives, **Then** Cloud agent triages the email, categorizes it by domain, writes a draft reply to `/Pending_Approval/email/`, and logs the action
2. **Given** Multiple emails arrive while offline, **When** local machine comes back online, **Then** All email drafts appear in Pending_Approval with proper timestamps and domain categorization
3. **Given** Cloud agent detects an urgent email (keywords: urgent, asap, deadline), **When** triage occurs, **Then** Email is flagged as HIGH_PRIORITY in the vault signal

---

### User Story 2 - Local Executive Approval Workflow (Priority: P1)

As a business owner, I want to review and approve all outgoing communications and financial actions before they execute, so that I maintain final control over my business reputation and finances.

**Why this priority**: Human-in-the-loop is a constitutional requirement. Without approval workflow, the system cannot safely operate autonomously.

**Independent Test**: Cloud agent creates draft email in Pending_Approval. Local agent detects pending approval. User approves via Dashboard.md or explicit approval file. Local agent executes send via MCP and moves to Done.

**Acceptance Scenarios**:

1. **Given** Draft email exists in `/Pending_Approval/email/draft-001.md`, **When** user approves by moving to `/Approved/` or adding approval stamp, **Then** Local agent executes send via mcp_email, logs result, moves file to `/Done/email/`
2. **Given** Draft social post exists in `/Pending_Approval/social/`, **When** user rejects by adding `REJECTED: [reason]` comment, **Then** Local agent does NOT execute send, moves file to `/Rejected/social/` with reason logged
3. **Given** User is offline, **When** approval deadline passes (default 24 hours), **Then** Item remains in Pending_Approval with EXPIRED flag (no auto-action)

---

### User Story 3 - Vault Sync with Claim-by-Move (Priority: P1)

As a distributed AI system, I want cloud and local agents to coordinate work through a synced vault without conflicts, so that multiple agents never work on the same task simultaneously.

**Why this priority**: Without coordination, multiple agents could duplicate work or corrupt vault state. This is foundational for all cloud-local cooperation.

**Independent Test**: Set up Git sync between cloud and local vaults. Create task in Needs_Action. Start both cloud and local agents. Verify only one agent claims task by moving to In_Progress. Verify other agents ignore claimed task.

**Acceptance Scenarios**:

1. **Given** Task exists in `/Needs_Action/email/`, **When** two agents attempt processing simultaneously, **Then** First agent to move file to `/In_Progress/<agent-name>/` owns the task, second agent skips file
2. **Given** Cloud agent writes update to `/Updates/cloud-signal-001.md`, **When** Git sync runs, **Then** Local agent receives update and merges into Dashboard.md without conflicts
3. **Given** Sync conflict occurs (both agents edit different sections), **When** merge happens, **Then** Git merge conflict is detected and logged to `/Errors/sync/` for human resolution

---

### User Story 4 - Cloud Odoo Integration (Priority: P2)

As a business owner, I want my cloud agent to draft accounting actions in Odoo for my later approval, so that financial records are continuously maintained even when I'm offline.

**Why this priority**: Extends 24/7 capability to accounting domain. P2 because it builds on P1 cloud/local pattern and requires cloud Odoo deployment.

**Independent Test**: Cloud agent detects transaction signal. Calls mcp_odoo to create draft invoice. Verify draft appears in Odoo (cloud) with state=draft. Local user approves. Local agent calls mcp_odoo to post invoice.

**Acceptance Scenarios**:

1. **Given** Cloud agent receives payment notification, **When** drafting accounting action, **Then** Creates draft invoice in Odoo via MCP, writes approval file to `/Pending_Approval/accounting/`
2. **Given** Draft invoice exists in Odoo, **When** local user approves, **Then** Local agent posts invoice via MCP, records transaction in vault, moves to Done
3. **Given** Cloud Odoo loses connection, **When** MCP call fails, **Then** Error is logged to `/Errors/odoo/`, graceful degradation activates, raw data saved to `/Needs_Action/accounting/` for retry

---

### User Story 5 - Health Monitoring & Recovery (Priority: P2)

As a system operator, I want to monitor cloud agent health and auto-recover from failures, so that the system maintains high uptime without manual intervention.

**Why this priority**: Production systems need observability and resilience. P2 because system can function with basic monitoring before full auto-recovery.

**Independent Test**: Deploy cloud agent with health endpoint. Configure external monitoring (UptimeRobot). Kill agent process. Verify monitoring detects failure. Verify auto-restart mechanism recovers agent.

**Acceptance Scenarios**:

1. **Given** Cloud agent is running, **When** health endpoint is called, **Then** Returns JSON with status: healthy, last_activity: timestamp, active_watchers: list
2. **Given** Agent crashes or becomes unresponsive, **When** failure is detected, **Then** Supervisor process restarts agent, logs incident to `/Errors/system/`, sends alert if configured
3. **Given** Watcher thread hangs, **When** health check detects timeout, **Then** Watcher is terminated and restarted, other watchers continue unaffected

---

### User Story 6 - Secrets Isolation (Priority: P1 - Security Gate)

As a security-conscious user, I want secrets (tokens, credentials, sessions) to NEVER be stored on cloud infrastructure, so that compromise of cloud VM exposes only non-sensitive operational data.

**Why this priority**: This is a critical security requirement. P1 because violation exposes sensitive credentials and violates constitutional privacy principle.

**Independent Test**: Audit cloud VM file system and environment variables. Verify no .env files, no tokens, no WhatsApp sessions, no banking credentials. Verify .gitignore blocks secrets. Test sync excludes secrets.

**Acceptance Scenarios**:

1. **Given** Cloud VM is provisioned, **When** file system is audited, **Then** No .env files, no credential files, no session tokens exist anywhere on cloud
2. **Given** Git sync runs, **When** pushing to remote, **Then** .env, .claude/, session files are in .gitignore and never pushed
3. **Given** Cloud agent needs credential for action, **When** attempting to use secret, **Then** Agent skips action, writes placeholder to `/Needs_Action/local-only/`, logs reason: "SECRET_REQUIRED_LOCAL"
4. **Given** Syncthing is configured (alternative to Git), **When** sync patterns are reviewed, **Then** .env, tokens, sessions are in ignore list, only .md and state files sync

---

### User Story 7 - Optional A2A Messaging Upgrade (Priority: P3)

As a system architect, I want to optionally upgrade some file handoffs to direct agent-to-agent messages, so that latency is reduced while vault remains the audit trail.

**Why this priority**: P3 because file-based vault coordination is fully functional. A2A is an optimization, not a requirement for Platinum Tier.

**Independent Test**: Configure A2A messaging between cloud and local agents. Send test message. Verify direct delivery. Verify action logged to vault. Verify fallback to file if A2A unavailable.

**Acceptance Scenarios**:

1. **Given** A2A is enabled, **When** cloud agent completes task, **Then** Sends direct message to local agent, writes summary to `/Updates/a2a-signal-001.md` as audit record
2. **Given** A2A message fails (network, recipient offline), **When** send fails, **Then** Falls back to file-based handoff in `/Needs_Action/`, logs failure reason
3. **Given** A2A and file-based both active, **When** audit trail is reviewed, **Then** All actions appear in vault regardless of communication method

---

### Edge Cases

- **Sync conflict**: What happens when both cloud and local agents edit the same vault file simultaneously?
  - *Resolution*: Git detects conflict, writes conflict markers, logs to `/Errors/sync/`, halts further processing until human resolves

- **Cloud offline**: What happens when cloud VM loses internet connectivity?
  - *Resolution*: Agents continue processing local data, queue outgoing actions, retry sync when connection restored

- **Local offline**: What happens when local machine is asleep/off during cloud activity?
  - *Resolution*: Cloud continues triage and drafting, writes to Pending_Approval, local processes queue on wake

- **Secret request on cloud**: What happens when cloud agent attempts action requiring credential?
  - *Resolution*: Action skipped, placeholder written to `/Needs_Action/local-only/` with "SECRET_REQUIRED_LOCAL" tag

- **Odoo cloud migration**: What happens to data when migrating from local Odoo (Phase 3) to cloud Odoo?
  - *Resolution*: pg_dump backup, restore to cloud Odoo, verify data integrity, update MCP server URL

- **Health check spam**: What happens if external monitoring pings health endpoint too frequently?
  - *Resolution*: Rate limit health checks (max 1/second), return 429 if exceeded

- **Vault drift**: What happens if cloud and local vaults diverge significantly?
  - *Resolution*: Sync fails with error, requires manual reconciliation, system halts vault writes until resolved

- ** watcher crash loop**: What happens if a watcher repeatedly crashes?
  - *Resolution*: After 3 crashes within 10 minutes, watcher is disabled, incident logged, alert sent if configured

---

## Requirements

### Constitutional Constraints
**GATE: All requirements MUST comply with constitution principles**

- [x] **Document Adherence**: No scope creep beyond Platinum Tier in hackathon blueprint
- [x] **Privacy & Security**: Secrets (.env, tokens, sessions) stay local-only, never on cloud
- [x] **Human-in-the-Loop**: Sensitive actions (sends, posts, payments) require `/Pending_Approval/` workflow
- [x] **MCP Pattern**: External actions use connected MCP servers (mcp_email, mcp_odoo, mcp_social_*)
- [x] **Vault Structure**: All files stay within defined folder structure (/Needs_Action, /In_Progress, /Pending_Approval, /Done, /Updates, /Errors)
- [x] **Agent Skills**: All new AI functionality implemented as Agent Skills in vault

### Functional Requirements

#### Cloud Deployment (FR-001 to FR-006)
- **FR-001**: System MUST deploy AI Employee to a Cloud VM or persistent runtime with 24/7 availability
- **FR-002**: Cloud VM MUST include all watchers (gmail_watcher, filesystem_watcher, scheduling), orchestrator script, and health monitoring
- **FR-003**: Cloud agent MUST provide HTTP health endpoint returning status, last activity timestamp, and active watchers
- **FR-004**: System MUST support external monitoring service integration (UptimeRobot or equivalent) for uptime proof
- **FR-005**: Cloud deployment MUST include auto-restart mechanism (supervisor, systemd, or container restart policy)
- **FR-006**: Cloud runtime MAY use free tier services (Oracle Always Free, Google e2-micro, AWS t4g.micro, Render worker, Fly.io) within published limits

#### Work-Zone Specialization (FR-007 to FR-013)
- **FR-007**: Cloud agent MUST own: Email triage, draft reply generation, social post drafting, post scheduling
- **FR-008**: Local agent MUST own: Approvals, WhatsApp session management, payments/banking, final "send/post" actions
- **FR-009**: Cloud agent MUST NOT execute send/post/payment actions directly
- **FR-010**: Local agent MUST NOT process raw email/social streams (only review drafts from cloud)
- **FR-011**: Cloud agent MUST write all output to vault folders: `/Needs_Action/<domain>/`, `/Plans/<domain>/`, `/Pending_Approval/<domain>/`, `/Updates/`
- **FR-012**: Local agent MUST be the single writer for `Dashboard.md` (cloud writes to `/Updates/`, local merges)
- **FR-013**: System MUST enforce domain ownership boundaries with validation checks before actions

#### Vault Sync & Coordination (FR-014 to FR-022)
- **FR-014**: System MUST synchronize vault between cloud and local using Git (recommended) or Syncthing
- **FR-015**: Sync MUST include only markdown and state files (.md, .json, .txt excluding secrets)
- **FR-016**: Sync MUST exclude: .env files, credential files, tokens, WhatsApp sessions, banking credentials
- **FR-017**: System MUST implement claim-by-move coordination: first agent to move item from `/Needs_Action/` to `/In_Progress/<agent>/` owns the task
- **FR-018**: Agents MUST check `/In_Progress/<agent>/` before claiming new tasks and skip already-claimed items
- **FR-019**: System MUST detect and handle sync conflicts by logging to `/Errors/sync/` and halting conflicting writes
- **FR-020**: Sync interval MUST be configurable (default: 30 seconds for Git, immediate for Syncthing)
- **FR-021**: System MUST verify vault consistency after sync (file count, critical files exist)
- **FR-022**: Sync failures MUST trigger graceful degradation: continue processing locally, retry sync, alert if persistent

#### Secrets Isolation (FR-023 to FR-028)
- **FR-023**: Cloud VM MUST NOT store .env files, credential files, tokens, WhatsApp sessions, or banking credentials
- **FR-024**: Git repository MUST have .gitignore rules blocking all secret files
- **FR-025**: Cloud agent attempting action requiring secret MUST skip action and write placeholder to `/Needs_Action/local-only/`
- **FR-026**: System MUST provide audit log proving no secrets on cloud (filesystem scan, git history check)
- **FR-027**: Local .env MUST contain all credentials needed for local-only actions
- **FR-028**: Cloud .env (if exists) MUST contain only non-sensitive config (watcher intervals, folder paths, MCP URLs without auth)

#### Odoo Cloud Integration (FR-029 to FR-035)
- **FR-029**: System MUST deploy Odoo Community on Cloud VM with HTTPS enabled
- **FR-030**: Cloud Odoo MUST have automated backups (cron pg_dump daily, retain 7 days)
- **FR-031**: Cloud Odoo MUST have health monitoring (HTTP response check, database connection test)
- **FR-032**: Cloud agent MUST integrate with Odoo via MCP for draft-only actions (create draft invoice, create draft payment)
- **FR-033**: Local agent MUST approve and post Odoo actions via MCP (post invoice, confirm payment)
- **FR-034**: System MUST migrate/integrate data from local Odoo (Phase 3) to cloud Odoo
- **FR-035**: Odoo MCP server MUST be configured for cloud URL with local-only credentials for posting actions

#### Health Monitoring & Recovery (FR-036 to FR-042)
- **FR-036**: System MUST provide HTTP health endpoint at `/health` returning JSON status
- **FR-037**: Health response MUST include: status (healthy/degraded), last_activity timestamp, active_watchers list, error_count
- **FR-038**: System MUST auto-restart crashed agents within 60 seconds
- **FR-039**: System MUST detect hung watchers (no activity for 5 minutes) and restart them
- **FR-040**: System MUST disable watchers after 3 crashes within 10 minutes and log incident
- **FR-041**: Health endpoint MUST rate limit requests (max 1/second, return 429 if exceeded)
- **FR-042**: System MUST log all incidents to `/Errors/system/` with timestamp, error details, recovery action

#### Platinum Demo Scenario (FR-043 to FR-047)
- **FR-043**: System MUST demonstrate: Email arrives offline → Cloud drafts reply → Writes approval file → User approves → Local executes send → Logs → Moves to Done
- **FR-044**: Cloud agent MUST generate contextually appropriate draft replies based on email content and business context
- **FR-045**: Approval file MUST include: original email summary, draft reply content, metadata (timestamp, domain, priority)
- **FR-046**: Local send MUST use mcp_email MCP server with proper error handling and retry
- **FR-047**: Dashboard.md MUST reflect completed action with cloud contribution acknowledged

#### Optional A2A Upgrade (FR-048 to FR-052)
- **FR-048**: [OPTIONAL] System MAY support direct agent-to-agent messaging for some handoffs
- **FR-049**: If A2A enabled, system MUST maintain vault as primary audit trail (all actions logged to `/Updates/a2a-*.md`)
- **FR-050**: A2A MUST fall back to file-based handoff if message delivery fails
- **FR-051**: File-based coordination MUST remain primary functional path (A2A is optimization only)
- **FR-052**: System MUST allow disabling A2A via configuration flag

#### Agent Skills Requirement (FR-053)
- **FR-053**: All new AI functionality introduced in Phase 4 MUST be implemented exclusively as Agent Skills in `.claude/commands/` folder

---

## Key Entities

- **Vault Folder Structure**: Distributed file-based coordination system with subfolders for different states (Needs_Action, In_Progress, Pending_Approval, Done, Updates, Errors)
  - Attributes: Folder path, domain subfolders, state files, ownership rules
  - Relationships: Synced between cloud and local via Git/Syncthing

- **Task Claim**: File moved from Needs_Action to In_Progress to establish ownership
  - Attributes: Task ID, claiming agent name, claim timestamp, file path
  - Relationships: One task has one claiming agent, prevents duplicate work

- **Approval File**: File in Pending_Approval awaiting human decision
  - Attributes: Draft content, approval type (email/social/payment), timestamp, priority, domain
  - Relationships: Created by cloud (or local), consumed by local executive, moves to Done or Rejected

- **Health Status**: JSON response from health endpoint
  - Attributes: status, last_activity, active_watchers, error_count, uptime_seconds
  - Relationships: Monitored by external service, triggers recovery actions

- **Sync State**: Git repository or Syncthing folder state
  - Attributes: Last sync timestamp, conflict count, file count, sync status
  - Relationships: Shared between cloud and local, must be consistent for operations

- **Signal File**: Update file written by cloud to be merged into Dashboard.md by local
  - Attributes: Signal type, timestamp, agent name, content payload
  - Relationships: Cloud writes, local reads and merges, single-writer rule for Dashboard.md

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Cloud agent maintains 99% uptime over 7-day period (measured by external health monitoring)
- **SC-002**: Email triage and draft generation completes within 5 minutes of email arrival during cloud operation
- **SC-003**: Vault sync completes within 30 seconds (Git) or 5 seconds (Syncthing) with 99.9% success rate
- **SC-004**: Claim-by-move coordination prevents duplicate work (0 incidents of two agents processing same task in 7-day test)
- **SC-005**: Secrets isolation verified via security audit: 0 credential files found on cloud VM
- **SC-006**: Human approval workflow processes 100% of sensitive actions with user consent before execution
- **SC-007**: Cloud Odoo responds to health checks within 2 seconds, 99% uptime over 7-day period
- **SC-008**: Auto-recovery restores crashed agents within 60 seconds, 95% success rate
- **SC-009**: Platinum demo scenario completes end-to-end in under 10 minutes (offline → cloud draft → approve → send)
- **SC-010**: Dashboard.md accurately reflects both cloud and local activity with updated timestamps within 1 minute of action

### Quality Gates

- **GATE-1**: All Gold Tier (Phase 3) functionality remains intact and functional
- **GATE-2**: No secrets (credentials, tokens, sessions) present on cloud infrastructure (verified by audit)
- **GATE-3**: Cloud/local work-zone boundaries enforced (no cloud executes send/post/payment)
- **GATE-4**: Vault sync reliable with conflict detection and recovery
- **GATE-5**: Health monitoring and auto-recovery operational
- **GATE-6**: All Phase 4 AI functions implemented as Agent Skills

---

## Assumptions

1. Cloud platform: Free tier VM available (Oracle Always Free preferred for 24/7, alternatives: Google e2-micro, AWS t4g.micro, Render worker, Fly.io)
2. Git repository hosting available (GitHub, GitLab, or self-hosted) for vault sync
3. Domain name available for Odoo HTTPS (or use IP with self-signed cert for testing)
4. Local machine has Claude Code with agent skills from Phases 1-3 installed
5. MCP servers (mcp_email, mcp_odoo, mcp_social_*) are configured and accessible
6. User has basic familiarity with Git for conflict resolution (if needed)
7. Cloud VM has sufficient resources for watchers + orchestrator + Odoo (minimum: 1GB RAM, 10GB disk for testing)
8. Network connectivity exists between cloud and local for Git/Syncthing sync
9. User accepts that A2A messaging is optional and file-based coordination is primary
10. Platinum demo can be simulated with test email if production email unavailable

---

## Dependencies

### External Dependencies
- Cloud VM provider (Oracle Cloud, Google Cloud, AWS, Render, or Fly.io)
- Git hosting service (GitHub, GitLab, or equivalent)
- External monitoring service (UptimeRobot, Pingdom, or equivalent) - free tier sufficient
- SSL certificate for Odoo HTTPS (Let's Encrypt free or cloud provider certs)

### Phase Dependencies
- **Phase 1 (Bronze)**: Base agent skills, vault structure, Gmail watcher, human-in-loop
- **Phase 2 (Silver)**: A2A messaging capability (optional upgrade), MCP patterns
- **Phase 3 (Gold)**: Odoo integration, social posting, weekly audit, all watchers functional

### Internal Dependencies
- All Gold Tier deliverables must remain intact
- Existing MCP servers must be reconfigured for cloud Odoo URL
- Git repository must be initialized with vault folder structure
- Cloud VM must have Python/runtime environment for agents and Odoo

---

## Out of Scope

The following are explicitly OUT OF SCOPE for Phase 4:

- New agent functionality beyond Platinum Tier requirements (no new tiers)
- Mobile app or web UI for approvals (Dashboard.md remains primary interface)
- Multi-user support (single business owner context maintained)
- Advanced A2A orchestration (file-based remains primary, A2A is optional enhancement)
- Cloud-to-cloud multi-region deployment (single cloud VM, single local machine)
- Real-time streaming notifications (email polling intervals maintained from Phase 3)
- Advanced authentication/authorization for vault (local file system permissions only)
- Automated conflict resolution without human intervention (conflicts require manual resolution)
- Migration tools from other AI employee systems (greenfield build on Phases 1-3)
- Paid monitoring services (free tiers sufficient for health checks)
- High-availability Odoo deployment (single instance with backups, no clustering)
