---
id: 003
title: tasks platinum tier
stage: tasks
date: 2026-02-21
surface: agent
model: claude-sonnet-4-6
feature: phase-4-platinum-tier
branch: 004-platinum-tier
user: User
command: /sp.tasks
labels: ["phase-4", "platinum-tier", "tasks", "implementation"]
links:
  spec: specs/004-platinum-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-platinum-tier/tasks.md
tests: []
---

## Prompt

**Phase 4 plan ready** acknowledged.

The plan for **Phase 4 (Platinum Tier — Always-On Cloud + Local Executive)** has been successfully generated in `/phase-4/` (or the equivalent SpecifyPlus-managed location) and is now the binding roadmap for this final phase.

It strictly respects the approved Phase 4 spec and builds incrementally on Phases 1–3, with clear steps for:

- Selecting and setting up a 24/7 cloud runtime (VM, Render worker, Fly.io machine, etc.)
- Implementing domain specialization (Cloud drafts vs Local finals)
- Configuring synced vault delegation (Git/Syncthing, claim-by-move, /Updates/ merge)
- Migrating Odoo to cloud with HTTPS + backups
- Executing the required offline→online demo flow
- Optional A2A upgrade
- Full verification & documentation

We now move to the next required step.

### 4.3 TASKS PROMPT for Phase 4

Copy-paste and run the following **exactly** in SpecifyPlus:

```
/sp.tasks

Phase: 4
Phase Name: Platinum Tier - Always-On Cloud + Local Executive (Production-ish AI Employee)
Phase Folder: /phase-4/

Generate small, verifiable, sequential tasks strictly based on the approved Phase 4 plan and spec.
Each task must be:
- Atomic (doable in 60–180 minutes)
- Clearly testable (explicit pass/fail or proof artifact)
- Limited to Platinum Tier requirements only (no new features beyond spec)
- Building directly on Phases 1–3
- Using ONLY pre-created Agent Skills and connected MCP servers
- No new code from scratch outside of configuring/calling existing skills

Suggested task breakdown (use this structure or similar — create numbered checklist with [ ] checkboxes in /phase-4/tasks.md or equivalent):

1. Choose & Set Up Cloud Runtime (24/7 Base)
   → Select provider: Oracle Always Free VM / Google e2-micro / Render background worker / Fly.io machine (or document local fallback if unavailable)
   → Deploy Ubuntu/base OS, install Python 3.13+, Node.js v24+, git
   → Copy Phase 3 vault/code to cloud (via scp/git clone)
   → Set up systemd service or platform-native worker for watchers + orchestrator
   → Verify: process runs after reboot, simple health check (curl localhost:port or log tail)

2. Implement Work-Zone Specialization
   → Cloud process: configure to run only draft/triage logic (email triage, social drafts) — skip final send/post
   → Local process: configure to run only approval + final MCP execute logic
   → Add logic (via Agent Skills) to detect domain: Cloud skips WhatsApp/banking actions
   → Test: Cloud processes email → creates draft → stops (no send); Local can send after approval

3. Set Up Synced Vault with Git (Recommended)
   → Create private GitHub repo for vault sync
   → On cloud & local: git init/clone, add .gitignore (exclude .env, sessions, creds, .obsidian/cache)
   → Create domain subfolders: /Needs_Action/cloud/, /Needs_Action/local/, /Plans/cloud/, etc.
   → Implement claim-by-move: script or skill moves file to /In_Progress/cloud-agent/ or /In_Progress/local-agent/
   → Set single-writer: Local only modifies Dashboard.md
   → Cloud writes to /Updates/ → Local cron merges (append or Claude consolidate) into Dashboard.md
   → Test sync: create file on cloud → git push → local git pull → file appears

4. Alternative Sync Test (if Git fails — Syncthing)
   → Install Syncthing on cloud & local
   → Share vault folder (ignore secrets folders)
   → Test file propagation + claim-by-move

5. Migrate Odoo to Cloud
   → Deploy Odoo Community on cloud VM (follow earlier Odoo install guide)
   → Set up Nginx reverse proxy + Let's Encrypt for HTTPS
   → Cron pg_dump backup to cloud storage or external
   → Health check script: curl localhost:8069 → log success/fail
   → Update mcp-odoo skill to use cloud Odoo URL (draft-only)

6. Security & Secrets Isolation Check
   → Verify .gitignore / Syncthing ignore patterns exclude all secrets
   → Inspect cloud vault clone — confirm no .env, WhatsApp sessions, banking tokens present
   → Test: attempt sensitive action on cloud → fails or redirects to Local

7. Implement & Test Platinum Demo Flow
   → Pause/stop Local process (simulate offline)
   → Send test email → Cloud watcher triggers → Cloud drafts reply → writes /Pending_Approval/local/email_[id].md
   → Resume Local process → approve file → Local executes send via mcp-email
   → Verify: log entry, file moved to /Done/, email sent (test inbox)

8. Optional A2A Upgrade (if time permits)
   → Replace one file handoff (e.g. draft → approval) with direct HTTP call between cloud & local
   → Still write full audit to vault log

9. Final Verification & Documentation
   → Update Dashboard.md with cloud/local status indicators
   → Create /phase-4/verification.md with proof:
     - Cloud uptime log/screenshot
     - Domain split demo (cloud draft only, local send)
     - Sync test (file movement across instances)
     - Secrets check (cloud vault clean)
     - Odoo cloud + local approval flow
     - Full offline email demo (logs + timestamps)
   → State "Platinum Tier Always-On Cloud + Local Executive achieved" (or "Local Fallback Mode used due to

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Response snapshot

Successfully generated comprehensive task list for Phase 4 (Platinum Tier) implementation.

**Tasks Document**: `specs/004-platinum-tier/tasks.md`

**Task Summary**:
- **Total Tasks**: 87
- **Total Estimated Effort**: 46-61 hours
- **Phases**: 10 implementation phases
- **User Stories**: 7 (4 P1 critical, 2 P2 important, 1 P3 optional)

**Breakdown by Phase**:

| Phase | Focus | Tasks | Hours | Priority |
|-------|-------|-------|-------|----------|
| 1 | Setup & Infrastructure | 6 | 4 | Required |
| 2 | Foundational Components | 8 | 6 | Required |
| 3 | US1: Cloud 24/7 Email Triage | 10 | 8 | P1 Critical |
| 4 | US2: Local Executive Approval | 9 | 6 | P1 Critical |
| 5 | US3: Vault Sync & Claim-by-Move | 12 | 8 | P1 Critical |
| 6 | US6: Secrets Isolation | 8 | 5 | P1 Critical |
| 7 | US4: Cloud Odoo Integration | 10 | 8 | P2 Important |
| 8 | US5: Health Monitoring & Recovery | 8 | 5 | P2 Important |
| 9 | US7: Optional A2A Upgrade | 6 | 4 | P3 Optional |
| 10 | Final Verification & Documentation | 10 | 6 | Required |

**Task Organization**:
- Tasks organized by user story (US1-US7) for independent implementation
- All tasks follow strict checklist format: `- [ ] T### [P] [US#] Description with file path`
- Each task includes specific file paths and proof/artifact requirements
- Parallelizable tasks marked with `[P]`

