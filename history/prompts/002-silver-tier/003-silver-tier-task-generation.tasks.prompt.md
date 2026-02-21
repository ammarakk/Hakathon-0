---
id: 003
title: silver-tier-task-generation
stage: tasks
date_iso: 2025-02-20
surface: agent
model: claude-sonnet-4-6
feature: 002-silver-tier
branch: 002-silver-tier
user: User
command: /sp.tasks
labels:
  - tasks
  - phase-2
  - silver-tier
  - implementation
links:
  spec: specs/002-silver-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-silver-tier/tasks.md
tests:
  - Task format validation (all tasks follow checklist format)
---

## Prompt

**Phase 2 plan ready** acknowledged.

The plan for **Phase 2 (Silver Tier — Functional Assistant)** has been successfully created in `/phase-2/` (or the corresponding SpecifyPlus location) and is now the binding roadmap for this phase.
It remains strictly incremental from Phase 1 and aligned with the Silver Tier requirements in the hackathon document.

Proceeding to the next required step.

### 4.3 TASKS PROMPT for Phase 2

Copy-paste and run the following **exactly** in SpecifyPlus:

```
/sp.tasks

Phase: 2
Phase Name: Silver Tier - Functional Assistant
Phase Folder: /phase-2/

Generate small, verifiable, sequential tasks strictly based on the approved Phase 2 plan and spec.
Each task must be:
- Atomic (doable in 30–90 minutes)
- Clearly testable (has explicit pass/fail or verification condition)
- Limited to Silver Tier requirements only (no Odoo, no FB/IG/X full integration, no weekly briefing, no cloud delegation)
- Building directly on Phase 1 deliverables
- Using ONLY pre-created Agent Skills and connected MCP servers
- No new Python/Node code from scratch — reference/adapt/extend existing skills only

Suggested task breakdown (use this structure or similar — create numbered checklist in /phase-2/tasks.md or equivalent):

1. Update global Dashboard.md for Silver visibility
   → Add section "Active Watchers" (list names & last check time placeholder)
   → Add section "Pending Approvals" and "Recent Plans" (simple bullet or table placeholders)
   → Verify updates visible in Obsidian

2. Update Company_Handbook.md with Silver rules
   → Add rules: "All external posts/sends must be drafted and approved", "Use MCP for sending emails and posting to LinkedIn", "Flag any action involving money or public posting"
   → Verify rules are readable and referenced in reasoning

3. Activate second Watcher (WhatsApp recommended)
   → Reference whatsapp_watcher.md skill
   → Set up session persistence (use placeholder/test session — never commit real session)
   → Run both Phase 1 watcher + WhatsApp watcher
   → Send test WhatsApp message containing keyword (e.g. "urgent invoice") → confirm new .md in /Needs_Action/
   → Verify no conflicts between watchers

4. Implement basic Claude reasoning + Plan.md creation
   → Reference reasoning_loop.md + ralph_wiggum_loop.md skills
   → Manually trigger Claude on a /Needs_Action/ file
   → Claude must: read file → think → create /Plans/Plan_[id or timestamp].md with at least 3 checkbox steps
   → Use Ralph Wiggum pattern to iterate at least once (self-check if plan complete)
   → Verify Plan.md exists and has checkboxes

5. Set up human-in-the-loop approval mechanism
   → Reference human_approval_workflow.md skill
   → For any "send" or "post" action: Claude writes request to /Pending_Approval/action_[id].md
   → File contains: description, draft content preview, [ ] Approve / [ ] Reject + comment field
   → Test: create dummy sensitive action → confirm file appears → manually approve (edit file) → confirm Claude can detect approval on next run

6. Configure one MCP server (email or LinkedIn – start with email)
   → Use mcp-email (simpler)
   → Create test flow: Claude drafts sample email reply based on /Needs_Action/ item
   → Draft saved to vault + approval request created
   → After manual approval → trigger MCP to "send" (use test SMTP or log "sent")
   → Verify action logged or email arrives in test inbox

7. Implement LinkedIn posting flow (draft + approve + MCP)
   → Trigger from business-related /Needs_Action/ item (e.g. completed task or client message)
   → Reference linked_in_posting.md skill
   → Claude generates short promotional post
   → Saves draft + creates /Pending_Approval/ entry
   → After approval → use mcp-social-linkedin to post (or simulate/log if using test account)
   → Verify draft + approval + post attempt logged

8. Add basic scheduling for Watchers
   → Reference cron_scheduling.md skill
   → Create cron jobs (Linux) or Task Scheduler entries (Windows) for both watchers (e.g. every 2–5 minutes)
   → Test: kill watcher processes → wait → confirm they auto-restart and process new items
   → Optional: schedule simple Claude trigger script (if exists) every 30 min

9. Final integration test & verification
   → Create /phase-2/verification.md
   → Document with proof:
     - Two watchers running & creating files
     - Sample Plan.md with iteration
     - Approval flow (before/after file edit)
     - One MCP action completed (email sent or LinkedIn post simulated)
     - Cron jobs listed & auto-run demonstrated
   → State "Silver Tier Functional Assistant achieved" if all pass

Constraints:
- All tasks must stay within Silver scope
- Real external posts/sends should use test accounts only
- Human approval must be enforced for MCP actions
- Mark each task with [ ] checkbox
- No scope from Gold/Platinum

These tasks form the exact implementation contract.
```

