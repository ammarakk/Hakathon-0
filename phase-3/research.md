# Research Decisions: Gold Tier - Autonomous Employee

**Feature**: 003-gold-tier
**Created**: 2026-02-20
**Status**: Complete

---

## Decision 1: Odoo Community Edition Installation Method

**Decision**: Install Odoo 19+ locally using Windows installer (primary) with Docker as fallback

**Rationale**:
- Windows installer is most straightforward for Windows users
- Odoo 19 is latest stable version with full Community features
- Local-only installation meets constitutional requirement (no cloud Odoo)
- Docker provides alternative if installer fails

**Alternatives Considered**:
1. **Odoo.sh (cloud)**: Rejected - violates constitutional constraint (no cloud deployment in Gold Tier)
2. **Odoo Enterprise**: Rejected - requires paid license, Community Edition has all needed features
3. **Source installation**: Rejected - too complex, harder to maintain

**Implementation Notes**:
- Download from: https://www.odoo.com/page/download
- Default port: 8069
- Default database: User-created during setup
- Master password: User-defined during setup (store securely)

**Reference**: Odoo Documentation, Installation Guide

---

## Decision 2: Odoo JSON-RPC vs XML-RPC

**Decision**: Use JSON-RPC for all Odoo API interactions

**Rationale**:
- JSON-RPC is modern Odoo standard
- Better JSON parsing support in Python
- Clearer error messages
- Easier debugging

**Alternatives Considered**:
1. **XML-RPC**: Rejected - legacy protocol, more verbose
2. **Odoo REST API**: Rejected - less documented, requires additional setup
3. **External API**: Rejected - requires Odoo Enterprise features

**Implementation Notes**:
- Endpoint: http://localhost:8069/jsonrpc
- Authentication: username/password (stored in phase-3/secrets/.odoo_credentials)
- Library: `odoorpc` or custom `requests` wrapper

**Reference**: Odoo JSON-RPC API Documentation

---

## Decision 3: Facebook/Instagram API Access Method

**Decision**: Use Facebook Graph API with Page Access Token for both platforms

**Rationale**:
- Single API covers both Facebook and Instagram
- Page Access Token allows posting to Facebook Page
- Instagram Business Account integration via Graph API
- Standard OAuth 2.0 flow

**Alternatives Considered**:
1. **Instagram Basic Display API**: Rejected - only works for personal Instagram, not business
2. **Separate FB and IG APIs**: Rejected - Graph API covers both, simpler to use one
3. **Instagram Graph API only**: Rejected - need both platforms

**Implementation Notes**:
- Create Meta Developer account: https://developers.facebook.com
- Create App with "Business" type
- Generate Page Access Token
- For Instagram: Connect Instagram Business Account to Facebook Page
- Store credentials in phase-3/secrets/.fb_credentials

**Required Permissions**:
- `pages_manage_posts` (Facebook posting)
- `instagram_basic` (Instagram reading)
- `instagram_content_publish` (Instagram posting)
- `pages_read_engagement` (engagement metrics)

**Reference**: Facebook Graph API Documentation, Instagram Graph API Documentation

---

## Decision 4: Twitter/X API Access Method

**Decision**: Use Twitter API v2 with Bearer Token (App-only authentication)

**Rationale**:
- API v2 is current version (v1.1 deprecated)
- Bearer Token simplifies authentication (no OAuth flow for app-only)
- Sufficient for posting tweets
- Rate limits: 300 tweets per 15 minutes (window)

**Alternatives Considered**:
1. **OAuth 1.0a User Context**: Rejected - more complex, not needed for posting
2. **OAuth 2.0 Authorization Code Flow**: Rejected - overkill for simple posting
3. **API v1.1**: Rejected - deprecated

**Implementation Notes**:
- Create X Developer account: https://developer.twitter.com
- Create Project and App
- Generate Bearer Token
- Store in phase-3/secrets/.x_credentials
- Use POST /2/tweets endpoint for posting

