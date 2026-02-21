# Tasks: Silver Tier - Functional Assistant (Phase 2)

**Input**: Design documents from `/specs/002-silver-tier/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual verification only - no automated tests in Silver phase.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[TaskID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Global vault folders**: `AI_Employee_Vault/` (Dashboard.md, Company_Handbook.md, Needs_Action/, Done/, Plans/, Pending_Approval/)
- **Phase-specific code**: `phase-2/` for all implementation files
- **Phase-1 code**: `phase-1/` (from Bronze Tier - remains intact)

---

## Phase 1: Setup (Vault Updates for Silver)

**Purpose**: Update global vault files to reflect Silver Tier capabilities

- [ ] T001 [P] Update Dashboard.md in AI_Employee_Vault/ to add "Silver Tier Status" section with "Active Watchers" table (Watcher Name, Status, Last Check, Items Found)
- [ ] T002 [P] Update Dashboard.md in AI_Employee_Vault/ to add "Pending Approvals" table (Action, Type, Priority, Waiting Since)
- [ ] T003 [P] Update Dashboard.md in AI_Employee_Vault/ to add "Recent Plans" table (Plan, Tasks, Progress, Status)
- [ ] T004 [P] Update Company_Handbook.md in AI_Employee_Vault/ to add Silver rule: "All external posts and sends must be drafted for approval before execution"
- [ ] T005 [P] Update Company_Handbook.md in AI_Employee_Vault/ to add Silver rule: "Use MCP servers for sending emails and posting to LinkedIn"
- [ ] T006 [P] Update Company_Handbook.md in AI_Employee_Vault/ to add Silver rule: "Flag any action involving payments, public posting, or data transfers for human approval"

**Checkpoint**: Vault files updated with Silver status sections

---

## Phase 2: Foundational (Second Watcher Setup)

**Purpose**: Set up Gmail Watcher alongside existing FilesystemWatcher

**⚠️ CRITICAL**: Second watcher must be operational before user story testing

- [ ] T007 Install Python dependencies: google-auth, google-api-python-client, google-auth-oauthlib (pip install)
- [ ] T008 [P] Create phase-2/secrets/ directory for Gmail credentials (add to .gitignore)
- [ ] T009 [P] Set up Gmail API OAuth flow per gmail_watcher.md skill: Create project in Google Cloud Console, enable Gmail API, create OAuth credentials
- [ ] T010 [P] Download Gmail credentials JSON and save to phase-2/secrets/gmail_credentials.json (NEVER commit this file)
- [ ] T011 [P] Create phase-2/code/gmail_watcher.py based on gmail_watcher.md Agent Skill (reference: .claude/commands/gmail_watcher.md)
- [ ] T012 [P] Create phase-2/code/test_config.py with VAULT_PATH (absolute path to AI_Employee_Vault) and GMAIL_LABEL (filter for "important" emails)
- [ ] T013 [P] Create phase-2/code/launch_gmail_watcher.bat script to run GmailWatcher with test_config.py parameters
- [ ] T014 [P] Test Gmail OAuth authorization flow: Run python gmail_watcher.py --auth and complete browser authorization

**Checkpoint**: Gmail Watcher code ready to run

---

## Phase 3: User Story 1 - Multi-Source Monitoring (Priority: P1) 🎯 MVP

**Goal**: Verify Gmail and Filesystem watchers run concurrently and create files in /Needs_Action/

**Independent Test**: Start both watchers, trigger events in both sources (email + file drop), verify separate action files created

### Setup for User Story 1

- [ ] T015 [P] [US1] Create Gmail test label "AI Employee Test" in Gmail account for testing
- [ ] T016 [P] [US1] Update phase-2/code/test_config.py with correct VAULT_PATH and GMAIL_LABEL="AI Employee Test"

### Verification for User Story 1

- [ ] T017 [US1] Start FilesystemWatcher in terminal: cd phase-1/code && python filesystem_watcher.py
- [ ] T018 [US1] Start GmailWatcher in terminal: cd phase-2/code && python gmail_watcher.py
- [ ] T019 [US1] Drop test file into test_drop_folder: echo "Multi-watcher test" > test_drop_folder/test_file.txt
- [ ] T020 [US1] Send test email to self with subject "Test Multi-Watcher" and label "AI Employee Test"
- [ ] T021 [US1] Verify two separate .md files created in AI_Employee_Vault/Needs_Action/ (one from filesystem, one from Gmail)
- [ ] T022 [US1] Verify files have unique timestamps and different source metadata (source: filesystem vs source: gmail)
- [ ] T023 [US1] Stop both watchers (Ctrl+C in both terminals)
- [ ] T024 [US1] Update Dashboard.md "Active Watchers" section to show both watchers as tested with last check times

**Checkpoint**: Multi-source monitoring verified - both watchers create independent files

---

## Phase 4: User Story 2 - Human Approval Workflow (Priority: P1) 🎯 MVP

**Goal**: Implement human-in-the-loop approval for sensitive actions

**Independent Test**: Trigger sensitive action, verify approval request created, manually approve, verify action executes

### Implementation for User Story 2

- [ ] T025 [P] [US2] Create phase-2/code/approval_detector.py based on human_in_loop.md skill to detect sensitive actions (payments >$500, sends, posts)
- [ ] T026 [P] [US2] Create phase-2/code/approval_request_creator.py to write approval requests to /Pending_Approval/action_[id].md
- [ ] T027 [P] [US2] Create phase-2/code/approval_poller.py to poll /Pending_Approval/ every 30 seconds for [x] Approved or [x] Rejected

### Verification for User Story 2

- [ ] T028 [US2] Manually create test sensitive action: Create file in /Needs_Action/ with content indicating "Send email to client"
- [ ] T029 [US2] Run approval_detector.py and approval_request_creator.py to process sensitive action
- [ ] T030 [US2] Verify approval request file created in AI_Employee_Vault/Pending_Approval/ with [ ] Approve / [ ] Reject checkboxes
- [ ] T031 [US2] Edit approval request file to add [x] Approved
- [ ] T032 [US2] Run approval_poller.py to detect approval and log "Would execute action" (or execute if using test MCP)
- [ ] T033 [US2] Verify approval poller logs show approval detected and action marked for execution
- [ ] T034 [US2] Test rejection: Create another sensitive action, mark [x] Rejected, verify action cancelled and note written to AI_Employee_Vault/Logs/

**Checkpoint**: Human approval workflow functional - sensitive actions require approval

---

## Phase 5: User Story 3 - MCP Email Integration (Priority: P2) 🎯 MVP

**Goal**: Integrate MCP Email server for sending approved emails

**Independent Test**: Draft email, get approval, send via MCP, verify email received

### Implementation for User Story 3

- [ ] T035 [P] [US3] Install MCP Email server: npm install -g @modelcontextprotocol/server-email
- [ ] T036 [P] [US3] Create phase-2/.env file with MCP_EMAIL_HOST=localhost and MCP_EMAIL_PORT=3000
- [ ] T037 [P] [US3] Create phase-2/code/mcp_email_client.py based on mcp_email.md skill to send emails via MCP
- [ ] T038 [P] [US3] Update approval_poller.py to call mcp_email_client.py when email approval detected

### Verification for User Story 3

- [ ] T039 [US3] Start MCP Email server in test mode: mcp-email --port 3000 --test-mode
- [ ] T040 [US3] Create test email draft in /Pending_Approval/email_draft_test.md with To, Subject, Body
- [ ] T041 [US3] Approve email draft: Edit file to add [x] Approved
- [ ] T042 [US3] Run approval_poller.py to detect approval and trigger MCP send
- [ ] T043 [US3] Verify MCP Email server logs show send attempt (or check test email inbox)
- [ ] T044 [US3] Verify email draft file moved to AI_Employee_Vault/Done/ with sent timestamp
- [ ] T045 [US3] Stop MCP Email server (Ctrl+C in terminal)

**Checkpoint**: MCP Email integration working - approved emails sent via MCP

---

## Phase 6: User Story 4 - Reasoning Loop with Plan.md (Priority: P1) 🎯 MVP

**Goal**: Implement Claude reasoning loop that creates and iterates Plan.md files

**Independent Test**: Trigger Claude on /Needs_Action/ item, verify Plan.md created with checkboxes, verify iteration

### Implementation for User Story 4

- [ ] T046 [P] [US4] Create phase-2/code/reasoning_trigger.py based on reasoning_loop.md skill to trigger Claude processing
- [ ] T047 [P] [US4] Create phase-2/code/plan_creator.py based on ralph_wiggum_loop.md skill to create Plan.md files
- [ ] T048 [P] [US4] Create phase-2/code/plan_iterator.py to iterate through Plan.md tasks using Stop hook pattern

### Verification for User Story 4

- [ ] T049 [US4] Create test action file in AI_Employee_Vault/Needs_Action/ with content "Client asks for project update"
- [ ] T050 [US4] Run reasoning_trigger.py to trigger Claude processing
- [ ] T051 [US4] Verify Plan.md created in AI_Employee_Vault/Plans/Plan_[timestamp].md
- [ ] T052 [US4] Verify Plan.md contains at least 3 checkbox tasks (e.g., "- [ ] Review project status", "- [ ] Draft response", "- [ ] Send update")
- [ ] T053 [US4] Run plan_iterator.py to execute first task (mark checkbox as complete)
- [ ] T054 [US4] Verify Plan.md updated with first task checked (- [x] instead of - [ ])
- [ ] T055 [US4] Run plan_iterator.py again to execute second task
- [ ] T056 [US4] Verify Plan.md updated with second task checked
- [ ] T057 [US4] Run plan_iterator.py to complete all remaining tasks
- [ ] T058 [US4] Verify Plan.md marked complete and moved to AI_Employee_Vault/Done/
- [ ] T059 [US4] Update Dashboard.md "Recent Plans" section to show completed plan

**Checkpoint**: Reasoning loop functional - Plan.md created and iterated to completion

---

## Phase 7: User Story 5 - LinkedIn Posting Flow (Priority: P2) 🎯 MVP

**Goal**: Implement LinkedIn business posting with approval workflow

**Independent Test**: Trigger business item, draft LinkedIn post, approve, post via MCP (or simulate)

### Implementation for User Story 5

- [ ] T060 [P] [US5] Install MCP LinkedIn server: npm install -g @modelcontextprotocol/server-social-linkedin
- [ ] T061 [P] [US5] Create phase-2/code/linkedin_post_generator.py based on linked_in_posting.md skill
- [ ] T062 [P] [US5] Create phase-2/code/mcp_linkedin_client.py based on mcp_social_linkedin.md skill
- [ ] T063 [P] [US5] Update approval_poller.py to call mcp_linkedin_client.py when LinkedIn post approved

### Verification for User Story 5

- [ ] T064 [US5] Create business-related test file in test_drop_folder/business_completed.txt
- [ ] T065 [US5] Run FilesystemWatcher to detect business file and create action in /Needs_Action/
- [ ] T066 [US5] Run linkedin_post_generator.py to process business action and generate LinkedIn post draft
- [ ] T067 [US5] Verify LinkedIn post draft created in /Pending_Approval/linkedin_post_[id].md with content and hashtags
- [ ] T068 [US5] Approve LinkedIn post: Edit file to add [x] Approved
- [ ] T069 [US5] Start MCP LinkedIn server in test mode: mcp-social-linkedin --port 3001 --test-mode
- [ ] T070 [US5] Run approval_poller.py to detect approval and trigger LinkedIn post
- [ ] T071 [US5] Verify MCP LinkedIn server logs show post attempt (or verify post logged in /Logs/)
- [ ] T072 [US5] Verify LinkedIn post draft moved to AI_Employee_Vault/Done/ with posted timestamp
- [ ] T073 [US5] Stop MCP LinkedIn server (Ctrl+C in terminal)

**Checkpoint**: LinkedIn posting flow functional - business posts drafted and approved

---

## Phase 8: User Story 6 - Scheduling (Priority: P2) 🎯 MVP

**Goal**: Configure automatic watcher execution via Windows Task Scheduler

**Independent Test**: Create scheduled tasks, restart watchers automatically, verify they process new items

### Implementation for User Story 6

- [ ] T074 [P] [US6] Create phase-2/code/create_schedules.ps1 PowerShell script to configure Task Scheduler entries
- [ ] T075 [P] [US6] Create Task Scheduler entry for FilesystemWatcher: Run every 5 minutes using phase-1/code/filesystem_watcher.py
- [ ] T076 [P] [US6] Create Task Scheduler entry for GmailWatcher: Run every 5 minutes using phase-2/code/gmail_watcher.py
- [ ] T077 [P] [US6] Create Task Scheduler entry for Approval Poller: Run every 1 minute using phase-2/code/approval_poller.py

### Verification for User Story 6

- [ ] T078 [US6] List Task Scheduler entries: schtasks /query | findstr "AI Employee"
- [ ] T079 [US6] Verify all three scheduled tasks exist (Filesystem Watcher, Gmail Watcher, Approval Poller)
- [ ] T080 [US6] Kill all watcher processes (if running) to test auto-restart
- [ ] T081 [US6] Wait 6 minutes (next scheduled cycle)
- [ ] T082 [US6] Drop test file in test_drop_folder
- [ ] T083 [US6] Verify new .md file created in AI_Employee_Vault/Needs_Action/ (proves watcher auto-started and processed file)
- [ ] T084 [US6] Check Task Scheduler logs to confirm tasks ran successfully
- [ ] T085 [US6] Update Dashboard.md "Active Watchers" section with current status and last check times

**Checkpoint**: Scheduling functional - watchers auto-start and process items

---

## Phase 9: Integration & Verification

**Purpose**: Document Phase 2 completion and verify all acceptance criteria

- [ ] T086 [P] Create phase-2/verification.md documenting: chosen watchers (Filesystem + Gmail), MCP servers integrated (Email + LinkedIn), scheduling method
- [ ] T087 [P] Document multi-watcher test results with screenshots or copy-paste of action files from both sources
- [ ] T088 [P] Document approval workflow with before/after examples (approval request file before and after [x] Approved)
- [ ] T089 [P] Add copy-paste of sample Plan.md file showing task completion progression
- [ ] T090 [P] Document MCP Email test results (email draft, approval, send confirmation or log)
- [ ] T091 [P] Document MCP LinkedIn test results (post draft, approval, post log or confirmation)
- [ ] T092 [P] Document scheduling results (Task Scheduler entries listed, auto-run verification)
- [ ] T093 [P] Verify all SC-001 through SC-012 success criteria from spec.md:
  - [ ] SC-001: Two watchers run 10+ minutes without crashing
  - [ ] SC-002: Action files created from 2+ unique sources (filesystem + gmail)
  - [ ] SC-003: 100% of sensitive actions create approval requests
  - [ ] SC-004: 95% of approved actions execute within 30 seconds
  - [ ] SC-005: Plan.md files created for complex tasks with 3+ sub-steps
  - [ ] SC-006: Ralph Wiggum loop iterates through Plan.md tasks until completion
  - [ ] SC-007: LinkedIn posting flow completes in under 2 minutes
  - [ ] SC-008: MCP email achieves 99% delivery rate (test mode acceptable)
  - [ ] SC-009: Scheduled watchers start automatically at configured time
  - [ ] SC-010: Dashboard.md shows real-time pending counts by source
  - [ ] SC-011: Zero secrets in vault files (manual verification)
  - [ ] SC-012: All AI uses Agent Skills exclusively (verified by referencing only skills)
- [ ] T094 Write "Silver Tier Functional Assistant achieved" in phase-2/verification.md if all tests pass

**Checkpoint**: Phase 2 complete and ready for user to close

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS multi-watcher testing
- **Phase 3 (User Story 1)**: Depends on Phase 2 completion - requires Gmail Watcher
- **Phase 4 (User Story 2)**: Depends on Phase 1 completion - can run in parallel with Phase 3
- **Phase 5 (User Story 3)**: Depends on Phase 4 completion - requires approval workflow
- **Phase 6 (User Story 4)**: No dependencies - can run independently
- **Phase 7 (User Story 5)**: Depends on Phase 4 completion - requires approval workflow
- **Phase 8 (User Story 6)**: Depends on Phase 2 and Phase 3 completion - requires watchers to be ready
- **Phase 9 (Verification)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Phase 1 - Independent of US1
- **User Story 3 (P2)**: Can start after Phase 4 - Requires US2 approval workflow
- **User Story 4 (P1)**: No dependencies - Can run independently
- **User Story 5 (P2)**: Can start after Phase 4 - Requires US2 approval workflow
- **User Story 6 (P2)**: Depends on Phase 2 and Phase 3 - Requires watchers to be ready

### Parallel Opportunities

- Phase 1: All T001, T002, T003, T004, T005, T006 can run in parallel (update different sections of Dashboard.md and Company_Handbook.md)
- Phase 2: T008, T009, T010, T011, T012 can run in parallel after T007 (create secrets, setup OAuth, create watcher code)
- Phase 4: T025, T026, T027 can run in parallel (create approval detector, request creator, poller)
- Phase 5: T035, T036, T037, T038 can run in parallel (install MCP, create config, create client)
- Phase 6: T046, T047, T048 can run in parallel (create trigger, plan creator, iterator)
- Phase 7: T060, T061, T062, T063 can run in parallel (install MCP, create generators)
- Phase 9: All T086, T087, T088, T089, T090, T091, T092 can run in parallel (create verification docs)

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Vault Updates (T001-T006)
2. Complete Phase 2: Foundational (T007-T014)
3. Add User Story 1 (T015-T024) → Test multi-watcher
4. Add User Story 2 (T025-T034) → Test approval workflow
5. **STOP and VALIDATE**: Test both user stories independently
6. Demo if ready

### Incremental Delivery (All User Stories)

1. Complete Phase 1 → Vault ready
2. Complete Phase 2 → Gmail Watcher ready
3. Add User Story 1 → Test multi-watcher → Verify (Perception expanded!)
4. Add User Story 2 → Test approval workflow → Verify (Safety added!)
5. Add User Story 3 → Test MCP email → Verify (External action working!)
6. Add User Story 4 → Test reasoning loop → Verify (Intelligence added!)
7. Add User Story 5 → Test LinkedIn posting → Verify (Business value!)
8. Add User Story 6 → Test scheduling → Verify (24/7 operation!)
9. Each story adds value without breaking previous stories

### Sequential Strategy (Recommended for Phase 2)

1. Vault Setup (T001-T006)
2. Gmail Watcher Setup (T007-T014)
3. Test US1: Multi-watcher (T015-T024)
4. Test US2: Approval workflow (T025-T034)
5. Test US3: MCP Email (T035-T045)
6. Test US4: Reasoning loop (T046-T059)
7. Test US5: LinkedIn posting (T060-T073)
8. Test US6: Scheduling (T074-T085)
9. Final verification (T086-T094)

---

## Notes

- All tasks stay within Silver Tier scope (no Gold/Platinum features)
- All watcher implementations use existing Agent Skills - no new code outside skills
- MCP servers used: mcp-email, mcp-social-linkedin (local only, no cloud deployment)
- No Odoo integration (Gold+ feature)
- No Facebook/Instagram/X integration (Gold+ feature)
- No weekly audit/CEO briefing (Gold+ feature)
- No cloud deployment/VM (Platinum+ feature)
- No vault synchronization (Platinum+ feature)
- No direct A2A messaging (Platinum+ feature)
- All AI logic uses Agent Skills exclusively
- [P] marks parallelizable tasks (same as T012, T013, T014 can run together)
- [US1], [US2], [US3], [US4], [US5], [US6] mark user story tasks
- Each task is atomic (30-90 minutes) and clearly testable
- Real external posts/sends should use test accounts only
- Human approval must be enforced for all MCP actions

---

**Total Tasks**: 94
**Total Phases**: 9
**Estimated Time**: 13 days (based on plan.md roadmap)
**Ready for Implementation**: ✅ All tasks follow checklist format with file paths
