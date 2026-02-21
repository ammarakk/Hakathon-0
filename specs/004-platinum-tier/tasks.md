# Implementation Tasks: Phase 4 - Platinum Tier

**Feature**: Phase 4 - Always-On Cloud + Local Executive
**Branch**: `004-platinum-tier`
**Total Tasks**: 87
**Estimated Effort**: 46-61 hours

---

## Task Legend

- `- [ ]` = Pending task
- `T###` = Sequential task ID
- `[P]` = Parallelizable (can run simultaneously with other `[P]` tasks)
- `[US#]` = User Story mapping (US1-US7 from spec.md)

---

## Phase 1: Setup & Infrastructure (6 tasks, ~4 hours)

**Goal**: Provision cloud VM and prepare base infrastructure

**Acceptance**: Cloud VM running with Python, Git, SSH access verified

- [ ] T001 Create Oracle Cloud account and provision VM (4 ARM CPUs, 24GB RAM, Ubuntu 22.04)
  - **File**: `phase-4/cloud/provision/oracle-cloud-setup.sh`
  - **Proof**: VM public IP assigned, SSH login successful

- [ ] T002 Configure networking rules (firewall: SSH port 22, HTTP 80, HTTPS 443, Health 8080, Odoo 8069)
  - **File**: `phase-4/cloud/provision/security-hardening.sh`
  - **Proof**: `nmap` shows only allowed ports open

- [ ] T003 Install base dependencies (Python 3.10+, Git 2.34+, PostgreSQL 14, Nginx 1.18+)
  - **File**: `phase-4/cloud/provision/install-dependencies.sh`
  - **Proof**: `python3 --version`, `git --version`, `psql --version`, `nginx -v` all return expected versions

- [ ] T004 [P] Setup SSH key authentication for GitHub/GitLab access
  - **File**: `~/.ssh/id_ed25519` on cloud VM
  - **Proof**: `ssh -T git@github.com` returns successful authentication

- [ ] T005 [P] Create vault directory structure on cloud (`/vault`, `/vault/Needs_Action/`, `/vault/In_Progress/`, etc.)
  - **File**: `phase-4/vault/structure.md`
  - **Proof**: All folders exist with correct permissions

- [ ] T006 Clone repository to cloud VM and verify Phase 1-3 code present
  - **File**: `/opt/ai-employee/` on cloud
  - **Proof**: Agent Skills from Phases 1-3 accessible

---

## Phase 2: Foundational Components (8 tasks, ~6 hours)

**Goal**: Implement shared services required by all user stories

**Dependencies**: Phase 1 complete

**Acceptance**: Health endpoint running, systemd services configured, Git repo initialized

- [ ] T007 Create health endpoint HTTP server (Flask, returns JSON status on port 8080)
  - **File**: `phase-4/cloud/agent/health-server.py`
  - **Proof**: `curl http://localhost:8080/health` returns `{"status":"healthy",...}`

- [ ] T008 [P] Create systemd unit for health service with auto-restart
  - **File**: `phase-4/cloud/agent/systemd-units/ai-employee-health.service`
  - **Proof**: `systemctl status ai-employee-health` shows active (running)

- [ ] T009 [P] Create systemd unit for orchestrator service
  - **File**: `phase-4/cloud/agent/systemd-units/ai-employee-orchestrator.service`
  - **Proof**: Service enabled and starts on boot

- [ ] T010 [P] Create systemd unit for Gmail watcher service
  - **File**: `phase-4/cloud/agent/systemd-units/ai-employee-gmail-watcher.service`
  - **Proof**: Service configured with Restart=on-failure

- [ ] T011 [P] Create systemd unit for filesystem watcher service
  - **File**: `phase-4/cloud/agent/systemd-units/a-employee-filesystem-watcher.service`
  - **Proof**: Service configured with Restart=on-failure

- [ ] T012 Initialize Git repository for vault sync (local and cloud)
  - **File**: `/vault/.git/` and `AI_Employee_Vault/.git/`
  - **Proof**: `git status` works on both cloud and local

- [ ] T013 Create `.gitignore` excluding all secrets (.env, *.session, *.token, *.cred, .claude/)
  - **File**: `/vault/.gitignore` and `AI_Employee_Vault/.gitignore`
  - **Proof**: `git check-ignore .env` returns `.env`

- [ ] T014 Create GitHub/GitLab private repository for vault sync
  - **File**: Remote repository URL
  - **Proof**: `git remote -v` shows origin URL

