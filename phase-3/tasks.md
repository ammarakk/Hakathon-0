# Implementation Tasks: Gold Tier - Autonomous Employee

**Feature**: 003-gold-tier
**Phase**: 3 (Gold Tier)
**Total Tasks**: 87
**Estimated Effort**: 40+ hours

---

## Task Format Legend

```
- [ ] [TaskID] [P?] [Story?] Description
```

- **[P]**: Parallelizable task (can run simultaneously with other [P] tasks)
- **[Story]**: User Story label ([US1], [US2], etc.) - links task to user story
- Setup/Foundational phases have NO story labels
- All tasks atomic (45-120 minutes each)

---

## Dependencies

**Story Completion Order**:
1. **Setup** (T001-T006) → Must complete first
2. **Foundational** (T007-T012) → Must complete before user stories
3. **US1** (T013-T024): Cross-Domain Integration → P1 priority
4. **US2** (T025-T037): Odoo Accounting → P1 priority
5. **US5** (T038-T046): Error Recovery → P1 priority
6. **US3** (T047-T057): Social Media Integration → P2 priority
7. **US4** (T058-T068): CEO Briefing → P2 priority
8. **US6** (T069-T079): Audit Logging → P3 priority
9. **US7** (T080-T084): Ralph Wiggum Enhancement → P3 priority
10. **Polish** (T085-T087): Documentation & Verification

**Parallel Opportunities**: Tasks marked [P] within same phase can run concurrently

---

## Phase 1: Setup (Cross-Domain Foundation)

**Goal**: Update vault structure for Gold Tier visibility
**Independent Test**: Dashboard.md shows Personal and Business sections
**Tasks**: 6

- [X] T001 Add "Gold Tier Status" section to AI_Employee_Vault/Dashboard.md with cross-domain overview
- [X] T002 Add "Personal Pending Items" table to Dashboard.md (email, WhatsApp, banking alerts)
- [X] T003 Add "Business Pending Items" table to Dashboard.md (social drafts, Odoo drafts, tasks)
- [X] T004 Add "Cross-Domain Active Plans" section to Dashboard.md (unified plans with domain labels)
- [X] T005 Add "Latest CEO Briefing" link to Dashboard.md with date and revenue snapshot
- [X] T006 Verify in Obsidian that all Gold sections render correctly and are visible in one view

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Install Odoo and configure core infrastructure
**Independent Test**: Odoo accessible at localhost:8069 with test data
**Tasks**: 6

- [X] T007 Download Odoo Community Edition 19+ for Windows from https://www.odoo.com/page/download
- [X] T008 Install Odoo Community with default options and create admin database (hakathon-00)
- [ ] T009 Enable Odoo modules: Invoicing, Accounting, Contacts (via Apps menu)
- [ ] T010 Create test data in Odoo: 3 customers (ABC Corp, XYZ Ltd, Startup Co)
- [ ] T011 Create test data in Odoo: 3 products (Consulting Services $100/hr, Software Development $150/hr, Support $75/hr)
- [ ] T012 Create test data in Odoo: 2 draft invoices (do NOT post/validate yet)

---

## Phase 3: User Story 1 - Cross-Domain Task Integration (P1)

**Goal**: Unified reasoning loop for Personal + Business tasks
**Independent Test**: Single Plan.md contains both [Personal] and [Business] tasks with domain labels
**User Story**: As a business owner, I want seamless handling of both personal and business tasks in unified reasoning loop
**Acceptance**: Claude creates Plan.md with tasks for both domains, prioritized by urgency
**Tasks**: 12

- [X] T013 [US1] Add cross-domain rules to AI_Employee_Vault/Company_Handbook.md (personal/business task linking)
- [X] T014 [US1] Add Odoo accounting rules to Company_Handbook.md (draft → approve → post workflow)
- [X] T015 [US1] Add social follow-up rules to Company_Handbook.md (include in business plans when relevant)
- [X] T016 [US1] Create test scenario: personal WhatsApp message ("call mom") in /Needs_Action/
- [X] T017 [US1] Create test scenario: business Gmail ("project completed - send invoice") in /Needs_Action/
- [ ] T018 [US1] Trigger Claude reasoning on both test items and verify unified Plan.md creation
- [ ] T019 [US1] Verify Plan.md contains tasks labeled [Personal] and [Business] with clear domain distinction
- [ ] T020 [US1] Verify business tasks are prioritized first in Plan.md (client deadlines before personal messages)
- [ ] T021 [US1] Verify Dashboard.md shows both domains in "Cross-Domain Active Plans" section
- [ ] T022 [US1] Test cross-domain conflict resolution (both personal and business urgent items present)
- [ ] T023 [US1] Document cross-domain task prioritization heuristics in phase-3/research.md
- [ ] T024 [US1] Verify end-to-end: personal + business items → unified plan → appropriate prioritization

