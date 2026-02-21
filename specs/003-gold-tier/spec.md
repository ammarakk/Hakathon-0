# Feature Specification: Gold Tier - Autonomous Employee

**Feature Branch**: `003-gold-tier`
**Created**: 2026-02-20
**Status**: Draft
**Input**: User description: "Full cross-domain integration (Personal + Business), Odoo Community Edition accounting system (self-hosted, local), Odoo MCP integration via JSON-RPC APIs with draft-only actions, Facebook and Instagram integration, Twitter (X) integration, Multiple MCP servers coordination, Weekly CEO Briefing generation, Error recovery and graceful degradation, Comprehensive audit logging, Ralph Wiggum loop for autonomous multi-step tasks, Architecture documentation, All AI functionality as Agent Skills"

**Builds Strictly On**: Phase 1 (Bronze Tier) + Phase 2 (Silver Tier)

---

## User Scenarios & Testing

### User Story 1 - Cross-Domain Task Integration (Priority: P1)

As a business owner, I want my AI Employee to seamlessly handle both personal and business tasks in a unified reasoning loop, so that I don't have to switch contexts between different domains and can see all pending items in one dashboard view.

**Why this priority**: This is the foundation for autonomous operation. Without unified reasoning, the system cannot intelligently prioritize across domains (e.g., deciding whether to respond to a personal WhatsApp message or a business email first).

**Independent Test**: Can be tested by creating items from different sources (personal WhatsApp message, business Gmail, bank transaction) and verifying that Claude creates a single unified Plan.md that addresses all domains with appropriate prioritization.

**Acceptance Scenarios**:

1. **Given** a personal WhatsApp invoice request and a business Gmail client inquiry arrive within 5 minutes, **When** Claude processes the /Needs_Action/ items, **Then** Claude creates a single Plan.md with tasks for both domains, prioritized by urgency and business impact
2. **Given** items from multiple sources in /Needs_Action/, **When** Claude generates reasoning, **Then** Dashboard.md shows a unified view with separate sections for "Personal Pending" and "Business Pending" but a single "Active Plan" section
3. **Given** a personal bank transaction and business task both require attention, **When** Claude creates Plan.md, **Then** the plan explicitly labels each task with domain: [Personal] or [Business] for clarity

---

### User Story 2 - Odoo Accounting Integration (Priority: P1)

As a business owner, I want my AI Employee to maintain an accounting system in Odoo Community Edition, so that I can track invoices, expenses, and transactions without manual bookkeeping while maintaining full control through draft-only actions requiring approval.

**Why this priority**: Financial management is core to business operations. This enables autonomous invoice creation and transaction tracking while preserving human control over all financial postings.

**Independent Test**: Can be tested by installing Odoo locally, configuring the MCP integration, creating a draft invoice from a /Needs_Action/ item, and verifying that approval is required before posting.

**Acceptance Scenarios**:

1. **Given** a client email requesting services in /Needs_Action/, **When** Claude processes the request, **Then** Claude creates a draft invoice in Odoo (via MCP) and creates an approval request in /Pending_Approval/ with invoice details
2. **Given** a draft invoice in /Pending_Approval/, **When** user manually approves by adding [x] Approved, **Then** MCP posts the invoice to Odoo and updates the status to "posted"
3. **Given** Odoo contains posted invoices and transactions, **When** Claude queries accounting data, **Then** Claude can read current revenue, outstanding invoices, and expenses for CEO Briefing generation
4. **Given** Claude attempts to create a payment or post financial transaction, **When** the action is triggered, **Then** the action MUST create a draft in Odoo and require /Pending_Approval/ before final posting

---

### User Story 3 - Multi-Platform Social Media Integration (Priority: P2)

As a business owner, I want my AI Employee to manage posts across LinkedIn, Facebook/Instagram, and Twitter (X), so that I can maintain consistent social media presence across all platforms without manual posting while ensuring all content is reviewed before publication.

**Why this priority**: Social media presence is critical for business growth, but requires careful content control. This extends the LinkedIn posting capability from Phase 2 to additional platforms.

**Independent Test**: Can be tested by triggering business-related /Needs_Action/ items (e.g., completed project, client testimonial) and verifying that Claude creates post drafts for all configured platforms with separate approval requests.

**Acceptance Scenarios**:

