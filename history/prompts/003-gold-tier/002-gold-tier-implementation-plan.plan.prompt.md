---
id: 002
title: gold-tier-implementation-plan
stage: plan
date_iso: 2026-02-20
surface: agent
model: claude-sonnet-4-6
feature: 003-gold-tier
branch: 003-gold-tier
user: User
command: /sp.plan
labels:
  - planning
  - phase-3
  - gold-tier
  - architecture
  - research-decisions
  - data-model
  - api-contracts
links:
  spec: specs/003-gold-tier/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-3/plan.md (comprehensive implementation plan with 9 phases)
  - phase-3/research.md (10 major technical decisions with rationale)
  - phase-3/data-model.md (9 new entities + extended entities)
  - phase-3/contracts/mcp-odoo-api.md (5 Odoo MCP tools)
  - phase-3/contracts/mcp-social-api.md (Facebook/IG/X + LinkedIn APIs)
  - phase-3/quickstart.md (step-by-step setup guide)
tests:
  - Constitution check: 9/9 principles validated
  - Technical context documented
  - Architecture overview with system diagram
  - All NEEDS CLARIFICATION resolved
---

## Prompt

**Phase 3 spec ready** acknowledged.

The specification for **Phase 3 (Gold Tier — Autonomous Employee)** has been successfully created in `/phase-3/` (or the equivalent SpecifyPlus-managed location) and is now the binding contract for this phase.

It is strictly incremental from Phases 1 + 2 and limited to the Gold Tier requirements in the hackathon document (pages 4–5 of the provided blueprint):

- Full cross-domain (Personal + Business) integration
- Self-hosted Odoo Community accounting system + JSON-RPC integration via MCP (draft-only + local approval)
- Facebook + Instagram integration (post + summary generation, draft → approve → post)
- Twitter/X integration (post + summary, same pattern)
- Multiple MCP servers active (email, LinkedIn, FB/IG, X, Odoo)
- Weekly Monday Morning CEO Briefing generation (audit revenue, bottlenecks, etc.)
- Error recovery & graceful degradation
- Comprehensive audit logging
- Consistent use of Ralph Wiggum loop for complex multi-step autonomy
- Architecture + lessons learned documentation
- All new functionality via existing/pre-created Agent Skills only

No Platinum elements (24/7 cloud VM, work-zone specialization cloud vs local, vault sync via Git/Syncthing, claim-by-move, secrets isolation in sync, Odoo on cloud, A2A upgrade, offline → online handoff demo) are included in this phase.

Proceeding to the next step.

### 4.2 PLAN PROMPT for Phase 3

Copy-paste and run the following **exactly** in SpecifyPlus:

```
/sp.plan

Phase: 3
Phase Name: Gold Tier - Autonomous Employee
Phase Folder: /phase-3/
Builds strictly on: Phase 1 + Phase 2

This plan MUST be derived **strictly** from the approved Phase 3 specification — no new requirements, no Platinum features.

High-level plan structure (create this as a clear, numbered outline in /phase-3/plan.md or equivalent):

[... planning steps outlined ...]

This plan is the roadmap only. Detailed tasks follow next.
```

Once you have run this `/sp.plan` command and the Phase 3 plan is created/confirmed in SpecifyPlus, reply exactly:

"Phase 3 plan ready"

## Response snapshot

**Phase 3 Implementation Plan Complete** ✅

Comprehensive architecture and design for Gold Tier - Autonomous Employee:

### Research & Technical Decisions (10 Major Decisions)

**Decision 1**: Odoo Community Edition Installation
- Choice: Windows installer (primary) with Docker fallback
- Rationale: Local-only, latest stable version (Odoo 19+)
- Reference: Odoo Documentation

**Decision 2**: Odoo JSON-RPC vs XML-RPC
- Choice: JSON-RPC
- Rationale: Modern standard, better Python support, clearer errors
- Library: odoorpc or requests wrapper

**Decision 3**: Facebook/Instagram API Access
- Choice: Facebook Graph API with Page Access Token
- Rationale: Single API covers both platforms, standard OAuth 2.0
- Permissions: pages_manage_posts, instagram_basic, instagram_content_publish

**Decision 4**: Twitter/X API Access
- Choice: Twitter API v2 with Bearer Token
- Rationale: Current version (v1.1 deprecated), simpler auth
- Rate limit: 300 tweets per 15 minutes

