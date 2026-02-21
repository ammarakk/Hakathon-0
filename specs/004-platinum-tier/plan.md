# Implementation Plan: Phase 4 - Platinum Tier (Always-On Cloud + Local Executive)

**Branch**: `004-platinum-tier` | **Date**: 2026-02-21 | **Spec**: [spec.md](../spec.md)
**Input**: Feature specification from `/phase-4/spec/spec.md`

---

## Summary

Phase 4 delivers the **Platinum Tier** - a production-ready, 24/7 AI Employee system combining cloud-based continuous operation with local executive control. The system achieves work-zone specialization: Cloud agents handle email triage, draft generation, and social scheduling (draft-only), while Local agents retain authority for approvals, WhatsApp sessions, banking, and final send/post actions. Communication flows through a Git-synced vault with claim-by-move coordination rules ensuring no duplicate work.

**Key Technical Decisions** (from research.md):
- **Cloud Platform**: Oracle Cloud Always Free VM (Ubuntu 22.04, 4 ARM CPUs, 24GB RAM)
- **Vault Sync**: Git with 30-second intervals, conflict detection, human resolution workflow
- **Secrets Isolation**: Multi-layered (gitignore + pre-sync audit + cloud env validation)
- **Odoo Deployment**: Odoo 16 Community + PostgreSQL 14 + Nginx + Let's Encrypt HTTPS
- **Health Monitoring**: HTTP `/health` endpoint + UptimeRobot external monitoring + systemd supervision

---

## Technical Context

**Language/Version**: Python 3.10+ (watchers, orchestrator, health server), Bash (deployment scripts)
**Primary Dependencies**: watchdog (filesystem monitoring), gmail-api, pyyaml, requests, flask (health endpoint)
**Storage**: PostgreSQL 14 (Odoo), Markdown files in vault (AI state)
**Testing**: pytest (unit), integration tests (cloud-local sync simulation)
**Target Platform**: Linux server (Ubuntu 22.04 on Oracle Cloud), Windows/macOS (local)
**Project Type**: Distributed system (cloud + local agents)
**Performance Goals**:
- Email triage: <5 minutes from arrival to draft
- Vault sync: <30 seconds (Git), <5 seconds (pending)
- Health endpoint: <200ms response time
- Cloud uptime: 99% over 7-day period
**Constraints**:
- Secrets NEVER on cloud (.env, tokens, sessions excluded from sync)
- All new AI functions as Agent Skills only
- Work stays in /phase-4/ (no modifications to Phases 1-3)
- Free tier cloud resources where possible
**Scale/Scope**:
- Single business owner context
- 5-10 watchers active simultaneously
- 100-1000 vault files synced daily
- 10-50 daily email/social actions

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Document Adherence**: Deliverables match hackathon Platinum Tier exactly (24/7 cloud, work-zone specialization, vault sync, Odoo cloud, secrets isolation) - no scope creep
- [x] **Privacy & Security**: Multi-layered secrets protection (gitignore, pre-sync audit, cloud env validation) - all secrets excluded from synced files
- [x] **Human-in-the-Loop**: Sensitive actions (sends, posts, payments) require `/Pending_Approval/` workflow - Local agent only
- [x] **MCP Pattern**: External actions use connected MCP servers (mcp_email, mcp_odoo, mcp_social_*) - draft → approve → execute pattern
- [x] **Ralph Wiggum Loop**: Multi-step tasks use Stop hook pattern for completion verification (inherited from Phase 3)
- [x] **Watcher-Triggered**: Architecture uses file drops in `/Needs_Action/` for triggers (inherited from Phase 1-3)
- [x] **Vault-Only R/W**: Claude Code reads/writes only to Obsidian vault structure - all state as markdown
- [x] **Incremental Phases**: Work stays in `/phase-4/`, Phases 1-3 remain untouched
- [x] **Agent Skills**: All new AI functionality implemented as Agent Skills (not new prompts)

**Status**: ✅ All gates PASSED - ready for implementation

---

## Project Structure

### Documentation (this feature)