1. **Given** a completed project milestone in /Needs_Action/, **When** Claude detects the business context, **Then** Claude creates social post drafts for LinkedIn, Facebook, Instagram, and Twitter (X) with platform-appropriate formatting
2. **Given** social post drafts created, **When** drafts are saved to vault, **Then** each draft creates a separate approval request in /Pending_Approval/ with platform-specific content preview
3. **Given** an approved LinkedIn post in /Pending_Approval/, **When** user approves with [x] Approved, **Then** MCP posts to LinkedIn and logs the action in /Logs/audit.md
4. **Given** approved Facebook and Instagram posts, **When** user approves, **Then** MCP posts to both platforms and logs the actions
5. **Given** an approved Twitter (X) post, **When** user approves, **Then** MCP posts to Twitter/X and logs the action
6. **Given** posts are created for multiple platforms, **When** Claude generates Plan.md, **Then** the plan includes separate tasks for each platform's approval and posting workflow

---

### User Story 4 - Weekly CEO Briefing Generation (Priority: P2)

As a business owner, I want my AI Employee to automatically generate a comprehensive Monday Morning CEO Briefing every week, so that I can start my week with a clear overview of business performance, pending items, and strategic recommendations.

**Why this priority**: Regular business review is essential for management. This provides structured insight without requiring manual report generation.

**Independent Test**: Can be tested by manually triggering the weekly audit script and verifying that a CEO Briefing is generated with all required sections (revenue summary, pending items, recommendations).

**Acceptance Scenarios**:

1. **Given** it is Monday morning (or a manual trigger), **When** the weekly audit script runs, **Then** Claude scans /Accounting/, Odoo data via MCP, /Plans/, /Done/, and /Pending_Approval/
2. **Given** Claude has scanned all data sources, **When** the briefing is generated, **Then** Claude creates CEO_Briefing_YYYY-MM-DD.md in the vault root with sections: Revenue Summary, Pending Items, Bottlenecks, Recommendations
3. **Given** the CEO Briefing is created, **When** the document is reviewed, **Then** it includes specific metrics: total revenue month-to-date, outstanding invoices count, pending approvals count, active plans count
4. **Given** recommendations are generated, **When** Claude analyzes the data, **Then** recommendations are actionable and prioritized (e.g., "Follow up on 3 overdue invoices", "Approve 2 pending social posts")
5. **Given** the briefing is complete, **When** it is saved to the vault, **Then** it appears in Obsidian and Dashboard.md shows "Latest Briefing: [date]"

---

### User Story 5 - Error Recovery and Graceful Degradation (Priority: P1)

As a business owner, I want my AI Employee to continue operating even when individual components fail (e.g., MCP server down, Odoo unavailable), so that I don't lose monitoring and task management capabilities due to single-point failures.

**Why this priority**: System reliability is critical for 24/7 operation. Without error recovery, a single failed component would halt all operations.

**Independent Test**: Can be tested by simulating failures (stop MCP server, disconnect Odoo) and verifying that watchers continue creating /Needs_Action/ files and errors are logged gracefully.

**Acceptance Scenarios**:

1. **Given** the Gmail Watcher is running and the Odoo MCP server is down, **When** an important email arrives requiring invoice creation, **Then** Claude creates Plan.md with invoice task, logs the Odoo unavailability error to /Logs/errors.md, and continues processing other /Needs_Action/ items
2. **Given** the Approval Poller encounters a corrupted approval file, **When** the error occurs, **Then** the poller logs the error, skips the corrupted file, and continues processing other approval requests
3. **Given** a watcher fails to start (e.g., Gmail API token expired), **When** the error is detected, **Then** the error is logged to /Logs/errors.md with timestamp and details, other watchers continue running, and Dashboard.md shows the watcher status as "Error: [reason]"
4. **Given** Claude reasoning loop fails (e.g., vault locked), **When** the failure occurs, **Then** the failure is logged, watchers continue creating /Needs_Action/ files, and the system retries reasoning on next schedule
5. **Given** multiple errors occur in a 10-minute period, **When** errors are logged, **Then** each error is logged separately with timestamp, actor (watcher/MCP/reasoning), action, and result

---

### User Story 6 - Comprehensive Audit Logging (Priority: P1)

As a business owner and security-conscious user, I want every major action in the system logged to an audit trail, so that I can review what actions were taken, when, and by whom (human or AI), ensuring accountability and debugging capability.

