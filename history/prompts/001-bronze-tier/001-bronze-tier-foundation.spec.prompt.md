---
stage: spec
title: Bronze Tier Foundation Specification
date_iso: 2025-02-20
surface: agent
model: claude-sonnet-4-6
feature: 001-bronze-tier
branch: 001-bronze-tier
user: User
command: /sp.specify
labels:
  - specification
  - phase-1
  - bronze-tier
  - foundation
links:
  spec: specs/001-bronze-tier/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/001-bronze-tier/spec.md
  - specs/001-bronze-tier/checklists/requirements.md
tests_yaml: []
---

# Prompt History Record

## User Input (verbatim)

```
/sp.specify

Phase: 1
Phase Name: Bronze Tier - Foundation (Minimum Viable Deliverable)
Phase Folder: /phase-1/
Estimated Effort: 8-12 hours

This phase MUST deliver ONLY the Bronze Tier requirements from the hackathon document. No features from Silver, Gold, or Platinum are allowed in this phase.

Mandatory Deliverables (exactly these — no more, no less):
- Fully functional Obsidian vault with at minimum:
  - Dashboard.md (basic real-time summary placeholder — can be simple markdown table or sections for bank balance, pending messages, active projects)
  - Company_Handbook.md (contains at least basic "Rules of Engagement" e.g. politeness guidelines, approval thresholds like payments >$500)
- One working Watcher script (choose ONE: either Gmail OR filesystem monitoring — implement using the corresponding pre-created Agent Skill: gmail_watcher.md OR filesystem_watcher.md)
- Claude Code is able to successfully read from and write to files inside the vault (demonstrate by creating/reading at least one test .md file in /Needs_Action/ or /Done/)
- Basic folder structure created exactly as defined in constitution:
  - /Needs_Action/
  - /Done/
  - (Note: /Inbox is mentioned in document but not required in constitution — use only constitution folders unless explicitly needed)
- All AI-related functionality (reading, planning, decision logic, file creation) MUST be implemented exclusively via pre-created Agent Skills — no loose prompts or inline Claude instructions outside skills.

Constraints:
- Work ONLY inside /phase-1/ for phase-specific files (specs, plans, tasks, code, tests)
- Global folders (Dashboard.md, Company_Handbook.md, Agent_Skills/, /Needs_Action/, /Done/) may be modified/used as needed for this phase
- Use only the connected MCP servers if required (none are strictly needed for Bronze — MCP is Silver+)
- No scheduling, no multi-watcher, no social posting, no Odoo, no cloud, no Ralph Wiggum loop yet (those are Silver/Gold)
- Human-in-the-loop not yet required in this minimal phase
- Privacy rule: no secrets in vault files

Acceptance Criteria:
- Vault opens in Obsidian and shows Dashboard.md + Company_Handbook.md
- Chosen Watcher script runs in background (terminal or daemon), detects at least one new item (email or file drop), and creates a correctly formatted .md file in /Needs_Action/
- Run Claude Code manually pointing at vault → it can read the Watcher-created file and write a simple response file (e.g. move to /Done/ or create note)
- All logic that would normally require AI reasoning is wrapped in / called via Agent Skills

Output Format inside /phase-1/:
- Create subfolder /phase-1/spec/ if not auto-created
- Document the spec clearly (this prompt text can be saved as reference)

This is a strict contract. Do not expand scope. Do not implement yet — wait for plan/tasks/implement steps.
```

## Response Summary

Created Phase 1 (Bronze Tier) specification with strict scope boundary enforcement.

**Specification Structure:**
- 3 prioritized user stories (P1 = MVP foundation)
- 13 functional requirements covering vault setup, watcher implementation, Claude Code integration
- 10 measurable, technology-agnostic success criteria
- Explicit scope boundaries excluding Silver/Gold/Platinum features
- Constitutional compliance checklist embedded

**Key Features Specified:**
- Obsidian vault with Dashboard.md and Company_Handbook.md
- Single watcher (Gmail OR filesystem) - choice left to implementation
- Claude Code read/write integration with vault
- Agent Skills-only requirement for AI functionality

**Scope Enforcement:**
- "Out of Scope" section explicitly excludes: WhatsApp watcher, finance watcher, social posting, Odoo, scheduling, Ralph Wiggum loop, human approval, cloud deployment, MCP servers
- All phase-specific work constrained to /phase-1/ folder
- Privacy rule: no secrets in vault files

**Validation:** All quality checks passed - specification ready for planning phase.

## Outcome

- Branch created: 001-bronze-tier
- Spec file: specs/001-bronze-tier/spec.md
- Requirements checklist: specs/001-bronze-tier/checklists/requirements.md
- Status: Ready for /sp.plan
