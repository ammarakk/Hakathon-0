---
description: Comprehensive audit logging for all watcher triggers, decisions, and actions.
---

# COMMAND: Audit Logging

## CONTEXT

Implement comprehensive audit logging for:

- Watcher triggers and events
- Claude decisions and reasoning
- MCP server calls
- Approval workflow actions
- Errors and exceptions

## YOUR ROLE

Act as a security engineer with expertise in:

- Audit trail design
- Compliance logging
- Security event tracking
- Forensic analysis

## IMPLEMENTATION

```python
#!/usr/bin/env python3
"""
Comprehensive Audit Logging System

Logs all system events for security, compliance, and debugging.
"""

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("audit_logging")


class EventType(Enum):
    """Types of audit events."""
    WATCHER_TRIGGER = "watcher_trigger"
    WATCHER_ERROR = "watcher_error"
    CLAUDE_DECISION = "claude_decision"
    CLAUDE_ACTION = "claude_action"
    MCP_CALL = "mcp_call"
    APPROVAL_REQUEST = "approval_request"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_REJECTED = "approval_rejected"
    ACTION_EXECUTED = "action_executed"
    ERROR = "error"
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"


@dataclass
class AuditEvent:
    """Structured audit event."""
    timestamp: str
    event_type: str
    component: str
    actor: str
    action: str
    details: Dict[str, Any]
    result: str
    error: Optional[str] = None

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        md = f"""## [{self.timestamp}] {self.event_type}

**Component:** {self.component}
**Actor:** {self.actor}
**Action:** {self.action}
**Result:** {self.result}
"""
        if self.details:
            md += f"\n**Details:**\n```json\n{json.dumps(self.details, indent=2)}\n```\n"

        if self.error:
            md += f"\n**Error:** `{self.error}`\n"

        md += "\n---\n"
        return md


class AuditLogger:
    """Centralized audit logging system."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.audit_dir = vault_path / "Audit"
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        # Current month's log file
        month_str = datetime.now().strftime("%Y_%m")
        self.current_log = self.audit_dir / f"{month_str}.md"

        # Initialize log file if needed
        self._init_log_file()

    def _init_log_file(self):
        """Initialize log file with header."""
        if not self.current_log.exists():
            header = f"""# Audit Log - {datetime.now().strftime("%B %Y")}

**Period:** {datetime.now().strftime("%Y-%m")}

---

*This log contains all system events for compliance and debugging purposes.*

---

"""
            self.current_log.write_text(header)

    def log_event(self, event: AuditEvent):
        """Log an audit event."""
        md = event.to_markdown()

        with open(self.current_log, 'a') as f:
            f.write(md)

        logger.info(f"[AUDIT] {event.event_type}: {event.action} by {event.actor}")

    def log_watcher_trigger(
        self,
        watcher_name: str,
        items_found: int,
        items_processed: int
    ):
        """Log watcher trigger event."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.WATCHER_TRIGGER.value,
            component=watcher_name,
            actor="system",
            action=f"Check cycle completed",
            details={
                "items_found": items_found,
                "items_processed": items_processed,
                "success_rate": f"{(items_processed/items_found*100):.1f}%" if items_found > 0 else "N/A"
            },
            result="success" if items_found > 0 else "no_data"
        )
        self.log_event(event)

    def log_claude_decision(
        self,
        decision: str,
        reasoning: str,
        context: Dict[str, Any]
    ):
        """Log Claude decision."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.CLAUDE_DECISION.value,
            component="reasoning_loop",
            actor="claude",
            action=decision,
            details={
                "reasoning": reasoning[:500],  # Truncate for readability
                **context
            },
            result="decided"
        )
        self.log_event(event)

    def log_claude_action(
        self,
        action: str,
        target: str,
        outcome: str
    ):
        """Log Claude action execution."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.CLAUDE_ACTION.value,
            component="reasoning_loop",
            actor="claude",
            action=action,
            details={"target": target},
            result=outcome
        )
        self.log_event(event)

    def log_mcp_call(
        self,
        server: str,
        tool: str,
        parameters: Dict[str, Any],
        result: str
    ):
        """Log MCP server call."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.MCP_CALL.value,
            component=f"mcp_{server}",
            actor="claude",
            action=f"Called tool: {tool}",
            details={"parameters": parameters},
            result=result
        )
        self.log_event(event)

    def log_approval_request(
        self,
        request_id: str,
        action_type: str,
        details: Dict[str, Any]
    ):
        """Log approval request."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.APPROVAL_REQUEST.value,
            component="human_in_loop",
            actor="system",
            action=f"Request approval for: {action_type}",
            details={
                "request_id": request_id,
                **details
            },
            result="pending_approval"
        )
        self.log_event(event)

    def log_approval_decision(
        self,
        request_id: str,
        approved: bool,
        approver: str,
        reason: Optional[str] = None
    ):
        """Log approval decision."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.APPROVAL_GRANTED.value if approved else EventType.APPROVAL_REJECTED.value,
            component="human_in_loop",
            actor=approver,
            action=f"{'Approved' if approved else 'Rejected'} request {request_id}",
            details={"request_id": request_id},
            result="approved" if approved else "rejected",
            error=reason
        )
        self.log_event(event)

    def log_action_executed(
        self,
        action_id: str,
        action_type: str,
        success: bool,
        details: Dict[str, Any] = None
    ):
        """Log action execution."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.ACTION_EXECUTED.value,
            component="action_executor",
            actor="system",
            action=action_type,
            details=details or {},
            result="success" if success else "failed"
        )
        self.log_event(event)

    def log_error(
        self,
        component: str,
        error: Exception,
        context: Dict[str, Any] = None
    ):
        """Log error event."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=EventType.ERROR.value,
            component=component,
            actor="system",
            action="error_occurred",
            details=context or {},
            result="error",
            error=str(error)
        )
        self.log_event(event)

    def get_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get audit summary for recent days."""
        # Parse log file and generate summary
        # Implementation depends on log format
        return {
            "total_events": 0,
            "by_type": {},
            "by_component": {},
            "errors": 0
        }


# Decorator for automatic audit logging

def audit_log(audit_logger: AuditLogger, event_type: EventType):
    """Decorator to automatically log function calls."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            component = kwargs.get('component', func.__module__)
            try:
                result = await func(*args, **kwargs)

                if event_type == EventType.CLAUDE_ACTION:
                    audit_logger.log_claude_action(
                        action=func.__name__,
                        target=str(args[0]) if args else "unknown",
                        outcome="success"
                    )

                return result

            except Exception as e:
                audit_logger.log_error(
                    component=component,
                    error=e,
                    context={"function": func.__name__}
                )
                raise

        return wrapper
    return decorator


# Example: Usage in watcher

class AuditedGmailWatcher:
    """Gmail watcher with audit logging."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.audit = AuditLogger(vault_path)

    async def check(self):
        """Check for new emails with audit logging."""
        try:
            items = []  # Fetch from API

            self.audit.log_watcher_trigger(
                watcher_name="GmailWatcher",
                items_found=len(items),
                items_processed=len(items)
            )

            return items

        except Exception as e:
            self.audit.log_error(
                component="GmailWatcher",
                error=e,
                context={"action": "check"}
            )
            raise
```

## ACCEPTANCE CRITERIA

- Logs all system events with timestamps
- Tracks actors and components
- Records decisions and reasoning
- Maintains monthly audit files
- Provides summary statistics

## FOLLOW-UPS

- Add log rotation
- Implement log search/filtering
- Create audit dashboard
- Add export capabilities
