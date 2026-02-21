# Data Model: Bronze Tier Entities

**Date**: 2025-02-20
**Phase**: 1 (Bronze Tier)

## Core Entities

### Vault

The root directory containing all AI Employee files and subdirectories.

**Attributes:**
- `path`: Absolute filesystem path
- `folders`: List of subfolders (Dashboard.md, Company_Handbook.md, Needs_Action/, Done/, etc.)
- `type`: "obsidian_vault"

**Relationships:**
- Contains many ActionItems
- Contains many ProcessedItems
- References many AgentSkills

### ActionItem

A markdown file in /Needs_Action/ representing a detected event requiring processing.

**Attributes:**
- `id`: Unique identifier (timestamp-based)
- `type`: "action_item"
- `source`: "filesystem" or "gmail"
- `timestamp`: ISO-8601 datetime when detected
- `priority`: "low" | "medium" | "high"
- `title`: Human-readable title
- `content`: Item content (email body, file description, etc.)
- `suggested_actions`: List of recommended actions (checkboxes)

**File Location:** `/Needs_Action/{timestamp}_{source}_{title}.md`

**Relationships:**
- Belongs to Vault
- Processed into ProcessedItem

**Example:**
```markdown
---
type: action_item
source: filesystem
timestamp: 2025-02-20T14:30:00Z
priority: medium
---
# File Drop: document.pdf

**Source**: Filesystem
**Detected**: 2025-02-20 14:30:00 UTC
**Priority**: MEDIUM

## Content

File dropped in monitored folder.

**File Info**:
- Original: document.pdf
- Size: 2.5 MB
- Type: application/pdf

## Actions Required
- [ ] Review document
- [ ] Determine appropriate action
- [ ] File or process
```

### ProcessedItem

A markdown file in /Done/ representing a completed action.

**Attributes:**
- `id`: Unique identifier
- `type`: "processed_item"
- `source`: "filesystem" or "gmail"
- `timestamp`: ISO-8601 datetime when originally detected
- `processed_at`: ISO-8601 datetime when processing completed
- `title`: Human-readable title
- `actions_taken`: List of actions performed
- `notes`: Additional notes or context

**File Location:** `/Done/{timestamp}_{source}_{title}.md`

**Relationships:**
- Derived from ActionItem
- Belongs to Vault

**Example:**
```markdown
---
type: processed_item
source: filesystem
timestamp: 2025-02-20T14:30:00Z
processed_at: 2025-02-20T14:35:00Z
---
# File Drop: document.pdf

**Status**: Completed
**Processed**: 2025-02-20 14:35:00 UTC

## Actions Taken
- Reviewed document (invoice)
- Categorized as: Accounting
- Filed in: /Accounting/Invoices/

## Notes
Document is an invoice from ABC Corp. Added to accounting records.
```

### Watcher

Background process that monitors an external system (filesystem, Gmail) and creates ActionItems.

**Attributes:**
- `name`: "FilesystemWatcher" or "GmailWatcher"
- `type`: "watcher"
- `check_interval`: Seconds between checks (default: 60)
- `state`: "running" | "stopped" | "error"
- `items_processed`: Count of ActionItems created

**Relationships:**
- Creates ActionItems
- References AgentSkills

## File Format Contracts

### ActionItem Format Contract

**Location:** `/Needs_Action/*.md`

**Required Frontmatter:**
```yaml
---
type: action_item
source: filesystem|gmail
timestamp: ISO-8601
priority: low|medium|high
---
```

**Required Body Sections:**
1. `# Title` - Human-readable title
2. `**Source**: {source}` - Source system
3. `**Detected**: {timestamp}` - Detection time
4. `## Content` - Item content
5. `## Actions Required` - Checklist of actions

### ProcessedItem Format Contract

**Location:** `/Done/*.md`

**Required Frontmatter:**
```yaml
---
type: processed_item
source: filesystem|gmail
timestamp: ISO-8601
processed_at: ISO-8601
---
```

**Required Body Sections:**
1. `# Title` - Human-readable title
2. `**Status**: Completed`
3. `## Actions Taken` - List of performed actions
4. `## Notes` - Additional context

## State Transitions

```
External Event (file drop / email)
         ↓
    Watcher detects
         ↓
  Create ActionItem
    (in /Needs_Action/)
         ↓
    Claude processes
         ↓
  Create ProcessedItem
      (in /Done/)
```

## Validation Rules

1. **File Naming**: Must use pattern `{timestamp}_{source}_{description}.md`
2. **Timestamps**: Must be valid ISO-8601 format
3. **Priorities**: Must be one of: low, medium, high
4. **Sources**: Must be one of: filesystem, gmail
5. **Required Fields**: All frontmatter fields must be present
6. **Markdown Format**: Must be valid markdown that renders in Obsidian