**Dependencies**:
- Critical path: Phase 1 → Phase 2 → Phase 5 (Vault Sync) → Phase 6 (Secrets) → Phase 10
- Parallel opportunities: US1/US2 can run in parallel, US4/US5 can run in parallel, all verification tests can run in parallel

**MVP Scope**: Phases 1-2-3-5-6-10 (27 hours, core Platinum Tier functionality)

**Key Features**:
- Atomic tasks (60-180 minutes each)
- Clearly testable with explicit pass/fail criteria
- File paths specified for every task
- Building on Phases 1-3 (no modifications to previous phases)
- Using existing Agent Skills only

## Outcome

- ✅ Impact: Generated 87 atomic, testable tasks organized by user story for Phase 4 implementation
- 🧪 Tests: Each task includes proof/artifact requirement (test outputs, file existence, log entries)
- 📁 Files: Created specs/004-platinum-tier/tasks.md with complete task breakdown
- 🔁 Next prompts: `/sp.implement` to begin task execution, or start with Phase 1 tasks individually
- 🧠 Reflection: Task list successfully maps all Platinum Tier requirements to actionable implementation steps. Tasks are properly sized (60-180 min), testable, and organized by user story for parallel execution. MVP scope (27 hours) provides fast path to core value, while full Platinum Tier (46 hours) delivers all P1 and P2 features.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Format validation PASSED - all tasks follow checklist format with checkbox, ID, labels, file paths
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - tasks complete, ready for implementation

---

## Format Validation Summary

✅ **All 87 tasks follow required format**:
- Checkbox prefix: `- [ ]`
- Task ID: `T001` through `T087`
- Parallel marker: `[P]` on 18 parallelizable tasks
- Story label: `[US1]` through `[US7]` on user story tasks
- File path: Every task includes specific output file
- Proof criteria: Every task includes explicit verification

✅ **Task Organization**:
- Phase 1-2: Setup and foundational (no story labels)
- Phase 3-9: User stories US1-US7 (story labels included)
- Phase 10: Verification (no story labels)

✅ **Dependencies Clear**:
- Critical path identified
- Parallel opportunities marked
- MVP scope defined (27 hours)
