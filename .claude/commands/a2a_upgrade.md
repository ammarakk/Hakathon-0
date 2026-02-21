---
description: Phase 2 A2A upgrade for direct agent-to-agent messaging with vault audit trail.
---

# COMMAND: A2A Upgrade (Phase 2)

## CONTEXT

Optional Phase 2 upgrade to replace file handoffs with:

- Direct agent-to-agent messages
- Real-time communication
- Vault as audit record only
- Event-driven architecture

## YOUR ROLE

Act as a systems architect with expertise in:

- Message queues (RabbitMQ, Redis)
- Event-driven architecture
- Microservices communication
- Audit trail design

## IMPLEMENTATION

### 1. Message Queue Setup

```python
# a2a_messaging.py

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict
from dataclasses import dataclass

# For local development, use asyncio queues
# For production, replace with Redis/RabbitMQ

logger = logging.getLogger("a2a_messaging")


@dataclass
class Message:
    """Agent-to-agent message."""
    id: str
    from_agent: str
    to_agent: str
    type: str
    payload: Dict[str, Any]
    timestamp: str
    correlation_id: str = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'from_agent': self.from_agent,
            'to_agent': self.to_agent,
            'type': self.type,
            'payload': self.payload,
            'timestamp': self.timestamp,
            'correlation_id': self.correlation_id
        }


class MessageBus:
    """Message bus for agent communication."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.queues: Dict[str, asyncio.Queue] = {}
        self.handlers: Dict[str, Callable] = {}
        self.audit_log = vault_path / "Audit" / "a2a_messages.md"

    def subscribe(self, agent_name: str, handler: Callable):
        """Subscribe an agent to the message bus."""
        self.queues[agent_name] = asyncio.Queue()
        self.handlers[agent_name] = handler
        logger.info(f"{agent_name} subscribed to message bus")

    async def publish(self, message: Message):
        """Publish a message to an agent."""
        # Log to vault for audit
        self._log_message(message)

        # Deliver to recipient
        if message.to_agent in self.queues:
            await self.queues[message.to_agent].put(message)
            logger.info(f"Message {message.id} sent to {message.to_agent}")
        else:
            logger.warning(f"Recipient not found: {message.to_agent}")

    async def start_agent(self, agent_name: str):
        """Start processing messages for an agent."""
        queue = self.queues.get(agent_name)
        if not queue:
            raise ValueError(f"Agent not subscribed: {agent_name}")

        handler = self.handlers[agent_name]

        while True:
            message = await queue.get()
            try:
                response = await handler(message)
                if response:
                    await self.publish(response)
            except Exception as e:
                logger.error(f"Error handling message: {e}")

    def _log_message(self, message: Message):
        """Log message to vault audit trail."""
        entry = f"""
## [{message.timestamp}] {message.type}

**From:** {message.from_agent}
**To:** {message.to_agent}
**Message ID:** {message.id}

**Payload:**
```json
{json.dumps(message.payload, indent=2)}
```

---
"""
        with open(self.audit_log, 'a') as f:
            f.write(entry)


# Global message bus instance
_message_bus = None


def get_message_bus(vault_path: Path) -> MessageBus:
    """Get or create global message bus."""
    global _message_bus
    if _message_bus is None:
        _message_bus = MessageBus(vault_path)
    return _message_bus
```

### 2. Agent Wrapper with A2A

