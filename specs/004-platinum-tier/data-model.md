# Data Model: Phase 4 - Platinum Tier

**Feature**: Phase 4 - Always-On Cloud + Local Executive
**Date**: 2026-02-21
**Status**: Complete

---

## Overview

Phase 4 introduces new vault entities for cloud-local coordination while maintaining compatibility with Phase 1-3 entities. All entities are represented as markdown files in the vault structure, ensuring human readability and git-based synchronization.

---

## Core Entities

### 1. Vault Task File

**Location**: `/Needs_Action/<domain>/task-<timestamp>-<id>.md`

**Purpose**: Represents an incoming task from watchers or external sources requiring processing.

**Fields**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| task_id | string | Yes | Unique task identifier | `task-20260221-001` |
| domain | enum | Yes | Domain classification | `personal`, `business`, `accounting`, `social` |
| priority | enum | Yes | Task priority | `low`, `medium`, `high`, `urgent` |
| created_at | ISO8601 | Yes | Creation timestamp | `2026-02-21T10:30:00Z` |
| source | string | Yes | Origin of task | `gmail_watcher`, `filesystem_watcher`, `manual` |
| content | string | Yes | Task description/payload | Email content, file path, etc. |
| metadata | object | No | Additional context | `{email_from: "client@example.com"}` |

**Markdown Template**:

```markdown
# Task: <task_id>

**Domain**: <domain>
**Priority**: <priority>
**Created**: <created_at>
**Source**: <source>

## Content

<content>

## Metadata

<metadata>

## Processing Log

<!-- Claim history, state transitions -->
```

**State Transition**: `Needs_Action` → `In_Progress` (via claim-by-move)

---

### 2. Claim File

**Location**: `/In_Progress/<agent_name>/task-<timestamp>-<id>.md`

**Purpose**: Represents a task claimed by an agent for processing.

**Fields**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| original_task_id | string | Yes | Reference to original task | `task-20260221-001` |
| claimed_by | string | Yes | Agent claiming the task | `cloud`, `local` |
| claimed_at | ISO8601 | Yes | Claim timestamp | `2026-02-21T10:30:05Z` |
| status | enum | Yes | Processing status | `processing`, `awaiting_approval`, `completed`, `failed` |
| progress_notes | string | No | Agent progress log | "Drafted reply, awaiting approval" |

**Markdown Template**:

```markdown
# Claimed Task: <original_task_id>

**Claimed By**: <claimed_by>
**Claimed At**: <claimed_at>
**Status**: <status>

## Progress

<progress_notes>

## Actions Taken

<!-- List of actions performed by agent -->
```

**Validation Rules**:
- `claimed_by` must be valid agent name: `cloud`, `local`
- `status` must be one of: `processing`, `awaiting_approval`, `completed`, `failed`
- File must be moved (not copied) from `/Needs_Action/` to `/In_Progress/<agent>/`

**State Transition**: `In_Progress` → `Pending_Approval` OR `Done` OR `Rejected`

---

### 3. Approval File

**Location**: `/Pending_Approval/<domain>/draft-<timestamp>-<id>.md`

**Purpose**: Represents a sensitive action awaiting human approval before execution.

**Fields**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| draft_id | string | Yes | Unique draft identifier | `draft-20260221-001` |
| domain | enum | Yes | Domain classification | `email`, `social`, `accounting` |
| draft_type | enum | Yes | Type of action | `email_send`, `social_post`, `payment`, `invoice_post` |
| created_by | string | Yes | Agent that created draft | `cloud`, `local` |
| created_at | ISO8601 | Yes | Creation timestamp | `2026-02-21T10:31:00Z` |
| content | string | Yes | Draft content | Email body, post text, invoice details |
| approval_status | enum | Yes | Current approval state | `pending`, `approved`, `rejected`, `expired` |
| approved_at | ISO8601 | No | Approval timestamp | `2026-02-21T10:35:00Z` |
| approved_by | string | No | Approval source | `user` (human) |
| rejection_reason | string | No | Reason for rejection | "Incorrect information" |
| expires_at | ISO8601 | No | Expiration timestamp | `2026-02-22T10:31:00Z` (24h) |

**Markdown Template**:

```markdown
# Draft: <draft_id>

**Domain**: <domain>
**Type**: <draft_type>
**Created By**: <created_by>
**Created At**: <created_at>
**Status**: <approval_status>

## Content

```
<content>
```

## Approval

<!-- Human adds: APPROVED or REJECTED: <reason> -->

## Metadata

- Expires: <expires_at>
```