---

## Phase 3: US1 - Cloud 24/7 Email Triage (10 tasks, ~8 hours)

**Priority**: P1 (Critical)
**Goal**: Cloud agent processes emails offline and creates drafts for approval

**Dependencies**: Phase 2 complete

**Independent Test**: Turn off local machine, send test email, verify draft in Pending_Approval

- [ ] T015 [US1] Create cloud environment configuration (`AGENT_ROLE=CLOUD`, `ALLOWED_ACTIONS=triage,draft,schedule`)
  - **File**: `phase-4/cloud/config/cloud.env`
  - **Proof**: `grep AGENT_ROLE cloud.env` returns `CLOUD`

- [ ] T016 [US1] Create cloud agent setup script (Python venv, install requirements)
  - **File**: `phase-4/cloud/agent/setup-agent.sh`
  - **Proof**: Venv created, dependencies installed

- [ ] T017 [P] [US1] Configure Gmail watcher for cloud (API credentials, label watching)
  - **File**: `phase-4/cloud/config/gmail-watcher-config.json`
  - **Proof**: Watcher connects to Gmail API

- [ ] T018 [P] [US1] Create email triage skill (classify emails by domain and priority)
  - **File**: `AI_Employee_Vault/Agent_Skills/email_triage_skill.md`
  - **Proof**: Skill processes email and outputs domain/priority

- [ ] T019 [US1] Implement draft reply generation (context-aware, no send)
  - **File**: `AI_Employee_Vault/Agent_Skills/draft_reply_skill.md`
  - **Proof**: Generated draft saved to `/Pending_Approval/email/`

- [ ] T020 [US1] Create urgent keyword detection (urgent, asap, deadline → HIGH_PRIORITY flag)
  - **File**: `phase-4/cloud/agent/urgent_detector.py`
  - **Proof**: Email with "urgent" tagged HIGH_PRIORITY

- [ ] T021 [US1] Configure cloud orchestrator to process emails and write drafts only (no send)
  - **File**: `phase-4/cloud/agent/orchestrator.py`
  - **Proof**: Orchestrator skips send actions, creates drafts

- [ ] T022 [US1] Deploy and start cloud agent services (orchestrator + watchers)
  - **File**: Systemd services active
  - **Proof**: `systemctl status ai-employee-*` shows all running

- [ ] T023 [US1] Test offline email processing: Stop local, send email, verify draft created
  - **File**: `phase-4/tests/us1-offline-email-test.sh`
  - **Proof**: Draft exists in `/Pending_Approval/email/` with timestamp

- [ ] T024 [US1] Verify multiple emails batched correctly while offline
  - **File**: Test results log
  - **Proof**: Multiple drafts in Pending_Approval with proper timestamps

---

## Phase 4: US2 - Local Executive Approval Workflow (9 tasks, ~6 hours)

**Priority**: P1 (Critical)
**Goal**: Local agent reviews drafts, executes approvals via MCP

**Dependencies**: Phase 3 complete (cloud creates drafts)

**Independent Test**: Cloud creates draft, local approves, action executed via MCP

- [ ] T025 [US2] Create local environment configuration (`AGENT_ROLE=LOCAL`, `ALLOWED_ACTIONS=approve,send,post`)
  - **File**: `phase-4/local/config/local.env`
  - **Proof**: `grep AGENT_ROLE local.env` returns `LOCAL`

- [ ] T026 [P] [US2] Create approval watcher skill (monitor `/Pending_Approval/` for changes)
  - **File**: `AI_Employee_Vault/Agent_Skills/approval_watcher_skill.md`
  - **Proof**: Watcher detects new approval files

- [ ] T027 [P] [US2] Create approval parser (read APPROVED/REJECTED stamps from files)
  - **File**: `phase-4/local/agent/approval_parser.py`
  - **Proof**: Parser extracts approval status correctly

- [ ] T028 [US2] Configure mcp_email integration on local (credentials in local .env only)
  - **File**: `phase-4/local/config/mcp-email-config.json`
  - **Proof**: MCP server connects, sends test email

- [ ] T029 [US2] Create email send executor (via mcp_email after approval)
  - **File**: `AI_Employee_Vault/Agent_Skills/email_send_skill.md`
  - **Proof**: Approved draft sent, logged to Done

