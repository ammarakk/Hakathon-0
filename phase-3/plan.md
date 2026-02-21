# Implementation Plan: Gold Tier - Autonomous Employee

**Feature**: 003-gold-tier
**Branch**: 003-gold-tier
**Created**: 2026-02-20
**Status**: Draft
**Builds On**: Phase 1 (Bronze) + Phase 2 (Silver)

---

## Technical Context

**Tech Stack** (building on Phases 1+2):
- **Language**: Python 3.11+ (watchers, MCP clients)
- **Vault**: Obsidian markdown (local file system)
- **Accounting**: Odoo Community Edition 19+ (self-hosted, local)
- **MCP Servers**: mcp-email, mcp-social-linkedin, mcp-social-fb-ig, mcp-social-x, mcp-odoo
- **Scheduling**: Windows Task Scheduler / cron
- **Agent Skills**: All AI logic via pre-existing skills (no new prompts)

**Key Libraries** (adding to Phase 1+2):
- `odoorpc` or `requests` (Odoo JSON-RPC integration)
- `python-dotenv` (environment variables for Odoo credentials)
- Existing libraries: `watchdog` (filesystem), `google-api-python-client` (Gmail), etc.

**External Dependencies**:
- Odoo Community Edition (local installation)
- Odoo MCP server (mcp-odoo or equivalent)
- Facebook/Instagram MCP server (mcp-social-fb-ig)
- Twitter/X MCP server (mcp-social-x)
- Test accounts for social platforms

