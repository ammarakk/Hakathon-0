# Implementation Plan: Bronze Tier - Foundation (Phase 1)

**Branch**: `001-bronze-tier` | **Date**: 2025-02-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-bronze-tier/spec.md`

**Note**: This plan is derived strictly from the approved Phase 1 specification. No features from Silver/Gold/Platinum tiers are included.

## Summary

Build the minimum viable AI Employee foundation: an Obsidian vault with dashboard and handbook, one working watcher (Gmail or filesystem), and Claude Code integration for reading/writing vault files. This phase establishes the core perception layer (watcher) and vault-based memory system without any advanced features like scheduling, multi-watcher coordination, or human approval workflows.

## Technical Context

**Language/Version**: Python 3.11+ (for watcher scripts), Markdown (for vault files)
**Primary Dependencies**:
- Watchers: `watchdog` (filesystem), `google-api-python-client` + `google-auth-oauthlib` (Gmail - optional)
- Vault: Obsidian (markdown editor)
- AI: Claude Code (terminal-based)

**Storage**: Markdown files in local filesystem (Obsidian vault)
**Testing**: Manual verification (Obsidian open test, watcher run test, Claude Code read/write test)
**Target Platform**: Local filesystem (Linux/Mac/Windows), Python 3.11+, Obsidian
**Project Type**: Single project - local AI Employee system
**Performance Goals**:
- Watcher checks every 60 seconds
- Vault file operations complete in <1 second
- Watcher runs continuously for 10+ minutes without failure

**Constraints**:
- No network API calls except Gmail (if chosen)
- All secrets (.env, tokens) stored locally outside vault
- No MCP servers (Silver+ feature)
- No scheduling/cron (Silver+ feature)
- No Ralph Wiggum loop (Silver+ feature)

**Scale/Scope**:
- 1 watcher instance
- 1 vault directory
- 10-100 action items in /Needs_Action/ during testing
- Single user (local)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Document Adherence: Deliverables match hackathon blueprint exactly (Bronze Tier only - no Silver/Gold/Platinum features)
- [x] Privacy & Security: All secrets (.env, tokens, sessions) excluded from synced files - credentials stored locally only
- [n/a] Human-in-the-Loop: Not required in Bronze phase (deferred to Silver+)
- [n/a] MCP Pattern: Not required in Bronze phase (deferred to Silver+)
- [n/a] Ralph Wiggum Loop: Not required in Bronze phase (deferred to Silver+)
- [x] Watcher-Triggered: Architecture uses file drops in /Needs_Action/ for triggers
- [x] Vault-Only R/W: Claude Code reads/writes only to Obsidian vault structure
- [x] Incremental Phases: Work stays in /phase-1/ folder, doesn't modify previous phases
- [x] Agent Skills: All AI functionality implemented as vault Agent Skills (base_watcher.md, gmail_watcher.md, filesystem_watcher.md)

## Project Structure

### Documentation (this feature)

```text
specs/001-bronze-tier/
├── plan.md              # This file
├── research.md          # Phase 0 output (watcher selection analysis)
├── data-model.md        # Phase 1 output (vault data structures)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (file format specifications)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Single project structure for local AI Employee

phase-1/                          # Phase-specific work
├── code/                         # Watcher implementations
│   ├── filesystem_watcher.py    # Filesystem monitoring (CHOSEN)
│   ├── gmail_watcher.py          # Gmail monitoring (alternative)
│   └── test_config.py            # Configuration for testing
├── tests/                        # Manual test scripts
│   ├── test_vault_setup.py
│   ├── test_watcher.py
│   └── test_claude_integration.py
├── README.md                     # Phase 1 documentation
└── test-log.md                   # Test results log

# Global vault folders (created/modified across phases)
AI_Employee_Vault/
├── Dashboard.md                  # Real-time summary (created)
├── Company_Handbook.md           # Rules of engagement (created)
├── Needs_Action/                 # Watcher drops files here
├── Done/                        # Processed items
├── Agent_Skills/                 # Pre-created skills (reference)
├── Logs/                        # System logs
├── Accounting/                  # Accounting records (empty placeholder)
├── Plans/                       # Future plans (empty placeholder)
├── Pending_Approval/            # Approval workflow (empty placeholder)
├── In_Progress/                 # Active work (empty placeholder)
└── Updates/                     # Updates (empty placeholder)
```

**Structure Decision**: Single local project with phase-specific code in `/phase-1/` and global vault folders. Watchers are standalone Python scripts. No build process required - direct script execution.

## Complexity Tracking

> **No violations** - All constitution checks passed. No complexity tracking required.

## Phase 0: Research & Decisions

### Research Tasks

1. **Watcher Selection Analysis**
   - **Decision**: Choose FilesystemWatcher over GmailWatcher
   - **Rationale**:
     - No API credentials required (simpler setup)
     - No OAuth flow complexity
     - Immediate testability with any file drop
     - No network dependency
     - Faster to demonstrate MVP
   - **Alternatives considered**:
     - GmailWatcher: Provides real email monitoring but requires Google Cloud project setup, OAuth credentials, and network connectivity
   - **Reference**: `filesystem_watcher.md` Agent Skill

2. **Vault Format Standards**
   - **Decision**: Use Obsidian-compatible markdown with YAML frontmatter
   - **Rationale**: Obsidian is the specified interface, markdown is human-readable, frontmatter enables metadata
   - **Alternatives considered**: Plain text (no metadata support), JSON (not human-readable in Obsidian)
   - **Reference**: Obsidian documentation

3. **File Naming Convention**
   - **Decision**: ISO timestamp prefix + source + description (e.g., `20250220_143000_filesystem_testfile.md`)
   - **Rationale**: Sortable by time, includes source context, descriptive
   - **Alternatives considered**: UUID (not human-readable), sequential numbers (collision risk)
   - **Reference**: Existing best practices for file naming

### Research Output

See [research.md](research.md) for detailed findings on:
- Watcher implementation patterns
- Vault folder structure requirements
- File format specifications
- Testing methodologies

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for entity definitions:

**Core Entities:**
- **Vault**: Root container with metadata
- **ActionItem**: File in /Needs_Action/ representing detected event
- **ProcessedItem**: File in /Done/ representing completed work
- **Watcher**: Background process monitoring external system

**File Format Contracts:**

ActionItem (.md in /Needs_Action/):
```yaml
---
type: action_item
source: filesystem|gmail
timestamp: ISO-8601
priority: low|medium|high
---
# Title

**Source**: {source}
**Detected**: {timestamp}
**Priority**: {priority}

## Content

{item content}

## Actions Required
- [ ] Review item
- [ ] Determine response
- [ ] Execute action
```

ProcessedItem (.md in /Done/):
```yaml
---
type: processed_item
source: filesystem|gmail
timestamp: ISO-8601
processed_at: ISO-8601
---
# Title

**Status**: Completed
**Actions Taken**: {list}
---
```

### Quick Start Guide

See [quickstart.md](quickstart.md) for:
1. Create vault directory structure
2. Create Dashboard.md with placeholder sections
3. Create Company_Handbook.md with Rules of Engagement
4. Set up filesystem watcher
5. Test watcher with file drop
6. Test Claude Code integration
7. Verify end-to-end flow

---

**Next Step**: Run `/sp.tasks` to generate actionable task list from this plan.
