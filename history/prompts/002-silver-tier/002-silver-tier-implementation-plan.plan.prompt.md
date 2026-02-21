---
id: 002
title: silver-tier-implementation-plan
stage: plan
date_iso: 2025-02-20
surface: agent
model: claude-sonnet-4-6
feature: 002-silver-tier
branch: 002-silver-tier
user: User
command: /sp.plan
labels:
  - planning
  - phase-2
  - silver-tier
  - architecture
  - technical-design
links:
  spec: specs/002-silver-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-silver-tier/plan.md
  - specs/002-silver-tier/research.md
  - specs/002-silver-tier/data-model.md
  - specs/002-silver-tier/quickstart.md
  - specs/002-silver-tier/contracts/ (directory created)
tests:
  - Constitution compliance check (pre-design): 9/9 PASS
  - Constitution compliance check (post-design): 9/9 PASS
---

## Prompt

**Phase 2 spec ready** acknowledged.

The specification for **Phase 2 (Silver Tier — Functional Assistant)** has been successfully created in `/phase-2/` (or the equivalent SpecifyPlus-managed location) and is now the binding contract for this phase.
It is explicitly incremental from Phase 1 and strictly limited to the Silver Tier items listed in the hackathon document:

- Multiple Watchers (≥2)
- LinkedIn auto-posting (draft → approve → post via MCP)
- Reasoning loop that produces Plan.md files
- One working MCP for external action (focus on email or LinkedIn)
- Human-in-the-loop approval workflow
- Basic scheduling (cron / Task Scheduler)
- All new logic via Agent Skills only

No Gold/Platinum elements (Odoo, FB/IG/X integration, weekly briefing, cloud sync, multi-domain delegation, etc.) are included.

Proceeding to the next step.

### 4.2 PLAN PROMPT for Phase 2

Copy-paste and run the following **exactly** in SpecifyPlus:

```
/sp.plan

Phase: 2
Phase Name: Silver Tier - Functional Assistant
Phase Folder: /phase-2/
Builds on: Phase 1 (Bronze)

This plan MUST be derived **strictly** from the approved Phase 2 specification — no new requirements, no Gold/Platinum features.

High-level plan structure (create this as a clear, numbered outline in /phase-2/plan.md or equivalent):

1. Extend Vault Dashboard & Handbook (incremental updates)
   - Update Dashboard.md to show status from multiple watchers (e.g. add section "Watcher Status" or "Pending from Multiple Sources")
   - Add any Silver-specific rules to Company_Handbook.md (e.g. "Draft all social posts for approval", "Use MCP for external sends")

2. Activate & Test Multiple Watchers
   - Keep the Phase 1 watcher running
   - Add at least one more (strongly recommend whatsapp_watcher.md — most business-relevant after Gmail)
   - Alternative: add filesystem_watcher.md or finance_watcher.md if WhatsApp setup is complex
   - Verify both watchers independently create .md files in /Needs_Action/ when triggered
   - Test overlapping triggers (e.g. email + WhatsApp message arrives close together)

3. Implement Claude Reasoning & Planning Loop
   - Use ralph_wiggum_loop.md skill to enable iterative task completion
   - When Claude processes /Needs_Action/ item(s):
     - Analyze content
     - Create /Plans/Plan_[timestamp or id].md with markdown checkboxes for steps
     - Iterate until all checkboxes checked or task criteria met
   - Demonstrate on a simple multi-step example (e.g. "Client asks for update → plan reply → draft reply → approve → send")

4. Set up Human-in-the-Loop Approval Workflow
   - Use human_approval_workflow.md skill
   - Define sensitive actions in Company_Handbook.md or skill (e.g. any send/post, payments, attachments)
   - When detected: write request file to /Pending_Approval/action_[id].md
   - Include clear instructions: "[ ] Approve / [ ] Reject + reason"
   - Pause reasoning → wait for user edit → resume via manual Claude run or file watcher

5. Configure One MCP Server for External Action
   - Focus on mcp-email (simplest & most universal) OR mcp-social-linkedin (for the LinkedIn requirement)
   - If email: Claude drafts reply → writes draft.md → user approves → MCP sends
   - If LinkedIn: Claude generates business post draft → writes to vault → user approves → MCP posts
   - Test end-to-end with dummy/ test account (never real production credentials)

6. Implement LinkedIn Business Posting Flow
   - Trigger: business-related item in /Needs_Action/ (e.g. new client message, completed task)
   - Claude (via skill) drafts promotional/ value post
   - Draft saved to vault + approval request to /Pending_Approval/
   - After approval: use mcp-social-linkedin to post (or log "would post" if testing)

7. Add Basic Scheduling
   - Use cron_scheduling.md skill
   - Create cron entries (Linux) or Task Scheduler jobs (Windows) for:
     - Each watcher script (run every 1–5 minutes)
     - Optional: periodic Claude reasoning pass (e.g. python trigger_claude.py every 30 min)
   - Test: restart machine → watchers auto-start, process new items without manual run

8. Integration & Verification
   - Update Dashboard.md to reflect multi-watcher activity, pending approvals, recent plans
   - Create /phase-2/verification.md documenting:
     - Watchers active & tested
     - Sample Plan.md example
     - Approval flow demo (before/after)
     - MCP action (sent email or posted LinkedIn — use test account)
     - Scheduling confirmation (jobs listed, auto-run proven)
     - Any blockers & workarounds

Constraints:
- All new behavior MUST call existing Agent Skills (no new inline code)
- Keep human approval mandatory for real external actions
- Work stays inside /phase-2/ except when updating global vault files
- No Odoo, no other social platforms, no cloud, no weekly audit

This plan is the roadmap only. Detailed tasks follow next.
```