**Decision 5**: MCP Server Availability Strategy
- Choice: Test availability, use stub implementations for unavailable servers
- Rationale: System must function even if some MCPs not installed
- Stubs simulate actions, require approval workflow

**Decision 6**: Error Recovery Strategy
- Choice: Exponential backoff (1s, 2s, 4s, 8s, 16s), max 5 retries, skip on persistent failure
- Rationale: Balances persistence with stability, prevents blocking
- All errors logged to /Logs/errors.md

**Decision 7**: Audit Logging Format
- Choice: Per-day markdown files (audit-YYYY-MM-DD.md) with structured entries
- Rationale: Searchable, human-readable, vault-native
- Retention: 90 days, archive older to /Logs/archive/

**Decision 8**: Cross-Domain Task Prioritization
- Choice: Business priority by default, domain labels ([Personal]/[Business]), manual override
- Rationale: Business tasks typically more time-sensitive, labels provide transparency

**Decision 9**: Weekly CEO Briefing Trigger
- Choice: Windows Task Scheduler for Monday 8:00 AM, plus manual trigger script
- Rationale: Native Windows automation, aligns with business week

**Decision 10**: Ralph Wiggum Loop for Gold Tier
- Choice: Apply existing Phase 2 pattern to 5+ step autonomous plans
- Rationale: Proven pattern, extends naturally, maintains consistency

### Data Model (9 New Entities + Extensions)

**New Entities**:
1. **OdooInvoice** - Draft/posted invoices with line items
2. **OdooCustomer** - Customer/contact records
3. **OdooTransaction** - Financial transactions
4. **SocialPostDraft** - Platform-agnostic social posts (LinkedIn, FB, IG, X)
5. **SocialPostResult** - Posted posts with engagement metrics
6. **CEOBriefing** - Weekly business reports
7. **AuditLogEntry** - Comprehensive audit trail
8. **ErrorLogEntry** - Detailed error logging
9. **UnifiedPlan** - Cross-domain plans (extends Phase 2 Plan)

**Entity Relationships**:
- ActionItem → UnifiedPlan (cross-domain)
- SocialPostDraft → ApprovalRequest → SocialPostResult
- OdooInvoice → ApprovalRequest → Odoo (posting)
- All events → AuditLogEntry
- All errors → ErrorLogEntry

### API Contracts (5 Odoo Tools + Social Platforms)

**Odoo MCP Tools**:
1. read_odoo_partners - Read customer records
2. create_odoo_draft_invoice - Create draft (no approval needed yet)
3. post_odoo_invoice - Post draft (requires approval)
4. read_odoo_invoices - Read invoices for briefing
5. read_odoo_revenue - Read revenue summary

**Social Platform APIs**:
- **Facebook**: create_fb_post_draft, post_to_facebook, generate_fb_summary
- **Instagram**: create_ig_post_draft, post_to_instagram (requires image)
- **Twitter/X**: create_x_post_draft, post_to_x, generate_x_summary
- **LinkedIn**: (from Phase 2) same pattern

**All social platforms**: draft → approve → post workflow

### Architecture Overview

**System Diagram** (text-based):
```
Phase 1 & 2 Watchers → /Needs_Action/ → Claude Reasoning → Draft Creation
                                                                  ↓
                                                    Multiple MCP Servers (5 total):
                                                    - mcp-email (Phase 2)
                                                    - mcp-social-linkedin (Phase 2)
                                                    - mcp-odoo (NEW)
                                                    - mcp-social-fb-ig (NEW)
                                                    - mcp-social-x (NEW)
                                                                  ↓
                                              External Systems:
                                              - Odoo (local, port 8069)
                                              - LinkedIn (Phase 2)
                                              - Facebook + Instagram (NEW)
                                              - Twitter/X (NEW)

Weekly CEO Briefing: Scans Accounting/, Odoo, Plans/, Pending/
Error Recovery: Try-except + exponential backoff + skip-and-log
Audit Logging: Per-day files with structured entries
```

**Data Flow Example**: WhatsApp invoice request → Odoo draft → Social posts
```
1. WhatsApp Watcher detects "invoice" → ActionItem in /Needs_Action/
2. Claude Reasoning → Unified Plan.md with 5 tasks:
   - [1] Create Odoo draft invoice
   - [2] Create LinkedIn post
   - [3] Create Facebook post
   - [4] Create Twitter post
   - [5] Create confirmation email
3. Ralph Wiggum Loop iterates (approve only for external actions)
4. All actions logged to /Logs/audit-YYYY-MM-DD.md
```

