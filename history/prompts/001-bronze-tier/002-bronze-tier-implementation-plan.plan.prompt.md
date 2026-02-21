---
stage: plan
title: Bronze Tier Implementation Plan
date_iso: 2025-02-20
surface: agent
model: claude-sonnet-4-6
feature: 001-bronze-tier
branch: 001-bronze-tier
user: User
command: /sp.plan
labels:
  - planning
  - phase-1
  - bronze-tier
  - foundation
links:
  spec: specs/001-bronze-tier/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/001-bronze-tier/plan.md
  - specs/001-bronze-tier/research.md
  - specs/001-bronze-tier/data-model.md
  - specs/001-bronze-tier/quickstart.md
  - specs/001-bronze-tier/contracts/file_formats.md
tests_yaml: []
---

# Prompt History Record

## User Input (verbatim)

```
/sp.plan

Phase: 1
Phase Name: Bronze Tier - Foundation (Minimum Viable Deliverable)
Phase Folder: /phase-1/

This plan MUST be derived **strictly** from the approved Phase 1 specification — no new requirements, no features from Silver/Gold/Platinum.

High-level plan structure (create this as a clear, numbered or bulleted outline in /phase-1/plan.md or equivalent):

1. Vault & Dashboard Setup
   - Create or verify Dashboard.md with basic placeholder sections (e.g. headings for Pending Messages, Bank Summary, Active Projects — can be empty tables or simple text at this stage)
   - Create Company_Handbook.md with minimal Rules of Engagement (at least 3–5 bullet points, e.g. "Be polite in all communications", "Flag payments > $500", "Archive processed items")

2. Folder Structure Enforcement
   - Ensure /Needs_Action/ and /Done/ folders exist in the root of the vault
   - (Optional but recommended) Create empty placeholder subfolders if needed for future phases, but do not populate them

3. Select & Prepare One Watcher (choose ONE only)
   - Decision: Choose either Gmail Watcher or Filesystem Watcher (recommend Filesystem Watcher for simplicity — no API credentials needed)
   - If Gmail: Use gmail_watcher.md skill, prepare credentials stub (do not commit real creds)
   - If Filesystem: Use filesystem_watcher.md skill
   - Create a small test script or config to run the chosen watcher (e.g. python gmail_watcher.py --vault /path/to/vault)

4. Watcher → Vault Integration
   - Run the watcher manually or in background
   - Trigger at least one event (send test email or drop test file into monitored folder)
   - Verify a correctly formatted .md file appears in /Needs_Action/ (with frontmatter + content as per skill)

5. Claude Code → Vault Read/Write Validation
   - Run Claude Code in terminal pointed at the vault root
   - Issue simple test command: read the Watcher-generated file from /Needs_Action/
   - Have Claude write a response file (e.g. simple note or move file to /Done/)
   - Verify file appears in vault and is readable in Obsidian

6. Documentation & Verification
   - Create a short README.md or test-log.md in /phase-1/ documenting:
     - Chosen watcher
     - Setup steps performed
     - Test results (screenshots or copy-paste of file contents if possible)
     - Any issues & resolutions

Constraints for this plan:
- All implementation logic MUST call/use the pre-created Agent Skills — no new code outside skills
- No MCP servers used in this phase (not required)
- No scheduling/cron yet
- No Ralph Wiggum / multi-step loops yet
- Keep everything minimal & verifiable
- Work stays inside /phase-1/ except when modifying global vault files (Dashboard.md, Company_Handbook.md, /Needs_Action/, /Done/)

This plan is a roadmap only — detailed, small, verifiable tasks come next.

Do not implement anything yet.
```

## Response Summary

Created comprehensive Phase 1 implementation plan with:

**Technical Decisions:**
- Chose FilesystemWatcher over GmailWatcher (simpler, no credentials needed)
- Python 3.11+ for watcher scripts
- Markdown with YAML frontmatter for vault files
- 60-second watcher check interval

**Architecture:**
- Single project structure with /phase-1/ for phase-specific work
- Global vault folders (Dashboard.md, Company_Handbook.md, etc.)
- File-based agent communication (/Needs_Action/ → /Done/)

**Deliverables:**
- Vault structure with 10 folders
- Dashboard.md with placeholder sections
- Company_Handbook.md with Rules of Engagement
- FilesystemWatcher implementation
- Claude Code read/write integration

**All Constitution Checks Passed:**
- Document adherence: Bronze Tier only
- Privacy: Secrets local-only
- Watcher-triggered architecture
- Vault-only read/write
- Agent Skills for AI functionality
- Incremental phases (no Silver/Gold/Platinum features)

## Outcome

- Plan file: specs/001-bronze-tier/plan.md
- Research: specs/001-bronze-tier/research.md (watcher selection, format decisions)
- Data model: specs/001-bronze-tier/data-model.md (entities, file formats, state transitions)
- Quick start: specs/001-bronze-tier/quickstart.md (step-by-step setup guide)
- Contracts: specs/001-bronze-tier/contracts/file_formats.md (format specifications)

**Next**: Ready for /sp.tasks to generate actionable task list.