```python
# a2a_agent.py

from abc import ABC, abstractmethod


class A2AAgent(ABC):
    """Base agent with A2A messaging capabilities."""

    def __init__(self, name: str, vault_path: Path):
        self.name = name
        self.vault_path = vault_path
        self.message_bus = get_message_bus(vault_path)

        # Subscribe to message bus
        self.message_bus.subscribe(self.name, self.handle_message)

    @abstractmethod
    async def handle_message(self, message: Message) -> Message:
        """Handle incoming message."""
        pass

    async def send_message(
        self,
        to_agent: str,
        message_type: str,
        payload: Dict[str, Any]
    ) -> str:
        """Send message to another agent."""
        message = Message(
            id=f"{self.name}_{datetime.now().timestamp()}",
            from_agent=self.name,
            to_agent=to_agent,
            type=message_type,
            payload=payload,
            timestamp=datetime.now().isoformat()
        )

        await self.message_bus.publish(message)
        return message.id


# Example: GmailWatcher with A2A

class A2AGmailWatcher(A2AAgent):
    """Gmail watcher with A2A messaging."""

    async def handle_message(self, message: Message) -> Message:
        """Handle incoming messages."""
        if message.type == "check_request":
            # Check for new emails
            emails = await self.check()

            # Send response
            return Message(
                id=f"response_{datetime.now().timestamp()}",
                from_agent=self.name,
                to_agent=message.from_agent,
                type="check_response",
                payload={"emails": emails, "count": len(emails)},
                timestamp=datetime.now().isoformat(),
                correlation_id=message.id
            )

        elif message.type == "mark_read":
            # Mark email as read
            email_id = message.payload.get("email_id")
            await self.mark_as_read(email_id)

    async def check(self) -> list:
        """Check for new emails."""
        # Implementation here
        pass

    async def mark_as_read(self, email_id: str):
        """Mark email as read."""
        # Implementation here
        pass

    async def on_new_email(self, email: dict):
        """Called when new email detected."""
        # Notify reasoning loop directly
        await self.send_message(
            to_agent="reasoning_loop",
            message_type="new_item",
            payload={
                "source": "gmail",
                "item": email
            }
        )
```

### 3. Reasoning Loop with A2A

```python
# a2a_reasoning.py

class A2AReasoningLoop(A2AAgent):
    """Reasoning loop with A2A messaging."""

    def __init__(self, vault_path: Path):
        super().__init__("reasoning_loop", vault_path)
        self.pending_items = []

    async def handle_message(self, message: Message) -> Message:
        """Handle incoming messages."""
        if message.type == "new_item":
            # New item from watcher
            self.pending_items.append(message.payload)

            # Process if we have enough items
            if len(self.pending_items) >= 3:
                await self.process_items()

        elif message.type == "execute_action":
            # Execute an action
            result = await self.execute_action(message.payload)
            return Message(
                id=f"result_{datetime.now().timestamp()}",
                from_agent=self.name,
                to_agent=message.from_agent,
                type="action_result",
                payload={"result": result},
                timestamp=datetime.now().isoformat(),
                correlation_id=message.id
            )

    async def process_items(self):
        """Process pending items."""
        # Generate plan
        plan = await self.create_plan(self.pending_items)

        # Send tasks to worker agents
        for task in plan.tasks:
            await self.send_message(
                to_agent="worker",
                message_type="execute_task",
                payload=task
            )

        self.pending_items.clear()

    async def create_plan(self, items: list) -> dict:
        """Create execution plan."""
        # Implementation here
        pass
```

### 4. Migration Strategy

```python
# migration.py

class HybridMode:
    """Support both file-based and A2A messaging during migration."""

    def __init__(self, vault_path: Path, enable_a2a: bool = False):
        self.vault_path = vault_path
        self.enable_a2a = enable_a2a

        if enable_a2a:
            self.message_bus = get_message_bus(vault_path)

    async def notify_new_item(self, item: dict):
        """Notify about new item (hybrid approach)."""
        # Always write to file (audit trail)
        self._write_action_file(item)

        # Also send A2A message if enabled
        if self.enable_a2a:
            await self.message_bus.publish(Message(
                id=f"notify_{datetime.now().timestamp()}",
                from_agent="watcher",
                to_agent="reasoning_loop",
                type="new_item",
                payload=item,
                timestamp=datetime.now().isoformat()
            ))

    def _write_action_file(self, item: dict):
        """Write action file to vault (for audit)."""
        # Existing file-based implementation
        pass
```

## ACCEPTANCE CRITERIA

- Agents can send direct messages
- Vault maintains audit trail
- Hybrid mode supports migration
- Message queue handles failures

## FOLLOW-UPS

- Add message persistence
- Implement dead letter queue
- Create message monitoring
- Add replay capability
