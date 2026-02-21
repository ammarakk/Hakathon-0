# Vault Structure Specification

**Phase**: 4 - Platinum Tier
**Vault Name**: AI_Employee_Vault
**Last Updated**: 2026-02-21

---

## Overview

This document defines the complete folder structure for the AI Employee Vault, including Phase 4 Platinum Tier additions for cloud-local coordination and claim-by-move workflow.

---

## Complete Vault Structure

```
AI_Employee_Vault/
├── Dashboard.md                  # Real-time summary (single-writer: Local only)
├── Company_Handbook.md           # Rules of engagement
├── Welcome.md                    # Vault welcome message
│
├── Needs_Action/                 # Incoming tasks from watchers
│   ├── personal/                 # NEW: Domain-specific subfolder
│   │   └── task-*.md
│   ├── business/                 # NEW: Domain-specific subfolder
│   │   └── task-*.md
│   ├── email/                    # NEW: Domain-specific subfolder
│   │   └── task-*.md
│   └── social/                   # NEW: Domain-specific subfolder
│       └── task-*.md
│
├── In_Progress/                  # NEW: Claim-by-move coordination
│   ├── cloud/                    # Cloud agent claims
│   │   └── task-*.md
│   └── local/                    # Local agent claims
│       └── task-*.md
│
├── Pending_Approval/             # Sensitive actions awaiting human approval
│   ├── email/
│   │   └── draft-*.md
│   ├── social/
│   │   └── draft-*.md
│   ├── accounting/
│   │   └── draft-*.md
│   └── payments/
│       └── draft-*.md
│
├── Plans/                        # Agent-generated plans
│   ├── cloud/
│   │   └── plan-*.md
│   └── local/
│       └── plan-*.md
│
├── Done/                         # Completed tasks
│   ├── email/
│   ├── social/
│   ├── accounting/
│   └── payments/
│
├── Updates/                      # NEW: Cloud → local signals (single-writer merge target)
│   ├── signal-*.md               # Cloud writes here
│   └── a2a-*.md                  # A2A messages (optional upgrade)
│
├── Errors/                       # Error logs and incidents
│   ├── sync/                     # NEW: Sync conflicts
│   │   └── conflict-*.md
│   ├── odoo/
│   │   └── error-*.md
│   ├── security/
│   │   └── violation-*.md
│   └── system/
│       └── incident-*.md
│
├── Logs/                         # Audit logs
│   ├── agent-activity.log
│   ├── sync-activity.log
│   └── security-audit.log
│
├── Accounting/                   # Financial records (Gold Tier)
│   ├── Current_Month.md
│   ├── odoo-drafts/
│   └── transactions/
│
├── CEO_Briefings/                # Weekly reports (Gold Tier)
│   └── briefing-*.md
│
├── Agent_Skills/                 # All AI skills (Constitution requirement)
│   ├── base_watcher.md
│   ├── gmail_watcher.md
│   ├── whatsapp_watcher.md
│   ├── filesystem_watcher.md
│   ├── finance_watcher.md
│   ├── reasoning_loop.md
│   ├── human_in_loop.md
│   ├── vault_sync.md
│   ├── security_rules.md
│   ├── cloud_deployment.md
│   └── [other skills from Phases 1-3]
│
├── phase-1/                      # Bronze Tier (Foundation)
│   ├── spec/
│   ├── plan/
│   └── tasks/
│
├── phase-2/                      # Silver Tier (Functional Assistant)
│   ├── spec/
│   ├── plan/
│   └── tasks/
│
├── phase-3/                      # Gold Tier (Autonomous Employee)
│   ├── spec/
│   ├── plan/
│   └── tasks/
│
├── phase-4/                      # NEW: Platinum Tier (Cloud + Local)
│   ├── spec/
│   │   ├── spec.md
│   │   └── checklists/
│   │       └── requirements.md
│   ├── cloud/
│   │   ├── provision/
│   │   │   ├── oracle-cloud-setup.sh
│   │   │   ├── install-dependencies.sh
│   │   │   └── security-hardening.sh
│   │   ├── odoo/
│   │   │   ├── odoo-install.sh
│   │   │   ├── nginx-ssl-setup.sh
│   │   │   ├── backup-script.sh
│   │   │   └── health-check.sh
│   │   ├── agent/
│   │   │   ├── setup-agent.sh
│   │   │   ├── orchestrator.py
│   │   │   ├── health-server.py
│   │   │   ├── sync-daemon.sh
│   │   │   └── systemd-units/
│   │   │       ├── ai-employee-health.service
│   │   │       ├── ai-employee-orchestrator.service
│   │   │       ├── ai-employee-gmail-watcher.service
│   │   │       └── ai-employee-filesystem-watcher.service
│   │   └── config/
│   │       ├── cloud.env
│   │       ├── cloud.env.example
│   │       └── gmail-watcher-config.json
│   ├── local/
│   │   ├── agent/
│   │   │   ├── setup-local.sh
│   │   │   ├── orchestrator.py
│   │   │   └── sync-local.sh
│   │   └── config/
│   │       ├── local.env
│   │       └── local.env.example
│   ├── vault/
│   │   ├── git-sync-guide.md
│   │   ├── security-audit.sh
│   │   └── structure.md (this file)
│   ├── tests/
│   │   ├── platinum-demo/
│   │   │   └── test-offline-email.sh
│   │   ├── integration/
│   │   │   ├── test-cloud-local-sync.sh
│   │   │   ├── test-claim-by-move.sh
│   │   │   └── test-domain-split.sh
│   │   └── security/
│   │       └── test-secrets-isolation.sh
│   ├── docs/
│   │   ├── cloud-deployment.md
│   │   ├── troubleshooting.md
│   │   └── migration-guide.md
│   └── verification.md
│
├── .git/                         # Git repository (NEW for Phase 4)
├── .gitignore                    # Secret exclusion patterns (NEW for Phase 4)
└── .obsidian/                    # Obsidian plugin settings
```