**Integration Points**:
- Odoo JSON-RPC API (http://localhost:8069/jsonrpc)
- Facebook Graph API (via MCP)
- Twitter/X API v2 (via MCP)
- Existing Phase 2 MCP servers (email, LinkedIn)

---

## Constitution Check

### Pre-Design Evaluation

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Document Adherence | ✅ PASS | Gold Tier only - no Platinum features included |
| II. Privacy & Security | ✅ PASS | Odoo credentials stored in phase-3/secrets/, not in vault |
| III. Human-in-the-Loop | ✅ PASS | All Odoo postings and social posts require /Pending_Approval/ |
| IV. MCP Server Pattern | ✅ PASS | All external actions via MCP servers (5 total) |
| V. Ralph Wiggum Loop | ✅ PASS | Applied for complex multi-step tasks (invoice + social posts) |
| VI. Watcher-Triggered | ✅ PASS | Extends Phase 2 watchers, no new watcher types |
| VII. Vault-Only Read/Write | ✅ PASS | Claude reads/writes vault only, Odoo via MCP |
| VIII. Incremental Phases | ✅ PASS | Builds strictly on Phase 1+2, no modifications |
| IX. Agent Skills | ✅ PASS | All AI logic via existing skills (odoo_integration, facebook_instagram, twitter_x, weekly_audit, error_recovery, audit_logging) |

**Gate Status**: ✅ ALL PASS - Proceed with design

---

## Architecture Overview

### System Diagram (Text-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                     PHASE 3: GOLD TIER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │ Phase 1 & 2  │      │   PHASE 3    │                        │
│  │   Watchers   │      │  ADDITIONS   │                        │
│  ├──────────────┤      ├──────────────┤                        │
│  │ • Filesystem │      │ • Odoo Setup │                        │
│  │ • Gmail      │──────┤   (Local)    │                        │
│  │ • WhatsApp   │      │ • Error      │                        │
│  └──────┬───────┘      │   Recovery   │                        │
│         │              │ • Audit      │                        │
│         ▼              │   Logging    │                        │
│  ┌──────────────┐      └──────┬───────┘                        │
│  │ /Needs_Action/◄─────────────┘                                │
│  └──────┬───────┘                                              │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐      ┌──────────────────────────────────┐   │
│  │   Claude     │─────►│  CROSS-DOMAIN REASONING           │   │
│  │  Reasoning   │      │  • Personal + Business tasks      │   │
│  │    Loop      │      │  • Unified Plan.md               │   │
│  └──────┬───────┘      │  • Ralph Wiggum iteration        │   │
│         │              └──────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐      ┌──────────────────────────────────┐   │
│  │     Vault    │      │      DRAFT CREATION               │   │
│  ├──────────────┤      │  • /Plans/Plan.md                 │   │
│  │ • Plans/     │      │  • Odoo draft invoices            │   │
│  │ • Pending_   │      │  • Social post drafts (all plats) │   │
│  │   Approval/  │      │  • Email drafts                   │   │
│  │ • Accounting/│      └──────────────────────────────────┘   │
│  │ • Logs/      │                                              │
│  └──────┬───────┘                                              │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────┐     │
│  │         MULTIPLE MCP SERVERS (5 total)                │     │
│  ├──────────────────────────────────────────────────────┤     │
│  │ Phase 2:              │  Phase 3 Additions:           │     │
│  │ • mcp-email           │  • mcp-odoo                   │     │
│  │ • mcp-social-linkedin │  • mcp-social-fb-ig           │     │
│  │                       │  • mcp-social-x               │     │
│  └──────────────┬─────────────────────────────────────┘     │
│                 │                                              │
│                 ▼                                              │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              EXTERNAL SYSTEMS                          │     │
│  ├──────────────────────────────────────────────────────┤     │
│  │ • Odoo (local, http://localhost:8069)                 │     │
│  │ • Gmail (existing)                                     │     │
│  │ • LinkedIn (existing)                                  │     │
│  │ • Facebook + Instagram (NEW)                          │     │
│  │ • Twitter/X (NEW)                                     │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │         WEEKLY CEO BRIEFING (Monday 8AM)              │     │
│  │ Scans: Accounting/, Odoo, Plans/, Pending/            │     │
│  │ Generates: CEO_Briefing_YYYY-MM-DD.md                 │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow for Cross-Domain Task

**Example**: WhatsApp invoice request → Odoo draft → Social posts

```
1. WhatsApp Watcher detects message with keyword "invoice"
   └─> Creates ActionItem in /Needs_Action/

2. Claude Reasoning Loop triggers
   ├─> Reads /Needs_Action/ items
   ├─> Detects business context (invoice request)
   ├─> Creates Plan.md with tasks:
   │   ├─ [1] Create Odoo draft invoice
   │   ├─ [2] Create LinkedIn post (project completion)
   │   ├─ [3] Create Facebook post (project completion)
   │   ├─ [4] Create Twitter post (project completion)
   │   └─ [5] Create confirmation email
   └─> Applies Ralph Wiggum Loop (iterate until all done)

3. For each task requiring external action:
   ├─> Claude creates draft in vault
   ├─> Creates approval request in /Pending_Approval/
   ├─> Waits for human approval ([x] Approved)
   └─> After approval: MCP executes action

4. All actions logged to /Logs/audit.md
```

---

## Phase 0: Research & Decisions

### Research Tasks

1. **Odoo Community Edition Installation**
   - Decision: Install Odoo 19+ locally using Windows installer or Docker
   - Rationale: Latest stable version, full Community features, local-only
   - Alternatives considered: Odoo.sh (cloud - excluded), Odoo Enterprise (paid - excluded)
   - Implementation: User runs installer, configure admin database, enable modules

2. **Odoo JSON-RPC Authentication**
   - Decision: Use XML-RPC/JSON-RPC with username/password authentication
   - Rationale: Standard Odoo API, no OAuth complexity for local setup
   - Alternatives considered: Odoo REST API (less documented), External API (requires setup)
   - Implementation: Store credentials in phase-3/secrets/.odoo_credentials

3. **Facebook/Instagram API Access**
   - Decision: Use Facebook Graph API via Page Access Token
   - Rationale: Standard API, supports both FB and Instagram
   - Alternatives considered: Instagram Basic Display API (FB Graph covers both)
   - Implementation: User creates Facebook App, generates Page Access Token, stored in phase-3/secrets/

4. **Twitter/X API Access**
   - Decision: Use Twitter API v2 with Bearer Token
   - Rationale: Latest API version, supports posting tweets
   - Alternatives considered: API v1.1 (deprecated)
   - Implementation: User creates X Developer account, generates Bearer Token, stored in phase-3/secrets/

5. **MCP Server Availability**
   - Decision: Use existing MCP servers where available, create stubs for testing
   - Rationale: Not all MCP servers may be publicly available
   - Alternatives considered: Build all MCP servers from scratch (too time-consuming)
   - Implementation: Test MCP availability, create mock responses for testing

6. **Error Recovery Strategy**
   - Decision: Exponential backoff with max 5 retries, skip on persistent failure
   - Rationale: Balances persistence with system stability
   - Alternatives considered: Infinite retry (can block), immediate skip (too aggressive)
   - Implementation: Wrapper function for all MCP calls and watcher operations

7. **Audit Logging Format**
   - Decision: Per-day files (audit-YYYY-MM-DD.md) with structured entries
   - Rationale: Easier to search and archive than single large file
   - Alternatives considered: Single audit.md (hard to search), database (overkill)
   - Implementation: Log rotation script, structured markdown entries

---

## Phase 1: Design & Contracts

### Data Model Extensions

**New Entities for Gold Tier**:

#### OdooInvoice
```yaml
entity: OdooInvoice
fields:
  - invoice_id: int (Odoo internal ID)
  - customer_id: int (Odoo partner ID)
  - line_items: list of {product_id, quantity, price, description}
  - total_amount: decimal
  - status: enum (draft/posted/paid)
  - due_date: date
  - vault_file_path: str (path to draft .md in vault)
relationships:
  - belongs_to: OdooCustomer
  - has_many: OdooInvoiceLineItem
```

#### SocialPostDraft (platform-agnostic)
```yaml
entity: SocialPostDraft
fields:
  - post_id: str (UUID)
  - platform: enum (linkedin/facebook/instagram/twitter)
  - content: str
  - hashtags: list[str]
  - media_attachments: list[str] (optional)
  - business_context: str
  - status: enum (draft/pending_approval/posted/failed)
  - created_at: datetime
  - posted_at: datetime (optional)
  - post_url: str (optional, after posting)
relationships:
  - created_from: ActionItem
  - requires_approval: ApprovalRequest
```

#### CEOBriefing
```yaml
entity: CEOBriefing
fields:
  - briefing_id: str (UUID)
  - date: date (YYYY-MM-DD)
  - revenue_summary:
    - total_mtd: decimal
    - outstanding_invoices: int
    - expenses_mtd: decimal
    - top_customers: list[{name, revenue}]
  - pending_items:
    - approvals_count: int
    - plans_count: int
    - overdue_tasks: int
  - bottlenecks: list[str]
  - recommendations: list[{priority, action}]
  - vault_file_path: str
```

#### AuditLogEntry
```yaml
entity: AuditLogEntry
fields:
  - entry_id: str (UUID)
  - timestamp: datetime (ISO-8601)
  - actor: str (component name)
  - action: str (description)
  - result: enum (success/failure/pending)
  - related_file: str (path, optional)
  - details: dict (additional context)
```

#### ErrorLogEntry
```yaml
entity: ErrorLogEntry
fields:
  - error_id: str (UUID)
  - timestamp: datetime
  - component: str (watcher/MCP/reasoning)
  - error_type: str
  - error_message: str
  - stack_trace: str (optional)
  - retry_count: int
  - resolved: boolean
```

### API Contracts (MCP Tools)

#### Odoo MCP Tools

```python
# Tool: read_odoo_partners
# Description: Read customer/partner records from Odoo
# Input: filters (optional dict)
# Output: list of {id, name, email, phone}
read_odoo_partners(filters: Optional[Dict] = None) -> List[Dict]

# Tool: create_odoo_draft_invoice
# Description: Create draft invoice in Odoo
# Input: customer_id, line_items, due_date
# Output: {invoice_id, status: "draft", total_amount}
create_odoo_draft_invoice(
    customer_id: int,
    line_items: List[Dict],
    due_date: str
) -> Dict

# Tool: post_odoo_invoice
# Description: Post draft invoice to Odoo (requires approval)
# Input: invoice_id
# Output: {invoice_id, status: "posted"}
post_odoo_invoice(invoice_id: int) -> Dict

# Tool: read_odoo_invoices
# Description: Read invoices from Odoo for CEO Briefing
# Input: date_range (optional)
# Output: list of {id, customer, total, status, date}
read_odoo_invoices(date_range: Optional[Dict] = None) -> List[Dict]

# Tool: read_odoo_revenue
# Description: Read revenue summary from Odoo
# Input: month, year
# Output: {total_revenue, outstanding, paid}
read_odoo_revenue(month: int, year: int) -> Dict
```

#### Facebook/Instagram MCP Tools

```python
# Tool: create_fb_post_draft
# Description: Create draft Facebook post
# Input: content, hashtags, media_urls (optional)
# Output: {post_id, platform: "facebook", status: "draft"}
create_fb_post_draft(
    content: str,
    hashtags: List[str],
    media_urls: Optional[List[str]] = None
) -> Dict

# Tool: create_ig_post_draft
# Description: Create draft Instagram post
# Input: content, hashtags, image_url (required for IG)
# Output: {post_id, platform: "instagram", status: "draft"}
create_ig_post_draft(
    content: str,
    hashtags: List[str],
    image_url: str
) -> Dict

# Tool: post_to_facebook
# Description: Post draft to Facebook (requires approval)
# Input: post_id
# Output: {post_id, platform: "facebook", status: "posted", post_url}
post_to_facebook(post_id: str) -> Dict

# Tool: post_to_instagram
# Description: Post draft to Instagram (requires approval)
# Input: post_id
# Output: {post_id, platform: "instagram", status: "posted", post_url}
post_to_instagram(post_id: str) -> Dict

# Tool: generate_fb_summary
# Description: Generate summary of FB post engagement
# Input: post_url
# Output: {likes, comments, shares, summary_text}
generate_fb_summary(post_url: str) -> Dict
```

#### Twitter/X MCP Tools

```python
# Tool: create_x_post_draft
# Description: Create draft Twitter/X post
# Input: content (max 280 chars)
# Output: {post_id, platform: "twitter", status: "draft"}
create_x_post_draft(content: str) -> Dict

# Tool: post_to_x
# Description: Post draft to Twitter/X (requires approval)
# Input: post_id
# Output: {post_id, platform: "twitter", status: "posted", tweet_url}
post_to_x(post_id: str) -> Dict

# Tool: generate_x_summary
# Description: Generate summary of X post engagement
# Input: tweet_url
# Output: {likes, retweets, replies, summary_text}
generate_x_summary(tweet_url: str) -> Dict
```

---

## Quick Start Guide

### Prerequisites

1. **Odoo Community Edition** (local installation)
   - Download: https://www.odoo.com/page/download
   - Install Odoo 19+ for Windows
   - Create admin database during setup
   - Note admin credentials for MCP configuration

2. **Social Platform Developer Accounts**
   - Facebook: Create Meta Developer account, create App, generate Page Access Token
   - Twitter/X: Create X Developer account, create Project, generate Bearer Token
   - LinkedIn: Already configured from Phase 2

3. **MCP Servers**
   - Ensure Phase 2 MCP servers are running: mcp-email, mcp-social-linkedin
   - Install/configure new MCP servers: mcp-odoo, mcp-social-fb-ig, mcp-social-x

### Installation Steps

#### Step 1: Install Odoo Community

1. Download Odoo 19+ Windows installer from https://www.odoo.com/page/download
2. Run installer with default options
3. During setup, create master password (store securely)
4. Create new database (e.g., "ai_employee_business")
5. Access Odoo at http://localhost:8069
6. Login with admin credentials
7. Enable modules: Invoicing, Accounting, Contacts
8. Create test data:
   - 2-3 Customers (Contacts → Create)
   - 2-3 Products (Products → Create)
   - 1-2 sample draft invoices

#### Step 2: Configure Odoo MCP Integration

1. Create `phase-3/secrets/.odoo_credentials`:
   ```
   ODOO_URL=http://localhost:8069
   ODOO_DB=ai_employee_business
   ODOO_USER=admin
   ODOO_PASSWORD=your_admin_password
   ```

2. Install Odoo MCP server:
   ```bash
   npm install -g @modelcontextprotocol/server-odoo
   ```

3. Configure MCP server in Claude Code settings (reference MCP documentation)

4. Test MCP connection:
   ```python
   # Test script provided in phase-3/code/test_odoo_mcp.py
   python phase-3/code/test_odoo_mcp.py
   ```

#### Step 3: Configure Social Platform MCPs

1. **Facebook/Instagram**:
   - Create `phase-3/secrets/.fb_credentials`:
     ```
     FB_PAGE_ACCESS_TOKEN=your_page_access_token
     FB_PAGE_ID=your_page_id
     IG_BUSINESS_ACCOUNT_ID=your_ig_account_id
     ```
   - Install MCP server:
     ```bash
     npm install -g @modelcontextprotocol/server-social-fb-ig
     ```

2. **Twitter/X**:
   - Create `phase-3/secrets/.x_credentials`:
     ```
     X_BEARER_TOKEN=your_bearer_token
     ```
   - Install MCP server:
     ```bash
     npm install -g @modelcontextprotocol/server-social-x
     ```

3. Configure both MCP servers in Claude Code settings

#### Step 4: Update Vault Structure

1. Update `AI_Employee_Vault/Dashboard.md`:
   - Add "Personal Pending Items" section
   - Add "Business Pending Items" section
   - Add "Cross-Domain Active Plans" section
   - Add "Latest CEO Briefing" link

2. Update `AI_Employee_Vault/Company_Handbook.md`:
   - Add cross-domain rules
   - Add Odoo approval thresholds
   - Add social media posting guidelines

3. Create new folders:
   ```bash
   mkdir AI_Employee_Vault/CEO_Briefings
   mkdir AI_Employee_Vault/Accounting/Odoo
   ```

#### Step 5: Test Cross-Domain Integration

1. Create test scenario:
   - Send WhatsApp message with "invoice request from client ABC"
   - Send Gmail with "project completed"

2. Verify:
   - Both watchers create ActionItems in /Needs_Action/
   - Claude creates unified Plan.md with both domains
   - Tasks are labeled [Personal] or [Business]
   - Odoo draft invoice created (if invoice request)
   - Social post drafts created (if project completed)

#### Step 6: Test Weekly CEO Briefing

1. Manually trigger briefing generation:
   ```bash
   python phase-3/code/generate_ceo_briefing.py
   ```

2. Verify:
   - CEO_Briefing_YYYY-MM-DD.md created in vault root
   - Revenue summary from Odoo data
   - Pending items counted correctly
   - Recommendations are actionable

#### Step 7: Test Error Recovery

1. Stop one MCP server (e.g., Odoo)
2. Trigger action requiring that MCP
3. Verify:
   - Error logged to /Logs/errors.md
   - Other components continue operating
   - System retries with exponential backoff
   - Dashboard.md shows "Error: Odoo unavailable"

### Verification Checklist

- [ ] Odoo running at http://localhost:8069
- [ ] Odoo modules enabled (Invoicing, Accounting, Contacts)
- [ ] Odoo test data created (customers, products, invoices)
- [ ] All 5 MCP servers configured and accessible
- [ ] Dashboard.md updated with cross-domain sections
- [ ] Company_Handbook.md updated with cross-domain rules
- [ ] Test cross-domain scenario creates unified Plan.md
- [ ] CEO Briefing generates with all sections
- [ ] Error recovery tested and verified
- [ ] Audit logging verified in /Logs/audit-YYYY-MM-DD.md

---

## Implementation Phases

### Phase 1: Vault Updates (Foundation)
**Deliverable**: Cross-domain visibility in Dashboard and Handbook
**Tasks**:
- Update Dashboard.md structure
- Enhance Company_Handbook.md rules
- Create new vault folders (CEO_Briefings/, Accounting/Odoo/)
**Success**: Dashboard shows Personal/Business sections, Handbook has cross-domain rules

### Phase 2: Odoo Setup & Integration
**Deliverable**: Local Odoo with MCP integration
**Tasks**:
- Install Odoo Community Edition
- Configure modules and test data
- Set up Odoo MCP server
- Create Odoo client code
- Test draft invoice creation
**Success**: Odoo accessible via MCP, draft invoices created from /Needs_Action/

### Phase 3: Social Platform Integration
**Deliverable**: FB/IG/X posting flows
**Tasks**:
- Configure FB/IG MCP server
- Configure X MCP server
- Create social post generators
- Test draft → approve → post flow
**Success**: All three platforms can post with approval workflow

### Phase 4: MCP Coordination
**Deliverable**: Unified MCP routing
**Tasks**:
- Create MCP router logic
- Test all 5 MCP servers accessible
- Verify routing by action type
**Success**: Claude selects correct MCP for each action type

### Phase 5: Weekly CEO Briefing
**Deliverable**: Automated Monday Morning reports
**Tasks**:
- Create briefing generator script
- Scan Odoo, /Accounting/, /Plans/, /Pending_Approval/
- Schedule via Task Scheduler
**Success**: Briefing generated every Monday with all required sections

### Phase 6: Error Recovery
**Deliverable**: Graceful degradation
**Tasks**:
- Add try-except to all watchers
- Implement exponential backoff
- Add error logging
- Test failure scenarios
**Success**: System continues operating when one component fails

### Phase 7: Audit Logging
**Deliverable**: Complete audit trail
**Tasks**:
- Create audit logger utility
- Log all watcher triggers
- Log all Claude decisions
- Log all MCP actions
- Log all approvals
**Success**: /Logs/audit-YYYY-MM-DD.md contains entries for 5+ event types

### Phase 8: Enhanced Ralph Wiggum Loop
**Deliverable**: Autonomous multi-step completion
**Tasks**:
- Apply loop to cross-domain tasks
- Test 3+ step plans
- Verify iteration until complete
**Success**: Complex plans (invoice + social posts + email) complete autonomously

### Phase 9: Documentation & Verification
**Deliverable**: Complete architecture docs and proof
**Tasks**:
- Create architecture.md
- Document lessons learned
- Create verification.md with proofs
**Success**: All Gold deliverables documented and verified

---

## Success Metrics

### Quantitative
- Odoo installed with 3+ customers, 3+ products, 2+ invoices
- 5 MCP servers running and accessible
- CEO Briefing generated with all sections (Revenue, Pending, Recommendations)
- Error recovery tested with 3+ failure scenarios
- Audit log contains 5+ different event types
- Ralph Wiggum loop tested with 3+ step autonomous plan

### Qualitative
- Cross-domain tasks processed in unified manner
- User maintains control via approval workflow
- System continues operating despite single component failure
- Complete audit trail available for review
- Architecture clearly documented with lessons learned

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Odoo installation fails | High | Provide detailed installation guide, create Docker alternative |
| MCP servers unavailable | Medium | Create mock/stub implementations for testing |
| Social API rate limits | Medium | Implement rate limiting, queue posts for delayed posting |
| Error recovery complexity | Medium | Start with simple try-except, add retries incrementally |
| User credential management | High | Clear documentation on credential storage in phase-3/secrets/ |
| Cross-domain prioritization conflicts | Low | Default to business priority, label tasks clearly for manual review |

---

## Next Steps

1. **User installs Odoo Community Edition** locally
2. **User configures social platform developer accounts** (FB, IG, X)
3. **Proceed to `/sp.tasks`** to generate detailed implementation tasks
4. **Execute tasks** following the 9-phase implementation plan

---

**Status**: Ready for task generation
**Next Command**: `/sp.tasks`
