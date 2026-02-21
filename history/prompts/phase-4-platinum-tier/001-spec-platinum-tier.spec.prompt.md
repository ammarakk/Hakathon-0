---
id: 001
title: spec platinum tier
stage: spec
date: 2026-02-21
surface: agent
model: claude-sonnet-4-6
feature: phase-4-platinum-tier
branch: 004-platinum-tier
user: User
command: /sp.specify
labels: ["phase-4", "platinum-tier", "cloud-deployment", "vault-sync", "secrets-isolation"]
links:
  spec: phase-4/spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-4/spec/spec.md
  - phase-4/spec/checklists/requirements.md
tests: []
---

## Prompt

**Phase 3 closed** acknowledged.

**Phase 3 (Gold Tier — Autonomous Employee)** is now officially **closed and locked**.
No further modifications will be made to Phase 3 code, vault files, skills, MCPs, Odoo setup, or any related artifacts.

The system has reached a complete **autonomous employee** state with:

- Unified cross-domain processing (personal Gmail/WhatsApp/banking + business social/accounting/tasks)
- Self-hosted Odoo Community (local) with JSON-RPC MCP integration (draft invoices/transactions → approval → post)
- Facebook/Instagram + Twitter/X posting + summary generation (draft → human approval → MCP post)
- Multiple active MCP servers with correct action routing
- Scheduled weekly Monday Morning CEO Briefing (revenue summary, bottlenecks, recommendations)
- Error recovery, graceful degradation, and full audit logging
- Reliable Ralph Wiggum loop for complex multi-step autonomy
- Architecture overview + lessons learned documented

We now proceed to the **final phase**: **Phase 4** (Platinum Tier: Always-On Cloud + Local Executive).

### 4.1 SPEC PROMPT for Phase 4

Copy-paste and run the following **exactly** in your SpecifyPlus environment:

```
/sp.specify

Phase: 4
Phase Name: Platinum Tier - Always-On Cloud + Local Executive (Production-ish AI Employee)
Phase Folder: /phase-4/
Estimated Effort: 60+ hours
Builds strictly on: Phase 1 + Phase 2 + Phase 3

This phase MUST deliver ONLY the Platinum Tier requirements from the hackathon document — plus everything achieved in previous phases. This is the final phase; no additional tiers beyond this.

Mandatory Deliverables (exactly these incremental additions):
1. All Gold Tier deliverables remain intact and functional
2. Run the AI Employee on Cloud 24/7 (always-on watchers + orchestrator + health monitoring)
   - Deploy to a Cloud VM or equivalent persistent runtime (e.g., Oracle Always Free, Google e2-micro, AWS t4g.micro free tier, Render background worker, Fly.io machine — subject to limits/availability)
   - Include watchers, orchestrator script, health checks (e.g., simple HTTP endpoint + external monitoring like UptimeRobot)
3. Work-Zone Specialization (domain ownership)
   - Cloud owns: Email triage + draft replies + social post drafts/scheduling (draft-only; requires Local approval before send/post)
   - Local owns: approvals, WhatsApp session, payments/banking, and final "send/post" actions
4. Delegation via Synced Vault (Phase 1 of sync)
   - Agents communicate by writing files into:
     - /Needs_Action/<domain>/
     - /Plans/<domain>/
     - /Pending_Approval/<domain>/
   - Prevent double-work using:
     - /In_Progress/<agent>/ claim-by-move rule
     - single-writer rule for Dashboard.md (Local only)
     - Cloud writes updates to /Updates/ (or /Signals/), and Local merges them into Dashboard.md
   - For Vault sync: use Git (recommended) or Syncthing
   - Claim-by-move rule: first agent to move an item from /Needs_Action to /In_Progress/<agent>/ owns it; other agents must ignore it
5. Security rule: Vault sync includes only markdown/state. Secrets never sync (.env, tokens, WhatsApp sessions, banking creds)
   - Cloud never stores or uses WhatsApp sessions, banking credentials, or payment tokens
6. Deploy Odoo Community on a Cloud VM (24/7) with HTTPS, backups, and health monitoring
   - Migrate/integrate from local Odoo (Phase 3)
   - Integrate Cloud Agent with Odoo via MCP for draft-only accounting actions and Local approval for posting invoices/payments
7. Optional A2A Upgrade (Phase 2): Replace some file handoffs with direct A2A messages later, while keeping the vault as the audit record
8. Platinum demo (minimum passing gate): Email arrives while Local is offline → Cloud drafts reply + writes approval file → when Local returns, user approves → Local executes send via MCP → logs → moves task to /Done
9. All new AI functionality MUST be implemented exclusively as Agent Skills

Constraints:
- Work ONLY inside /phase-4/ for phase-specific files (specs, plans, tasks, cloud config, tests)
- Modify global folders only as needed: add subfolders for <domain> (personal/business), /Updates/, /In_Progress/<agent>/
- Use ONLY existing Agent Skills and connected MCP servers
- Cloud runtime: free tiers OK (Oracle, Google, Render free worker, Fly.io credit, etc.) — monitor limits
- Sync: markdown/state only; no secrets in Git/Syncthing
- A2A: optional upgrade — keep file-based as primary for auditability
- Human-in-the-loop: mandatory for local-owned actions (approvals, sends, payments)
- No new tiers or features beyond Platinum

Acceptance Criteria:
- System runs 24/7 on cloud with watchers/orchestrator/health monitoring (uptime proof)
- Domain specialization: Cloud drafts/triage, Local final approvals/sends
- Vault sync working: Git/Syncthing syncs files, claim-by-move prevents conflicts, Dashboard.md merged locally
- Secrets isolated: no sensitive data on cloud (verified)
- Odoo on cloud: HTTPS, backups (e.g. cron pg_dump), health checks; draft actions via MCP + local approval
- A2A (if done): file handoffs partially replaced by direct messages, vault remains audit trail
- Platinum demo: full offline email → cloud draft → local approve → execute + log
- Dashboard.md reflects seamless cloud/local updates

Output Format inside /phase-4/:
- Create subfolder /phase-4/spec/ if not auto-created
- Document the spec clearly (this prompt text can be

## Response snapshot

Successfully created Phase 4 (Platinum Tier) specification with the following deliverables:

**Branch**: `004-platinum-tier`

**Specification Created**: `phase-4/spec/spec.md`

**Contents**:
- 7 prioritized user stories (P1: critical, P2: important, P3: optional)
  - P1: Cloud 24/7 Email Triage
  - P1: Local Executive Approval Workflow
  - P1: Vault Sync with Claim-by-Move
  - P1: Secrets Isolation (Security Gate)
  - P2: Cloud Odoo Integration
  - P2: Health Monitoring & Recovery
  - P3: Optional A2A Messaging Upgrade

- 53 Functional Requirements across 8 domains:
  - Cloud Deployment (FR-001 to FR-006)
  - Work-Zone Specialization (FR-007 to FR-013)
  - Vault Sync & Coordination (FR-014 to FR-022)
  - Secrets Isolation (FR-023 to FR-028)
  - Odoo Cloud Integration (FR-029 to FR-035)
  - Health Monitoring & Recovery (FR-036 to FR-042)
  - Platinum Demo Scenario (FR-043 to FR-047)
  - Optional A2A Upgrade (FR-048 to FR-052)

- 10 Success Criteria (measurable and technology-agnostic)
- 10 Edge Cases with resolution strategies
- 6 Key Entities (Vault Folder Structure, Task Claim, Approval File, Health Status, Sync State, Signal File)
- Dependencies and Assumptions clearly documented
- Out of Scope items explicitly listed

**Quality Checklist**: `phase-4/spec/checklists/requirements.md`
- All validation items PASSED
- No [NEEDS CLARIFICATION] markers required
- Specification is ready for planning phase

## Outcome

- ✅ Impact: Phase 4 Platinum Tier specification completed, establishing requirements for production-ready 24/7 AI Employee with cloud/local work-zone specialization
- 🧪 Tests: N/A (specification phase)
- 📁 Files: Created phase-4/spec/spec.md and phase-4/spec/checklists/requirements.md
- 🔁 Next prompts: `/sp.plan` to generate architecture plan, or `/sp.clarify` if any ambiguities exist
- 🧠 Reflection: Specification successfully balances technical precision (cloud deployment, vault sync, secrets isolation) with stakeholder accessibility (user stories focus on business value). Constitutional compliance built into all requirements. No clarifications needed - requirements are clear, testable, and measurable.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Requirements quality checklist PASSED all items
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - specification complete, proceed to planning
