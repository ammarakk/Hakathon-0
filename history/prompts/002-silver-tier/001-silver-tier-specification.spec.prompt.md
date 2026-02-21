---
id: 001
title: silver-tier-specification
stage: spec
date_iso: 2025-02-20
surface: agent
model: claude-sonnet-4-6
feature: 002-silver-tier
branch: 002-silver-tier
user: User
command: /sp.specify
labels:
  - specification
  - phase-2
  - silver-tier
  - multi-watcher
  - human-in-loop
  - mcp-integration
links:
  spec: specs/002-silver-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-silver-tier/spec.md
  - specs/002-silver-tier/checklists/requirements.md
tests:
  - Requirements validation checklist (all items passed)
---

## Prompt

**Phase 1 closed** acknowledged.

**Phase 1 (Bronze Tier — Foundation)** is now officially **closed and locked**.
No further modifications will be made to Phase 1 deliverables. The minimal viable base is complete:

- Obsidian vault with `Dashboard.md` + `Company_Handbook.md`
- Required folders (`/Needs_Action/`, `/Done/`)
- One functional Watcher (using its Agent Skill) proven to drop at least one actionable `.md` file
- Claude Code read/write capability validated against the vault
- Verification documented in `/phase-1/`

We now advance to **Phase 2** (Silver Tier: Functional Assistant).

### 4.1 SPEC PROMPT for Phase 2

Copy-paste and run the following **exactly** as-is in your SpecifyPlus environment:

```
/sp.specify

Phase: 2
Phase Name: Silver Tier - Functional Assistant
Phase Folder: /phase-2/
Estimated Effort: 20-30 hours
Builds strictly on: Phase 1 (Bronze)

This phase MUST deliver ONLY the Silver Tier requirements from the hackathon document — plus everything already achieved in Bronze. No Gold or Platinum features are permitted in this phase.

Mandatory Deliverables (exactly these — incremental additions only):
1. All Bronze Tier deliverables remain intact and functional
2. Two or more Watcher scripts active (at minimum: the one from Phase 1 + at least one more; recommended combination: Gmail + WhatsApp OR Gmail + Filesystem + one other from skills)
   - Use only pre-created Agent Skills: gmail_watcher.md, whatsapp_watcher.md, filesystem_watcher.md, finance_watcher.md
   - Watchers must save actionable .md files into /Needs_Action/
3. Automatically post on LinkedIn about business to generate sales
   - Content generation + draft creation via Claude (using Agent Skills)
   - Final posting executed via MCP (use mcp-social-linkedin)
   - Human-in-the-loop approval required before actual post
4. Claude reasoning loop that creates Plan.md files
   - When processing /Needs_Action/ items, Claude creates a Plan.md (in /Plans/) with checkbox tasks/steps
   - Use Ralph Wiggum loop pattern (via ralph_wiggum_loop.md skill) to iterate until plan complete
5. One working MCP server for external action (minimum: email sending)
   - Use mcp-email
   - Claude drafts email → writes draft to vault → human approves in /Pending_Approval/ → MCP sends
6. Human-in-the-loop approval workflow for sensitive actions
   - Detect sensitive items (e.g. payments, final social posts, emails with attachments)
   - Write approval request to /Pending_Approval/*.md
   - Pause execution until user edits file (e.g. adds [x] Approved) or creates flag
   - Resume via manual Claude trigger or watcher
7. Basic scheduling via cron (Linux) or Task Scheduler (Windows)
   - Schedule watcher scripts to run continuously / periodically
   - Optional: schedule periodic Claude reasoning pass (e.g. every 15–60 min)
8. All new AI functionality (reasoning, planning, content generation, approval logic) MUST be implemented exclusively as pre-created Agent Skills — no loose prompts

Constraints:
- Work ONLY inside /phase-2/ for phase-specific files (specs, plans, tasks, code stubs, tests)
- Modify global folders only as needed: /Needs_Action/, /Plans/, /Pending_Approval/, /Done/, Dashboard.md (add Silver status), Agent_Skills/ (if extending)
- Use ONLY the connected MCP servers (focus on mcp-email and mcp-social-linkedin for this phase)
- Privacy & security: no secrets in vault; drafts only until approved
- No Odoo, no Facebook/Instagram/X integration, no weekly audit, no cloud sync, no multi-domain specialization — those are Gold/Platinum
- No direct A2A messaging yet

Acceptance Criteria:
- At least two Watchers running → create .md files in /Needs_Action/ from different sources
- Claude processes an item → creates Plan.md with steps → iterates (via Ralph Wiggum) → completes simple multi-step task
- LinkedIn post flow: Watcher triggers business-related item → Claude drafts post → writes to vault → user approves → MCP posts (or simulates post)
- One MCP (email or LinkedIn) successfully handles an approved action
- Human approval demonstrated: sensitive action paused → file in /Pending_Approval/ → user approves → action completes
- Watchers scheduled to run automatically (cron/Task Scheduler entry exists and tested)
- Dashboard.md updated to show pending items / status from multiple watchers

Output Format inside /phase-2/:
- Create subfolder /phase-2/spec/ if not auto-created
- Save this prompt text as reference

This is a strict contract — incremental from Phase 1 only. Do not implement yet — wait for plan/tasks/implement steps.
```