**Rate Limits**:
- Post tweet: 300 requests per 15 minutes
- User lookup: 900 requests per 15 minutes

**Reference**: Twitter API v2 Documentation

---

## Decision 5: MCP Server Availability Strategy

**Decision**: Test MCP server availability at startup, create stub/mock implementations for unavailable servers

**Rationale**:
- Not all MCP servers may be publicly available or documented
- System must function even if some MCPs are not installed
- Stubs allow testing without full MCP implementation
- User can install MCPs incrementally

**Alternatives Considered**:
1. **Require all MCPs installed**: Rejected - blocks testing, high barrier to entry
2. **Build all MCPs from scratch**: Rejected - too time-consuming for hackathon
3. **Skip features if MCP unavailable**: Rejected - breaks functionality

**Implementation Notes**:
- Each MCP client has `is_available()` check
- If unavailable, log warning and use stub implementation
- Stub implementations:
  - Create draft files in vault (simulate MCP action)
  - Log "would post to [platform]" in audit trail
  - Require approval workflow (same as real MCP)
- User can install real MCP servers later

**Reference**: Model Context Protocol Specification

---

## Decision 6: Error Recovery Strategy

**Decision**: Exponential backoff with max 5 retries, skip on persistent failure, log all errors

**Rationale**:
- Exponential backoff is standard pattern (1s, 2s, 4s, 8s, 16s)
- Max 5 retries prevents infinite loops
- Skip on failure prevents blocking other operations
- Comprehensive logging enables debugging

**Alternatives Considered**:
1. **Immediate retry**: Rejected - can overwhelm failing services
2. **Infinite retry**: Rejected - blocks system indefinitely
3. **Fail fast (no retry)**: Rejected - too aggressive for transient errors
4. **Circuit breaker pattern**: Rejected - more complex than needed for Gold Tier

**Implementation Notes**:
- Retry delays: 1s, 2s, 4s, 8s, 16s (total 31s max wait)
- Retry only on transient errors (network timeout, 5xx status)
- Immediate fail on permanent errors (401 unauthorized, 404 not found)
- All errors logged to /Logs/errors.md with timestamp, component, stack trace

**Pseudo-code**:
```python
def with_retry(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt
            time.sleep(wait)
        except PermanentError as e:
            raise  # Don't retry permanent errors
```

**Reference**: Exponential Backoff Pattern (AWS Architecture Blog)

---

## Decision 7: Audit Logging Format

**Decision**: Per-day markdown files (audit-YYYY-MM-DD.md) with structured entries

**Rationale**:
- Per-day files easier to search and archive
- Markdown format human-readable and vault-native
- Structured entries enable parsing
- Date-based rotation simplifies retention

**Alternatives Considered**:
1. **Single audit.md file**: Rejected - becomes large, hard to search
2. **JSON log files**: Rejected - not human-readable, breaks vault pattern
3. **Database (SQLite)**: Rejected - overkill, not vault-native
4. **syslog**: Rejected - not vault-native, harder to review

**Implementation Notes**:
- File location: /Logs/audit-YYYY-MM-DD.md
- Entry format:
  ```markdown
  ## [HH:MM:SS] [Actor] [Action]

  **Result**: [success/failure/pending]
  **Related File**: [path if applicable]
  **Details**: [JSON or text]
  ```
- Log rotation: Create new file at midnight
- Retention: Keep 90 days, archive older to /Logs/archive/

**Reference**: Audit Logging Best Practices (NIST)

---

## Decision 8: Cross-Domain Task Prioritization

**Decision**: Business priority by default, domain labels for clarity, manual override for conflicts

**Rationale**:
- Business tasks typically more time-sensitive (client deadlines, payments)
- Domain labels ([Personal]/[Business]) provide transparency
- Manual override preserves human control
- Simple heuristic reduces Claude decision complexity