Once you have run this `/sp.tasks` command and the Phase 2 tasks are created/confirmed in SpecifyPlus, reply exactly:

"Phase 2 tasks ready"

## Response Snapshot

**Phase 2 Task List Generated Successfully**

Comprehensive task breakdown created for Silver Tier - Functional Assistant:

**Task Organization**:
- Phase 1: Setup (6 tasks) - Vault updates for Silver
- Phase 2: Foundational (8 tasks) - Gmail Watcher setup
- Phase 3: User Story 1 (10 tasks) - Multi-source monitoring
- Phase 4: User Story 2 (10 tasks) - Human approval workflow
- Phase 5: User Story 3 (11 tasks) - MCP Email integration
- Phase 6: User Story 4 (14 tasks) - Reasoning loop with Plan.md
- Phase 7: User Story 5 (14 tasks) - LinkedIn posting flow
- Phase 8: User Story 6 (12 tasks) - Scheduling
- Phase 9: Verification (9 tasks) - Final documentation

**Total: 94 atomic tasks** across 9 phases

**Key Features**:
- All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description`
- Parallelizable tasks marked with [P]
- User story tasks marked with [US1], [US2], [US3], [US4], [US5], [US6]
- All tasks include specific file paths
- Each task is atomic (30-90 minutes) and clearly testable
- All Agent Skills referenced (no new code)

**Task Breakdown by Phase**:

1. **Vault Updates** (T001-T006): Update Dashboard.md and Company_Handbook.md with Silver status sections
2. **Gmail Watcher Setup** (T007-T014): Install dependencies, setup OAuth, implement watcher based on gmail_watcher.md skill
3. **US1 - Multi-Source Monitoring** (T015-T024): Test FilesystemWatcher + GmailWatcher running concurrently
4. **US2 - Human Approval** (T025-T034): Implement approval detection, request creation, polling based on human_in_loop.md skill
5. **US3 - MCP Email** (T035-T045): Install MCP Email server, create client, test send with approval
6. **US4 - Reasoning Loop** (T046-T059): Implement Plan.md creation and iteration using ralph_wiggum_loop.md skill
7. **US5 - LinkedIn Posting** (T060-T073): Install MCP LinkedIn, create post generator, test approval and posting
8. **US6 - Scheduling** (T074-T085): Create Task Scheduler entries, test auto-restart
9. **Verification** (T086-T094): Document results, verify all 12 success criteria

**Constitutional Compliance**:
- ✅ Silver Tier only (no Gold/Platinum features)
- ✅ Agent Skills referenced only (gmail_watcher, human_in_loop, ralph_wiggum_loop, linked_in_posting, mcp_email, mcp_social_linkedin, reasoning_loop, cron_scheduling)
- ✅ No MCP servers for cloud deployment
- ✅ No scheduling for Claude reasoning (Silver+)
- ✅ Privacy: Secrets stay local-only
- ✅ Human approval enforced for MCP actions

## Outcome

- ✅ Impact: Comprehensive task list for Phase 2 implementation with 94 atomic tasks across 9 phases
- 🧪 Tests: Task format validated - ALL tasks follow checklist format with checkboxes, IDs, and file paths
- 📁 Files: specs/002-silver-tier/tasks.md
- 🔁 Next prompts: Ready for /sp.implement to execute tasks
- 🧠 Reflection: Task list is immediately executable with clear dependencies and parallel opportunities. All tasks strictly scoped to Silver Tier requirements.

## Evaluation Notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Task format validation - ALL PASS (94/94 tasks follow correct format)
- Prompt variant (if applicable): Standard sp.tasks execution
- Next experiment (smallest change to try): Proceed to /sp.implement to begin task execution
