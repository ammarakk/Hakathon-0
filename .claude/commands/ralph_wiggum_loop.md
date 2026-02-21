---
description: Ralph Wiggum loop pattern for multi-step task completion with Stop hook.
---

# COMMAND: Ralph Wiggum Loop (Multi-Step Task Iteration)

## CONTEXT

The user needs to implement a "Ralph Wiggum Loop" pattern that:

- Keeps Claude iterating until multi-step tasks are complete
- Uses a Stop hook pattern to detect task completion
- Prevents premature termination of complex workflows
- Integrates with the reasoning engine

**Name Origin:** Named after Ralph Wiggum's "I'm winning!" meme - the loop keeps going until it actually wins (completes the task).

## YOUR ROLE

Act as an AI agent architect with expertise in:

- Multi-step task orchestration
- State persistence and tracking
- Loop termination conditions
- Agent hook systems

## OUTPUT STRUCTURE

Create a Ralph Wiggum Loop implementation with:

1. **Stop Hook Pattern** for completion detection
2. **Task State Tracking** with checkpoints
3. **Iteration Logic** with smart stopping
4. **Integration Examples** for reasoning engine
5. **Setup Instructions** for various use cases

## Step 1: Stop Hook Pattern

The Ralph Wiggum Loop uses a "Stop Hook" that checks if work is truly complete.