**Alternatives Considered**:
1. **Time-based prioritization**: Rejected - complex, doesn't account for impact
2. **Round-robin**: Rejected - doesn't reflect business needs
3. **Pure manual prioritization**: Rejected - adds friction to every plan
4. **Machine learning model**: Rejected - overkill for Gold Tier

**Implementation Notes**:
- Default priority order:
  1. Business payments (invoices > $500)
  2. Business client communications (emails, messages)
  3. Business social media posts
  4. Personal urgent items (bank alerts, important messages)
  5. Personal routine items
- All tasks labeled with domain in Plan.md
- If user wants different priority: edit Plan.md task order

**Reference**: Task Prioritization Best Practices (Getting Things Done)

---

## Decision 9: Weekly CEO Briefing Trigger

**Decision**: Scheduled via Windows Task Scheduler for Monday 8:00 AM, plus manual trigger script

**Rationale**:
- Scheduled automation matches "always-on" goal
- Monday morning aligns with business week start
- Manual trigger enables testing and ad-hoc briefings
- Task Scheduler native to Windows (no additional dependencies)

**Alternatives Considered**:
1. **Cron only**: Rejected - not native to Windows
2. **Claude-based trigger**: Rejected - adds unnecessary complexity
3. **Webhook trigger**: Rejected - requires cloud deployment (Platinum)
4. **Pure manual**: Rejected - violates automation goal

**Implementation Notes**:
- Task Scheduler command:
  ```
  python phase-3/code/generate_ceo_briefing.py
  ```
- Trigger: Every Monday at 8:00 AM
- Manual trigger: Run script directly
- Script creates CEO_Briefing_YYYY-MM-DD.md in vault root

**Reference**: Windows Task Scheduler Documentation

---

## Decision 10: Ralph Wiggum Loop for Gold Tier

**Decision**: Apply existing Ralph Wiggum pattern from Phase 2, extend to 5+ step autonomous plans

**Rationale**:
- Pattern proven in Phase 2
- Extends naturally to complex cross-domain tasks
- Maintains consistency across phases
- No new logic needed, just application to more scenarios

**Alternatives Considered**:
1. **New autonomous loop pattern**: Rejected - unnecessary complexity
2. **Human in loop for every step**: Rejected - defeats autonomy goal
3. **Fixed workflow engine**: Rejected - less flexible than Ralph Wiggum

**Implementation Notes**:
- Use existing ralph_wiggum_loop.md Agent Skill
- Apply to tasks like:
  1. WhatsApp invoice request
  2. Create Odoo draft invoice
  3. Create LinkedIn post
  4. Create Facebook post
  5. Create Twitter post
  6. Create confirmation email
- Loop iterates until all 6 tasks checked
- Approval only required for external actions (steps 2, 3, 4, 5, 6)

**Reference**: Ralph Wiggum Loop Pattern (Phase 2 implementation)

---

## Summary of Key Technical Choices

| Area | Technology | Rationale |
|------|-----------|-----------|
| Odoo Installation | Windows Installer (v19+) | Local, stable, full features |
| Odoo API | JSON-RPC | Modern, well-documented |
| Facebook/Instagram | Graph API (Page Access Token) | Single API for both platforms |
| Twitter/X | API v2 (Bearer Token) | Current version, simple auth |
| MCP Availability | Stub implementations | System works even if MCPs missing |
| Error Recovery | Exponential backoff (5 retries) | Standard pattern, prevents blocking |
| Audit Logging | Per-day markdown files | Human-readable, searchable |
| Cross-Domain Priority | Business first, domain labels | Matches business needs |
| CEO Briefing Trigger | Task Scheduler (Mon 8AM) | Native Windows automation |
| Multi-Step Autonomy | Ralph Wiggum Loop | Proven Phase 2 pattern |

---

**Status**: ✅ All research decisions complete
**Next**: Proceed to `/sp.tasks` for detailed implementation tasks
