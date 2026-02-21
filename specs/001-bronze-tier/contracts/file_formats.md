# File Format Contracts: Phase 1

**Version**: 1.0
**Date**: 2025-02-20

## Contract 1: ActionItem File Format

**Location:** `/Needs_Action/*.md`
**Created By:** FilesystemWatcher or GmailWatcher
**Purpose:** Represent detected items requiring processing

### Specification

```yaml
---
type: action_item
source: filesystem | gmail
timestamp: ISO-8601 datetime
priority: low | medium | high
---
# {Title}

**Source**: {source system}
**Detected**: {ISO-8601 datetime}
**Priority**: {priority level}

## Content

{Item content - email body, file description, etc.}

## Actions Required
- [ ] {Action 1}
- [ ] {Action 2}
- [ ] {Action 3}

---
*Created by {watcher_name} at {timestamp}*
```

### Required Fields

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `type` | string | literal "action_item" | Document type identifier |
| `source` | string | "filesystem" or "gmail" | Source system |
| `timestamp` | string | ISO-8601 | Detection timestamp |
| `priority` | string | "low", "medium", or "high" | Urgency level |
| `# Title` | heading | Markdown H1 | Human-readable title |
| `## Content` | heading | Markdown H2 | Item content section |
| `## Actions Required` | heading | Markdown H2 | Checklist of actions |

### Validation Rules

1. File MUST have YAML frontmatter delimited by `---`
2. All required frontmatter fields MUST be present
3. `timestamp` MUST be valid ISO-8601 format
4. `priority` MUST be one of: low, medium, high
5. File MUST be readable in Obsidian (valid markdown)

## Contract 2: ProcessedItem File Format

**Location:** `/Done/*.md`
**Created By:** Claude Code (AI processing)
**Purpose:** Represent completed actions

### Specification

```yaml
---
type: processed_item
source: filesystem | gmail
timestamp: ISO-8601 datetime
processed_at: ISO-8601 datetime
---
# {Title}

**Status**: Completed
**Processed**: {ISO-8601 datetime}

## Actions Taken
- {Action 1 performed}
- {Action 2 performed}
- {Action 3 performed}

## Notes

{Additional context or notes}

---
*Processed at {timestamp}*
```

### Required Fields

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `type` | string | literal "processed_item" | Document type identifier |
| `source` | string | "filesystem" or "gmail" | Source system |
| `timestamp` | string | ISO-8601 | Original detection timestamp |
| `processed_at` | string | ISO-8601 | Processing completion timestamp |
| `**Status**` | string | literal "Completed" | Status indicator |
| `## Actions Taken` | heading | Markdown H2 | Performed actions list |
| `## Notes` | heading | Markdown H2 | Additional context |

### Validation Rules

1. File MUST have YAML frontmatter delimited by `---`
2. All required frontmatter fields MUST be present
3. Both timestamps MUST be valid ISO-8601 format
4. `processed_at` MUST be later than or equal to `timestamp`
5. File MUST be readable in Obsidian (valid markdown)

## Contract 3: Dashboard.md Format

**Location:** `/Dashboard.md`
**Created By:** Manual setup (Phase 1)
**Purpose:** Real-time summary of vault state

### Minimum Specification

```markdown
# AI Employee Dashboard

## Bank Summary

| Account | Balance | Last Updated |
|---------|---------|--------------|
| Checking | $0.00 | - |
| Savings | $0.00 | - |

## Pending Messages

| Source | Count | Last Checked |
|--------|-------|--------------|
| Gmail | 0 | - |
| WhatsApp | 0 | - |

## Active Projects

| Project | Status | Last Activity |
|----------|--------|---------------|
| - | - | - |

---

*Last updated: {date}*
```

### Required Sections

1. `# AI Employee Dashboard` - Main heading
2. `## Bank Summary` - Financial summary table
3. `## Pending Messages` - Message counts table
4. `## Active Projects` - Projects table

## Contract 4: Company_Handbook.md Format

**Location:** `/Company_Handbook.md`
**Created By:** Manual setup (Phase 1)
**Purpose:** Rules of engagement and operational guidelines

### Minimum Specification

```markdown
# Company Handbook

## Rules of Engagement

### Communication Style
- Be polite in all communications
- Use professional yet friendly tone
- Be concise but thorough
- Avoid jargon unless necessary

### Approval Thresholds
- **Payments >$500**: Require human approval
- **Email sends**: Require human review
- **Social media posts**: Require human approval
- **File deletions**: Require human confirmation

### Workflow
1. Watchers detect items → create files in /Needs_Action/
2. Process items systematically
3. Move completed items to /Done/
4. Archive processed items regularly

### Privacy & Security
- Never share credentials
- Keep .env files local-only
- Don't log sensitive information
- Ask for approval on uncertain actions

---

*Version: 1.0 - Bronze Tier*
```

### Required Sections

1. `# Company Handbook` - Main heading
2. `## Rules of Engagement` - Main rules section
3. `### Communication Style` - Tone and style guidelines
4. `### Approval Thresholds` - When human approval is needed
5. `### Workflow` - Process flow
6. `### Privacy & Security` - Security rules

## File Naming Convention

**Pattern:** `{timestamp}_{source}_{description}.md`

**Components:**
- `timestamp`: `YYYYMMDD_HHMMSS` (local time) or `YYYYMMDD_HHMMSS_{microseconds}`
- `source`: `filesystem`, `gmail`, `whatsapp`, etc.
- `description`: Brief description (max 50 chars, spaces replaced with underscores)

**Examples:**
- `20250220_143000_filesystem_test_document.md`
- `20250220_143015_gmail_invoice_abc_corp.md`

**Validation:**
- Filename MUST be unique
- Description MUST be URL-safe (a-z, A-Z, 0-9, _, -)
- Total filename length SHOULD be < 255 characters

## Contract Compliance

All Phase 1 implementations MUST:

1. ✅ Create files matching these specifications
2. ✅ Include all required frontmatter fields
3. ✅ Follow markdown formatting rules
4. ✅ Use approved naming conventions
5. ✅ Validate output before writing to vault

Non-compliant files SHOULD be rejected with error logging.