- [ ] T030 [US2] Create rejection handler (move to `/Rejected/` with reason logged)
  - **File**: `phase-4/local/agent/rejection_handler.py`
  - **Proof**: Rejected draft moves to Rejected folder

- [ ] T031 [US2] Implement approval timeout (24h expiry, EXPIRED flag)
  - **File**: `phase-4/local/agent/approval_timeout.py`
  - **Proof**: Draft older than 24h marked EXPIRED

- [ ] T032 [US2] Configure local orchestrator to process approvals and execute via MCP
  - **File**: `phase-4/local/agent/orchestrator.py`
  - **Proof**: Orchestrator reads approvals, calls MCP, moves to Done

- [ ] T033 [US2] Test approval workflow: Cloud draft → Local approve → Send via MCP
  - **File**: `phase-4/tests/us2-approval-test.sh`
  - **Proof**: Email sent, file in `/Done/email/`, log entry present

---

## Phase 5: US3 - Vault Sync with Claim-by-Move (12 tasks, ~8 hours)

**Priority**: P1 (Critical)
**Goal**: Git-based vault sync with claim-by-move coordination

**Dependencies**: Phase 2 complete

**Independent Test**: Create task, both agents start, only one claims it

- [ ] T034 [US3] Create sync daemon script (git pull → git push loop, 30s interval)
  - **File**: `phase-4/cloud/agent/sync-daemon.sh`
  - **Proof**: Daemon runs, syncs every 30 seconds

- [ ] T035 [P] [US3] Create pre-sync security audit script (scan for secrets before push)
  - **File**: `phase-4/vault/security-audit.sh`
  - **Proof**: Script detects .env files, blocks push

- [ ] T036 [P] [US3] Implement conflict detection (check git exit code, log to `/Errors/sync/`)
  - **File**: `phase-4/cloud/agent/conflict_detector.py`
  - **Proof**: Sync conflict logged, processing stops

- [ ] T037 [US3] Create claim-by-move skill (atomic rename from Needs_Action to In_Progress)
  - **File**: `AI_Employee_Vault/Agent_Skills/claim_task_skill.md`
  - **Proof**: File moved atomically, claim recorded

- [ ] T038 [US3] Create claim verification skill (check file still claimed before processing)
  - **File**: `AI_Employee_Vault/Agent_Skills/verify_claim_skill.md`
  - **Proof**: Returns false if file no longer in In_Progress

- [ ] T039 [US3] Implement agent claim loop (check Needs_Action, claim with retry backoff)
  - **File**: `phase-4/cloud/agent/claim_loop.py`
  - **Proof**: Agent claims tasks, backs off on conflicts

- [ ] T040 [US3] Create domain subfolders (`/Needs_Action/personal/`, `/Needs_Action/business/`, etc.)
  - **File**: Vault directory structure
  - **Proof**: All domain folders exist on cloud and local

- [ ] T041 [P] [US3] Create `/In_Progress/cloud/` and `/In_Progress/local/` folders
  - **File**: Vault directory structure
  - **Proof**: Agent folders exist

- [ ] T042 [US3] Implement single-writer Dashboard.md rule (local only, cloud writes to Updates)
  - **File**: `phase-4/local/agent/dashboard_merger.py`
  - **Proof**: Cloud writes to `/Updates/`, local merges to Dashboard.md

- [ ] T043 [US3] Create update signal merge skill (consolidate `/Updates/` into Dashboard.md)
  - **File**: `AI_Employee_Vault/Agent_Skills/merge_updates_skill.md`
  - **Proof**: Updates merged, signal files marked Merged=true

- [ ] T044 [US3] Test bidirectional sync: Create file on cloud, verify appears on local
  - **File**: `phase-4/tests/integration/test-cloud-local-sync.sh`
  - **Proof**: File content matches, timestamps correct

- [ ] T045 [US3] Test claim-by-move: Two agents, one task, verify only one claims
  - **File**: `phase-4/tests/integration/test-claim-by-move.sh`
  - **Proof**: Task in only one In_Progress folder, no duplicates

---

## Phase 6: US6 - Secrets Isolation (8 tasks, ~5 hours)

**Priority**: P1 (Security Gate)
**Goal**: Multi-layered secrets protection, cloud VM has zero secrets

**Dependencies**: Phase 5 complete (sync configured)

**Independent Test**: Audit cloud VM, verify no .env/tokens/sessions