**Why this priority**: Audit logging is essential for security, debugging, and compliance. Without it, there is no traceability of autonomous actions.

**Independent Test**: Can be tested by performing various actions (watcher triggers, Claude decisions, approvals, MCP calls) and verifying that all are logged to /Logs/audit.md with complete metadata.

**Acceptance Scenarios**:

1. **Given** the FilesystemWatcher detects a new file, **When** an ActionItem is created, **Then** the watcher logs to /Logs/audit.md: timestamp, actor="FilesystemWatcher", action="create_action_item", result=ActionItem filename
2. **Given** Claude processes a /Needs_Action/ item and creates Plan.md, **When** the plan is created, **Then** Claude logs: timestamp, actor="Claude", action="create_plan", result=Plan.md filename, source=ActionItem ID
3. **Given** user approves an action in /Pending_Approval/, **When** approval is detected, **Then** the poller logs: timestamp, actor="User", action="approve", result="execution_resumed", approval_file=filename
4. **Given** MCP sends an email after approval, **When** the send completes, **Then** the MCP client logs: timestamp, actor="mcp-email", action="send_email", result="success", recipient=email
5. **Given** MCP posts to LinkedIn after approval, **When** the post completes, **Then** the MCP client logs: timestamp, actor="mcp-social-linkedin", action="post_linkedin", result="success", post_url=URL
6. **Given** an error occurs in any component, **When** the error is caught, **Then** the error is logged: timestamp, actor=component_name, action=failed_action, result="error", error_message=details

---

### User Story 7 - Advanced Ralph Wiggum Loop for Complex Multi-Step Tasks (Priority: P3)

As a business owner, I want my AI Employee to autonomously complete complex multi-step tasks (e.g., invoice creation + social media follow-up + email confirmation) without requiring manual intervention at each intermediate step, so that I can offload entire workflows while maintaining approval only for final external actions.

**Why this priority**: This extends the Ralph Wiggum loop from Phase 2 to handle more complex autonomous workflows, reducing friction for routine multi-domain tasks.

**Independent Test**: Can be tested by creating a complex /Needs_Action/ item (e.g., "Project completed - send invoice, post to social media, email client") and verifying that Claude iterates through all steps autonomously, requesting approval only for external actions.

**Acceptance Scenarios**:

1. **Given** a /Needs_Action/ item for "Project completed - invoice client, post testimonial to LinkedIn/Facebook/Twitter, email confirmation", **When** Claude processes the item, **Then** Claude creates Plan.md with 5 tasks: [1] Create Odoo invoice draft, [2] Create LinkedIn post draft, [3] Create Facebook post draft, [4] Create Twitter post draft, [5] Create confirmation email draft
2. **Given** Plan.md with multiple tasks, **When** Claude iterates using Ralph Wiggum loop, **Then** Claude checks off [1] after Odoo draft created, moves to [2], [3], [4], [5] autonomously, creating approval requests only for external actions
3. **Given** all drafts are created and in /Pending_Approval/, **When** user approves all actions, **Then** Claude executes all approvals, marks tasks complete, and moves Plan.md to /Done/
4. **Given** a multi-step task fails at step 3 (e.g., LinkedIn draft creation fails), **When** the error occurs, **Then** Claude logs the error, marks step 3 as failed, and either continues to step 4 or pauses based on error severity (logged in /Logs/errors.md)
5. **Given** a Plan.md is partially complete (3 of 5 tasks done), **When** Claude reasoning is interrupted and later resumed, **Then** Claude reads the existing Plan.md, detects completed tasks, and continues from task 4 without redoing work

---

### Edge Cases

- What happens when Odoo database is corrupted or inaccessible?
  - **System Behavior**: Log error to /Logs/errors.md, continue operating with other components, retry Odoo connection after exponential backoff (1min, 5min, 15min, 1hour), create placeholder ActionItem if invoice creation is critical

- What happens when multiple social platform MCP servers are simultaneously down?
  - **System Behavior**: Create drafts for all platforms, log which MCP servers are unavailable, queue posts locally, retry posting every 30 minutes for up to 24 hours, alert user via Dashboard.md if queue exceeds 10 posts