Once you have run this `/sp.plan` command and the Phase 2 plan is created/confirmed in SpecifyPlus, reply exactly:

"Phase 2 plan ready"

## Response Snapshot

**Phase 2 Implementation Plan Created Successfully**

Comprehensive technical plan generated for Silver Tier - Functional Assistant:

### Technical Decisions Made

**Key Choices**:
1. **Second Watcher**: Gmail Watcher (business-relevant, good API)
2. **MCP Priority**: Email first, LinkedIn second (universality)
3. **Approval Detection**: File polling every 30 seconds (simplicity)
4. **Plan Iteration**: Ralph Wiggum Loop pattern (proven)
5. **Scheduling**: Windows Task Scheduler (native to platform)

**Technology Stack**:
- Python 3.11+ (inherited from Phase 1)
- Gmail API (google-api-python-client)
- MCP servers (email, LinkedIn)
- Windows Task Scheduler
- Agent Skills (ralph_wiggum_loop, human_in_loop, etc.)

### Architecture Design

**Data Model**: 6 new entities
- ApprovalRequest: Human approval workflow
- Plan: Multi-step execution plans
- Task: Plan sub-tasks
- LinkedInPost: Drafted social media posts
- EmailDraft: Drafted emails
- WatcherSchedule: Scheduled execution config

**File Format Contracts**: 4 new formats defined
- ApprovalRequest format
- Plan format
- LinkedInPost draft format
- EmailDraft format

**State Transitions**: Fully defined for all entities
- Approval: pending → approved/rejected → executed/archived
- Plan: in_progress → complete/failed → archived
- Posts/Emails: pending → approved → posted/sent → archived

### Implementation Roadmap

**7 Milestones** (13 days estimated):
1. Vault Updates (Day 1)
2. Gmail Watcher Integration (Days 2-3)
3. Approval Workflow (Days 4-5)
4. MCP Integration (Days 6-7)
5. Reasoning Loop (Days 8-9)
6. Scheduling (Days 10-11)
7. Integration & Verification (Days 12-13)

### Research Completed

**7 Major Decisions** Resolved:
1. Second Watcher: Gmail (chosen over WhatsApp/Finance)
2. MCP Priority: Email first (simplest + universal)
3. Approval Detection: Polling 30s (simple + reliable)
4. Plan Iteration: Ralph Wiggum (proven pattern)
5. Scheduling: Windows Task Scheduler (native)
6. Sensitivity Detection: Rule-based (transparent)
7. Dashboard Updates: Incremental (backward compatible)

**Best Practices Documented**:
- Gmail API integration (OAuth, rate limits, batching)
- MCP server integration (local-only, error handling, retry logic)
- Human-in-the-loop design (clear instructions, checkbox-based, audit trail)

### Supporting Artifacts Created

1. **plan.md**: Comprehensive implementation plan
   - Technical context
   - Constitution compliance (pre/post design)
   - Architecture decisions
   - Data model
   - File format contracts
   - Implementation roadmap
   - Risk analysis
   - Success metrics

2. **research.md**: Technical research and decisions
   - 7 major decisions with rationale
   - Alternatives considered
   - Best practices documentation
   - Open questions resolved

3. **data-model.md**: Entity definitions
   - 6 new entities (ApprovalRequest, Plan, Task, LinkedInPost, EmailDraft, WatcherSchedule)
   - Relationships and constraints
   - State transitions
   - File system mapping
   - Data access patterns
   - Migration path from Bronze

4. **quickstart.md**: Step-by-step setup guide
   - Gmail API setup (30 min)
   - MCP server installation (15 min)
   - Environment configuration (10 min)
   - Gmail watcher implementation (45 min)
   - Approval workflow (45 min)
   - Scheduling configuration (30 min)
   - End-to-end testing (30 min)
   - Troubleshooting guide

5. **contracts/**: Directory created for file format specifications
   - ApprovalRequest format
   - Plan format
   - LinkedInPost draft format
   - EmailDraft format

### Constitutional Compliance

**Pre-Design Check**: ✅ 9/9 PASS
**Post-Design Check**: ✅ 9/9 PASS

All constitutional principles validated:
- Document Adherence: Silver Tier only
- Privacy & Security: Secrets local-only
- Human-in-the-Loop: Approval workflow mandatory
- MCP Pattern: External actions via MCP only
- Ralph Wiggum Loop: Iterative reasoning
- Watcher-Triggered: All starts with /Needs_Action/
- Vault-Only Read/Write: Claude vault-only access
- Incremental Phase Execution: Phase 1 intact
- Agent Skills: All new logic via skills

### Gate Evaluation

✅ **ALL GATES PASSED** - Design approved for implementation

No Gold/Platinum features included. All Silver requirements addressed. All constitutional principles upheld.

## Outcome

- ✅ Impact: Comprehensive Phase 2 technical plan with 7 milestones, 13-day roadmap, complete architecture design
- 🧪 Tests: Constitution compliance validated (9/9 pre-design, 9/9 post-design)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/ directory
- 🔁 Next prompts: Ready for /sp.tasks to create detailed task list
- 🧠 Reflection: Design is incremental, technically sound, and strictly scoped to Silver Tier. All decisions justified with clear rationale.

## Evaluation Notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution compliance - ALL PASS (9/9 pre, 9/9 post)
- Prompt variant (if applicable): Standard sp.plan execution
- Next experiment (smallest change to try): Proceed to /sp.tasks to generate actionable task list for implementation
