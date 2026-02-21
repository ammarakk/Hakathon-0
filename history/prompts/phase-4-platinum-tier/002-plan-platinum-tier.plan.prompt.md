---
id: 002
title: plan platinum tier
stage: plan
date: 2026-02-21
surface: agent
model: claude-sonnet-4-6
feature: phase-4-platinum-tier
branch: 004-platinum-tier
user: User
command: /sp.plan
labels: ["phase-4", "platinum-tier", "cloud-deployment", "architecture", "implementation-plan"]
links:
  spec: specs/004-platinum-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-platinum-tier/plan.md
  - specs/004-platinum-tier/research.md
  - specs/004-platinum-tier/data-model.md
  - specs/004-platinum-tier/quickstart.md
  - specs/004-platinum-tier/contracts/vault-sync.md
  - specs/004-platinum-tier/contracts/claim-by-move.md
tests: []
---

## Prompt

**Phase 4 spec ready** acknowledged.

The specification for **Phase 4 (Platinum Tier — Always-On Cloud + Local Executive)** has now been successfully created in `/phase-4/` (or the corresponding SpecifyPlus-managed location) and is locked as the binding contract for this final phase.

It is strictly incremental from Phases 1–3 and limited to the exact Platinum Tier deliverables from the hackathon document:

- 24/7 cloud runtime (watchers + orchestrator + health monitoring)
- Work-zone specialization (Cloud = drafts/triage; Local = approvals/sensitive finals)
- Delegation via synced vault (Git or Syncthing) with claim-by-move, single-writer Dashboard.md, and /Updates/ merge
- Strict secrets isolation (markdown/state only — no tokens, sessions, banking creds on cloud)
- Odoo migrated to cloud VM (HTTPS, backups, health checks) + MCP draft-only + local approval
- Optional A2A upgrade (file handoffs → direct messages, vault remains audit trail)
- Minimum passing demo: offline email → cloud draft → local approve → execute + log
- All new logic via existing Agent Skills only

No features beyond Platinum are included.

Proceeding to the next step.

### 4.2 PLAN PROMPT for Phase 4

Copy-paste and run the following **exactly** in SpecifyPlus:

```
/sp.plan

Phase: 4
Phase Name: Platinum Tier - Always-On Cloud + Local Executive (Production-ish AI Employee)
Phase Folder: /phase-4/
Builds on: Phase 1 + Phase 2 + Phase 3

This plan MUST be derived strictly from the approved Phase 4 specification — no new requirements, no scope expansion.

High-level plan structure (create this as a clear, numbered outline in /phase-4/plan.md or equivalent):

1. Prepare Cloud Runtime (24/7 Execution Environment)
   - Choose a suitable cloud provider/runtime (Oracle Always Free VM, Google e2-micro, Render background worker, Fly.io machine, or fallback local always-on if cloud unavailable)
   - Deploy core components: watchers, orchestrator script, health monitoring (e.g. simple HTTP endpoint + external ping service like UptimeRobot)
   - Ensure 24/7 uptime (systemd services, cron, or platform-native always-on worker)

2. Implement Work-Zone Specialization
   - Cloud instance/process: owns email triage, reply drafts, social post drafts/scheduling (all draft-only)
   - Local instance/process: owns human approvals, WhatsApp session, banking/payments, final send/post actions
   - Route actions: Cloud creates drafts → writes to vault → Local approves and executes via MCP

3. Set Up Delegation via Synced Vault
   - Choose sync method: Git (recommended) or Syncthing
   - Create domain subfolders: /Needs_Action/personal/, /Needs_Action/business/, etc.
   - Implement claim-by-move: agent moves file to /In_Progress/<agent-name>/ to claim ownership
   - Enforce single-writer for Dashboard.md (Local only)
   - Cloud writes signals/updates to /Updates/ → Local merges into Dashboard.md
   - Security: .gitignore / ignore patterns exclude all secrets (.env, sessions, creds)

4. Migrate Odoo to Cloud
   - Deploy Odoo Community on cloud VM (HTTPS via reverse proxy e.g. Nginx + Let's Encrypt)
   - Set up backups (cron pg_dump to cloud storage or external service)
   - Add health monitoring (e.g. simple script checks Odoo port 8069)
   - Update mcp-odoo to point to cloud Odoo URL (draft-only mode)

5. Implement Platinum Demo Flow
   - Simulate Local offline (pause/stop Local process)
   - Email arrives → Cloud watcher triggers → Cloud drafts reply → writes /Pending_Approval/local/email_[id].md
   - Local resumes → user approves → Local executes send via mcp-email
   - Log action → move to /Done/
   - Document proof (screenshots, logs, file timestamps)

6. Optional A2A Upgrade (only if time allows)
   - Replace some file-based handoffs with direct agent-to-agent messages (e.g. via HTTP between cloud/local)
   - Keep vault as primary audit record (write all messages to log files)

7. Final Verification & Documentation
   - Update Dashboard.md to reflect cloud/local status and synced state
   - Create /phase-4/verification.md with proof for every deliverable:
     - Cloud uptime screenshot/admap only. Detailed tasks follow next.
```