Once you have executed this `/sp.specify` command and confirmed that the Phase 2 specification is created in SpecifyPlus, reply exactly:

"Phase 2 spec ready"

## Response Snapshot

**Phase 2 Specification Created Successfully**

Created comprehensive specification for Silver Tier - Functional Assistant:

**Feature Analysis**:
- Branch: 002-silver-tier
- Short Name: silver-tier
- Build Dependency: 001-bronze-tier (Phase 1)

**User Stories**: 6 independent testable stories
- US1 (P1): Multi-Source Monitoring - Gmail + Filesystem watchers
- US2 (P1): Human Approval for Sensitive Actions - /Pending_Approval/ workflow
- US3 (P2): Automated LinkedIn Posting - Business content generation
- US4 (P1): Reasoning Loop with Plan Creation - Ralph Wiggum pattern
- US5 (P2): Scheduled Watcher Execution - Cron/Task Scheduler
- US6 (P2): MCP Email Integration - Draft and send emails

**Functional Requirements**: 31 total (FR-001 to FR-031)
- Multi-watcher support (4 requirements)
- Human-in-loop approval (6 requirements)
- LinkedIn posting (5 requirements)
- Reasoning loop (5 requirements)
- MCP email (4 requirements)
- Scheduling (4 requirements)
- Dashboard updates (3 requirements)

**Success Criteria**: 12 measurable outcomes
- SC-001: Two watchers run 10+ minutes without crashing
- SC-002: Action files from 2+ unique sources
- SC-003: 100% of sensitive actions create approval requests
- SC-004: 95% of approved actions execute within 30 seconds
- SC-005: Plan.md files created for complex tasks
- SC-006: Ralph Wiggum loop iterates to completion
- SC-007: LinkedIn posting completes in under 2 minutes
- SC-008: MCP email 99% delivery rate
- SC-009: Scheduled watchers start automatically
- SC-010: Dashboard shows real-time pending counts
- SC-011: Zero secrets in vault files
- SC-012: All AI uses Agent Skills exclusively

**Key Entities**: 6 data entities defined
- ActionItem (extends Bronze)
- ApprovalRequest
- Plan
- WatcherSchedule
- LinkedInPost
- EmailDraft

**Constitutional Compliance**: ✅ All gates passed
- Document Adherence: Silver Tier only
- Privacy & Security: Secrets local-only, drafts until approved
- Vault Structure: /phase-2/ for code, global folders for vault
- Agent Skills: All AI logic via skills only
- Human-in-the-Loop: Approval workflow mandatory
- MCP Pattern: External actions via MCP only
- Incremental: Bronze features intact

**Quality Validation**: ✅ Checklist complete
- Content Quality: 4/4 items passed
- Requirement Completeness: 8/8 items passed
- Feature Readiness: 4/4 items passed
- Constitution Compliance: 7/7 items passed

**Edge Cases**: 7 scenarios covered
- Gmail API credential expiration
- Simultaneous multi-watcher events
- Unresponsive approval requests
- Plan.md execution failures
- MCP server unreachable
- Large /Needs_Action/ queues
- Watcher crash handling

**Out of Scope** (explicitly excluded):
- ❌ Odoo accounting (Gold+)
- ❌ Facebook/Instagram/X posting (Gold+)
- ❌ Weekly audit/CEO briefing (Gold+)
- ❌ Cloud deployment/VM (Platinum+)
- ❌ Vault synchronization (Platinum+)
- ❌ Direct A2A messaging (Platinum+)

## Outcome

- ✅ Impact: Comprehensive Phase 2 specification created with 6 user stories, 31 requirements, 12 success criteria
- 🧪 Tests: Requirements checklist validated - all items passed (23/23)
- 📁 Files: specs/002-silver-tier/spec.md (main spec), specs/002-silver-tier/checklists/requirements.md (validation)
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan with technical decisions
- 🧠 Reflection: Specification is technology-agnostic, focused on user value, and strictly scoped to Silver Tier only

## Evaluation Notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Requirements validation - ALL PASS (23/23 items)
- Prompt variant (if applicable): Standard sp.specify execution
- Next experiment (smallest change to try): Proceed to /sp.plan to create technical implementation plan