```python
#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Keep iterating until multi-step tasks are complete

This pattern prevents premature task completion by maintaining state
and checking for actual completion before stopping.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("RalphWiggumLoop")


class TaskState:
    """Track the state of a multi-step task."""

    def __init__(self, task_id: str, total_steps: int, state_dir: Path):
        """
        Initialize task state.

        Args:
            task_id: Unique task identifier
            total_steps: Number of steps in the task
            state_dir: Directory to store state files
        """
        self.task_id = task_id
        self.total_steps = total_steps
        self.state_dir = state_dir
        self.state_file = state_dir / f"{task_id}.json"

        self.completed_steps: List[str] = []
        self.current_step: Optional[str] = None
        self.failed_steps: List[str] = []
        self.iterations = 0
        self.max_iterations = total_steps * 3  # Safety limit

        self._load_state()

    def _load_state(self):
        """Load existing state if available."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                self.completed_steps = data.get('completed_steps', [])
                self.current_step = data.get('current_step')
                self.failed_steps = data.get('failed_steps', [])
                self.iterations = data.get('iterations', 0)
            except Exception as e:
                logger.warning(f"Could not load state: {e}")

    def _save_state(self):
        """Save current state to file."""
        self.state_dir.mkdir(parents=True, exist_ok=True)

        data = {
            'task_id': self.task_id,
            'total_steps': self.total_steps,
            'completed_steps': self.completed_steps,
            'current_step': self.current_step,
            'failed_steps': self.failed_steps,
            'iterations': self.iterations,
            'updated_at': datetime.now().isoformat()
        }

        self.state_file.write_text(json.dumps(data, indent=2))

    def start_step(self, step_name: str):
        """Mark a step as started."""
        self.current_step = step_name
        self._save_state()
        logger.info(f"[{self.task_id}] Starting step: {step_name}")

    def complete_step(self, step_name: str):
        """Mark a step as completed."""
        if step_name not in self.completed_steps:
            self.completed_steps.append(step_name)

        if step_name in self.failed_steps:
            self.failed_steps.remove(step_name)

        self.current_step = None
        self._save_state()
        logger.info(f"[{self.task_id}] Completed step: {step_name} ({len(self.completed_steps)}/{self.total_steps})")

    def fail_step(self, step_name: str, error: str):
        """Mark a step as failed."""
        if step_name not in self.failed_steps:
            self.failed_steps.append(step_name)

        self.current_step = None
        self._save_state()
        logger.warning(f"[{self.task_id}] Failed step: {step_name} - {error}")

    def is_complete(self) -> bool:
        """Check if all steps are completed."""
        return len(self.completed_steps) >= self.total_steps

    def should_continue(self) -> bool:
        """Check if loop should continue iterating."""
        self.iterations += 1
        self._save_state()

        if self.is_complete():
            logger.info(f"[{self.task_id}] Task complete! ✓")
            return False

        if self.iterations >= self.max_iterations:
            logger.warning(f"[{self.task_id}] Max iterations reached ({self.max_iterations})")
            return False

        return True

    def get_next_step(self, all_steps: List[str]) -> Optional[str]:
        """Get the next incomplete step."""
        for step in all_steps:
            if step not in self.completed_steps:
                return step
        return None

    def get_progress(self) -> Dict[str, Any]:
        """Get current progress status."""
        return {
            'task_id': self.task_id,
            'progress': len(self.completed_steps) / self.total_steps * 100,
            'completed': len(self.completed_steps),
            'total': self.total_steps,
            'current': self.current_step,
            'failed': len(self.failed_steps),
            'iterations': self.iterations
        }


class RalphWiggumLoop:
    """
    Main loop orchestration for multi-step tasks.

    Implements the Stop Hook pattern to ensure tasks complete
    before the loop terminates.
    """

    def __init__(
        self,
        task_id: str,
        steps: List[str],
        vault_path: Path,
        max_iterations: Optional[int] = None
    ):
        """
        Initialize the loop.

        Args:
            task_id: Unique task identifier
            steps: List of step names in order
            vault_path: Path to vault directory
            max_iterations: Override default max iterations
        """
        self.task_id = task_id
        self.steps = steps
        self.vault_path = vault_path
        self.state_dir = vault_path / ".state" / "ralph_wiggum_loop"

        self.state = TaskState(
            task_id=task_id,
            total_steps=len(steps),
            state_dir=self.state_dir
        )

        if max_iterations:
            self.state.max_iterations = max_iterations

        # Stop hooks - functions that check completion conditions
        self.stop_hooks: List[callable] = []

        # Pre-iteration hooks
        self.pre_hooks: List[callable] = []

        # Post-iteration hooks
        self.post_hooks: List[callable] = []

    def register_stop_hook(self, hook: callable):
        """Register a stop hook function."""
        self.stop_hooks.append(hook)

    def register_pre_hook(self, hook: callable):
        """Register a pre-iteration hook."""
        self.pre_hooks.append(hook)

    def register_post_hook(self, hook: callable):
        """Register a post-iteration hook."""
        self.post_hooks.append(hook)

    async def run_iteration(self) -> bool:
        """
        Run a single iteration of the loop.

        Returns:
            True if should continue, False if should stop
        """
        # Run pre-hooks
        for hook in self.pre_hooks:
            try:
                await hook(self.state)
            except Exception as e:
                logger.error(f"Pre-hook error: {e}")

        # Get next step
        next_step = self.state.get_next_step(self.steps)

        if not next_step:
            logger.info("All steps completed!")
            return False

        # Execute step
        logger.info(f"Executing: {next_step}")
        self.state.start_step(next_step)

        try:
            # This is where the actual work happens
            # In practice, this would call the reasoning engine
            success = await self._execute_step(next_step)

            if success:
                self.state.complete_step(next_step)
            else:
                self.state.fail_step(next_step, "Execution failed")

        except Exception as e:
            logger.error(f"Error executing step {next_step}: {e}")
            self.state.fail_step(next_step, str(e))

        # Run post-hooks
        for hook in self.post_hooks:
            try:
                await hook(self.state)
            except Exception as e:
                logger.error(f"Post-hook error: {e}")

        # Check stop hooks
        for hook in self.stop_hooks:
            try:
                should_stop = await hook(self.state)
                if should_stop:
                    logger.info(f"Stop hook triggered: {hook.__name__}")
                    return False
            except Exception as e:
                logger.error(f"Stop hook error: {e}")

        # Check if we should continue
        return self.state.should_continue()

    async def _execute_step(self, step_name: str) -> bool:
        """
        Execute a single step.

        In practice, this calls the reasoning engine or agent.
        Override this method or provide a callback.

        Args:
            step_name: Name of the step to execute

        Returns:
            True if successful, False otherwise
        """
        # This is a placeholder - actual implementation would
        # call the reasoning engine or agent to perform the step

        logger.info(f"[EXECUTE] {step_name}")
        await asyncio.sleep(0.1)  # Simulate work
        return True

    async def run(self):
        """Run the full loop until completion."""
        logger.info(f"Starting Ralph Wiggum Loop: {self.task_id}")
        logger.info(f"Steps: {', '.join(self.steps)}")

        while True:
            should_continue = await self.run_iteration()
            if not should_continue:
                break

            # Small delay between iterations
            await asyncio.sleep(1)

        # Final status
        progress = self.state.get_progress()
        logger.info(f"Loop finished: {progress}")
        self._write_completion_report()

    def _write_completion_report(self):
        """Write a completion report."""
        report_path = self.vault_path / "Updates" / f"{self.task_id}_complete.md"

        progress = self.state.get_progress()

        report = f"""# Ralph Wiggum Loop Report

**Task ID:** {self.task_id}
**Status:** {'✓ Complete' if self.state.is_complete() else '✗ Incomplete'}
**Progress:** {progress['progress']:.1f}%
**Completed:** {progress['completed']}/{progress['total']}
**Iterations:** {progress['iterations']}

## Steps

"""
        for i, step in enumerate(self.steps, 1):
            status = "✓" if step in self.state.completed_steps else "✗"
            report += f"{i}. {status} {step}\n"

        if self.state.failed_steps:
            report += "\n## Failed Steps\n\n"
            for step in self.state.failed_steps:
                report += f"- {step}\n"

        report += f"\n---\n*Generated at {datetime.now().isoformat()}*\n"

        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report)

        logger.info(f"Report written to: {report_path}")


## Step 2: Prompt-Based Ralph Wiggum Loop

For use with Claude, here's a prompt template that implements the pattern:

```
# Ralph Wiggum Loop Protocol

