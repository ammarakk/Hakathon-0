<!--
SYNC IMPACT REPORT
==================
Version change: (none) → 1.0.0
Modified principles: N/A (initial constitution)
Added sections: All sections (initial constitution)
Removed sections: N/A
Templates requiring updates:
  ✅ plan-template.md - Reviewed for constitution compliance
  ✅ spec-template.md - Reviewed for constitution compliance
  ✅ tasks-template.md - Reviewed for constitution compliance
Follow-up TODOs: None
-->

# Personal AI Employee Constitution

## Core Principles

### I. Document Adherence (NON-NEGOTIABLE)
Follow the provided hackathon document EXACTLY. No invented features, no scope creep. All deliverables MUST match the Bronze → Silver → Gold → Platinum tier progression as specified.

**Rationale**: The hackathon blueprint has been carefully designed to build incrementally. Deviations create technical debt and break the phased learning approach.

### II. Privacy & Security First
Local-first architecture. Secrets MUST NEVER be in synced files. The following MUST stay local-only: `.env` files, API tokens, WhatsApp sessions, banking credentials, OAuth tokens.

**Rationale**: Sensitive credentials in synced vaults create security vulnerabilities. Local-only secrets ensure protection even if vault is compromised.

### III. Human-in-the-Loop for Sensitive Actions
Mandatory human approval required for: payments >$500, final email sends, final social media posts, deletions, and any actions with irreversible consequences. Approval workflow: draft → /Pending_Approval/ → human approval → execute.

**Rationale**: AI should not autonomously execute high-impact actions. Human judgment prevents costly errors and maintains accountability.

### IV. MCP Server Pattern for External Actions
All external actions MUST go through MCP servers (mcp-email, mcp-odoo, mcp-social-linkedin, mcp-social-fb-ig, mcp-social-x). Pattern: draft → local approval → execute. No direct API calls from watchers or reasoning loop.

**Rationale**: Centralizes external action handling, enables approval workflow, provides audit trail, and maintains separation of concerns.

### V. Ralph Wiggum Loop (Stop Hook Pattern)
MUST be used for all multi-step autonomous task completion. The loop continues until all completion criteria are met. Stop hook checks: all steps complete, tests pass, files exist, documentation updated.

**Rationale**: Prevents premature task completion. The "Ralph Wiggum" pattern ensures Claude doesn't declare "I'm done" until work is actually complete.

### VI. Watcher-Triggered Architecture
Watchers trigger Claude Code via file drops in /Needs_Action/. No internet-listening without watchers. No always-on Claude without triggers. Watchers: Gmail, WhatsApp, Filesystem, Finance (expandable).

**Rationale**: Event-driven architecture prevents resource waste. Claude Code activates only when there's actual work to do.

### VII. Vault-Only Read/Write
Claude Code reads and writes ONLY to the Obsidian vault. No direct file system operations outside vault structure. No external database writes. All state persisted as markdown in vault folders.

**Rationale**: Vault as single source of truth ensures visibility, auditability, and portability. Markdown enables human review and editing.

### VIII. Incremental Phase Execution
Phases MUST be executed one at a time. Each phase builds on previous phases. Previous phases MUST remain untouched. No skipping, merging, or redoing phases. Next phase starts ONLY after explicit user confirmation of "Phase X closed".

**Rationale**: Incremental builds ensure learning and validation at each stage. Modifying previous phases breaks the tiered foundation.

### IX. Agent Skills Implementation
All AI functionality MUST be implemented exclusively as Agent Skills in the vault (Agent_Skills/*.md). No prompt engineering outside of skills. Focus on agent engineering, not prompt hacking.

**Rationale**: Skills are reusable, testable, and versionable. Prompt engineering scattered across code creates unmaintainable systems.

## Vault Folder Structure

The following structure MUST be created in AI_Employee_Vault and enforced globally:

```
AI_Employee_Vault/
├── Dashboard.md                  # Real-time summary: bank balance, pending messages, active projects
├── Company_Handbook.md           # Rules of Engagement, approval thresholds, politeness rules
├── Needs_Action/                 # Incoming items from Watchers (emails, messages, files, etc.)
├── In_Progress/                 # Subfolders per agent/domain for claim-by-move (Platinum)
├── Pending_Approval/            # Sensitive actions waiting for human OK
├── Plans/                       # Plan.md files created by reasoning loop
├── Done/                        # Completed tasks
├── Accounting/                  # Current_Month.md + Odoo integration files (Gold+)
├── Logs/                        # Audit logs, errors
├── Updates/                     # Cloud → local signals (Platinum)
├── Agent_Skills/                # All .md skills (base_watcher.md, gmail_watcher.md, etc.)
├── phase-1/                     # Bronze Tier: Foundation
├── phase-2/                     # Silver Tier: Functional Assistant (builds on phase-1)
├── phase-3/                     # Gold Tier: Autonomous Employee (builds on phase-2)
└── phase-4/                     # Platinum Tier: Always-On Cloud + Local (builds on phase-3)
```

## Phase Execution Rules

1. Work in ONLY the current /phase-X/ folder and referenced global folders (Agent_Skills/, Dashboard.md, etc.)
2. Specs, plans, tasks, implementations stay inside their /phase-X/ subfolders
3. NEVER modify previous phases
4. Use ONLY the pre-created Agent Skills and connected MCP servers
5. Human approval files go to /Pending_Approval/
6. After each phase step (spec/plan/tasks/implement), wait for explicit user confirmation before next step
7. Phase is NOT closed until user says "Phase X closed" — do NOT auto-advance

## Phase Definitions (Exact Tier Mapping)

- **Phase 1 = Bronze Tier (Foundation)**
  Deliverables: Base watcher skills, basic folder structure, Gmail watcher, simple file drops, manual Claude triggers

- **Phase 2 = Silver Tier (Functional Assistant)**
  Deliverables: WhatsApp watcher, filesystem watcher, reasoning loop, Ralph Wiggum pattern, auto-processing

- **Phase 3 = Gold Tier (Autonomous Employee)**
  Deliverables: Finance watcher, Odoo integration, all MCP servers connected, scheduling, weekly CEO briefings

- **Phase 4 = Platinum Tier (Always-On Cloud + Local Executive)**
  Deliverables: Cloud deployment, vault sync (Git/Syncthing), claim-by-move, security rules enforcement, A2A upgrade (optional)

## Governance

### Amendment Procedure
This constitution is created ONLY ONCE and MUST NOT be regenerated or edited lightly. Amendments require:
1. Documented rationale for change
2. Impact analysis on all phases
3. Update to CONSTITUTION_VERSION (semantic versioning)
4. Propagation across all dependent templates

### Versioning Policy
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance Review
All future /sp.* commands MUST respect these rules without exception. Phase gates verify constitution compliance before advancing.

**Version**: 1.0.0 | **Ratified**: 2025-02-20 | **Last Amended**: 2025-02-20