**Approval Process**:
1. Agent creates draft with `approval_status: pending`
2. Human reviews and adds `APPROVED` or `REJECTED: <reason>` to file
3. Local agent checks file, executes action if approved
4. File moved to `Done/` (approved) or `Rejected/` (rejected)

**State Transitions**:
- `pending` → `approved` (human approves)
- `pending` → `rejected` (human rejects)
- `pending` → `expired` (24 hours elapsed)

**Validation Rules**:
- Sensitive actions (`email_send`, `social_post`, `payment`, `invoice_post`) MUST go through approval
- `approved_by` must be `user` (no auto-approval)
- `approval_status` can only be set to `approved` or `rejected` by human action

---

### 4. Update Signal

**Location**: `/Updates/signal-<timestamp>-<id>.md`

**Purpose**: Cloud agent writes signals to be merged into Dashboard.md by local agent.

**Fields**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| signal_id | string | Yes | Unique signal identifier | `signal-20260221-001` |
| source_agent | string | Yes | Agent creating signal | `cloud` |
| timestamp | ISO8601 | Yes | Signal timestamp | `2026-02-21T10:30:00Z` |
| payload_type | enum | Yes | Type of signal | `email_triaged`, `social_scheduled`, `odoo_draft` |
| content | string | Yes | Signal content | "Email from client triaged as HIGH_PRIORITY" |
| metadata | object | No | Additional context | `{email_count: 5, urgent: 2}` |

**Markdown Template**:

```markdown
# Signal: <signal_id>

**Source**: <source_agent>
**Timestamp**: <timestamp>
**Type**: <payload_type>

## Content

<content>

## Metadata

<metadata>

## Merged

<!-- Local agent sets to true after merging into Dashboard.md -->
```

**Single-Writer Rule**: Only local agent can update `Dashboard.md`. Cloud agent writes to `/Updates/`, local agent merges signals.

---

### 5. Health Status

**Location**: HTTP response from `/health` endpoint (not stored in vault)

**Purpose**: Real-time health monitoring of cloud agent.

**Fields**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| status | enum | Yes | Health state | `healthy`, `degraded`, `error` |
| timestamp | ISO8601 | Yes | Status timestamp | `2026-02-21T10:30:00Z` |
| last_activity | ISO8601 | Yes | Last agent activity | `2026-02-21T10:29:45Z` |
| active_watchers | array | Yes | List of running watchers | `["gmail_watcher", "filesystem_watcher"]` |
| error_count | integer | Yes | Errors in last hour | `0` |
| uptime_seconds | integer | Yes | Agent uptime | `86400` (24 hours) |

**JSON Schema**:

```json
{
  "status": "healthy",
  "timestamp": "2026-02-21T10:30:00Z",
  "last_activity": "2026-02-21T10:29:45Z",
  "active_watchers": ["gmail_watcher", "filesystem_watcher"],
  "error_count": 0,
  "uptime_seconds": 86400
}
```

**Validation Rules**:
- `status` must be one of: `healthy`, `degraded`, `error`
- `active_watchers` must be subset of configured watchers
- `error_count` increments on errors, resets hourly

**HTTP Response Codes**:
- `200 OK`: Health check passed
- `429 Too Many Requests`: Rate limit exceeded (>1 req/sec)
- `503 Service Unavailable`: Agent degraded or error

---

### 6. Sync State

**Location**: Git repository state (not stored in vault)

**Purpose**: Tracks vault synchronization status between cloud and local.

**Fields**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| last_sync_timestamp | ISO8601 | Yes | Last successful sync | `2026-02-21T10:30:00Z` |
| conflict_count | integer | Yes | Unresolved conflicts | `0` |
| file_count | integer | Yes | Total files in vault | `142` |
| sync_status | enum | Yes | Current sync state | `idle`, `syncing`, `success`, `failed` |
| last_error | string | No | Last error message | "Connection timeout" |

**Validation Rules**:
- `sync_status` must be one of: `idle`, `syncing`, `success`, `failed`
- `conflict_count` must be `0` for `success` status
- Sync operation blocks if `conflict_count > 0`

---

## State Transition Diagrams

### Task Lifecycle

