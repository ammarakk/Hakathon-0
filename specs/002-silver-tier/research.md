# Research: Silver Tier - Functional Assistant

**Feature**: 002-silver-tier
**Phase**: 2 (Silver Tier)
**Date**: 2025-02-20
**Status**: Complete

---

## Research Summary

This document consolidates technical research and decisions for Phase 2 (Silver Tier) implementation. All "NEEDS CLARIFICATION" items from the planning phase have been resolved.

---

## Decision 1: Second Watcher Selection

### Decision
**Chosen**: Gmail Watcher

### Rationale
1. **Business Value**: Email is the primary communication channel for most professionals
2. **API Maturity**: Gmail API is well-documented, stable, and widely used
3. **Agent Skill Availability**: `gmail_watcher.md` skill exists and is well-defined
4. **Complementary**: Gmail + Filesystem cover digital + document sources

### Alternatives Considered
1. **WhatsApp Watcher**
   - Pros: Real-time, high engagement
   - Cons: Requires Playwright setup, more complex
   - Verdict: Defer to Gold+ tier
2. **Finance Watcher**
   - Pros: Transaction monitoring
   - Cons: Privacy concerns, bank access complexity
   - Verdict: Defer to Gold+ tier

### Implementation Notes
- Use OAuth 2.0 for Gmail authentication
- Store credentials in `phase-2/secrets/gmail_credentials.json`
- Implement token refresh logic
- Watch for "important" emails (starred or label-based)

---

## Decision 2: MCP Server Priority

### Decision
**Chosen**: Implement MCP Email first, LinkedIn second

### Rationale
1. **Universality**: Email is a universal business tool
2. **Simplicity**: Email sending is straightforward (SMTP/API)
3. **Testability**: Easy to test with test accounts
4. **Incremental Value**: Email provides immediate value; LinkedIn can be added later

### Alternatives Considered
1. **LinkedIn-First Approach**
   - Pros: Meets specific business requirement
   - Cons: LinkedIn API complexity, rate limits
   - Verdict: Better to master email flow first
2. **Parallel Implementation**
   - Pros: Both features delivered together
   - Cons: Increased complexity, harder to debug
   - Verdict: Sequential is safer for Silver tier

### Implementation Notes
- MCP Email: Use `mcp_email.md` skill
- MCP LinkedIn: Use `mcp_social_linkedin.md` skill
- Both use same approval workflow pattern
- Share `/Pending_Approval/` directory structure

---

## Decision 3: Approval Detection Mechanism

### Decision
**Chosen**: File polling every 30 seconds

### Rationale
1. **Simplicity**: No additional watcher needed
2. **Reliability**: Polling is predictable and easy to debug
3. **Acceptable Latency**: 30-second delay is acceptable for approval
4. **Resource Efficient**: Lower overhead than file system watching