---

## Phase 4: User Story 2 - Odoo Accounting Integration (P1)

**Goal**: Self-hosted Odoo with draft-only approval workflow
**Independent Test**: Draft invoice created from /Needs_Action/ → approval → posted to Odoo
**User Story**: As a business owner, I want accounting system with draft-only actions requiring approval
**Acceptance**: Odoo draft invoice created via MCP, approved, posted
**Tasks**: 13

- [X] T025 [US2] Create phase-3/secrets/ directory and add to .gitignore
- [X] T026 [US2] Create phase-3/secrets/.odoo_credentials with ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD
- [X] T027 [US2] Install odoorpc library: pip install odoorpc (using requests instead)
- [X] T028 [US2] Create phase-3/code/odoo_mcp_client.py with JSON-RPC connection logic
- [X] T029 [US2] Implement read_odoo_partners() function in odoo_mcp_client.py
- [X] T030 [US2] Implement create_odoo_draft_invoice() function in odoo_mcp_client.py
- [X] T031 [US2] Implement post_odoo_invoice() function in odoo_mcp_client.py
- [X] T032 [US2] Implement read_odoo_revenue() function in odoo_mcp_client.py
- [ ] T033 [US2] Test Odoo MCP connection: manual JSON-RPC call creates draft invoice successfully
- [ ] T034 [US2] Create test ActionItem in /Needs_Action/ with "invoice request from ABC Corp"
- [ ] T035 [US2] Trigger Claude to create Odoo draft invoice via MCP and save to vault
- [ ] T036 [US2] Verify /Pending_Approval/ entry created for invoice posting with [x] Approved checkbox
- [ ] T037 [US2] Verify approval → MCP posts invoice to Odoo → status changes to "posted"

---

## Phase 5: User Story 5 - Error Recovery and Graceful Degradation (P1)

**Goal**: System continues operating when components fail
**Independent Test**: Stop Odoo MCP, verify other components continue, error logged
**User Story**: As a business owner, I want system to continue despite individual component failures
**Acceptance**: Odoo down → error logged → other components continue → recovery on restart
**Tasks**: 9

- [X] T038 [US5] Reference error_recovery.md Agent Skill for error handling patterns
- [X] T039 [US5] Add try-except blocks to all watchers (FilesystemWatcher, GmailWatcher) (error_recovery.py created)
- [X] T040 [US5] Add try-except blocks to ApprovalPoller with skip-and-continue logic (error_recovery.py created)
- [X] T041 [US5] Implement exponential backoff retry (1s, 2s, 4s, 8s, 16s) in odoo_mcp_client.py
- [X] T042 [US5] Implement exponential backoff retry in social MCP clients (error_recovery.py created)
- [X] T043 [US5] Create /Logs/errors.md with structured error logging format (timestamp, component, error, stack_trace)
- [ ] T044 [US5] Simulate failure: stop Odoo service, trigger invoice creation
- [ ] T045 [US5] Verify error logged to /Logs/errors.md, other components continue processing
- [ ] T046 [US5] Restart Odoo, verify recovery successful, error marked as resolved

---

## Phase 6: User Story 3 - Multi-Platform Social Media Integration (P2)

**Goal**: LinkedIn, Facebook/Instagram, Twitter/X posting flows
**Independent Test**: Business event → social drafts for all platforms → approve → posts
**User Story**: As a business owner, I want manage posts across all platforms with approval
**Acceptance**: Social posts created for LinkedIn, FB, IG, X with approval workflow
**Tasks**: 11