```
┌─────────────────┐
│  Needs_Action   │
└────────┬────────┘
         │ Claim by move
         ▼
┌─────────────────┐
│   In_Progress   │
└────────┬────────┘
         │
         ├─→ Pending_Approval ──┐
         │                      ├─→ Done (approved)
         └─→ Done (no approval)│
                               └─→ Rejected (rejected)
```

### Approval Lifecycle

```
┌─────────────────┐
│     Pending     │
└────────┬────────┘
         │
         ├─→ Approved (by human) → Done
         ├─→ Rejected (by human) → Rejected
         └─→ Expired (24h timeout) → Pending (stale)
```

### Sync Lifecycle

```
┌─────────┐
│  Idle   │
└────┬────┘
     │ Trigger (30s interval)
     ▼
┌──────────┐
│ Syncing  │
└────┬─────┘
     │
     ├─→ Success (no conflicts)
     └─→ Failed (conflicts detected) → Idle (block)
```

---

## Relationships

```
┌──────────────┐      claims      ┌──────────────┐
│ Needs_Action │ ───────────────► │ In_Progress  │
└──────────────┘                  └──────┬───────┘
                                        │
                                        │ creates
                                        ▼
                               ┌──────────────────┐
                               │ Pending_Approval │
                               └─────────┬────────┘
                                         │
                        ┌────────────────┴────────────────┐
                        │                                 │
                        ▼                                 ▼
                   ┌───────────┐                    ┌───────────┐
                   │   Done    │                    │ Rejected  │
                   └───────────┘                    └───────────┘

┌──────────┐      writes      ┌─────────┐
│  Cloud   │ ────────────────►│ Updates │
│  Agent   │                  └────┬────┘
└──────────┘                        │
                                    │ merges
                                    ▼
                               ┌─────────────┐
                               │ Dashboard.md │
                               └─────────────┘
                                    ▲
                                    │ writes
                               ┌────┴─────┐
                               │  Local   │
                               │  Agent   │
                               └──────────┘
```

---

## Validation Rules Summary

### File-Level Validation

1. **Required Fields**: All required fields must be present
2. **Data Types**: Enums must match allowed values
3. **Timestamps**: Must be valid ISO8601 format
4. **References**: `original_task_id` must reference existing task

### State Transition Validation

1. **Claim-by-Move**: File must be moved, not copied
2. **Approval**: Only human can set `approved` or `rejected` status
3. **Sync Block**: No operations when `sync_status == failed`

### Security Validation

1. **Secrets Exclusion**: No `.env`, tokens, sessions in synced files
2. **Work-Zone**: Cloud cannot execute `send`, `post`, `payment` actions
3. **Approval Required**: All sensitive actions must go through `Pending_Approval`

---

## Data Retention

| Entity | Retention Period | Cleanup Action |
|--------|------------------|----------------|
| Needs_Action | No limit | Processed files moved to In_Progress |
| In_Progress | No limit | Completed files moved to Done |
| Pending_Approval | 30 days | Expired files marked, require manual review |
| Done | 30 days | Archived to `Done/YYYY-MM/` folder |
| Rejected | 90 days | Deleted after 90 days |
| Updates | 7 days | Deleted after merge to Dashboard.md |
| Errors | 90 days | Archived to `Errors/YYYY-MM/` folder |

---

## Indexing and Query

### Git Grep Patterns

```bash
# Find all pending approvals
git grep -l "approval_status: pending"

# Find high priority tasks
git grep "priority: urgent" Needs_Action/

# Find errors in last hour
git grep "Error" Logs/ --since="1 hour ago"

# Find unmerged updates
git grep "Merged: false" Updates/
```

### File Naming Convention

- **Tasks**: `task-YYYYMMDD-HHMMSS-<id>.md`
- **Drafts**: `draft-YYYYMMDD-HHMMSS-<id>.md`
- **Signals**: `signal-YYYYMMDD-HHMMSS-<id>.md`
- **Done**: `done-YYYYMMDD-HHMMSS-<id>.md`

Timestamp-based naming ensures chronological sorting and prevents filename collisions.

---

## Summary

Phase 4 data model introduces:
- **6 new entities**: Task, Claim, Approval, Update Signal, Health Status, Sync State
- **3 state machines**: Task lifecycle, Approval lifecycle, Sync lifecycle
- **2 coordination patterns**: Claim-by-move, Single-writer Dashboard.md
- **Security rules**: Work-zone separation, secrets exclusion, approval required

All entities are markdown files in the vault, ensuring human readability, git-based synchronization, and compatibility with Phase 1-3 entities.