- What happens when weekly CEO Briefing generation conflicts with active task processing?
  - **System Behavior**: Briefing generation takes priority, pause new reasoning tasks during briefing generation (typically <2 minutes), log the pause, resume reasoning after briefing complete

- What happens when /Pending_Approval/ folder contains 50+ approval requests (user away for extended period)?
  - **System Behavior**: Continue creating approval requests, log warning to Dashboard.md if threshold exceeded, implement FIFO queue for processing, do not block watchers or reasoning

- What happens when vault file locks prevent writing (e.g., Obsidian sync conflict)?
  - **System Behavior**: Retry write operation up to 3 times with 5-second delays, log all retry attempts, if all retries fail, create fallback file in /Logs/ with timestamp, alert user via Dashboard.md status

- What happens when human rejects an approval with "Reject + reason"?
  - **System Behavior**: Log rejection with reason, mark approval request as rejected, do NOT execute action, create ActionItem in /Needs_Action/ for human review of rejection, Claude does NOT auto-retry without new trigger

- What happens when personal and business items require conflicting immediate actions?
  - **System Behavior**: Claude prioritizes by business impact and urgency in Plan.md, labels tasks clearly with domain, if both are equally urgent, creates parallel tasks for human decision

---

## Requirements

### Constitutional Constraints
**GATE: All requirements MUST comply with constitution principles**

- [ ] Document Adherence: Gold Tier only - no Platinum features (cloud VM, vault sync, domain specialization, A2A messaging)
- [ ] Privacy & Security: Odoo credentials, social API tokens, banking details stay in phase-3/secrets/ (never in vault)
- [ ] Human-in-the-Loop: All Odoo postings, social posts, emails require /Pending_Approval/ workflow
- [ ] MCP Pattern: All external actions via MCP servers (mcp-odoo, mcp-social-fb-ig, mcp-social-x, mcp-email, mcp-social-linkedin)
- [ ] Vault Structure: Work in /phase-3/ only, update global folders only as specified (Dashboard.md, /Accounting/, /Logs/, /Plans/)
- [ ] Agent Skills: All AI logic via Agent Skills (odoo_integration.md, facebook_instagram.md, twitter_x.md, weekly_audit.md, error_recovery.md, audit_logging.md)
- [ ] Incremental: Builds strictly on Phase 1 + Phase 2, no modifications to previous phases
- [ ] Self-Hosted Odoo: Local only, no cloud Odoo (Platinum feature)
- [ ] Test Accounts: All social platforms use test/business accounts, never production profiles without explicit approval

### Functional Requirements

#### Cross-Domain Integration

- **FR-001**: System MUST process items from both personal sources (WhatsApp, personal Gmail, bank transactions) and business sources (business Gmail, completed tasks, accounting data) in the same reasoning loop
- **FR-002**: System MUST create unified Plan.md files that include both personal and business tasks with clear domain labels
- **FR-003**: Dashboard.md MUST display separate sections for "Personal Pending Items" and "Business Pending Items" but a unified "Active Plans" section
- **FR-004**: System MUST prioritize tasks across domains based on urgency and business impact (e.g., client inquiry > personal message, payment > social post)

#### Odoo Accounting System

- **FR-005**: System MUST install and configure Odoo Community Edition (latest stable, preferably Odoo 19+) locally on the same machine or VM
- **FR-006**: System MUST enable Odoo modules: Invoicing, Accounting, Contacts
- **FR-007**: System MUST create sample data in Odoo for testing (customers, products/services, sample invoices)
- **FR-008**: System MUST integrate with Odoo via JSON-RPC APIs using MCP server (mcp-odoo or equivalent)
- **FR-009**: System MUST support draft-only actions: Claude can read Odoo data and create draft invoices/transactions, but final posting requires /Pending_Approval/
- **FR-010**: System MUST create draft invoices in Odoo from /Needs_Action/ items (e.g., client email requesting services)
- **FR-011**: System MUST read Odoo data for CEO Briefing: revenue totals, outstanding invoices, expenses, customer list
- **FR-012**: System MUST post draft invoices/transactions to Odoo only after human approval via /Pending_Approval/ workflow

#### Multi-Platform Social Media Integration