You are in a Ralph Wiggum Loop. This means you will continue iterating
until ALL steps of the multi-step task are complete.

## Task
{TASK_DESCRIPTION}

## Steps
1. {STEP_1}
2. {STEP_2}
3. {STEP_3}
...

## Rules

1. **Never stop until all steps are complete**
2. After each step, verify it's actually done (check files, run tests, etc.)
3. If a step fails, retry up to 3 times before escalating
4. Update your progress after each step
5. Create a completion report when finished

## Stop Hook (CHECK THIS BEFORE STOPPING)

Before concluding, verify:
- [ ] All steps are marked complete
- [ ] Tests pass (if applicable)
- [ ] Files exist in expected locations
- [ ] Documentation is updated
- [ ] No partial or incomplete work

If ANY checkbox is unchecked, CONTINUE WORKING. Do not say "I'm done"
until all checks pass.

## Progress Tracking

After each step, update:
- Completed: {step_name}
- Timestamp: {now}
- Status: {success/failure}

Current Progress: {0/{total_steps}} steps complete

---

Begin with Step 1 now. Work through each step sequentially.
```

## Step 3: Integration with Reasoning Engine

### Example: Reading from /Needs_Action

```python
class NeedsActionLoop(RalphWiggumLoop):
    """Ralph Wiggum Loop for processing Needs_Action items."""

    async def _execute_step(self, step_name: str) -> bool:
        """Process a single item from Needs_Action."""
        needs_action_dir = self.vault_path / "Needs_Action"

        # Find the item file
        item_file = None
        for file in needs_action_dir.glob("*.md"):
            if step_name in file.stem:
                item_file = file
                break

        if not item_file:
            logger.warning(f"Item not found: {step_name}")
            return False

        # Read and process the item
        content = item_file.read_text()

        # Create Plan.md
        plan_content = self._generate_plan(content)
        plan_path = needs_action_dir / "Plan.md"
        plan_path.write_text(plan_content)

        # Execute plan items
        return await self._execute_plan(plan_path)

    def _generate_plan(self, item_content: str) -> str:
        """Generate a plan from item content."""
        return f"""# Execution Plan

Based on the action item, here are the steps:

{item_content}

## Checklist
- [ ] Analyze requirements
- [ ] Implement solution
- [ ] Test and verify
- [ ] Document results
"""

    async def _execute_plan(self, plan_path: Path) -> bool:
        """Execute the plan items."""
        # In practice, this would parse the plan and execute each item
        logger.info(f"Executing plan: {plan_path}")
        return True
```

### Example: Stop Hook for Completion

```python
async def stop_hook_verify_files(state: TaskState) -> bool:
    """Stop hook that verifies all expected files exist."""
    vault_path = Path("./vault")

    expected_files = [
        "Dashboard.md",
        "Updates/summary.md",
        "Accounting/Current_Month.md"
    ]

    for file_path in expected_files:
        if not (vault_path / file_path).exists():
            logger.warning(f"Missing expected file: {file_path}")
            return False  # Don't stop yet

    return True  # All checks passed, safe to stop


# Usage
loop = RalphWiggumLoop(
    task_id="daily_tasks",
    steps=["check_emails", "process_invoices", "update_dashboard"],
    vault_path=Path("./vault")
)

loop.register_stop_hook(stop_hook_verify_files)
await loop.run()
```

## ACCEPTANCE CRITERIA

- Loop continues until all steps are marked complete
- State persists between iterations
- Stop hooks prevent premature termination
- Progress is tracked and reportable
- Max iterations prevent infinite loops

## FOLLOW-UPS

- Add progress dashboard/visualization
- Implement parallel step execution
- Create recovery mode for failed loops
- Add integration with Claude API

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.
