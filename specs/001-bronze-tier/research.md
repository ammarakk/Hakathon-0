# Research: Watcher Selection & Technical Decisions

**Date**: 2025-02-20
**Phase**: 1 (Bronze Tier)
**Status**: Complete

## Decision 1: Watcher Selection

### Options Evaluated

| Option | Pros | Cons | Complexity |
|--------|------|-------|------------|
| **FilesystemWatcher** | No credentials needed, immediate testability, no network dependency, simple setup | Limited to local files only | Low |
| GmailWatcher | Real email monitoring, practical use case | Requires OAuth setup, Google Cloud project, network dependency, credentials management | High |

### Decision: FilesystemWatcher

**Rationale**:
1. **Zero Setup Friction**: No API keys, OAuth flows, or cloud project configuration
2. **Immediate Testing**: Can drop any file to test immediately
3. **Reliability**: No network failures or rate limits
4. **Privacy**: All data stays local
5. **Learning Value**: Simpler code base to understand watcher pattern before adding complexity

**Implementation Reference**: `filesystem_watcher.md` Agent Skill

## Decision 2: Vault File Format

### Options Evaluated

| Format | Human-Readable | Metadata Support | Obsidian Compatible |
|--------|----------------|------------------|---------------------|
| **Markdown with YAML frontmatter** | ✅ Yes | ✅ Yes | ✅ Yes |
| Plain text | ✅ Yes | ❌ No | ✅ Yes |
| JSON | ❌ No | ✅ Yes | ❌ No |

### Decision: Markdown with YAML Frontmatter

**Rationale**:
- Obsidian natively supports markdown
- YAML frontmatter enables machine-readable metadata
- Human can read and edit directly
- Enables sorting and filtering by metadata fields

**File Format Specification**:
```yaml
---
type: action_item
source: filesystem
timestamp: 2025-02-20T14:30:00Z
priority: medium
---
# Human-Readable Title

**Source**: Filesystem
**Detected**: 2025-02-20 14:30:00 UTC

## Content

Item content here...

## Actions
- [ ] Action 1
- [ ] Action 2
```

## Decision 3: Watcher Check Interval

### Options Evaluated

| Interval | Responsiveness | Resource Usage | Battery Impact |
|----------|----------------|----------------|---------------|
| 10 seconds | High | High | High |
| **60 seconds** | Medium | Low | Low |
| 5 minutes | Low | Very Low | Very Low |

### Decision: 60 Seconds

**Rationale**:
- Balance between responsiveness and resource usage
- Acceptable delay for non-urgent personal tasks
- Standard interval for background monitoring
- Aligns with base_watcher.md default

## Decision 4: Claude Code Integration Pattern

### Approach

**Manual Trigger** (Phase 1):
- User runs Claude Code with vault context
- Claude reads from /Needs_Action/
- Claude writes to /Done/
- Demonstrates basic read/write capability

**Future Automation** (Silver+):
- Automatic triggering on file drops
- Ralph Wiggum loop for completion
- Continuous background operation

**Rationale for Manual in Phase 1**:
- Validates core vault interaction without complexity
- Establishes that Claude can read/write vault files
- Provides foundation for automated patterns in later phases

## Dependencies Identified

1. **Python Libraries**:
   - `watchdog` - File system monitoring
   - `pathlib` - Cross-platform path handling (built-in)
   - `asyncio` - Async operations (built-in)
   - `logging` - Logging (built-in)

2. **External Tools**:
   - Obsidian - Vault viewer/editor
   - Claude Code - AI reasoning engine
   - Python 3.11+ - Script execution

3. **No MCP Servers Required**: Confirmed as Silver+ feature

## Technical Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Watcher crashes on file access | Low | Medium | Add exception handling, log errors |
| Vault file permissions issues | Medium | High | Verify permissions, create directories if missing |
| Claude Code cannot access vault | Low | High | Test file access before running integration |
| File name collisions | Low | Low | Use timestamp-based naming with microseconds |

## References

- `base_watcher.md` - Base watcher template and abstract methods
- `filesystem_watcher.md` - Filesystem watcher implementation
- `vault_folder_structure.md` - Vault layout specification