- **FR-013**: System MUST integrate with Facebook and Instagram via MCP server (mcp-social-fb-ig or equivalent)
- **FR-014**: System MUST integrate with Twitter (X) via MCP server (mcp-social-x or equivalent)
- **FR-015**: System MUST create social post drafts for LinkedIn, Facebook, Instagram, and Twitter (X) from business-related /Needs_Action/ items
- **FR-016**: System MUST create platform-appropriate post formatting (character limits for Twitter/X, hashtags for Instagram, professional tone for LinkedIn)
- **FR-017**: System MUST create separate approval requests in /Pending_Approval/ for each platform's post
- **FR-018**: System MUST post to each platform via respective MCP server only after human approval
- **FR-019**: System MUST generate platform-specific summaries after posting (e.g., engagement metrics, post URLs)

#### Multiple MCP Servers Coordination

- **FR-020**: System MUST coordinate multiple MCP servers: mcp-email, mcp-social-linkedin, mcp-social-fb-ig, mcp-social-x, mcp-odoo
- **FR-021**: System MUST route actions to appropriate MCP server based on action type (email → mcp-email, LinkedIn → mcp-social-linkedin, etc.)
- **FR-022**: System MUST handle MCP server unavailability gracefully (retry with backoff, log error, continue with other MCPs)
- **FR-023**: System MUST log all MCP actions to /Logs/audit.md with timestamp, actor, action, result

#### Weekly CEO Briefing Generation

- **FR-024**: System MUST generate Monday Morning CEO Briefing automatically every Monday (or via manual trigger/scheduled trigger)
- **FR-025**: System MUST scan multiple data sources for briefing: /Accounting/ folder, Odoo data via MCP, /Plans/ folder, /Done/ folder, /Pending_Approval/ folder
- **FR-026**: System MUST create CEO_Briefing_YYYY-MM-DD.md in vault root with sections: Revenue Summary, Pending Items, Bottlenecks, Recommendations
- **FR-027**: Revenue Summary MUST include: total revenue MTD, outstanding invoices count, expenses MTD, top 3 customers by revenue
- **FR-028**: Pending Items MUST include: pending approvals count, active plans count, overdue tasks count
- **FR-029**: Recommendations MUST be actionable and prioritized (e.g., "Follow up on 3 overdue invoices from Customer X", "Approve 2 pending LinkedIn posts")
- **FR-030**: System MUST use weekly_ceo_briefing.md Agent Skill for briefing generation logic

#### Error Recovery and Graceful Degradation

- **FR-031**: System MUST implement try-except error handling in all watchers (FilesystemWatcher, GmailWatcher, WhatsAppWatcher, etc.)
- **FR-032**: System MUST implement retry logic with exponential backoff for transient errors (1min, 5min, 15min, 1hour)
- **FR-033**: System MUST log all errors to /Logs/errors.md with timestamp, component, error details, stack trace
- **FR-034**: System MUST continue operating when one component fails (e.g., if Odoo MCP is down, continue processing emails and social posts)
- **FR-035**: System MUST skip failed items and continue processing queue (do not halt on single item failure)
- **FR-036**: System MUST update Dashboard.md watcher status to "Error: [reason]" when watcher fails
- **FR-037**: System MUST use error_recovery.md Agent Skill for error handling patterns

#### Comprehensive Audit Logging

- **FR-038**: System MUST log every major event to /Logs/audit.md with timestamp, actor, action, result
- **FR-039**: Major events include: watcher triggers, Claude decisions (Plan.md creation), MCP calls, approvals, rejections, errors
- **FR-040**: Audit log entries MUST include: timestamp (ISO-8601), actor (component name), action (description), result (success/failure/pending), related_file (if applicable)
- **FR-041**: System MUST maintain per-day audit log files (audit-YYYY-MM-DD.md) or append to single audit.md with clear date sections
- **FR-042**: System MUST use audit_logging.md Agent Skill for audit logging logic

#### Advanced Ralph Wiggum Loop

- **FR-043**: System MUST apply Ralph Wiggum loop (Stop hook pattern) for complex multi-step tasks with 3+ steps
- **FR-044**: System MUST autonomously iterate through Plan.md tasks, marking them complete without human intervention for non-sensitive steps
- **FR-045**: System MUST request human approval via /Pending_Approval/ only for sensitive actions (external sends/posts, payments)
- **FR-046**: System MUST resume Plan.md iteration after approval without restarting entire plan
- **FR-047**: System MUST handle task failures gracefully: log error, mark task failed, continue or pause based on severity
- **FR-048**: System MUST use ralph_wiggum_loop.md Agent Skill for iteration logic

