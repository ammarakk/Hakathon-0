---
id: 003
title: gold-tier-task-generation
stage: tasks
date_iso: 2026-02-20
surface: agent
model: claude-sonnet-4-6
feature: 003-gold-tier
branch: 003-gold-tier
user: User
command: /sp.tasks
labels:
  - tasks
  - phase-3
  - gold-tier
  - task-generation
  - implementation-contract
links:
  spec: specs/003-gold-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/tasks.md (87 atomic tasks across 10 phases)
tests:
  - Format validation: ALL tasks follow checklist format (checkbox, ID, labels, file paths)
  - Story mapping: All tasks map to user stories (US1-US7)
  - Parallel execution: 25+ tasks marked [P] for concurrent execution
---

## Prompt

**Phase 3 plan ready** acknowledged.

The plan for **Phase 3 (Gold Tier — Autonomous Employee)** has been successfully generated in `/phase-3/` (or the equivalent SpecifyPlus-managed location) and is now the binding roadmap for this phase.
It remains strictly incremental from Phases 1 + 2 and aligned with the Gold Tier requirements in the hackathon document.

Proceeding to the next required step.

### 4.3 TASKS PROMPT for Phase 3

Copy-paste and run the following **exactly** in SpecifyPlus:

```
/sp.tasks

Phase: 3
Phase Name: Gold Tier - Autonomous Employee
Phase Folder: /phase-3/

Generate small, verifiable, sequential tasks strictly based on the approved Phase 3 plan and spec.
Each task must be:
- Atomic (doable in 45–120 minutes)
- Clearly testable (explicit verification condition or proof artifact)
- Limited to Gold Tier requirements only (no cloud VM, no vault sync, no claim-by-move, no domain specialization, no A2A)
- Building directly on Phases 1 + 2
- Using ONLY pre-created Agent Skills and connected MCP servers
- No new code from scratch outside of configuring/calling existing skills

[... detailed task breakdown ...]

These tasks form the exact implementation contract.
```

Once you have run this `/sp.tasks` command and the Phase 3 tasks are created/confirmed in SpecifyPlus, reply exactly:

"Phase 3 tasks ready"

## Response snapshot

**Phase 3 Task List Generated Successfully** ✅

Comprehensive task breakdown for Gold Tier - Autonomous Employee:

**Total Tasks**: 87 atomic tasks
**Estimated Effort**: 40+ hours
**Format**: ✅ ALL tasks follow checklist format with checkboxes, IDs, story labels, file paths

**Task Organization by Phase**:

1. **Setup** (T001-T006): 6 tasks - Vault updates for cross-domain visibility
2. **Foundational** (T007-T012): 6 tasks - Odoo installation and test data
3. **US1 - Cross-Domain Integration** (T013-T024): 12 tasks - Unified reasoning for Personal + Business
4. **US2 - Odoo Accounting** (T025-T037): 13 tasks - Self-hosted Odoo with draft-only workflow
5. **US5 - Error Recovery** (T038-T046): 9 tasks - Graceful degradation and retry logic
6. **US3 - Social Media** (T047-T057): 11 tasks - LinkedIn + FB/IG + X posting flows
7. **US4 - CEO Briefing** (T058-T068): 11 tasks - Weekly Monday Morning reports
8. **US6 - Audit Logging** (T069-T079): 11 tasks - Comprehensive audit trail
9. **US7 - Ralph Wiggum Loop** (T080-T084): 5 tasks - Autonomous multi-step completion
10. **Polish** (T085-T087): 3 tasks - Architecture documentation and verification

**User Story Priorities**:
- **P1 (High)**: US1 (Cross-Domain), US2 (Odoo), US5 (Error Recovery) - 34 tasks
- **P2 (Medium)**: US3 (Social Media), US4 (CEO Briefing) - 22 tasks
- **P3 (Low)**: US6 (Audit Logging), US7 (Ralph Wiggum) - 16 tasks

**Parallel Opportunities**: 25+ tasks marked [P] for concurrent execution

**Key Features**:
- ✅ All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description`
- ✅ Each task atomic (45-120 minutes) and clearly testable
- ✅ Story labels ([US1]-[US7]) map to user stories from spec.md
- ✅ File paths specified for all code/config tasks
- ✅ Independent test criteria for each user story
- ✅ MVP scope defined: 31 tasks for cross-domain + Odoo foundation
- ✅ Incremental delivery strategy with 8 sprints
- ✅ Success criteria mapping (all 12 SCs validated)

**Constitutional Compliance**:
- ✅ Gold Tier only (no Platinum features: cloud VM, vault sync, claim-by-move, domain specialization, A2A)
- ✅ Agent Skills referenced only (odoo_integration, facebook_instagram, twitter_x, weekly_ceo_briefing, error_recovery, audit_logging, ralph_wiggum_loop)
- ✅ Human approval enforced (Odoo postings, social posts)
- ✅ Privacy: Credentials in phase-3/secrets/
- ✅ MCP Pattern: All external actions via MCP servers (5 total)
- ✅ Builds strictly on Phase 1+2 (no modifications to previous phases)

**Example Tasks**:
- T001: Add "Gold Tier Status" section to Dashboard.md
- T025 [US2]: Create phase-3/secrets/.odoo_credentials file
- T032 [US2]: Implement read_odoo_revenue() function
- T047 [US3]: Create phase-3/secrets/.fb_credentials file
- T069 [US6]: Reference audit_logging.md Agent Skill
- T082 [US7]: Create complex cross-domain test scenario

## Outcome

- ✅ Impact: Comprehensive task list for Phase 3 implementation with 87 atomic tasks across 10 phases, organized by user story priority
- 🧪 Tests: Format validation - ALL PASS (87/87 tasks follow correct checklist format with checkboxes, IDs, story labels, file paths)
- 📁 Files: phase-3/tasks.md
- 🔁 Next prompts: Ready for /sp.implement to execute tasks
- 🧠 Reflection: Task list is immediately executable with clear dependencies and parallel opportunities. All tasks strictly scoped to Gold Tier requirements. MVP scope (31 tasks) delivers core value quickly. Incremental delivery strategy enables validation at each user story.

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation completed successfully
- Graders run and results (PASS/FAIL): Format validation - ALL PASS (87/87 tasks), Story mapping - ALL PASS (all tasks mapped to US1-US7), Constitutional compliance - ALL PASS (Gold Tier only)
- Prompt variant (if applicable): Standard sp.tasks execution with user-provided task breakdown structure
- Next experiment (smallest change to try): Proceed to /sp.implement to begin task execution starting with Phase 1 (Setup) and Phase 2 (Foundational)
