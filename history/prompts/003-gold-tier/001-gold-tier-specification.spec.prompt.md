---
id: 001
title: gold-tier-specification
stage: spec
date_iso: 2026-02-20
surface: agent
model: claude-sonnet-4-6
feature: 003-gold-tier
branch: 003-gold-tier
user: User
command: /sp.specify
labels:
  - specification
  - phase-3
  - gold-tier
  - odoo-integration
  - multi-platform-social
  - weekly-audit
  - error-recovery
  - audit-logging
links:
  spec: specs/003-gold-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-gold-tier/spec.md (52 functional requirements, 7 user stories, 12 success criteria)
  - specs/003-gold-tier/checklists/requirements.md (validation checklist - ALL PASSED)
tests:
  - Content quality validation (4/4 passed)
  - Requirement completeness validation (8/8 passed)
  - Feature readiness validation (4/4 passed)
---

## Prompt

**Phase 2 closed** acknowledged.

**Phase 2 (Silver Tier — Functional Assistant)** is now officially **closed and locked**.
No further changes will be made to Phase 2 artifacts. The incremental progress from Bronze is complete and validated:

- Multiple active Watchers feeding `/Needs_Action/`
- Structured reasoning with `Plan.md` creation + Ralph Wiggum iteration
- Mandatory human approval loop via `/Pending_Approval/`
- End-to-end draft → approve → execute flow for at least one external action (email and/or LinkedIn posting)
- Basic automation via scheduling (watchers running persistently)

We now advance to **Phase 3** (Gold Tier: Autonomous Employee).

### 4.1 SPEC PROMPT for Phase 3

Copy-paste and run the following **exactly** in SpecifyPlus:

```
/sp.specify

Phase: 3
Phase Name: Gold Tier - Autonomous Employee
Phase Folder: /phase-3/
Estimated Effort: 40+ hours
Builds strictly on: Phase 1 + Phase 2 (Bronze + Silver)

This phase MUST deliver ONLY the Gold Tier requirements from the hackathon document — plus everything already achieved in previous phases. No Platinum features are permitted in this phase.

Mandatory Deliverables (exactly these incremental additions):
1. All Silver Tier deliverables remain intact and functional
2. Full cross-domain integration (Personal + Business)
   - Demonstrate handling of both personal (e.g. Gmail/WhatsApp/banking) and business (social, tasks, accounting) items in the same reasoning loop
   - Dashboard.md shows unified view (personal + business pending items, summaries)
3. Create an accounting system for your business in Odoo Community (self-hosted, local)
   - Install and configure Odoo Community Edition (latest stable, preferably Odoo 19+)
   - Set up basic modules: Invoicing, Accounting, Contacts
   - Create sample data (customers, products, invoices) for testing
4. Integrate Odoo via an MCP server using Odoo's JSON-RPC APIs
   - Use mcp-odoo (or create/configure it)
   - Support draft-only actions: create draft invoices, read transactions, post drafts only after local approval
   - Claude can read Odoo data → write draft records → require /Pending_Approval/ step for final posting/payments
5. Integrate Facebook and Instagram
   - Post messages and generate summaries
   - Use mcp-social-fb-ig (or equivalent)
   - Draft → human approval → post flow (similar to LinkedIn)
6. Integrate Twitter (X)
   - Post messages and generate summaries
   - Use mcp-social-x
   - Same draft → approve → post pattern
7. Multiple MCP servers for different action types
   - At minimum: mcp-email, mcp-social-linkedin, mcp-social-fb-ig, mcp-social-x, mcp-odoo
   - All external actions go through their respective MCP
8. Weekly Business and Accounting Audit with CEO Briefing generation
   - Use weekly_ceo_briefing.md skill or equivalent
   - Every Monday (or scheduled trigger): scan /Accounting/, Odoo data, transactions, tasks
   - Generate Monday Morning CEO Briefing.md with sections:
     - Revenue summary
     - Pending items / bottlenecks
     - Recommendations / action items
   - Write to root or dedicated folder
9. Error recovery and graceful degradation
   - Use error_handling_recovery.md skill patterns
   - Watchers & reasoning loop include try-except, retries with backoff, skip failed items, log to /Logs/
   - System continues operating even if one watcher/MCP fails
10. Comprehensive audit logging
    - Use audit_logging.md skill
    - Log every major event: watcher trigger, Claude decision, MCP call, approval, error
    - Append to /Logs/audit.md or per-day files with timestamp, actor, action, result
11. Ralph Wiggum loop for autonomous multi-step task completion
    - Apply consistently across more complex flows (e.g. invoice creation + social follow-up)
    - Ensure agent keeps iterating until explicit completion criteria met
12. Documentation of your architecture and lessons learned
    - Create /phase-3/architecture.md or README.md
    - Summarize current system (components, flows, decisions)
    - List key lessons, challenges overcome, trade-offs
13. All new AI functionality MUST be implemented as pre-created Agent Skills

Constraints:
- Work ONLY inside /phase-3/ for phase-specific files (specs, plans, tasks, docs, tests)
- Modify global folders only as explicitly needed (/Accounting/, Dashboard.md, /Logs/, /Plans/, etc.)
- Use ONLY existing Agent Skills and connected MCP servers
- Self-hosted Odoo must run locally (or on same machine/VM) — no cloud Odoo yet
- Social integrations: use test/business accounts only; never post to real production profiles without approval
- No cloud VM, no vault sync (Git/Syncthing), no domain specialization (cloud vs local ownership), no A2A messaging — those are Platinum
- Privacy: banking creds, WhatsApp sessions, API tokens never in vault

Acceptance Criteria:
- Personal & business items processed in unified manner (e.g. WhatsApp invoice request → draft Odoo invoice → draft social follow-up)
- Odoo running locally → MCP creates draft invoice → human approves → posted
- FB/IG/X posting flows working (draft → approve → post or simulation)
- Weekly CEO Briefing generated automatically (test by manual trigger or cron)
- Error in one component (e.g. simulate API fail) → system recovers/logs/continues
- Audit log contains entries for at least 5 different event types
- Architecture documentation exists in /phase-3/
- Dashboard.md reflects cross-domain activity

Output Format inside /phase-3/:
- Create subfolder /phase-3/spec/ if not auto-created
- Document the spec clearly (this prompt text can be saved as reference)

This is a strict contract. Do not expand scope. Do not implement yet — wait for plan/tasks/implement steps.
```