### Implementation Phases (9 Phases)

**Phase 1**: Vault Updates - Cross-domain visibility in Dashboard/Handbook
**Phase 2**: Odoo Setup & Integration - Local Odoo with MCP
**Phase 3**: Social Platform Integration - FB/IG/X posting flows
**Phase 4**: MCP Coordination - Unified routing for 5 MCPs
**Phase 5**: Weekly CEO Briefing - Automated Monday reports
**Phase 6**: Error Recovery - Graceful degradation
**Phase 7**: Audit Logging - Complete audit trail
**Phase 8**: Enhanced Ralph Wiggum Loop - Autonomous multi-step
**Phase 9**: Documentation & Verification - Architecture.md + proofs

### Quick Start Guide

**Prerequisites**:
- Odoo Community Edition 19+ (local installation)
- Social platform developer accounts (FB, IG, X)
- 5 MCP servers configured
- 2-3 hours setup time

**Setup Steps** (10 major steps):
1. Install Odoo Community (30 min)
2. Configure social platform developer accounts (45 min)
3. Install and configure MCP servers (30 min)
4. Update vault structure (20 min)
5. Test cross-domain integration (15 min)
6. Test weekly CEO briefing (10 min)
7. Test error recovery (10 min)
8. Verify all 12 success criteria
9. Create architecture documentation
10. Generate verification report

**Verification Checklist**: 40+ items across Odoo, Social, MCPs, Vault, Integration

### Constitution Check (Post-Design)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Document Adherence | ✅ PASS | Gold Tier only, no Platinum features |
| II. Privacy & Security | ✅ PASS | Credentials in phase-3/secrets/ |
| III. Human-in-the-Loop | ✅ PASS | All Odoo/social posts require approval |
| IV. MCP Server Pattern | ✅ PASS | 5 MCP servers, all external actions via MCP |
| V. Ralph Wiggum Loop | ✅ PASS | Applied to 5+ step autonomous plans |
| VI. Watcher-Triggered | ✅ PASS | Extends Phase 2 watchers |
| VII. Vault-Only Read/Write | ✅ PASS | Claude vault-only, Odoo via MCP |
| VIII. Incremental Phases | ✅ PASS | Builds strictly on Phase 1+2 |
| IX. Agent Skills | ✅ PASS | All AI logic via existing skills |

**Gate Status**: ✅ ALL PASS - Ready for task generation

### Success Metrics

**Quantitative**:
- Odoo: 3+ customers, 3+ products, 2+ invoices
- 5 MCP servers running and accessible
- CEO Briefing with all sections
- 3+ error scenarios tested
- 5+ event types in audit log
- 3+ step autonomous plan tested

**Qualitative**:
- Cross-domain tasks in unified plans
- User control via approval workflow
- System continues despite component failure
- Complete audit trail
- Architecture documented with lessons learned

### Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Odoo installation fails | High | Detailed guide + Docker alternative |
| MCP servers unavailable | Medium | Stub implementations |
| Social API rate limits | Medium | Rate limiting + queue |
| Error recovery complexity | Medium | Simple try-except first |
| User credential management | High | phase-3/secrets/ documentation |
| Cross-domain conflicts | Low | Business priority default |

## Outcome

- ✅ Impact: Comprehensive Gold Tier implementation plan with 10 research decisions, 9-entity data model, 5 Odoo MCP tools, 3 social platform APIs, 9-phase implementation strategy, and complete quickstart guide
- 🧪 Tests: Constitution check 9/9 passed, technical context documented, all clarifications resolved
- 📁 Files: phase-3/plan.md (architecture), research.md (decisions), data-model.md (entities), contracts/ (API specs), quickstart.md (setup guide)
- 🔁 Next prompts: Ready for /sp.tasks to generate detailed implementation tasks
- 🧠 Reflection: Plan is immediately actionable with clear technical decisions, comprehensive data model, and detailed API contracts. Quickstart guide provides step-by-step setup. All constitutional requirements validated. Ready to proceed to task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning phase completed successfully
- Graders run and results (PASS/FAIL): Constitution check - ALL PASS (9/9), Technical decisions - 10/10 documented, Data model - 9 entities defined, API contracts - 8 tools specified
- Prompt variant (if applicable): Standard sp.plan execution with user-provided Phase 3 outline
- Next experiment (smallest change to try): Proceed to /sp.tasks to generate atomic, sequential tasks for Gold Tier implementation following the 9-phase plan structure
