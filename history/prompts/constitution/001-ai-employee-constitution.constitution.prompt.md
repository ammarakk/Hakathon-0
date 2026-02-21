---
stage: constitution
title: AI Employee Constitution Creation
date_iso: 2025-02-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: master
user: User
command: /sp.constitution
labels:
  - constitution
  - governance
  - hackathon-project
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests_yaml: []
---

# Prompt History Record

## User Input (verbatim)

```
/sp.constitution

Project Name: Personal AI Employee - Autonomous Digital FTE (2026 Hackathon Blueprint)

Project Goal: Build a local-first, agent-driven Personal AI Employee using Claude Code as reasoning engine, Obsidian as dashboard/memory, Python Watchers for perception, and Node.js MCP servers for actions. The system proactively manages personal (Gmail, WhatsApp, banking) and business (social media, payments, tasks) affairs 24/7 with human-in-the-loop for sensitive operations. All AI functionality MUST be implemented exclusively as Agent Skills in the vault. No prompt engineering outside of skills; focus on agent engineering.

Core Rules (non-negotiable):
- Follow the provided hackathon document EXACTLY — no invented features, no scope creep.
- Privacy & security first: local-first, secrets NEVER in synced files (.env, tokens, WhatsApp sessions, banking creds stay local-only).
- Human-in-the-loop mandatory for payments >$500, final sends/posts, sensitive actions.
- All external actions go through MCP servers (draft → approve → execute pattern where applicable).
- Ralph Wiggum loop (Stop hook pattern) MUST be used for multi-step autonomous task completion.
- Watchers trigger agent via file drops in /Needs_Action/.
- Claude Code reads/writes ONLY to the Obsidian vault.
- No internet-listening without Watchers; no always-on Claude without triggers.
- Every phase builds incrementally; previous phases remain untouched.
- No skipping, merging, or redoing phases.
- Constitution is created ONLY ONCE — never regenerate or edit it.
- Phases are executed strictly one at a time; next phase starts only after explicit user confirmation of "Phase X closed".

Vault Folder Structure (enforced globally — create exactly this layout in AI_Employee_Vault):
- Dashboard.md                  (real-time summary: bank balance, pending messages, active projects)
- Company_Handbook.md           (Rules of Engagement, approval thresholds, politeness rules, etc.)
- /Needs_Action/                (incoming items from Watchers — emails, messages, files, etc.)
- /In_Progress/                 (subfolders per agent/domain for claim-by-move in Platinum)
- /Pending_Approval/            (sensitive actions waiting for human OK)
- /Plans/                       (Plan.md files created by reasoning loop)
- /Done/                        (completed tasks)
- /Accounting/                  (Current_Month.md + Odoo integration files in Gold+)
- /Logs/                        (audit logs, errors)
- /Updates/                     (cloud → local signals in Platinum)
- Agent_Skills/                 (all .md skills live here — base_watcher.md, gmail_watcher.md, etc.)
- /phase-1/                     (Bronze Tier: Foundation)
- /phase-2/                     (Silver Tier: Functional Assistant — builds on phase-1)
- /phase-3/                     (Gold Tier: Autonomous Employee — builds on phase-2)
- /phase-4/                     (Platinum Tier: Always-On Cloud + Local Executive — builds on phase-3)

Phases (exactly 4 — match hackathon tiers):
- Phase 1 = Bronze Tier (Foundation) — MUST complete all Bronze deliverables inside /phase-1/
- Phase 2 = Silver Tier (Functional Assistant) — MUST include all Silver additions inside /phase-2/
- Phase 3 = Gold Tier (Autonomous Employee) — MUST include all Gold additions inside /phase-3/
- Phase 4 = Platinum Tier (Always-On Cloud + Local Executive) — MUST include all Platinum additions inside /phase-4/

Phase Execution Rules:
- Work in ONLY the current /phase-X/ folder and referenced global folders (Agent_Skills/, Dashboard.md, etc.).
- Specs, plans, tasks, implementations stay inside their /phase-X/ subfolders.
- Never modify previous phases.
- Use ONLY the pre-created Agent Skills and connected MCP servers.
- Human approval files go to /Pending_Approval/.
- After each phase step (spec/plan/tasks/implement), wait for explicit user confirmation before next step.
- Phase is not closed until user says "Phase X closed" — do not auto-advance.

This constitution is now locked. All future /sp.* commands MUST respect these rules without exception.
```

## Response Summary

Created comprehensive project constitution (v1.0.0) for Personal AI Employee hackathon project with 9 core principles:

1. **Document Adherence** - Exact compliance with hackathon blueprint, no scope creep
2. **Privacy & Security First** - Local-first, secrets never synced
3. **Human-in-the-Loop** - Mandatory approval for sensitive actions (payments>$500, sends, posts)
4. **MCP Server Pattern** - All external actions through MCP servers (draft → approve → execute)
5. **Ralph Wiggum Loop** - Stop hook pattern for multi-step task completion
6. **Watcher-Triggered Architecture** - File drops in /Needs_Action/ trigger Claude
7. **Vault-Only Read/Write** - Claude Code operates only on Obsidian vault
8. **Incremental Phase Execution** - Phases build sequentially, no modification of previous phases
9. **Agent Skills Implementation** - All AI functionality as vault Agent Skills

Defined complete vault folder structure with phase-specific folders (/phase-1/ through /phase-4/) matching Bronze → Silver → Gold → Platinum tiers.

Established governance with semantic versioning, amendment procedures, and compliance review requirements.

Updated dependent templates (plan-template.md, spec-template.md, tasks-template.md) to include constitution compliance gates.

## Outcome

- Constitution created: `.specify/memory/constitution.md` (v1.0.0)
- Templates updated with constitutional constraints
- Phase execution rules documented
- MCP server integration enforced
- Security and privacy protocols established