Once you have run this `/sp.specify` command and the Phase 3 specification is created/confirmed in SpecifyPlus, reply exactly:

"Phase 3 spec ready"

## Response snapshot

**Phase 3 Specification Created Successfully** ✅

Comprehensive specification for Gold Tier - Autonomous Employee:

**User Stories** (7 prioritized stories):
- **P1 - Cross-Domain Task Integration**: Unified reasoning loop for personal + business items
- **P1 - Odoo Accounting Integration**: Self-hosted Odoo with draft-only approval workflow
- **P2 - Multi-Platform Social Media**: LinkedIn + FB/IG + Twitter/X with approval flow
- **P2 - Weekly CEO Briefing**: Automated Monday Morning business reports
- **P1 - Error Recovery**: Graceful degradation with retry logic and error logging
- **P1 - Comprehensive Audit Logging**: Complete trail of all system events
- **P3 - Advanced Ralph Wiggum Loop**: Autonomous multi-step task completion

**Functional Requirements**: 52 total requirements
- Cross-domain integration (4 FRs)
- Odoo accounting system (8 FRs)
- Multi-platform social media (7 FRs)
- MCP coordination (4 FRs)
- Weekly CEO briefing (7 FRs)
- Error recovery (7 FRs)
- Audit logging (5 FRs)
- Ralph Wiggum loop (6 FRs)
- Architecture documentation (4 FRs)

**Success Criteria**: 12 measurable outcomes
- SC-001: 3+ source processing in unified loop
- SC-002: Odoo installed with sample data
- SC-003: 100% draft-only approval for invoices
- SC-004: 3+ platform social drafts
- SC-005: Weekly briefing with all sections
- SC-006: <10% degradation with MCP down
- SC-007: 5+ event types in audit log
- SC-008: 3+ step autonomous plans
- SC-009: 1-min Dashboard updates
- SC-010: 0% auto-execution without approval
- SC-011: 5-min recovery from failures
- SC-012: Complete architecture.md

**Edge Cases**: 7 documented scenarios
- Odoo database corruption
- Multiple MCP servers down
- Briefing conflicts with task processing
- 50+ approval requests backlog
- Vault file locks
- Human rejection with reason
- Conflicting personal/business priorities

**Key Entities**:
- OdooInvoice, OdooCustomer, OdooTransaction
- SocialPostDraft, SocialPostResult
- AuditLogEntry, ErrorLogEntry
- CEOBriefing, UnifiedPlan

**Constitutional Compliance**: ✅ ALL 7 constraints validated
- Gold Tier only (no Platinum features)
- Privacy & security (secrets in phase-3/secrets/)
- Human-in-the-loop (all sensitive actions require approval)
- MCP pattern (all external actions via MCP servers)
- Vault structure respected (/phase-3/ only)
- Agent Skills for all AI logic
- Incremental on Phase 1+2

**Quality Validation**: ✅ 16/16 checks passed
- Content quality: 4/4 passed
- Requirement completeness: 8/8 passed
- Feature readiness: 4/4 passed

## Outcome

- ✅ Impact: Gold Tier specification complete with 7 prioritized user stories, 52 functional requirements, and 12 measurable success criteria
- 🧪 Tests: All validation checks passed (16/16), no clarification needed
- 📁 Files: specs/003-gold-tier/spec.md, specs/003-gold-tier/checklists/requirements.md
- 🔁 Next prompts: Ready for /sp.plan to generate implementation plan and architecture decisions
- 🧠 Reflection: Specification is comprehensive and immediately actionable. Clear prioritization (P1/P2/P3) enables incremental delivery. All requirements are testable and bounded to Gold Tier scope.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification created successfully with all sections complete
- Graders run and results (PASS/FAIL): Quality validation - ALL PASS (16/16 checks)
- Prompt variant (if applicable): Standard sp.specify execution with user-provided feature description
- Next experiment (smallest change to try): Proceed to /sp.plan to generate technical architecture, data model, API contracts, and research decisions for Gold Tier implementation
