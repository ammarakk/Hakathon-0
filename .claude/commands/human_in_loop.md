---
description: Human-in-loop approval workflow for sensitive actions.
---

# COMMAND: Human-in-Loop Approval Workflow

## CONTEXT

The user needs to implement a human-in-loop workflow that:

- Flags sensitive actions requiring approval
- Writes pending actions to /Pending_Approval
- Waits for user confirmation before execution
- Provides approval and rejection mechanisms

## YOUR ROLE

Act as a workflow designer with expertise in:

- Approval process design
- State management for pending actions
- User notification systems
- Audit trail creation

## Step 1: Human-in-Loop Implementation

```python
#!/usr/bin/env python3
"""
Human-in-Loop Approval Workflow

Handles actions that require human approval before execution.
Specially designed for sensitive operations like payments, deletions, etc.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HumanInLoop")


class ApprovalStatus(Enum):
    """Status of approval requests."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


class ApprovalRequest:
    """Represents an approval request."""

    def __init__(
        self,
        request_id: str,
        action_type: str,
        description: str,
        details: Dict[str, Any],
        requires_approval: bool = True,
        timeout_minutes: int = 60
    ):
        self.request_id = request_id
        self.action_type = action_type
        self.description = description
        self.details = details
        self.requires_approval = requires_approval
        self.timeout_minutes = timeout_minutes

        self.status = ApprovalStatus.PENDING
        self.created_at = datetime.now()
        self.approved_at: Optional[datetime] = None
        self.approved_by: Optional[str] = None
        self.rejection_reason: Optional[str] = None
        self.execution_result: Optional[str] = None

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        md = f"""# Approval Request: {self.request_id}

**Action Type:** {self.action_type}
**Status:** {self.status.value.upper()}
**Created:** {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}
**Timeout:** {self.timeout_minutes} minutes

## Description
{self.description}

## Details
```json
{json.dumps(self.details, indent=2)}
```

## Risk Assessment
{self._assess_risk()}

## Actions Required
"""
        if self.status == ApprovalStatus.PENDING:
            md += """
- [ ] Review the action details above
- [ ] Confirm this action is safe to execute
- [ ] Add any notes or conditions

**To Approve:** Change `Status: pending` to `Status: approved` and add your name to `Approved By`

**To Reject:** Change `Status: pending` to `Status: rejected` and add a reason
"""
        elif self.status == ApprovalStatus.APPROVED:
            md += f"""
✓ **Approved** by {self.approved_by} at {self.approved_at.strftime("%Y-%m-%d %H:%M:%S")}

Waiting for execution...
"""
        elif self.status == ApprovalStatus.REJECTED:
            md += f"""
✗ **Rejected**

Reason: {self.rejection_reason}
"""
        elif self.status == ApprovalStatus.EXECUTED:
            md += f"""
✓ **Executed Successfully**

Result: {self.execution_result}
"""
        elif self.status == ApprovalStatus.FAILED:
            md += f"""
✗ **Execution Failed**

Error: {self.execution_result}
"""

        md += f"\n---\n*Request ID: {self.request_id}*\n"
        return md

    def _assess_risk(self) -> str:
        """Assess the risk level of this action."""
        risk_factors = []

        # Check for payment actions
        if self.action_type in ['payment', 'transfer', 'withdrawal']:
            amount = self.details.get('amount', 0)
            if amount > 1000:
                risk_factors.append(f"💰 High value payment: ${amount}")
            elif amount > 100:
                risk_factors.append(f"💰 Medium value payment: ${amount}")

        # Check for deletion actions
        if 'delete' in self.action_type.lower():
            risk_factors.append("🗑️ Deletion operation - data loss risk")

        # Check for production changes
        if self.details.get('environment') == 'production':
            risk_factors.append("🚨 Production environment")

        # Check for bulk operations
        if self.details.get('bulk', False):
            risk_factors.append("📦 Bulk operation - multiple items affected")

        if not risk_factors:
            return "✓ Low risk - standard operation"
        else:
            return "\n".join(risk_factors)


class HumanInLoopOrchestrator:
    """
    Orchestrates human-in-loop approval workflows.
    """

    def __init__(self, vault_path: Path):
        """
        Initialize the orchestrator.

        Args:
            vault_path: Path to vault directory
        """
        self.vault_path = vault_path
        self.pending_dir = vault_path / "Pending_Approval"
        self.pending_dir.mkdir(parents=True, exist_ok=True)

        self.requests: Dict[str, ApprovalRequest] = {}
        self._load_existing_requests()

    def _load_existing_requests(self):
        """Load existing approval requests from files."""
        for request_file in self.pending_dir.glob("approval_*.md"):
            try:
                content = request_file.read_text()
                # Extract request ID from filename
                request_id = request_file.stem.replace("approval_", "")
                # Parse status from content
                if "Status: APPROVED" in content.upper():
                    status = ApprovalStatus.APPROVED
                elif "Status: REJECTED" in content.upper():
                    status = ApprovalStatus.REJECTED
                elif "Status: EXECUTED" in content.upper():
                    status = ApprovalStatus.EXECUTED
                else:
                    status = ApprovalStatus.PENDING

                # In a full implementation, we'd parse all fields
                # For now, just track that it exists
                self.requests[request_id] = ApprovalRequest(
                    request_id=request_id,
                    action_type="unknown",
                    description=f"Loaded from {request_file.name}",
                    details={}
                )

            except Exception as e:
                logger.error(f"Error loading request {request_file}: {e}")

    def requires_approval(
        self,
        action_type: str,
        details: Dict[str, Any],
        thresholds: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Determine if an action requires approval.

        Args:
            action_type: Type of action (payment, deletion, etc.)
            details: Action details
            thresholds: Approval thresholds

        Returns:
            True if approval required
        """
        thresholds = thresholds or {
            'payment_amount': 500,
            'bulk_operations': True,
            'production_changes': True,
        }

        # Payment threshold
        if action_type in ['payment', 'transfer', 'withdrawal']:
            amount = details.get('amount', 0)
            if amount >= thresholds.get('payment_amount', 500):
                return True

        # Bulk operations
        if details.get('bulk', False) and thresholds.get('bulk_operations', True):
            return True

        # Production changes
        if details.get('environment') == 'production' and thresholds.get('production_changes', True):
            return True

        # Deletion operations
        if 'delete' in action_type.lower():
            return True

        # Sensitive actions
        if action_type in ['api_key_create', 'user_permission_change', 'database_modification']:
            return True

        return False

    def create_approval_request(
        self,
        action_type: str,
        description: str,
        details: Dict[str, Any],
        timeout_minutes: int = 60
    ) -> ApprovalRequest:
        """
        Create a new approval request.

        Args:
            action_type: Type of action
            description: Human-readable description
            details: Action details
            timeout_minutes: Approval timeout

        Returns:
            ApprovalRequest object
        """
        request_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{action_type}"

        request = ApprovalRequest(
            request_id=request_id,
            action_type=action_type,
            description=description,
            details=details,
            requires_approval=True,
            timeout_minutes=timeout_minutes
        )

        # Save request
        self._save_request(request)
        self.requests[request_id] = request

        logger.info(f"Created approval request: {request_id}")
        return request

    def _save_request(self, request: ApprovalRequest):
        """Save approval request to file."""
        filename = f"approval_{request.request_id}.md"
        filepath = self.pending_dir / filename
        filepath.write_text(request.to_markdown(), encoding='utf-8')
        logger.info(f"Saved approval request: {filepath}")

    def check_approval_status(self, request_id: str) -> ApprovalStatus:
        """
        Check the current status of an approval request.

        Args:
            request_id: Request ID to check

        Returns:
            Current approval status
        """
        filepath = self.pending_dir / f"approval_{request_id}.md"

        if not filepath.exists():
            logger.warning(f"Request not found: {request_id}")
            return ApprovalStatus.FAILED

        content = filepath.read_text()

        # Parse status from content
        if "**Status:** APPROVED" in content or "Status: approved" in content.lower():
            return ApprovalStatus.APPROVED
        elif "**Status:** REJECTED" in content or "Status: rejected" in content.lower():
            return ApprovalStatus.REJECTED
        elif "**Status:** EXECUTED" in content or "Status: executed" in content.lower():
            return ApprovalStatus.EXECUTED
        else:
            return ApprovalStatus.PENDING

    async def wait_for_approval(
        self,
        request_id: str,
        check_interval: int = 10
    ) -> tuple[ApprovalStatus, Optional[str]]:
        """
        Wait for approval decision.

        Args:
            request_id: Request ID to wait for
            check_interval: Seconds between checks

        Returns:
            Tuple of (status, reason/comment)
        """
        request = self.requests.get(request_id)
        if not request:
            return ApprovalStatus.FAILED, "Request not found"

        timeout_seconds = request.timeout_minutes * 60
        start_time = datetime.now()

        logger.info(f"Waiting for approval: {request_id} (timeout: {request.timeout_minutes}min)")

        while True:
            # Check timeout
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= timeout_seconds:
                logger.warning(f"Approval timeout: {request_id}")
                return ApprovalStatus.REJECTED, "Timeout - no approval received"

            # Check status
            status = self.check_approval_status(request_id)

            if status == ApprovalStatus.APPROVED:
                logger.info(f"Request approved: {request_id}")
                return ApprovalStatus.APPROVED, None
            elif status == ApprovalStatus.REJECTED:
                logger.info(f"Request rejected: {request_id}")
                return ApprovalStatus.REJECTED, "Request rejected by user"

            # Wait before next check
            await asyncio.sleep(check_interval)

    def mark_executed(self, request_id: str, result: str):
        """
        Mark a request as executed.

        Args:
            request_id: Request ID
            result: Execution result message
        """
        filepath = self.pending_dir / f"approval_{request_id}.md"

        if filepath.exists():
            content = filepath.read_text()
            # Update status
            content = content.replace(
                f"**Status:** {ApprovalStatus.PENDING.value.upper()}",
                f"**Status:** EXECUTED"
            )
            content = content.replace(
                f"**Status:** {ApprovalStatus.APPROVED.value.upper()}",
                f"**Status:** EXECUTED"
            )

            # Add result if not already present
            if "**Status:** EXECUTED" in content and "Result:" not in content:
                content = content.replace(
                    "**Status:** EXECUTED",
                    f"**Status:** EXECUTED\n\n**Result:** {result}"
                )

            filepath.write_text(content)
            logger.info(f"Marked as executed: {request_id}")


# Usage Examples

async def example_payment_workflow():
    """Example: Payment requiring approval."""
    orchestrator = HumanInLoopOrchestrator(Path("./vault"))

    # Payment details
    payment_details = {
        'amount': 1500,
        'recipient': 'vendor@example.com',
        'currency': 'USD',
        'reference': 'INV-2024-001'
    }

    # Check if approval needed
    if orchestrator.requires_approval('payment', payment_details):
        # Create approval request
        request = orchestrator.create_approval_request(
            action_type='payment',
            description=f'Process payment of ${payment_details["amount"]} to {payment_details["recipient"]}',
            details=payment_details,
            timeout_minutes=60
        )

        print(f"⏳ Approval request created: {request.request_id}")
        print(f"📁 File: {orchestrator.pending_dir / f'approval_{request.request_id}.md'}")
        print("Please review and approve in the file, then wait...")

        # Wait for approval
        status, reason = await orchestrator.wait_for_approval(request.request_id)

        if status == ApprovalStatus.APPROVED:
            print("✓ Approval received! Processing payment...")
            # Execute payment
            result = "Payment processed successfully"
            orchestrator.mark_executed(request.request_id, result)
            print(f"✓ {result}")
        else:
            print(f"✗ Payment cancelled: {reason}")
    else:
        print("Processing payment without approval...")
        # Execute payment directly


if __name__ == "__main__":
    asyncio.run(example_payment_workflow())
```

## ACCEPTANCE CRITERIA

- Detects actions requiring approval based on rules
- Creates approval request files in /Pending_Approval
- Monitors files for approval status changes
- Handles timeouts for pending approvals
- Maintains audit trail of all approvals

## FOLLOW-UPS

- Add email notifications for pending approvals
- Implement approval reason capture
- Add approval history tracking
- Create approval dashboard
