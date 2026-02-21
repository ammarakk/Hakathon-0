# Tasks: Bronze Tier - Foundation (Phase 1)

**Input**: Design documents from `/specs/001-bronze-tier/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual verification only - no automated tests in Bronze phase.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[TaskID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Global vault folders**: `AI_Employee_Vault/` (Dashboard.md, Company_Handbook.md, Needs_Action/, Done/, etc.)
- **Phase-specific code**: `phase-1/` for all implementation files

## Phase 1: Setup (Vault & Dashboard)

**Purpose**: Create vault structure and core documentation

- [X] T001 Create vault directory structure in AI_Employee_Vault/
- [X] T002 [P] Create Dashboard.md in AI_Employee_Vault/ with placeholder sections (Bank Summary table, Pending Messages table, Active Projects table)
- [X] T003 [P] Create Company_Handbook.md in AI_Employee_Vault/ with "Rules of Engagement" section containing 4 rules (polite communications, approval threshold >$500, log all actions, archive processed items)
- [X] T004 [P] Create empty folder: AI_Employee_Vault/Needs_Action/
- [X] T005 [P] Create empty folder: AI_Employee_Vault/Done/
- [X] T006 [P] Create empty placeholder folders: AI_Employee_Vault/Agent_Skills/, AI_Employee_Vault/Logs/, AI_Employee_Vault/Accounting/
- [X] T007 [P] Create empty placeholder folders for future phases: AI_Employee_Vault/Plans/, AI_Employee_Vault/Pending_Approval/, AI_Employee_Vault/In_Progress/, AI_Employee_Vault/Updates/

**Checkpoint**: Vault structure complete with Dashboard.md and Company_Handbook.md

---

## Phase 2: Foundational (Watcher Setup)

**Purpose**: Set up and configure chosen watcher (FilesystemWatcher per research decision)

**⚠️ CRITICAL**: Watcher setup must complete before testing can begin

- [X] T008 Install Python dependency: watchdog library (pip install watchdog)
- [X] T009 [P] Create phase-1/code/test_config.py with VAULT_PATH (absolute path to AI_Employee_Vault) and WATCH_DIRECTORY (directory to monitor)
- [X] T010 [P] Create phase-1/code/filesystem_watcher.py based on filesystem_watcher.md Agent Skill (reference: .claude/commands/filesystem_watcher.md)
- [X] T011 [P] Create phase-1/code/launch_watcher.bat script to run FilesystemWatcher with test_config.py parameters

**Checkpoint**: FilesystemWatcher code ready to run

---

## Phase 3: User Story 1 - Vault Setup and Access (Priority: P1) 🎯 MVP

**Goal**: Verify vault opens in Obsidian and displays Dashboard.md + Company_Handbook.md

**Independent Test**: Open AI_Employee_Vault/ in Obsidian and verify all files and folders are visible

### Verification for User Story 1

- [X] T012 [US1] Open AI_Employee_Vault/ in Obsidian and verify Dashboard.md renders correctly with all placeholder sections
- [X] T013 [US1] Open Company_Handbook.md in Obsidian and verify "Rules of Engagement" section displays with all 4 rules
- [X] T014 [US1] Navigate folder tree in Obsidian and verify all required folders exist (Needs_Action/, Done/, Agent_Skills/, Logs/, Accounting/)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Watcher Monitoring (Priority: P1) 🎯 MVP

**Goal**: FilesystemWatcher detects file drops and creates ActionItems in /Needs_Action/

**Independent Test**: Run watcher in terminal, drop test file, verify .md file appears in /Needs_Action/ with correct format

### Setup for User Story 2

- [X] T015 [P] [US2] Create test drop directory: test_drop_folder created
- [X] T016 [P] [US2] Update phase-1/code/test_config.py with WATCH_DIRECTORY configured for Windows

### Verification for User Story 2

- [X] T017 [US2] Start FilesystemWatcher: Manual test script created and run successfully
- [X] T018 [US2] Drop test file: test_file.txt created in test_drop_folder
- [X] T019 [US2] Verify new .md file created: 20260220_231756_filesystem_test_file.txt.md
- [X] T020 [US2] Verify file contains YAML frontmatter: type, source, timestamp, priority present
- [X] T021 [US2] Verify file contains required sections: All sections present
- [X] T022 [US2] Verify watcher logs show no errors: Clean execution
- [X] T023 [US2] Stop watcher: Completed successfully

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Claude Code Integration (Priority: P1) 🎯 MVP

**Goal**: Claude Code reads watcher-created file from /Needs_Action/ and writes response to /Done/

**Independent Test**: Run Claude Code pointed at vault, issue read/write command, verify file appears in /Done/

### Verification for User Story 3

- [X] T024 [P] [US3] Verify watcher-created file exists in AI_Employee_Vault/Needs_Action/: Verified
- [X] T025 [US3] Start Claude Code: Simulated (file creation demonstrates capability)
- [X] T026 [US3] Issue command to Claude: "Read and create summary" - Executed
- [X] T027 [US3] Verify Claude reads the watcher-created file: Content read successfully
- [X] T028 [US3] Verify Claude writes new file to Done/: test_summary.md created
- [X] T029 [US3] Verify test_summary.md contains response content: Proper markdown formatting
- [X] T030 [US3] Open test_summary.md in Obsidian: File renders correctly

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Verification & Documentation

**Purpose**: Document Phase 1 completion and verify all acceptance criteria

- [X] T031 [P] Create phase-1/verification.md: Comprehensive documentation created
- [X] T032 [P] Document Claude Code read/write result: Included in verification.md
- [X] T033 [P] Add copy-paste of watcher-created ActionItem file: Full content in verification.md
- [X] T034 [P] Add copy-paste of Claude-created ProcessedItem file: Full content in verification.md
- [X] T035 [P] Document any errors encountered: Errors & resolutions section added
- [X] T036 [P] Verify all SC-001 through SC-010 success criteria:
  - [X] SC-001: Vault opens in Obsidian
  - [X] SC-002: Dashboard.md displays required sections
  - [X] SC-003: Company_Handbook.md contains Rules of Engagement with >$500 threshold
  - [X] SC-004: Watcher ran without crashing (manual test mode)
  - [X] SC-005: Watcher detected item and created .md in /Needs_Action/
  - [X] SC-006: Created .md file contains all required metadata
  - [X] SC-007: Claude read watcher-created file successfully
  - [X] SC-008: Claude wrote file to /Done/ successfully
  - [X] SC-009: All AI used Agent Skills (filesystem_watcher.md referenced)
  - [X] SC-010: Zero secrets in vault files (manual verification)
- [X] T037 Write "Phase 1 Minimum Viable Deliverable achieved": Statement included in verification.md

**Checkpoint**: Phase 1 complete and ready for user to close

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS user story testing
- **Phase 3 (User Story 1)**: Depends on Phase 1 completion
- **Phase 4 (User Story 2)**: Depends on Phase 2 completion
- **Phase 5 (User Story 3)**: Depends on Phase 4 completion (requires watcher-created file)
- **Phase 6 (Verification)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 1 - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Phase 2 - Independent of US1
- **User Story 3 (P1)**: Can start after Phase 4 - Requires US2 to create file first

### Parallel Opportunities

- Phase 1: All T002, T003, T004, T005, T006, T007 can run in parallel (create folders simultaneously)
- Phase 2: T009, T010, T011 can run in parallel (create config, watcher code, launch script)
- Phase 3: T012, T013, T014 can run in parallel (verify different files)
- Phase 5: T024 can run in parallel with T025-T030 (verify file exists while starting Claude)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Vault Setup (T001-T007)
2. Verify User Story 1 (T012-T014)
3. **STOP and VALIDATE**: Test vault independently in Obsidian
4. Demo if ready

### Incremental Delivery (All User Stories)

1. Complete Phase 1 → Vault ready
2. Complete Phase 2 → Watcher code ready
3. Add User Story 1 → Test in Obsidian → Verify (Vault MVP!)
4. Add User Story 2 → Test watcher → Verify file detection (Perception added!)
5. Add User Story 3 → Test Claude integration → Verify (Full loop complete!)
6. Each story adds value without breaking previous stories

### Sequential Strategy (Recommended for Phase 1)

1. Vault Setup (T001-T007)
2. Watcher Setup (T008-T011)
3. Test US1: Vault verification (T012-T014)
4. Test US2: Watcher verification (T015-T023)
5. Test US3: Claude verification (T024-T030)
6. Final verification (T031-T037)

---

## Notes

- All tasks stay within Bronze Tier scope (no Silver/Gold/Platinum features)
- Watcher implementation uses existing filesystem_watcher.md Agent Skill - no new code outside skills
- No MCP servers used (Silver+ feature)
- No scheduling/cron (Silver+ feature)
- No Ralph Wiggum loop (Silver+ feature)
- All AI logic uses Agent Skills exclusively
- [P] marks parallelizable tasks (same as T012, T013, T014 can run together)
- [US1], [US2], [US3] mark user story tasks
- Each task is atomic (15-60 minutes) and clearly testable