```text
specs/004-platinum-tier/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (research & tech decisions)
├── data-model.md        # Phase 1 output (vault entities, state transitions)
├── quickstart.md        # Phase 1 output (setup & deployment guide)
├── contracts/           # Phase 1 output (vault format specifications)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Phase-4 Implementation

```text
phase-4/
├── spec/
│   ├── spec.md
│   └── checklists/
│       └── requirements.md
├── cloud/
│   ├── provision/
│   │   ├── oracle-cloud-setup.sh       # Initial VM provisioning
│   │   ├── install-dependencies.sh     # Python, Git, PostgreSQL, Nginx
│   │   └── security-hardening.sh       # Firewall, user permissions
│   ├── odoo/
│   │   ├── odoo-install.sh             # Odoo 16 Community setup
│   │   ├── nginx-ssl-setup.sh          # Reverse proxy + Let's Encrypt
│   │   ├── backup-script.sh            # Daily pg_dump cron
│   │   └── health-check.sh             # Odoo health monitoring
│   ├── agent/
│   │   ├── setup-agent.sh              # Clone repo, install Python deps
│   │   ├── systemd-units/
│   │   │   ├── ai-employee-orchestrator.service
│   │   │   ├── ai-employee-gmail-watcher.service
│   │   │   ├── ai-employee-filesystem-watcher.service
│   │   │   └── ai-employee-health.service
│   │   ├── health-server.py            # HTTP /health endpoint
│   │   └── sync-daemon.sh              # Git pull/push loop
│   └── config/
│       ├── cloud.env.example           # Non-sensitive config template
│       └── gitignore                   # Vault sync rules
├── local/
│   ├── agent/
│   │   ├── setup-local.sh              # Local agent setup
│   │   └── systemd-units/              # Local services (optional)
│   └── config/
│       └── local.env.example           # Full config template (with secrets)
├── vault/
│   ├── structure.md                    # Vault folder specification
│   ├── sync-setup.md                   # Git repository initialization
│   └── security-audit.sh               # Pre-sync secret scanner
├── tests/
│   ├── integration/
│   │   ├── test-cloud-local-sync.sh    # Vault sync test
│   │   ├── test-claim-by-move.sh       # Coordination test
│   │   └── test-secrets-isolation.sh   # Security validation
│   └── platinum-demo/
│       ├── test-offline-email.sh       # Full demo scenario
│       └── verification-checklist.md   # Acceptance criteria checklist
├── docs/
│   ├── cloud-deployment.md             # Deployment guide
│   ├── troubleshooting.md              # Common issues & solutions
│   └── migration-guide.md              # Phase 3 → Phase 4 migration
└── verification.md                     # Final deliverable proof
```

### Global Vault Structure (Updates Only)

```text
AI_Employee_Vault/
├── Needs_Action/
│   ├── personal/                       # NEW: Domain subfolder
│   └── business/                       # NEW: Domain subfolder
├── In_Progress/                        # NEW: Claim-by-move coordination
│   ├── cloud/                          # Cloud agent claims
│   └── local/                          # Local agent claims
├── Updates/                            # NEW: Cloud → local signals
└── Agent_Skills/                       # Existing: No modifications needed
```

**Structure Decision**: Distributed cloud + local architecture. Cloud agent runs on Oracle Cloud VM, local agent runs on user's machine. Both access same Git-synced vault. Phase-4 code stays isolated in `/phase-4/` except for minimal global vault structure updates (new folders only, no modifications to existing Phase 1-3 code).

---

## Complexity Tracking

> **No constitutional violations - this section intentionally left blank**
>
> All design decisions comply with constitutional principles. No complexity justification required.

---

## Phase 0: Research & Technology Decisions ✅ COMPLETE

**Status**: Complete - See `research.md`

**Deliverables**:
- ✅ Cloud provider selected (Oracle Always Free with Google e2-micro backup)
- ✅ Vault sync method chosen (Git with periodic pulls/pushes)
- ✅ Secrets isolation strategy defined (multi-layered protection)
- ✅ Cloud Odoo architecture designed (Odoo 16 + PostgreSQL + Nginx + Let's Encrypt)
- ✅ Health monitoring approach finalized (HTTP endpoint + UptimeRobot + systemd)
- ✅ Work-zone specialization implementation planned (environment-based roles)
- ✅ Claim-by-move coordination pattern specified (atomic filesystem moves)
- ✅ A2A messaging evaluated and deferred (P3 optional, skipped for MVP)

**Key Decisions**:
1. Oracle Cloud Always Free provides 24/7 VM with generous resources
2. Git sync offers built-in conflict detection and audit trail
3. Multi-layered secrets protection (gitignore + pre-sync audit + env validation)
4. Odoo 16 Community with Nginx reverse proxy and Let's Encrypt HTTPS
5. Simple HTTP health endpoint with external monitoring (UptimeRobot free)

**Risks Identified**:
- Cloud VM uptime <99%: Mitigated by reliable provider + local fallback
- Secrets leak to cloud: Mitigated by multi-layer protection + audits
- Git sync conflicts: Mitigated by clear resolution process
- Odoo migration data loss: Mitigated by full backup + staging test

---

## Phase 1: Design & Contracts

### 1.1 Data Model

**Output**: `data-model.md` - Vault entities, state transitions, validation rules

**Entities to Design**:

1. **Vault Task File** (`/Needs_Action/<domain>/task-*.md`)
   - Fields: task_id, domain, priority, created_at, source, content
   - State: Needs_Action → In_Progress → Pending_Approval → Done/Rejected
   - Validation: required fields, domain enum, priority range

2. **Claim File** (`/In_Progress/<agent>/task-*.md`)
   - Fields: original_task_id, claimed_by, claimed_at, status
   - Validation: agent name, timestamp format

3. **Approval File** (`/Pending_Approval/<domain>/draft-*.md`)
   - Fields: draft_id, domain, draft_type, created_by, content, approval_status
   - States: pending → approved/rejected/expired
   - Validation: required approval for sends/posts/payments

4. **Update Signal** (`/Updates/signal-*.md`)
   - Fields: signal_id, source_agent, timestamp, payload_type, content
   - Validation: timestamp format, payload schema

5. **Health Status** (HTTP `/health` response)
   - Fields: status, timestamp, last_activity, active_watchers, error_count, uptime_seconds
   - Validation: status enum (healthy/degraded/error)

6. **Sync State** (Git repository state)
   - Fields: last_sync_timestamp, conflict_count, file_count, sync_status
   - Validation: sync status enum (syncing/success/failed)

**State Transitions**:
```
Task: Needs_Action → In_Progress → Pending_Approval → Done/Rejected
Approval: pending → approved (executed) → Done
Approval: pending → rejected → Rejected
Approval: pending → expired (24h timeout) → Pending_Approval (stale)
Sync: idle → syncing → success/failed → idle
```

### 1.2 Contracts

**Output**: `contracts/` directory with interface specifications

**Contracts to Generate**:

1. **Vault Sync Contract** (`contracts/vault-sync.md`)
   - Git operations: pull, push, status, conflict detection
   - Sync interval: 30 seconds default
   - Conflict resolution: stop + log + human intervention
   - Security: pre-sync audit for secrets

2. **Claim-by-Move Contract** (`contracts/claim-by-move.md`)
   - Claim operation: atomic move from Needs_Action to In_Progress/<agent>/
   - Verification: check file existence before processing
   - Race condition handling: retry with backoff
   - Release operation: move from In_Progress to next state

3. **Health Endpoint Contract** (`contracts/health-endpoint.md`)
   - GET `/health` - returns JSON status
   - Response schema: {status, timestamp, last_activity, active_watchers, error_count, uptime_seconds}
   - Rate limit: 1 request/second, return 429 if exceeded
   - Status codes: 200 (healthy), 503 (degraded), 429 (rate limited)

4. **Work-Zone Contract** (`contracts/work-zone-separation.md`)
   - Cloud allowed actions: triage, draft, schedule
   - Local allowed actions: approve, send, post, whatsapp, banking
   - Action routing: if action not allowed, create draft instead
   - Fallback: write to `/Needs_Action/local-only/` if secret required

5. **Odoo MCP Contract** (`contracts/odoo-mcp.md`)
   - Draft operations (cloud): create_draft_invoice, create_draft_payment
   - Post operations (local): post_invoice, confirm_payment
   - Health check: check_odoo_connection
   - Error handling: log to `/Errors/odoo/`, graceful degradation

### 1.3 Quickstart Guide

**Output**: `quickstart.md` - Step-by-step setup for cloud + local deployment

**Sections**:
1. Prerequisites (Oracle Cloud account, domain name, local machine)
2. Cloud VM provisioning (run `oracle-cloud-setup.sh`)
3. Odoo installation and SSL setup (run `odoo-install.sh`, `nginx-ssl-setup.sh`)
4. Cloud agent setup (run `setup-agent.sh`, configure systemd services)
5. Vault sync initialization (run `sync-setup.md`)
6. Local agent setup (run `setup-local.sh`)
7. Verification steps (health check, sync test, platinum demo)

### 1.4 Agent Context Update

**Output**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Update**: Add Phase 4 technologies to agent context:
- Oracle Cloud Always Free VM
- Git-based vault synchronization
- Odoo 16 Community with PostgreSQL 14
- Nginx reverse proxy + Let's Encrypt
- systemd service management
- Health endpoint monitoring

---

## Phase 2: Architecture & Detailed Design

### 2.1 Cloud Deployment Architecture

**Components**:

1. **Provisioning Layer** (`cloud/provision/`)
   - `oracle-cloud-setup.sh`: Create VM, configure network, SSH access
   - `install-dependencies.sh`: Python 3.10, Git, PostgreSQL 14, Nginx
   - `security-hardening.sh`: UFW firewall, fail2ban, non-root user

2. **Odoo Layer** (`cloud/odoo/`)
   - `odoo-install.sh`: Odoo 16 Community from source, PostgreSQL config
   - `nginx-ssl-setup.sh`: Nginx reverse proxy, Let's Encrypt certbot
   - `backup-script.sh`: pg_dump to object storage, cron job
   - `health-check.sh`: Check Odoo port, database connection

3. **Agent Layer** (`cloud/agent/`)
   - `setup-agent.sh`: Clone repo, Python venv, install requirements
   - `health-server.py`: Flask HTTP server, /health endpoint, metrics
   - `sync-daemon.sh`: Git pull/push loop, 30-second interval
   - `systemd-units/`: Service definitions for orchestrator + watchers

4. **Configuration** (`cloud/config/`)
   - `cloud.env.example`: Template (watcher intervals, vault path, Odoo URL)
   - `gitignore`: Vault sync rules (.env, tokens, sessions excluded)

### 2.2 Local Agent Architecture

**Components**:

1. **Local Setup** (`local/agent/`)
   - `setup-local.sh`: Python venv, install requirements, Git config
   - `systemd-units/`: Optional local services (user-level systemd)

2. **Configuration** (`local/config/`)
   - `local.env.example`: Full template (includes secret placeholders)

### 2.3 Vault Sync Architecture

**Components**:

1. **Git Repository** (`vault/sync-setup.md`)
   - Initialize repo on cloud and local
   - Configure SSH keys for GitHub/GitLab
   - Set up .gitignore for secrets exclusion

2. **Sync Daemon** (`cloud/agent/sync-daemon.sh`)
   - Loop: git pull → git push → sleep 30
   - Conflict detection: git status exit code
   - On conflict: stop, log to `/Errors/sync/`, send alert

3. **Security Audit** (`vault/security-audit.sh`)
   - Pre-sync scan for secret patterns
   - Block push if secrets detected
   - Log violations to `/Errors/security/`

### 2.4 Work-Zone Specialization

**Implementation**:

1. **Environment-Based Roles**:
   ```bash
   # Cloud .env
   AGENT_ROLE=CLOUD
   ALLOWED_ACTIONS=triage,draft,schedule
   MCPS_ENABLED=mcp_odoo_draft

   # Local .env
   AGENT_ROLE=LOCAL
   ALLOWED_ACTIONS=approve,send,post,whatsapp,banking
   MCPS_ENABLED=mcp_email,mcp_odoo_post,mcp_social_*
   ```

2. **Action Router** (Agent Skill):
   ```python
   def route_action(action_type, params):
       if action_type in ALLOWED_ACTIONS:
           return execute(action_type, params)
       elif AGENT_ROLE == "CLOUD" and action_type in ["send", "post"]:
           # Cloud drafts, Local approves
           create_draft(params)
           write_to_pending_approval(params)
       else:
           raise ActionNotAllowed(f"{action_type} not allowed for {AGENT_ROLE}")
   ```

### 2.5 Health Monitoring Architecture

**Components**:

1. **Health Server** (`cloud/agent/health-server.py`)
   - Flask HTTP server on port 8080
   - GET /health: returns JSON status
   - Rate limiting: 1 req/sec
   - Metrics: status, last_activity, active_watchers, errors, uptime

2. **Systemd Services** (`cloud/agent/systemd-units/`)
   - `ai-employee-orchestrator.service`: Main orchestrator, Restart=always
   - `ai-employee-gmail-watcher.service`: Gmail watcher, Restart=on-failure
   - `ai-employee-filesystem-watcher.service`: File system watcher, Restart=on-failure
   - `ai-employee-health.service`: Health server, Restart=always

3. **External Monitoring**:
   - UptimeRobot free tier: 50 monitors, 5-minute intervals
   - Alert on 2 consecutive failures
   - Email/webhook notification

### 2.6 Platinum Demo Flow

**Scenario**: Email arrives offline → Cloud drafts → Local approves → Execute

**Steps**:

1. **Setup** (tests/platinum-demo/test-offline-email.sh):
   ```bash
   # 1. Start cloud agent
   ssh cloud-vm "sudo systemctl start ai-employee-*"

   # 2. Stop local agent (simulate offline)
   sudo systemctl stop ai-employee-*

   # 3. Send test email
   echo "Test urgent email" | send-test-email

   # 4. Wait for cloud processing
   sleep 300  # 5 minutes

   # 5. Verify draft in Pending_Approval
   cat AI_Employee_Vault/Pending_Approval/email/draft-*.md

   # 6. Start local agent
   sudo systemctl start ai-employee-*

   # 7. Approve draft
   echo "APPROVED" >> AI_Employee_Vault/Pending_Approval/email/draft-*.md

   # 8. Wait for execution
   sleep 60

   # 9. Verify in Done
   cat AI_Employee_Vault/Done/email/sent-*.md
   ```

2. **Verification** (tests/platinum-demo/verification-checklist.md):
   - [ ] Cloud agent processed email while local offline
   - [ ] Draft written to Pending_Approval
   - [ ] Local agent detected approval
   - [ ] Email sent via mcp_email
   - [ ] Task moved to Done
   - [ ] Dashboard.md updated

---

## Phase 3: Implementation Tasks

**Note**: Detailed tasks will be generated by `/sp.tasks` command

**High-Level Task Breakdown**:

1. **Cloud Infrastructure** (10-15 hours):
   - Provision Oracle Cloud VM
   - Install dependencies (Python, Git, PostgreSQL, Nginx)
   - Security hardening (firewall, fail2ban)
   - Configure networking and SSH access

2. **Odoo Cloud Deployment** (8-10 hours):
   - Install Odoo 16 Community
   - Configure PostgreSQL database
   - Set up Nginx reverse proxy
   - Configure Let's Encrypt HTTPS
   - Set up backup scripts and cron

3. **Vault Sync Setup** (6-8 hours):
   - Initialize Git repositories (cloud + local)
   - Configure SSH keys for GitHub/GitLab
   - Implement sync daemon (pull/push loop)
   - Create security audit script
   - Test sync and conflict resolution

4. **Agent Deployment** (10-12 hours):
   - Deploy cloud agent (orchestrator + watchers)
   - Configure systemd services
   - Implement health endpoint server
   - Deploy local agent (optional services)
   - Test work-zone specialization

5. **Health Monitoring** (4-6 hours):
   - Set up health endpoint (/health)
   - Configure external monitoring (UptimeRobot)
   - Test failure detection and auto-recovery
   - Configure alerting

6. **Testing & Verification** (8-10 hours):
   - Integration tests (sync, claim-by-move, secrets)
   - Platinum demo (offline email scenario)
   - Security audit (secrets isolation verification)
   - Performance testing (uptime, response times)
   - Documentation (verification.md)

**Total Estimated Effort**: 46-61 hours (within 60+ hour estimate)

---

## Phase 4: Deployment & Verification

### 4.1 Deployment Steps

1. **Cloud Deployment**:
   ```bash
   # 1. Provision VM
   ssh oracle-cloud "bash <(curl -s https://raw.githubusercontent.com/.../oracle-cloud-setup.sh)"

   # 2. Install dependencies
   ssh oracle-cloud "sudo bash install-dependencies.sh"

   # 3. Deploy Odoo
   ssh oracle-cloud "sudo bash odoo/odoo-install.sh"
   ssh oracle-cloud "sudo bash odoo/nginx-ssl-setup.sh"

   # 4. Deploy agent
   ssh oracle-cloud "bash cloud/agent/setup-agent.sh"
   ssh oracle-cloud "sudo systemctl enable ai-employee-*"
   ssh oracle-cloud "sudo systemctl start ai-employee-*"
   ```

2. **Local Deployment**:
   ```bash
   # 1. Setup local agent
   bash local/agent/setup-local.sh

   # 2. Configure vault sync
   cd AI_Employee_Vault
   git init
   git remote add origin <repo-url>
   ```

3. **Verification**:
   ```bash
   # Health check
   curl https://cloud-vm.example.com/health

   # Sync test
   echo "test" > AI_Employee_Vault/Needs_Action/test.md
   git push
   ssh cloud-vm "cd /vault && git pull"

   # Platinum demo
   bash tests/platinum-demo/test-offline-email.sh
   ```

### 4.2 Verification Deliverables

**Output**: `verification.md` with proof for all Platinum Tier deliverables:

1. **Cloud Uptime**:
   - Screenshot from UptimeRobot showing 99%+ uptime over 7 days
   - Health endpoint logs showing continuous operation

2. **Domain Specialization**:
   - Demo log: draft on cloud → approval on local → execute
   - Vault files showing cloud draft + local approval

3. **Vault Sync**:
   - Sync test log (file created on cloud → appears on local)
   - Git history showing bidirectional sync

4. **Secrets Isolation**:
   - Security audit script output: 0 secrets on cloud
   - Filesystem scan: no .env, tokens, sessions on cloud VM

5. **Odoo Cloud**:
   - HTTPS screenshot (browser showing padlock)
   - Backup log showing successful pg_dump
   - Health check log showing Odoo responding

6. **Platinum Demo**:
   - Full offline email demo log with timestamps
   - Vault file trail: Needs_Action → In_Progress → Pending_Approval → Done

7. **Dashboard.md**:
   - Screenshot showing cloud/local status
   - Updated timestamps reflecting recent activity

---

## Post-Implementation

### Maintenance

1. **Daily**:
   - Check health monitoring dashboard
   - Review sync logs for conflicts
   - Verify Odoo backups completed

2. **Weekly**:
   - Review cloud resource usage (CPU, RAM, bandwidth)
   - Audit vault for secrets (security script)
   - Update Dashboard.md summary

3. **Monthly**:
   - Review and rotate secrets (credentials)
   - Clean up old vault files (Done > 30 days)
   - Update dependencies (Python packages, Odoo)

### Troubleshooting

**Common Issues**:
- Sync conflicts: Stop agents, resolve manually in Git, restart
- Cloud VM down: Check Oracle Cloud console, restart VM if needed
- Health check failing: Check systemd logs, restart services
- Odoo connection failed: Check PostgreSQL, restart Odoo service

**Documentation**: `docs/troubleshooting.md` with detailed solutions

---

## Success Criteria Verification

| Criterion | Target | Verification Method |
|-----------|--------|---------------------|
| Cloud uptime | 99% over 7 days | UptimeRobot dashboard |
| Email triage time | <5 minutes | Timestamp analysis |
| Vault sync time | <30 seconds | Git log timestamps |
| Claim-by-move | 0 duplicate work | Audit vault files |
| Secrets isolation | 0 secrets on cloud | Security audit script |
| Human approval | 100% of sensitive actions | Vault file audit |
| Odoo availability | 99% over 7 days | Health check logs |
| Auto-recovery | <60 seconds | Kill agent test |
| Platinum demo | Complete in <10 min | Demo log |
| Dashboard updates | <1 minute after action | File timestamps |

---

## Next Steps

1. ✅ **Phase 0 Complete**: Research and technology decisions finalized
2. ✅ **Phase 1 Complete**: Data model, contracts, quickstart designed (this document)
3. **Next**: Run `/sp.tasks` to generate detailed task list with dependencies
4. **Then**: Execute tasks sequentially to implement Phase 4
5. **Final**: Create PR and run verification checklist

---

**Plan Status**: ✅ Complete - Ready for `/sp.tasks`

**Architecture Decision Detected**: Cloud platform selection (Oracle vs Google vs AWS vs Render vs Fly.io) and vault sync method (Git vs Syncthing) are significant choices with long-term consequences. Document reasoning and tradeoffs? Run `/sp.adr cloud-platform-selection` or `/sp.adr vault-sync-method` if you'd like to create ADRs for these decisions.