---

## Phase 4 Additions

### New Folders

| Folder | Purpose | Write Access | Sync |
|--------|---------|--------------|------|
| `/Needs_Action/<domain>/` | Domain-specific tasks | All | Yes |
| `/In_Progress/cloud/` | Cloud agent claims | Cloud only | Yes |
| `/In_Progress/local/` | Local agent claims | Local only | Yes |
| `/Updates/` | Cloud signals for merge | Cloud only | Yes |
| `/Errors/sync/` | Sync conflicts | Auto (sync) | Yes |
| `phase-4/` | Platinum Tier artifacts | Local only | Partial* |

*Partial sync: Documentation synced, cloud/ synced, local/ NOT synced

### Single-Writer Rules

1. **Dashboard.md**: Local agent ONLY (Cloud blocked from modifying)
2. **/Updates/**: Cloud agent writes here, Local merges into Dashboard.md
3. **/In_Progress/cloud/**: Cloud agent ONLY
4. **/In_Progress/local/**: Local agent ONLY

### Claim-by-Move Flow

```
Task created in /Needs_Action/email/task-001.md
    ↓
Cloud agent claims: mv → /In_Progress/cloud/task-001.md
    ↓
Cloud processes, creates draft: /Pending_Approval/email/draft-001.md
    ↓
Local agent approves draft
    ↓
Local executes send, moves to: /Done/email/sent-001.md
```

---

## File Naming Conventions

### Task Files
- Format: `task-YYYYMMDD-HHMMSS-<id>.md`
- Example: `task-20260221-103045-001.md`

### Draft Files
- Format: `draft-YYYYMMDD-HHMMSS-<id>.md`
- Example: `draft-20260221-103100-001.md`

### Signal Files
- Format: `signal-YYYYMMDD-HHMMSS-<id>.md`
- Example: `signal-20260221-103200-001.md`

### Done Files
- Format: `done-YYYYMMDD-HHMMSS-<id>.md`
- Example: `done-20260221-103500-001.md`

---

## Permissions

### Cloud VM
- **Read**: All folders
- **Write**: `/In_Progress/cloud/`, `/Updates/`, `/Pending_Approval/`, `/Errors/`
- **FORBIDDEN**: `/In_Progress/local/`, `Dashboard.md`

### Local Machine
- **Read**: All folders
- **Write**: `/In_Progress/local/`, `/Pending_Approval/`, `/Done/`, `Dashboard.md`
- **FORBIDDEN**: `/In_Progress/cloud/`

---

## Sync Behavior

### Included in Git Sync
- All markdown files (.md)
- Domain subfolders (`/Needs_Action/<domain>/`)
- Approval files (`/Pending_Approval/<domain>/`)
- Completed tasks (`/Done/<domain>/`)
- Updates (`/Updates/*.md`)
- Phase 4 documentation (most of `phase-4/`)

### EXCLUDED from Git Sync
- `.env` files (all)
- `*.session`, `*.token`, `*.cred`, `*.key` files
- `/secrets/`, `/creds/`, `/tokens/` folders
- WhatsApp session files
- Banking credentials
- `.obsidian/` cache
- Python cache (`__pycache__/`)
- Node modules (`node_modules/`)

See `.gitignore` for complete exclusion list.

---

## Migration Notes

### From Phase 3 to Phase 4

**No Breaking Changes**: Phase 4 adds folders but doesn't modify existing Phase 1-3 structure.

**New Requirements**:
1. Initialize Git repository in vault root
2. Add `.gitignore` with secret patterns
3. Create domain subfolders in `/Needs_Action/`
4. Create `/In_Progress/cloud/` and `/In_Progress/local/`
5. Create `/Updates/` for cloud signals
6. Update `/Dashboard.md` with Phase 4 status

**Data Migration**:
- Existing `/Needs_Action/` files: Optional move to domain subfolders
- Existing `/In_Progress/` files: Move to `/In_Progress/local/`
- No data loss during migration

---

## Summary

Phase 4 introduces:
- **3 new top-level folders**: `/In_Progress/`, `/Updates/`, `/Errors/`
- **Domain subfolders**: `/Needs_Action/<domain>/`
- **Agent-specific claims**: `/In_Progress/<agent>/`
- **Git-based sync**: With secrets isolation
- **Single-writer rules**: Dashboard.md (Local), Updates (Cloud)

All changes are backward compatible with Phases 1-3.
