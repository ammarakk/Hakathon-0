---
description: Reasoning loop implementing perception-reasoning-action flow for agent decision making.
---

# COMMAND: Reasoning Loop (Perception-Reasoning-Action)

## CONTEXT

The user needs to implement a reasoning loop that:

- Reads items from /Needs_Action directory
- Thinks about what actions to take
- Creates Plan.md with checkboxes
- Triggers execution based on watcher inputs
- Completes the perception-reasoning-action cycle

## YOUR ROLE

Act as an AI agent architect with expertise in:

- Cognitive architecture patterns
- State machine design
- Plan generation and execution
- File-based orchestration

## Step 1: Reasoning Loop Implementation

```python
#!/usr/bin/env python3
"""
Reasoning Loop - Perception-Reasoning-Action flow

Implements a cognitive loop that:
1. PERCEIVES: Read items from Needs_Action
2. REASONS: Think about actions and create plans
3. ACTS: Execute plans and verify results
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ReasoningLoop")


class Percept:
    """Represents a perceived item from the environment."""

    def __init__(self, source: str, content: str, metadata: Dict[str, Any]):
        self.source = source
        self.content = content
        self.metadata = metadata
        self.timestamp = datetime.now()


class Thought:
    """Represents a reasoning step about a percept."""

    def __init__(self, percept: Percept, analysis: str, actions: List[str]):
        self.percept = percept
        self.analysis = analysis
        self.actions = actions
        self.timestamp = datetime.now()


class Plan:
    """Represents an executable plan with checkboxes."""

    def __init__(self, title: str, items: List[Dict[str, Any]]):
        self.title = title
        self.items = items  # Each item: {'task': str, 'done': bool}
        self.timestamp = datetime.now()

    def to_markdown(self) -> str:
        """Convert plan to markdown format."""
        md = f"""# {self.title}

**Created:** {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

## Tasks

"""
        for i, item in enumerate(self.items, 1):
            status = "- [x]" if item['done'] else "- [ ]"
            md += f"{status} {item['task']}\n"

        return md

    @classmethod
    def from_markdown(cls, content: str) -> 'Plan':
        """Parse plan from markdown."""
        title_match = re.search(r'^# (.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Plan"

        items = []
        for line in content.split('\n'):
            if line.strip().startswith('- ['):
                task = re.sub(r'^- \[[x ]\]\s*', '', line).strip()
                done = '[x]' in line
                items.append({'task': task, 'done': done})

        return cls(title, items)


class ReasoningLoop:
    """
    Main reasoning loop implementing perception-reasoning-action.
    """

    def __init__(self, vault_path: Path, check_interval: int = 30):
        """
        Initialize the reasoning loop.

        Args:
            vault_path: Path to vault directory
            check_interval: Seconds between perception cycles
        """
        self.vault_path = vault_path
        self.needs_action_dir = vault_path / "Needs_Action"
        self.updates_dir = vault_path / "Updates"
        self.check_interval = check_interval

        # Ensure directories exist
        self.needs_action_dir.mkdir(parents=True, exist_ok=True)
        self.updates_dir.mkdir(parents=True, exist_ok=True)

        # Working memory
        self.percepts: List[Percept] = []
        self.thoughts: List[Thought] = []
        self.current_plan: Optional[Plan] = None

        # Running state
        self.running = False

    async def perceive(self) -> List[Percept]:
        """
        PERCEPTION phase: Read items from Needs_Action.

        Returns:
            List of perceived items
        """
        logger.info("🔍 PERCEIVING: Scanning Needs_Action...")

        percepts = []
        action_files = list(self.needs_action_dir.glob("*.md"))

        # Exclude Plan.md from perception (it's output, not input)
        action_files = [f for f in action_files if f.name != "Plan.md"]

        for action_file in action_files:
            try:
                content = action_file.read_text(encoding='utf-8')
                metadata = self._extract_metadata(content, action_file)

                percept = Percept(
                    source=action_file.name,
                    content=content,
                    metadata=metadata
                )

                percepts.append(percept)
                logger.info(f"  Perceived: {action_file.name}")

            except Exception as e:
                logger.error(f"Error reading {action_file}: {e}")

        self.percepts = percepts
        logger.info(f"🔍 Perception complete: {len(percepts)} items")
        return percepts

    def _extract_metadata(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from action file content."""
        metadata = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'priority': 'medium',
            'action_type': 'unknown',
            'source': 'unknown'
        }

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\*\s*(\w+)', content, re.IGNORECASE)
        if priority_match:
            metadata['priority'] = priority_match.group(1).lower()

        # Extract action type
        type_match = re.search(r'\*\*Action Type:\*\*\s*(\w+)', content, re.IGNORECASE)
        if type_match:
            metadata['action_type'] = type_match.group(1).lower()

        # Extract source
        source_match = re.search(r'\*\*Source:\*\*\s*(\w+)', content, re.IGNORECASE)
        if source_match:
            metadata['source'] = source_match.group(1)

        return metadata

    async def reason(self, percepts: List[Percept]) -> List[Thought]:
        """
        REASONING phase: Analyze percepts and decide on actions.

        Args:
            percepts: List of perceived items

        Returns:
            List of thoughts (reasoning steps)
        """
        logger.info("🧠 REASONING: Analyzing percepts...")

        thoughts = []

        for percept in percepts:
            # Analyze the percept
            analysis = self._analyze_percept(percept)

            # Determine required actions
            actions = self._determine_actions(percept, analysis)

            thought = Thought(
                percept=percept,
                analysis=analysis,
                actions=actions
            )

            thoughts.append(thought)
            logger.info(f"  Thought: {percept.source} -> {len(actions)} actions")

        self.thoughts = thoughts
        logger.info(f"🧠 Reasoning complete: {len(thoughts)} thoughts")
        return thoughts

    def _analyze_percept(self, percept: Percept) -> str:
        """Analyze a percept and determine what it means."""
        content = percept.content.lower()

        # Email pattern
        if percept.metadata['source'] == 'gmail':
            if 'invoice' in content or 'payment' in content:
                return "Financial email requiring payment review"
            elif 'urgent' in content or 'asap' in content:
                return "Urgent communication requiring immediate attention"
            else:
                return "Standard email requiring response"

        # WhatsApp pattern
        elif percept.metadata['source'] == 'whatsapp':
            return "Instant message requiring quick response"

        # File drop pattern
        elif percept.metadata['source'] == 'filesystem':
            return f"File drop: {percept.metadata.get('category', 'unknown')}"

        # Transaction pattern
        elif percept.metadata['source'] == 'finance':
            return "Financial transaction requiring categorization"

        return "General action item requiring processing"

    def _determine_actions(self, percept: Percept, analysis: str) -> List[str]:
        """Determine required actions based on analysis."""
        actions = []

        # Common actions
        actions.append(f"Review {percept.source} item")

        # Source-specific actions
        if percept.metadata['source'] == 'gmail':
            actions.extend([
                "Read full email content",
                "Determine response needed",
                "Draft response if required",
                "Archive or mark as done"
            ])

        elif percept.metadata['source'] == 'whatsapp':
            actions.extend([
                "Read message context",
                "Determine if immediate reply needed",
                "Send appropriate response"
            ])

        elif percept.metadata['source'] == 'filesystem':
            actions.extend([
                "Examine file contents",
                "Categorize file appropriately",
                "Move to final destination"
            ])

        elif percept.metadata['source'] == 'finance':
            actions.extend([
                "Verify transaction details",
                "Assign correct category",
                "Update accounting records"
            ])

        # Priority-based actions
        if percept.metadata['priority'] == 'high':
            actions.insert(1, "⚡ Handle with priority")

        return actions

    async def plan(self, thoughts: List[Thought]) -> Plan:
        """
        Create a plan from thoughts.

        Args:
            thoughts: List of thoughts from reasoning phase

        Returns:
            Executable plan
        """
        logger.info("📋 PLANNING: Creating execution plan...")

        # Collect all actions from all thoughts
        all_items = []
        for thought in thoughts:
            for action in thought.actions:
                all_items.append({
                    'task': f"[{thought.percept.metadata['source']}] {action}",
                    'done': False,
                    'source_file': thought.percept.source
                })

        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        all_items.sort(key=lambda x: priority_order.get(
            self._get_item_priority(x), 1
        ))

        plan = Plan(
            title=f"Action Plan - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            items=all_items
        )

        self.current_plan = plan
        logger.info(f"📋 Plan created: {len(all_items)} tasks")
        return plan

    def _get_item_priority(self, item: Dict[str, Any]) -> str:
        """Get priority from item metadata."""
        # Find source file and extract priority
        source_file = item.get('source_file', '')
        source_path = self.needs_action_dir / source_file

        if source_path.exists():
            content = source_path.read_text()
            match = re.search(r'\*\*Priority:\*\*\s*(\w+)', content, re.IGNORECASE)
            if match:
                return match.group(1).lower()

        return 'medium'

    async def act(self, plan: Plan) -> bool:
        """
        ACTION phase: Execute the plan.

        Args:
            plan: Plan to execute

        Returns:
            True if all tasks completed, False otherwise
        """
        logger.info("⚡ ACTING: Executing plan...")

        # Save plan to file
        plan_path = self.needs_action_dir / "Plan.md"
        plan_path.write_text(plan.to_markdown(), encoding='utf-8')
        logger.info(f"Plan saved to: {plan_path}")

        # Execute each task
        completed = 0
        for item in plan.items:
            if not item['done']:
                logger.info(f"  Executing: {item['task']}")

                try:
                    success = await self._execute_task(item)

                    if success:
                        item['done'] = True
                        completed += 1
                    else:
                        logger.warning(f"  Task failed: {item['task']}")

                except Exception as e:
                    logger.error(f"  Error executing task: {e}")

        # Update plan file
        plan_path.write_text(plan.to_markdown(), encoding='utf-8')

        logger.info(f"⚡ Action complete: {completed}/{len(plan.items)} tasks done")
        return completed == len(plan.items)

    async def _execute_task(self, task: Dict[str, Any]) -> bool:
        """
        Execute a single task.

        In practice, this would call appropriate handlers or
        delegate to specialized agents. For now, it simulates execution.

        Args:
            task: Task dictionary

        Returns:
            True if successful, False otherwise
        """
        # Extract source file
        source_file = task.get('source_file')
        if source_file:
            source_path = self.needs_action_dir / source_file

            # Mark as processed by adding a checkmark
            if source_path.exists():
                content = source_path.read_text()
                if '**Status:**' not in content:
                    # Add status marker
                    content += f"\n\n**Status:** ⚡ Processed by ReasoningLoop at {datetime.now().isoformat()}\n"
                    source_path.write_text(content)

        # Simulate task execution
        await asyncio.sleep(0.1)
        return True

    async def run_cycle(self) -> bool:
        """
        Run a full perception-reasoning-action cycle.

        Returns:
            True if actions were taken, False otherwise
        """
        # Perceive
        percepts = await self.perceive()

        if not percepts:
            logger.debug("No items to process")
            return False

        # Reason
        thoughts = await self.reason(percepts)

        # Plan
        plan = await self.plan(thoughts)

        # Act
        await self.act(plan)

        return True

    async def run(self):
        """Run the continuous reasoning loop."""
        logger.info("🚀 Starting Reasoning Loop")
        self.running = True

        try:
            while self.running:
                await self.run_cycle()
                await asyncio.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.running = False
            logger.info("Reasoning Loop stopped")

    async def stop(self):
        """Stop the reasoning loop."""
        self.running = False


async def main():
    """Main entry point."""
    import os

    vault_path = Path(os.getenv("VAULT_PATH", "./vault"))

    loop = ReasoningLoop(
        vault_path=vault_path,
        check_interval=30
    )

    await loop.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Triggering via Watchers

Watchers trigger the reasoning loop by creating files in /Needs_Action:

```python
# In any watcher (GmailWatcher, WhatsAppWatcher, etc.)

async def create_action_file(self, item: Dict[str, Any]) -> Path:
    """Create an action file that triggers reasoning loop."""
    # Create action file as usual
    action_path = self.needs_action_dir / f"{timestamp}_action.md"
    action_path.write_text(content)

    # The reasoning loop will perceive this file on next cycle
    # and automatically trigger reasoning and action

    return action_path
```

## ACCEPTANCE CRITERIA

- Reads all items from /Needs_Action
- Creates structured plans with checkboxes
- Executes tasks sequentially
- Updates plan file as tasks complete
- Runs continuously until stopped

## FOLLOW-UPS

- Add parallel task execution
- Implement task delegation to specialized agents
- Add learning from completed tasks
- Create dashboard for loop status