- [ ] T046 [US6] Audit cloud VM filesystem for secrets (find .env, *.session, *.token, *.cred)
  - **File**: `phase-4/tests/security-audit.sh`
  - **Proof**: Scan returns 0 secret files

- [ ] T047 [P] [US6] Verify .gitignore blocks all secret patterns on cloud
  - **File**: `/vault/.gitignore`
  - **Proof**: `git check-ignore` blocks all secret patterns

- [ ] T048 [P] [US6] Verify .gitignore blocks all secret patterns on local
  - **File**: `AI_Employee_Vault/.gitignore`
  - **Proof**: `git check-ignore` blocks all secret patterns

- [ ] T049 [US6] Test pre-sync audit: Attempt to add .env to Git, verify blocked
  - **File**: `phase-4/tests/security/pre-sync-test.sh`
  - **Proof**: Pre-commit hook rejects .env files

- [ ] T050 [US6] Configure cloud .env with non-sensitive config only (no credentials)
  - **File**: `phase-4/cloud/config/cloud.env.example`
  - **Proof**: File contains URLs and intervals, no tokens/passwords

- [ ] T051 [US6] Configure local .env with full credentials (WhatsApp, banking, MCP tokens)
  - **File**: `phase-4/local/config/local.env.example`
  - **Proof**: File contains credential placeholders

- [ ] T052 [US6] Test cloud action requiring secret: Verify skipped, writes to `/Needs_Action/local-only/`
  - **File**: `phase-4/tests/security/secret-required-test.sh`
  - **Proof`: Action skipped, placeholder file created with SECRET_REQUIRED_LOCAL tag

- [ ] T053 [US6] Run full security audit: Verify 0 secrets on cloud, all secrets local-only
  - **File**: `phase-4/verification/security-audit-report.md`
  - **Proof**: Audit report shows clean cloud, secrets isolated locally

---

## Phase 7: US4 - Cloud Odoo Integration (10 tasks, ~8 hours)

**Priority**: P2 (Important)
**Goal**: Odoo on cloud with HTTPS, draft-only MCP integration

**Dependencies**: Phase 6 complete (secrets isolated, can safely deploy Odoo)

**Independent Test**: Cloud creates draft invoice, local approves, invoice posted

- [ ] T054 [US4] Install Odoo 16 Community on cloud VM (from source, PostgreSQL backend)
  - **File**: `phase-4/cloud/odoo/odoo-install.sh`
  - **Proof**: Odoo accessible on `http://localhost:8069`

- [ ] T055 [P] [US4] Configure PostgreSQL database for Odoo (user, password, database)
  - **File**: PostgreSQL configuration
  - **Proof**: Odoo connects to database successfully

- [ ] T056 [P] [US4] Create Nginx reverse proxy configuration for Odoo
  - **File**: `/etc/nginx/sites-available/odoo`
  - **Proof**: Nginx proxies to Odoo port 8069

- [ ] T057 [US4] Setup Let's Encrypt SSL certificate for Odoo domain
  - **File**: `phase-4/cloud/odoo/nginx-ssl-setup.sh`
  - **Proof**: `https://odoo-domain.com` shows padlock, valid certificate

- [ ] T058 [US4] Create Odoo backup script (pg_dump daily, retain 7 days)
  - **File**: `phase-4/cloud/odoo/backup-script.sh`
  - **Proof**: Cron job installed, backup file created

- [ ] T059 [US4] Create Odoo health check script (check port 8069, database connection)
  - **File**: `phase-4/cloud/odoo/health-check.sh`
  - **Proof**: Script returns success when Odoo running

- [ ] T060 [US4] Configure mcp_odoo for cloud (draft-only mode: create_draft_invoice)
  - **File**: `phase-4/cloud/config/mcp-odoo-config.json`
  - **Proof**: MCP connects, creates draft invoice

- [ ] T061 [US4] Configure mcp_odoo for local (post mode: post_invoice, confirm_payment)
  - **File**: `phase-4/local/config/mcp-odoo-config.json`
  - **Proof**: MCP connects, posts draft invoice

- [ ] T062 [US4] Create Odoo draft invoice skill (cloud agent, writes to `/Pending_Approval/accounting/`)
  - **File**: `AI_Employee_Vault/Agent_Skills/odoo_draft_invoice_skill.md`
  - **Proof**: Draft invoice created, approval file written

- [ ] T063 [US4] Test Odoo flow: Cloud draft → Local approve → Invoice posted
  - **File**: `phase-4/tests/us4-odoo-test.sh`
  - **Proof**: Draft in Odoo, approved, posted, logged to Done