### Alternatives Considered
1. **Filesystem Watcher on /Pending_Approval/**
   - Pros: Real-time detection (instant)
   - Cons: Another watcher to manage, complexity
   - Verdict: Overkill for approval workflow
2. **Manual Trigger Only**
   - Pros: Full user control
   - Cons: Not automated, defeats purpose
   - Verdict: Unacceptable for Silver tier

### Implementation Notes
- Polling script: `phase-2/code/approval_poller.py`
- Check interval: 30 seconds (configurable)
- Look for `[x] Approved` or `[x] Rejected` checkboxes
- Execute action and move file to `/Done/` on approval

---

## Decision 4: Plan Iteration Strategy

### Decision
**Chosen**: Ralph Wiggum Loop (Stop Hook Pattern)

### Rationale
1. **Proven Pattern**: Agent skill already exists (`ralph_wiggum_loop.md`)
2. **Error Handling**: Built-in error recovery and retry logic
3. **Completion Detection**: Clear Stop hook for plan completion
4. **Iterative**: Handles complex multi-step tasks well

### Alternatives Considered
1. **Simple Checkbox Iteration**
   - Pros: Easy to understand
   - Cons: No error handling, no completion detection
   - Verdict: Too basic for Silver tier
2. **Recursive Task Decomposition**
   - Pros: Handles arbitrarily complex tasks
   - Cons: Over-engineering, hard to debug
   - Verdict: Defer to Gold+ tier

### Implementation Notes
- Use `ralph_wiggum_loop.md` skill as reference
- Implement Stop hook: all checkboxes checked OR plan complete
- Update Plan.md after each task completion
- Log all iterations to `/Logs/`

---

## Decision 5: Scheduling Platform

### Decision
**Chosen**: Windows Task Scheduler (project runs on Windows)

### Rationale
1. **Platform Match**: Phase 1 implemented on Windows
2. **Built-in**: No additional software required
3. **GUI Available**: Easy to configure and verify
4. **Auto-start**: Can configure to run on system boot

### Alternatives Considered
1. **Cron (Linux)**
   - Pros: Standard for Unix systems
   - Cons: Not native to Windows, requires WSL or Git Bash
   - Verdict: Use Task Scheduler for native Windows support
2. **Python-Based Scheduler**
   - Pros: Cross-platform, flexible
   - Cons: Another process to manage
   - Verdict: Unnecessary complexity

### Implementation Notes
- Create tasks via `schtasks` command or Task Scheduler GUI
- Schedule: Run every 5 minutes for each watcher
- Auto-start: Configure "At startup" trigger
- Log to: `phase-2/logs/scheduler.log`

---

## Decision 6: Sensitivity Detection

### Decision
**Chosen**: Rule-based detection with configurable thresholds

### Rationale
1. **Transparent**: Rules are clear and auditable
2. **Configurable**: Easy to adjust via Company_Handbook.md
3. **Predictable**: Consistent behavior
4. **Implementable**: No ML/AI required

### Sensitivity Rules

| Action Type | Sensitivity | Requires Approval | Reason |
|-------------|-------------|-------------------|--------|
| Email send (no attachments) | Low | Yes | External communication |
| Email send (with attachments) | Medium | Yes | Data leakage risk |
| Email send (payments/contracts) | High | Yes | Financial/legal impact |
| LinkedIn post | Medium | Yes | Public representation |
| Payment >$500 | High | Yes | Financial threshold (from Bronze) |
| Payment ≤$500 | Low | No | Below threshold |
| File deletion | Medium | Yes | Data loss risk |

### Implementation Notes
- Rules defined in `Company_Handbook.md`
- Detection in Agent Skills (not inline code)
- Configurable via YAML frontmatter or handbook rules

---

## Decision 7: Dashboard Update Strategy

### Decision
**Chosen**: Incremental updates to Dashboard.md

### Rationale
1. **Preserves Bronze**: Bronze layout remains intact
2. **Additive**: Silver sections added without removing Bronze
3. **User Friendly**: Users see evolution of capabilities
4. **Backward Compatible**: Obsidian renders correctly

### New Dashboard Sections

```markdown
## Silver Tier Status

### Watcher Activity

| Watcher | Status | Last Check | Items Found |
|---------|--------|------------|-------------|
| Filesystem | Running | 2 mins ago | 3 |
| Gmail | Running | 1 min ago | 5 |

### Pending Approvals

| Action | Type | Priority | Waiting Since |
|--------|------|----------|---------------|
| Email send | email_send | Medium | 5 mins ago |
| LinkedIn post | linkedin_post | High | 15 mins ago |

### Active Plans

| Plan | Tasks | Progress | Status |
|------|-------|----------|--------|
| Client response | 5 | 3/5 | In Progress |
| Invoice review | 3 | 0/3 | Pending |
```

### Implementation Notes
- Add sections below Bronze sections
- Update via Agent Skill (not inline code)
- Manual refresh acceptable for Silver tier
- Auto-refresh可以考虑 for Gold+

---

## Best Practices Research

### Gmail API Integration

**Best Practices**:
1. **Use OAuth 2.0**: Don't store passwords, use tokens
2. **Implement Token Refresh**: Tokens expire after 1 hour
3. **Handle Rate Limits**: Gmail API has quota limits
4. **Batch Operations**: Fetch multiple emails at once
5. **Label-Based Filtering**: Use labels instead of scanning all emails

**Common Pitfalls**:
- ❌ Storing credentials in vault (use `phase-2/secrets/`)
- ❌ Ignoring rate limits (implement exponential backoff)
- ❌ Scanning all emails (use "important" label filter)

### MCP Server Integration

**Best Practices**:
1. **Local-Only**: Run MCP servers locally, not exposed
2. **Error Handling**: Always handle MCP failures gracefully
3. **Retry Logic**: Network failures happen, retry with backoff
4. **Logging**: Log all MCP calls for debugging
5. **Test Mode**: Use test accounts for development

**Common Pitfalls**:
- ❌ Hardcoding MCP URLs (use environment variables)
- ❌ No retry on failure (implement 3-retry logic)
- ❌ Sending real emails in tests (use test accounts)

### Human-in-the-Loop Design

**Best Practices**:
1. **Clear Instructions**: User knows exactly what to do
2. **Checkbox-Based**: Use `[ ]` for clear approval/rejection
3. **Reason Field**: Allow user to explain rejection
4. **Timeout Handling**: No auto-approval, indefinite wait is OK
5. **Audit Trail**: Log all approvals to `/Logs/`

**Common Pitfalls**:
- ❌ Auto-approving after timeout (never auto-approve)
- ❌ Unclear approval mechanism (use checkboxes)
- ❌ No rejection reason field (add "why" field)

---

## Open Questions & Resolutions

### Q1: What if Gmail API credentials fail?

**Resolution**:
1. Implement error handling in GmailWatcher
2. Log error to `/Logs/`
3. Continue running (retry with exponential backoff)
4. Notify user via Dashboard status

### Q2: What if MCP server is down?

**Resolution**:
1. Detect MCP connection failure
2. Keep approval request in `/Pending_Approval/`
3. Log error to `/Logs/`
4. Retry on next approval poll cycle
5. Manual fallback: User can execute action manually

### Q3: What if user never responds to approval?

**Resolution**:
1. No timeout - approval requests persist indefinitely
2. This is acceptable for Silver tier
3. Optional: Add "aging" indicator (e.g., "Waiting 2 days")
4. Consider escalation to Gold+ tier

### Q4: What if two watchers create files simultaneously?

**Resolution**:
1. Use timestamp with microseconds for uniqueness
2. Use UUID for guaranteed uniqueness (if needed)
3. File locking not needed - writes are atomic
4. No conflicts expected in practice

### Q5: What if Plan.md execution fails?

**Resolution**:
1. Mark task as `[ ] Failed` with error details
2. Log error to `/Logs/`
3. Decision point: Retry vs. Escalate
   - Retry: Transient failures (network, API)
   - Escalate: Permanent failures (permissions, missing data)
4. Update Plan.md status to `failed`

---

## Technology Choices Summary

| Component | Technology | Version | Notes |
|-----------|------------|---------|-------|
| **Gmail API** | google-api-python-client | Latest | OAuth 2.0 authentication |
| **MCP Email** | @modelcontextprotocol/server-email | Latest | Local server only |
| **MCP LinkedIn** | @modelcontextprotocol/server-social-linkedin | Latest | Local server only |
| **Scheduling** | Windows Task Scheduler | Built-in | Cron alternative for Linux |
| **Polling** | Python time.sleep | Standard | 30-second interval |
| **Agent Skills** | Markdown files | - | ralph_wiggum_loop, human_in_loop, etc. |

---

## Dependencies Summary

### Python Packages

```txt
# From Phase 1
watchdog>=6.0.0

# New for Phase 2
google-auth>=2.0.0
google-api-python-client>=2.0.0
google-auth-oauthlib>=1.0.0
requests>=2.0.0  # For MCP HTTP calls
```

### MCP Servers

```bash
npm install -g @modelcontextprotocol/server-email
npm install -g @modelcontextprotocol/server-social-linkedin
```

### External Services

- Gmail API (requires Google Cloud project)
- LinkedIn API (requires LinkedIn developer account)

---

## Research Complete

**Status**: ✅ All "NEEDS CLARIFICATION" items resolved
**Next Step**: Proceed to data model and contracts definition

**Date Completed**: 2025-02-20
**Researcher**: AI Assistant (Claude Sonnet 4.6)