#### Architecture Documentation

- **FR-049**: System MUST create /phase-3/architecture.md documenting current system components, flows, and decisions
- **FR-050**: architecture.md MUST include: component diagram (text/mermaid), data flow between watchers, reasoning loop, MCP servers, and vault
- **FR-051**: architecture.md MUST list key lessons learned from Phases 1-3 and challenges overcome
- **FR-052**: architecture.md MUST document trade-offs made (e.g., choice of Odoo vs. other accounting systems, polling vs. event-driven)

### Key Entities

#### Odoo-Related Entities

- **OdooInvoice**: Represents a draft or posted invoice in Odoo with attributes: invoice_id, customer_id, line_items (product/service, quantity, price), total_amount, status (draft/posted/paid), due_date
- **OdooCustomer**: Represents a customer/contact in Odoo with attributes: customer_id, name, email, phone, billing_address
- **OdooTransaction**: Represents a financial transaction in Odoo with attributes: transaction_id, type (income/expense), amount, category, date, reference, status

#### Social Media Entities

- **SocialPostDraft**: Represents a draft post for any social platform with attributes: post_id, platform (linkedin/facebook/instagram/twitter), content, hashtags, media_attachments (optional), business_context, status (draft/pending_approval/posted), created_at
- **SocialPostResult**: Represents the result of a posted social media item with attributes: post_id, platform, post_url, engagement_metrics (likes, comments, shares), posted_at

#### Audit and Error Entities

- **AuditLogEntry**: Represents an audit trail entry with attributes: entry_id, timestamp (ISO-8601), actor (component name), action (description), result (success/failure/pending), related_file (path), details (JSON)
- **ErrorLogEntry**: Represents an error log entry with attributes: error_id, timestamp, component (watcher/MCP/reasoning), error_type, error_message, stack_trace, retry_count, resolved (boolean)

#### CEO Briefing Entities

- **CEOBriefing**: Represents a weekly business report with attributes: briefing_id, date (YYYY-MM-DD), revenue_summary (total_mtd, outstanding_invoices, expenses_mtd, top_customers), pending_items (approvals_count, plans_count, overdue_tasks), bottlenecks (list), recommendations (prioritized list)

#### Cross-Domain Task Entities

- **UnifiedPlan**: Represents a plan containing both personal and business tasks with attributes: plan_id, created_from (ActionItem ID), created_at, tasks (list with domain labels: [Personal]/[Business]), progress (completed/total), status

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: System successfully processes items from at least 3 different sources (personal WhatsApp, business Gmail, bank transactions) in a single unified reasoning loop
- **SC-002**: Odoo Community Edition is installed locally and accessible via MCP server with at least 3 sample customers, 5 sample products/services, and 2 sample invoices created
- **SC-003**: Claude creates draft invoices in Odoo from /Needs_Action/ items with 100% of drafts requiring approval before posting (no auto-posting)
- **SC-004**: System creates social post drafts for at least 3 platforms (LinkedIn, Facebook/Instagram, Twitter/X) from business triggers with platform-appropriate formatting
- **SC-005**: Weekly CEO Briefing is generated automatically with all required sections (Revenue Summary, Pending Items, Recommendations) and includes specific metrics from Odoo data
- **SC-006**: System continues operating when one MCP server is down (e.g., Odoo unavailable) with <10% performance degradation and all errors logged to /Logs/errors.md
- **SC-007**: Audit log contains entries for at least 5 different event types (watcher trigger, Claude decision, approval, MCP action, error) within a 24-hour period
- **SC-008**: Ralph Wiggum loop autonomously completes at least 3-step plans (e.g., invoice draft + social posts + email) with approval requested only for external actions
- **SC-009**: Dashboard.md shows unified view with separate Personal and Business sections plus cross-domain Active Plans, updating within 1 minute of any change
- **SC-010**: All sensitive actions (Odoo postings, social posts, emails) require human approval with 0% auto-execution without /Pending_Approval/ step
- **SC-011**: System recovers from simulated failures (MCP server down, Odoo disconnected) within 5 minutes with error logged and operation resumed
- **SC-012**: architecture.md exists with complete component diagram, data flow documentation, and lessons learned from Phases 1-3