---

## Phase 8: US5 - Health Monitoring & Recovery (8 tasks, ~5 hours)

**Priority**: P2 (Important)
**Goal**: Auto-restart, health endpoint, external monitoring

**Dependencies**: Phase 7 complete (Odoo deployed, need monitoring)

**Independent Test**: Kill agent, verify auto-restart within 60 seconds

- [ ] T064 [US5] Configure external monitoring service (UptimeRobot free tier)
  - **File**: UptimeRobot account setup
  - **Proof**: Monitor configured for `/health` endpoint

- [ ] T065 [P] [US5] Implement health endpoint rate limiting (1 req/sec, return 429 if exceeded)
  - **File**: `phase-4/cloud/agent/health-server.py` (rate limit middleware)
  - **Proof**: Rapid requests return 429 after first

- [ ] T066 [P] [US5] Add watcher timeout detection (5 min inactivity = hung, restart watcher)
  - **File**: `phase-4/cloud/agent/watcher_health_monitor.py`
  - **Proof**: Hung watcher detected, restarted, other watchers unaffected

- [ ] T067 [US5] Configure systemd Restart=always for all services
  - **File**: Systemd unit files
  - **Proof**: `systemctl show ai-employee-orchestrator | grep Restart` shows `always`

- [ ] T068 [US5] Implement crash counter (3 crashes in 10 min = disable watcher, log incident)
  - **File**: `phase-4/cloud/agent/crash_counter.py`
  - **Proof**: Watcher disabled after 3 crashes, incident logged

- [ ] T069 [US5] Create health status aggregation (status, last_activity, active_watchers, error_count, uptime)
  - **File**: `phase-4/cloud/agent/health_aggregator.py`
  - **Proof**: `/health` returns all required fields

- [ ] T070 [US5] Test auto-restart: Kill orchestrator, verify restart within 60 seconds
  - **File**: `phase-4/tests/us5-autorestart-test.sh`
  - **Proof**: Service restarts, uptime counter resets

- [ ] T071 [US5] Test external monitoring: Verify UptimeRobot pings, alerts on failure
  - **File**: `phase-4/tests/us5-external-monitoring-test.sh`
  - **Proof**: Monitor dashboard shows uptime history

---

## Phase 9: US7 - Optional A2A Messaging Upgrade (6 tasks, ~4 hours)

**Priority**: P3 (Optional)
**Goal**: Direct agent-to-agent messaging with vault audit trail

**Dependencies**: Phase 5 complete (file-based coordination working)

**Note**: Only implement if time permits (P3 = optional)

- [ ] T072 [US7] Design A2A message protocol (HTTP POST between cloud and local)
  - **File**: `phase-4/docs/a2a-protocol.md`
  - **Proof**: Protocol specifies message format, endpoints, error handling

- [ ] T073 [P] [US7] Create A2A message receiver on local (HTTP server, authenticated)
  - **File**: `phase-4/local/agent/a2a_receiver.py`
  - **Proof**: Server accepts POST on `/api/a2a/messages`

- [ ] T074 [P] [US7] Create A2A message sender on cloud (POST to local endpoint)
  - **File**: `phase-4/cloud/agent/a2a_sender.py`
  - **Proof**: Cloud sends message, local receives

- [ ] T075 [US7] Implement A2A → vault audit trail (write all messages to `/Updates/a2a-*.md`)
  - **File**: `phase-4/cloud/agent/a2a_audit_logger.py`
  - **Proof**: Every A2A message logged to vault

- [ ] T076 [US7] Implement A2A fallback (if message fails, use file-based handoff)
  - **File**: `phase-4/cloud/agent/a2a_fallback.py`
  - **Proof**: Network error triggers file-based fallback

- [ ] T077 [US7] Test A2A messaging: Cloud sends, local receives, audit trail created
  - **File**: `phase-4/tests/us7-a2a-test.sh`
  - **Proof**: Message delivered, audit file in `/Updates/`

---

## Phase 10: Final Verification & Documentation (10 tasks, ~6 hours)

**Goal**: Complete Platinum Tier verification, document all deliverables

**Dependencies**: All P1 and P2 phases complete (US1-US6)

**Acceptance**: All verification tests passing, documentation complete

- [ ] T078 Create Dashboard.md with cloud/local status indicators
  - **File**: `AI_Employee_Vault/Dashboard.md`
  - **Proof**: Dashboard shows cloud status, local status, last sync time