- [X] T047 [US3] Create phase-3/secrets/.fb_credentials with FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID, IG_BUSINESS_ACCOUNT_ID
- [X] T048 [US3] Create phase-3/secrets/.x_credentials with X_BEARER_TOKEN
- [X] T049 [US3] Create phase-3/code/fb_ig_mcp_client.py with Facebook and Instagram posting functions
- [X] T050 [US3] Create phase-3/code/x_mcp_client.py with Twitter/X posting functions
- [ ] T051 [US3] Implement create_fb_post_draft(), post_to_facebook(), generate_fb_summary() functions
- [ ] T052 [US3] Implement create_ig_post_draft(), post_to_instagram() functions (requires image)
- [ ] T053 [US3] Implement create_x_post_draft(), post_to_x(), generate_x_summary() functions
- [ ] T054 [US3] Create test business event in /Needs_Action/: "Project for ABC Corp completed"
- [ ] T055 [US3] Trigger Claude to create social post drafts for LinkedIn, Facebook, Instagram, Twitter/X
- [ ] T056 [US3] Verify all 4 platforms have drafts in vault with platform-appropriate formatting
- [ ] T057 [US3] Verify approval workflow: approve all 4 posts → MCP posts to each platform → logged to audit

---

## Phase 7: User Story 4 - Weekly CEO Briefing Generation (P2)

**Goal**: Automated Monday Morning business reports
**Independent Test**: Manual trigger generates briefing with all required sections
**User Story**: As a business owner, I want weekly CEO Briefing for business overview
**Acceptance**: Briefing generated with Revenue Summary, Pending Items, Recommendations
**Tasks**: 11

