#!/usr/bin/env python3
"""
Audit Logger - Phase 3 Gold Tier

Comprehensive audit logging for all AI Employee actions.

This module provides per-day audit logging with timestamped entries for:
- Watcher triggers (FilesystemWatcher, GmailWatcher, WhatsAppWatcher)
- Plan creation (Claude reasoning)
- MCP calls (create_draft, post_invoice, post_social, send_email)
- Approvals (approval_detected, action_executed)
- Errors (with stack traces)

Log files are created per day: audit-YYYY-MM-DD.md
Stored in: AI_Employee_Vault/Logs/

Usage:
    from audit_logger import log_audit

    log_audit(
        actor="GmailWatcher",
        action="email_received",
        result="success",
        related_file="Needs_Action/email_001.md",
        details="Unread important email from client"
    )

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# Vault paths
VAULT_ROOT = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
LOGS_DIR = VAULT_ROOT / "Logs"


def log_audit(actor: str,
              action: str,
              result: str = 'success',
              related_file: Optional[str] = None,
              details: Optional[str] = None) -> bool:
    """
    Log an audit entry to the per-day audit log file

    Args:
        actor: Component that performed the action (e.g., "GmailWatcher", "Claude", "mcp-odoo")
        action: Action performed (e.g., "email_received", "create_plan", "create_draft_invoice")
        result: Result of action ("success", "failed", "error")
        related_file: Optional related vault file path
        details: Optional additional details about the action

    Returns:
        bool: True if log entry written successfully, False otherwise
    """
    try:
        # Ensure Logs directory exists
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Get current date for filename
        today = datetime.now()
        audit_filename = f"audit-{today.strftime('%Y-%m-%d')}.md"
        audit_path = LOGS_DIR / audit_filename

        # Create log entry
        timestamp = today.strftime('%Y-%m-%d %H:%M:%S')

        log_entry = f"""## [{timestamp}] {actor} - {action}

**Result**: {result}
"""

        if related_file:
            log_entry += f"**Related File**: {related_file}\n"

        if details:
            log_entry += f"**Details**: {details}\n"

        log_entry += "\n---\n\n"

        # Append to audit log file
        with open(audit_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        return True

    except Exception as e:
        print(f"[ERROR] Error writing audit log: {e}")
        return False


# Convenience functions for common audit scenarios

def log_watcher_trigger(watcher_name: str, source: str, count: int = 1) -> bool:
    """
    Log watcher trigger event

    Args:
        watcher_name: Name of watcher (e.g., "GmailWatcher")
        source: Source being watched (e.g., "gmail")
        count: Number of items detected

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor=watcher_name,
        action="trigger",
        result="success",
        details=f"Detected {count} new items from {source}"
    )


def log_action_item_created(actor: str, file_path: str, source: str) -> bool:
    """
    Log action item creation

    Args:
        actor: Component that created the action item
        file_path: Path to created file
        source: Source of action item (e.g., "email", "whatsapp")

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor=actor,
        action="create_action_item",
        result="success",
        related_file=file_path,
        details=f"Created action item from {source}"
    )


def log_plan_created(plan_file: str, task_count: int, domains: list) -> bool:
    """
    Log plan creation event

    Args:
        plan_file: Path to Plan.md file
        task_count: Number of tasks in plan
        domains: List of domains in plan (e.g., ["Personal", "Business"])

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor="Claude",
        action="create_plan",
        result="success",
        related_file=plan_file,
        details=f"Created unified plan with {task_count} tasks across domains: {', '.join(domains)}"
    )


def log_mcp_call(mcp_server: str, action: str, result: str = 'success',
                 details: Optional[str] = None) -> bool:
    """
    Log MCP server call

    Args:
        mcp_server: MCP server name (e.g., "mcp-odoo", "mcp-social-linkedin")
        action: Action performed (e.g., "create_draft_invoice", "post_social")
        result: Result of action
        details: Optional details

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor=mcp_server,
        action=action,
        result=result,
        details=details
    )


def log_approval_requested(action_type: str, file_path: str) -> bool:
    """
    Log approval request event

    Args:
        action_type: Type of action requiring approval (e.g., "post_invoice", "send_email")
        file_path: Path to approval request file

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor="System",
        action="approval_requested",
        result="pending",
        related_file=file_path,
        details=f"Human approval required for: {action_type}"
    )


def log_approval_granted(action_type: str, file_path: str) -> bool:
    """
    Log approval granted event

    Args:
        action_type: Type of action approved
        file_path: Path to approval file

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor="User",
        action="approval_granted",
        result="success",
        related_file=file_path,
        details=f"User approved action: {action_type}"
    )


def log_error(actor: str, error_type: str, error_message: str,
              related_file: Optional[str] = None) -> bool:
    """
    Log error event

    Args:
        actor: Component that encountered error
        error_type: Type of error (e.g., "connection_error", "validation_error")
        error_message: Error message
        related_file: Optional related file

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor=actor,
        action="error",
        result="failed",
        related_file=related_file,
        details=f"[{error_type}] {error_message}"
    )


def log_ceo_briefing_generated(briefing_file: str, revenue: float,
                               pending_count: int) -> bool:
    """
    Log CEO briefing generation

    Args:
        briefing_file: Path to briefing file
        revenue: Total revenue for the period
        pending_count: Number of pending items

    Returns:
        bool: True if logged successfully
    """
    return log_audit(
        actor="generate_ceo_briefing.py",
        action="generate_briefing",
        result="success",
        related_file=briefing_file,
        details=f"Generated CEO briefing: Revenue ${revenue:,.2f}, {pending_count} pending items"
    )


# Example usage and testing
if __name__ == "__main__":
    print("=== Audit Logger Test ===\n")

    # Test 1: Watcher trigger
    print("Test 1: Logging watcher trigger...")
    log_watcher_trigger("GmailWatcher", "gmail", 3)
    print("[OK] Watcher trigger logged")

    # Test 2: Action item created
    print("\nTest 2: Logging action item creation...")
    log_action_item_created("GmailWatcher", "Needs_Action/email_001.md", "gmail")
    print("[OK] Action item creation logged")

    # Test 3: Plan created
    print("\nTest 3: Logging plan creation...")
    log_plan_created("Plans/Plan_2026-02-21.md", 5, ["Personal", "Business"])
    print("[OK] Plan creation logged")

    # Test 4: MCP call
    print("\nTest 4: Logging MCP call...")
    log_mcp_call("mcp-odoo", "create_draft_invoice", "success",
                 details="Draft invoice ID: 123 for $1,000.00")
    print("[OK] MCP call logged")

    # Test 5: Approval requested
    print("\nTest 5: Logging approval request...")
    log_approval_requested("post_invoice", "Pending_Approval/invoice_123.md")
    print("[OK] Approval request logged")

    # Test 6: Approval granted
    print("\nTest 6: Logging approval granted...")
    log_approval_granted("post_invoice", "Pending_Approval/invoice_123.md")
    print("[OK] Approval granted logged")

    # Test 7: Error
    print("\nTest 7: Logging error...")
    log_error("mcp-odoo", "connection_error", "Connection refused", "Plans/Plan_001.md")
    print("[OK] Error logged")

    # Test 8: CEO briefing
    print("\nTest 8: Logging CEO briefing...")
    log_ceo_briefing_generated("CEO_Briefings/Briefing_2026-02-21.md", 12500.00, 8)
    print("[OK] CEO briefing logged")

    print("\n[OK] All audit log tests completed")
    print(f"[FILE] Audit log location: {LOGS_DIR / 'audit-' + datetime.now().strftime('%Y-%m-%d') + '.md'}")