- [ ] T079 [P] Run cloud uptime test (7 days, 99% target)
  - **File**: `phase-4/verification/uptime-log.md`
  - **Proof**: UptimeRobot screenshot or log showing 99%+ uptime

- [ ] T080 [P] Run domain specialization demo (cloud draft → local approve → execute)
  - **File**: `phase-4/verification/domain-split-demo.md`
  - **Proof**: Log showing cloud draft, local approval, execution

- [ ] T081 [P] Run vault sync test (file created on cloud, appears on local)
  - **File**: `phase-4/verification/sync-test-result.md`
  - **Proof**: File timestamps show sync propagation

- [ ] T082 [P] Run secrets isolation check (0 secrets on cloud)
  - **File**: `phase-4/verification/security-audit-result.md`
  - **Proof**: Audit report shows clean cloud VM

- [ ] T083 [P] Run Odoo cloud demo (draft invoice → local approve → posted)
  - **File**: `phase-4/verification/odoo-demo-result.md`
  - **Proof**: Invoice draft, approval, post all logged

- [ ] T084 Run full Platinum demo: Offline email → cloud draft → local approve → send
  - **File**: `phase-4/tests/platinum-demo/test-offline-email.sh`
  - **Proof**: Complete log with timestamps, email sent confirmation

- [ ] T085 Create verification.md with all deliverable proofs
  - **File**: `phase-4/verification.md`
  - **Proof**: All 9 deliverables verified with screenshots/logs

- [ ] T086 Create troubleshooting guide (common issues, solutions)
  - **File**: `phase-4/docs/troubleshooting.md`
  - **Proof**: Guide covers sync conflicts, secrets, Odoo, health issues

- [ ] T087 Update Dashboard.md with "Platinum Tier Always-On Cloud + Local Executive achieved"
  - **File**: `AI_Employee_Vault/Dashboard.md`
  - **Proof**: Dashboard shows Platinum Tier complete, all metrics green

---

## Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
    ├─→ Phase 3 (US1: Cloud Email) ─┐
    ├─→ Phase 4 (US2: Local Approval)─┤
    │                                │
    └─→ Phase 5 (US3: Vault Sync) ←──┘
           ↓
    ├─→ Phase 6 (US6: Secrets) ──────┐
    │                                 │
    ├─→ Phase 7 (US4: Odoo) ←────────┘
    │     ↓
    ├─→ Phase 8 (US5: Health)
    │
    ├─→ Phase 9 (US7: A2A - Optional)
    │
    └─→ Phase 10 (Verification)
```

**Critical Path**: Phase 1 → Phase 2 → Phase 5 (Vault Sync) → Phase 6 (Secrets) → Phase 10

**Parallel Opportunities**:
- Phase 3 (US1) and Phase 4 (US2) can run in parallel after Phase 2
- Phase 7 (US4) and Phase 8 (US5) can run in parallel after Phase 6
- All verification tests (T079-T083) can run in parallel

---

## MVP Scope (Minimum Viable Product)

**Recommended MVP**: Phases 1-2-3-5-6-10
- Setup infrastructure
- Cloud email triage (US1)
- Vault sync with claim-by-move (US3)
- Secrets isolation (US6)
- Core verification

**MVP Duration**: ~27 hours

**Full Platinum Tier**: All phases including P2 stories (US4, US5) = ~46 hours

**With Optional A2A**: ~50 hours

---

## Summary

| Phase | User Story | Tasks | Hours | Priority |
|-------|-----------|-------|-------|----------|
| 1 | Setup | 6 | 4 | Required |
| 2 | Foundational | 8 | 6 | Required |
| 3 | US1: Cloud Email | 10 | 8 | P1 Critical |
| 4 | US2: Local Approval | 9 | 6 | P1 Critical |
| 5 | US3: Vault Sync | 12 | 8 | P1 Critical |
| 6 | US6: Secrets | 8 | 5 | P1 Critical |
| 7 | US4: Odoo | 10 | 8 | P2 Important |
| 8 | US5: Health | 8 | 5 | P2 Important |
| 9 | US7: A2A | 6 | 4 | P3 Optional |
| 10 | Verification | 10 | 6 | Required |
| **Total** | | **87** | **46-61** | |

**Format Validation**: ✅ All tasks follow checklist format with checkbox, ID, labels, file paths