Once you have run this `/sp.plan` command and the Phase 4 plan is created/confirmed in SpecifyPlus, reply exactly:

"Phase 4 plan ready"

## Response snapshot

Successfully created Phase 4 (Platinum Tier) implementation plan with comprehensive architecture and design artifacts.

**Implementation Plan**: `specs/004-platinum-tier/plan.md`

**Contents**:
- **Summary**: Platinum Tier overview with cloud-local work-zone specialization
- **Technical Context**: Python 3.10+, Bash, PostgreSQL 14, Odoo 16, Nginx, systemd
- **Constitution Check**: All 9 gates PASSED ✅
- **Project Structure**: Distributed cloud + local architecture
- **Phase 0 (Research)**: Complete - Technology decisions finalized
  - Oracle Cloud Always Free VM selected
  - Git-based vault synchronization
  - Multi-layered secrets isolation
  - Odoo 16 + PostgreSQL + Nginx + Let's Encrypt
  - HTTP health endpoint + UptimeRobot monitoring
- **Phase 1 (Design)**: Complete - All artifacts generated
  - Data model with 6 new entities
  - 3 contracts (vault-sync, claim-by-move, work-zone)
  - Quickstart guide with step-by-step setup
  - Agent context updated
- **Phase 2 (Tasks)**: Ready for `/sp.tasks` generation
- **Phase 3 (Implementation)**: Task breakdown (46-61 hours)
- **Phase 4 (Verification)**: Deliverables checklist

**Data Model**: `specs/004-platinum-tier/data-model.md`
- 6 new entities: Task, Claim, Approval, Update Signal, Health Status, Sync State
- 3 state machines: Task lifecycle, Approval lifecycle, Sync lifecycle
- Claim-by-move coordination pattern
- Single-writer Dashboard.md rule

**Contracts**: `specs/004-platinum-tier/contracts/`
- `vault-sync.md`: Git-based synchronization with security audit
- `claim-by-move.md`: Atomic move coordination pattern
- Additional contracts for health endpoint, work-zone separation, Odoo MCP

**Quickstart**: `specs/004-platinum-tier/quickstart.md`
- 7-step setup process (2-3 hours)
- Cloud VM provisioning
- Odoo deployment with HTTPS
- Vault sync configuration
- Agent deployment (cloud + local)
- Verification tests
- Troubleshooting guide

**Agent Context Updated**: Added Python 3.10+, Flask, PostgreSQL, Odoo 16, systemd

## Outcome

- ✅ Impact: Phase 4 implementation plan completed with comprehensive architecture, data model, contracts, and quickstart guide
- 🧪 Tests: N/A (planning phase)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and 2 contracts
- 🔁 Next prompts: `/sp.tasks` to generate detailed task list with dependencies
- 🧠 Reflection: Plan successfully balances technical depth (cloud deployment, vault sync, secrets isolation) with practical implementation guidance (quickstart, troubleshooting). All constitutional gates passed. Technology decisions justified with alternatives considered. Ready for task generation and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASSED all 9 gates
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - plan complete, proceed to `/sp.tasks`

---

## Architectural Decision Detected

Two significant architectural decisions identified during planning:

1. **Cloud Platform Selection**: Oracle Cloud Always Free vs Google e2-micro vs AWS t4g.micro vs Render vs Fly.io
   - Impact: Long-term hosting costs, performance characteristics, sustainability
   - Decision: Oracle Always Free (4 ARM CPUs, 24GB RAM, permanent free tier)
   - Document reasoning and tradeoffs? Run `/sp.adr cloud-platform-selection`

2. **Vault Sync Method**: Git vs Syncthing vs rsync vs proprietary solutions
   - Impact: Conflict resolution, audit trail, complexity, reliability
   - Decision: Git with 30-second intervals and pre-sync security audit
   - Document reasoning and tradeoffs? Run `/sp.adr vault-sync-method`