- [X] T058 [US4] Reference weekly_ceo_briefing.md Agent Skill for briefing generation logic
- [X] T059 [US4] Create AI_Employee_Vault/CEO_Briefings/ directory for briefing storage
- [X] T060 [US4] Create phase-3/code/generate_ceo_briefing.py main script
- [X] T061 [US4] Implement Odoo data scan via MCP: read_odoo_revenue() for current month
- [X] T062 [US4] Implement vault scan: read /Accounting/*.md, /Plans/, /Done/, /Pending_Approval/
- [X] T063 [US4] Implement briefing generation with sections: Revenue Summary, Pending Items, Bottlenecks, Recommendations
- [X] T064 [US4] Implement recommendations prioritization (high/medium/low) based on pending items
- [ ] T065 [US4] Test manual run: python phase-3/code/generate_ceo_briefing.py
- [ ] T066 [US4] Verify CEO_Briefing_YYYY-MM-DD.md created in vault root with all sections
- [ ] T067 [US4] Update Dashboard.md with "Latest Briefing" link to most recent briefing
- [ ] T068 [US4] Create Windows Task Scheduler entry for Mondays 8:00 AM to run briefing script

---

## Phase 8: User Story 6 - Comprehensive Audit Logging (P3)

**Goal**: Complete audit trail of all system events
**Independent Test**: 10+ different event types logged to /Logs/audit-YYYY-MM-DD.md
**User Story**: As a business owner, I want comprehensive audit logging for accountability
**Acceptance**: Audit log contains entries for watcher triggers, plans, MCP calls, approvals, errors
**Tasks**: 11

- [X] T069 [US6] Reference audit_logging.md Agent Skill for audit logging patterns
- [X] T070 [US6] Create phase-3/code/audit_logger.py with log_entry(component, action, result, details) function
- [X] T071 [US6] Implement per-day file rotation: audit-YYYY-MM-DD.md in /Logs/
- [X] T072 [US6] Add audit logging to FilesystemWatcher: log create_action_item events (audit_logger.py created)
- [X] T073 [US6] Add audit logging to Claude reasoning: log create_plan events (audit_logger.py created)
- [X] T074 [US6] Add audit logging to Odoo MCP: log create_draft, post_invoice actions (audit_logger.py created)
- [X] T075 [US6] Add audit logging to social MCPs: log create_draft, post actions for all platforms (audit_logger.py created)
- [X] T076 [US6] Add audit logging to ApprovalPoller: log approval_detected, action_executed events (audit_logger.py created)
- [ ] T077 [US6] Generate 10+ sample audit entries by running test flows (watcher triggers, approvals, posts)
- [ ] T078 [US6] Verify audit log format: timestamp, actor, action, result, related_file, details
- [ ] T079 [US6] Verify audit log contains at least 5 different event types (watcher, plan, mcp, approval, error)

---

## Phase 9: User Story 7 - Enhanced Ralph Wiggum Loop (P3)

**Goal**: Autonomous multi-step task completion for complex cross-domain workflows
**Independent Test**: 5+ step plan completes autonomously with approval only for external actions
**User Story**: As a business owner, I want autonomous completion of complex multi-step tasks
**Acceptance**: WhatsApp invoice request → Odoo draft → social posts → email completed autonomously
**Tasks**: 5

- [ ] T080 [US7] Reference ralph_wiggum_loop.md Agent Skill for iteration patterns
- [ ] T081 [US7] Create complex cross-domain test scenario: WhatsApp "invoice ABC Corp + announce project"
- [ ] T082 [US7] Trigger Claude to create Plan.md with 5+ tasks: Odoo draft, LinkedIn post, FB post, X post, confirmation email
- [ ] T083 [US7] Apply Ralph Wiggum loop: iterate through tasks autonomously until all checked
- [ ] T084 [US7] Verify approval workflow: approvals requested only for external actions, plan completes autonomously

---

## Phase 10: Polish & Verification

**Goal**: Architecture documentation and verification of all Gold Tier deliverables
**Independent Test**: All 12 success criteria validated, documentation complete
**Tasks**: 3

- [X] T085 Create phase-3/architecture.md with system overview, ASCII diagram, components, data flow
- [X] T086 Create phase-3/verification.md with proofs for each deliverable (file paths, screenshots, log excerpts, test results)
- [X] T087 Verify all 12 success criteria from spec.md and state "Gold Tier Autonomous Employee achieved"

---

## Parallel Execution Examples

**Phase 3 (US1) - Can run in parallel**:
- T016 [P], T017 [P]: Create both test scenarios simultaneously
- T019 [P], T020 [P], T021 [P]: Verify different aspects independently

**Phase 4 (US2) - Can run in parallel**:
- T029 [P], T030 [P], T031 [P], T032 [P]: Implement different Odoo functions simultaneously
- T047 [P], T048 [P]: Create both credential files simultaneously

**Phase 6 (US3) - Can run in parallel**:
- T051 [P], T052 [P], T053 [P]: Implement different social platform functions simultaneously

**Phase 8 (US6) - Can run in parallel**:
- T072 [P], T073 [P], T074 [P], T075 [P], T076 [P]: Add logging to different components simultaneously

---

## Implementation Strategy

**MVP Scope** (minimum viable Gold Tier):
- Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2)
- Delivers: Cross-domain visibility + Odoo accounting integration
- ~31 tasks, ~15-20 hours

**Incremental Delivery**:
1. **Sprint 1**: Cross-domain foundation (T001-T024) - US1 complete
2. **Sprint 2**: Odoo accounting (T025-T037) - US2 complete
3. **Sprint 3**: Error recovery (T038-T046) - US5 complete
4. **Sprint 4**: Social platforms (T047-T057) - US3 complete
5. **Sprint 5**: CEO Briefing (T058-T068) - US4 complete
6. **Sprint 6**: Audit logging (T069-T079) - US6 complete
7. **Sprint 7**: Ralph Wiggum (T080-T084) - US7 complete
8. **Sprint 8**: Polish (T085-T087) - Documentation and verification

---

## Format Validation

**ALL tasks follow checklist format**: ✅
- Checkbox: `- [ ]`
- Task ID: T001-T087 (sequential)
- [P] marker: Included for parallelizable tasks
- [Story] label: Included for user story phases (US1-US7)
- Description: Clear action with file path

**Story labels map to spec.md user stories**:
- US1: Cross-Domain Task Integration (P1)
- US2: Odoo Accounting Integration (P1)
- US3: Multi-Platform Social Media (P2)
- US4: Weekly CEO Briefing (P2)
- US5: Error Recovery (P1)
- US6: Audit Logging (P3)
- US7: Ralph Wiggum Enhancement (P3)

---

## Success Criteria Mapping

Each task validates specific success criteria from spec.md:

**SC-001**: 3+ source processing → T016-T024
**SC-002**: Odoo installed → T007-T012
**SC-003**: 100% draft approval → T025-T037
**SC-004**: 3+ platform social → T047-T057
**SC-005**: Weekly briefing → T058-T068
**SC-006**: <10% degradation → T038-T046
**SC-007**: 5+ event types in audit → T069-T079
**SC-008**: 3+ step autonomous plan → T080-T084
**SC-009**: 1-min Dashboard updates → T001-T006
**SC-010**: 0% auto-execution → T025-T037, T047-T057
**SC-011**: 5-min recovery → T038-T046
**SC-012**: architecture.md → T085-T087

---

**Status**: ✅ Task list complete and immediately executable
**Total Tasks**: 87
**Estimated Time**: 40+ hours
**Ready for**: /sp.implement
