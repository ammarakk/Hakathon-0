# Claim-by-Move Contract

**Version**: 1.0
**Date**: 2026-02-21
**Status**: Final

---

## Overview

This contract defines the claim-by-move coordination pattern used by Phase 4 agents to prevent duplicate work. The first agent to move a file from `/Needs_Action/` to `/In_Progress/<agent>/` owns the task.

---

## Claim Operation

### Atomic Move

**Purpose**: Atomically claim ownership of a task

**Algorithm**:
```python
import os
import shutil

def claim_task(task_file: str, agent_name: str) -> bool:
    """
    Attempt to claim a task by moving it to In_Progress/<agent>/.

    Returns:
        True if claim successful, False if already claimed
    """
    # Path construction
    vault_path = "/vault"
    source_path = os.path.join(vault_path, "Needs_Action", task_file)
    target_dir = os.path.join(vault_path, "In_Progress", agent_name)
    target_path = os.path.join(target_dir, task_file)

    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)

    try:
        # Atomic rename (POSIX guarantee)
        os.rename(source_path, target_path)

        # Update file content with claim metadata
        add_claim_metadata(target_path, agent_name)

        return True  # Claim successful

    except FileNotFoundError:
        # File no longer exists - another agent claimed it
        return False

    except OSError as e:
        # Other error (permissions, disk full, etc.)
        log_error(f"Claim failed: {e}")
        return False
```

**Atomicity Guarantee**: On POSIX systems, `os.rename()` is atomic. If two agents attempt to claim simultaneously, only one succeeds.

### Claim Verification

**Purpose**: Verify task is still available before processing

**Algorithm**:
```python
def verify_claim(task_file: str) -> bool:
    """
    Verify that the claimed task still exists in In_Progress.

    Returns:
        True if task exists (claim valid), False otherwise
    """
    claim_path = os.path.join("/vault", "In_Progress", AGENT_NAME, task_file)
    return os.path.exists(claim_path)
```

**Usage**: Before processing a claimed task, verify it still exists.

---

## Release Operation

### Move to Next State

**Purpose**: Release task from `In_Progress` to next state

**Algorithm**:
```python
def release_task(task_file: str, agent_name: str, next_state: str) -> bool:
    """
    Move task from In_Progress/<agent>/ to next state folder.

    Args:
        task_file: Filename of the task
        agent_name: Current owning agent
        next_state: Target state (Pending_Approval, Done, Rejected)

    Returns:
        True if release successful, False otherwise
    """
    # Path construction
    source_path = os.path.join("/vault", "In_Progress", agent_name, task_file)
    target_dir = os.path.join("/vault", next_state)
    target_path = os.path.join(target_dir, task_file)

    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)

    try:
        # Move to next state
        os.rename(source_path, target_path)

        # Update file metadata
        update_metadata(target_path, next_state)

        return True

    except FileNotFoundError:
        # Task no longer exists (should not happen)
        log_error(f"Task not found: {task_file}")
        return False

    except OSError as e:
        log_error(f"Release failed: {e}")
        return False
```

**Next States**:
- `Pending_Approval`: Task requires human approval (sensitive action)
- `Done`: Task completed (no approval needed)
- `Rejected`: Task rejected (by human or agent)

---

## Agent Behavior

### Claim Loop

**Purpose**: Agent continuously checks for new tasks to claim

**Algorithm**:
```python
import time
import os

def claim_loop(agent_name: str, interval: int = 10):
    """
    Main claim loop for an agent.

    Args:
        agent_name: Name of the agent (cloud, local)
        interval: Check interval in seconds
    """
    while True:
        try:
            # List tasks in Needs_Action
            needs_action_dir = "/vault/Needs_Action"
            tasks = os.listdir(needs_action_dir)

            for task_file in tasks:
                if task_file.endswith('.md'):
                    # Attempt to claim
                    if claim_task(task_file, agent_name):
                        log(f"Claimed: {task_file}")

                        # Verify claim (double-check)
                        if verify_claim(task_file):
                            # Process task
                            process_task(task_file)
                        else:
                            log(f"Claim verification failed: {task_file}")

            # Wait for next interval
            time.sleep(interval)

        except Exception as e:
            log_error(f"Claim loop error: {e}")
            time.sleep(interval)
```

### Process Task

**Purpose**: Process a claimed task

**Algorithm**:
```python
def process_task(task_file: str):
    """
    Process a claimed task.

    Steps:
    1. Read task content
    2. Determine action type
    3. Execute or create draft
    4. Move to next state
    """
    # 1. Read task
    claim_path = os.path.join("/vault", "In_Progress", AGENT_NAME, task_file)
    task = read_task(claim_path)

    # 2. Determine action
    action_type = determine_action(task)

    # 3. Check if action is allowed for this agent
    if action_type in ALLOWED_ACTIONS:
        # Execute directly
        result = execute_action(action_type, task)

        # Move to Done
        release_task(task_file, AGENT_NAME, "Done")

    elif AGENT_ROLE == "CLOUD" and action_type in SENSITIVE_ACTIONS:
        # Cloud creates draft, Local approves
        draft_file = create_draft(task, action_type)
        release_task(task_file, AGENT_NAME, "Pending_Approval")

    else:
        # Action not allowed
        log_error(f"Action not allowed: {action_type}")
        release_task(task_file, AGENT_NAME, "Rejected")
```

---

## Race Condition Handling

### Race Window

**Scenario**: Two agents attempt to claim the same task simultaneously

**Timeline**:
```
Time  Agent A                          Agent B
----  --------                         --------
T1    Check file exists
T2    os.rename() (atomic)
T3                                     Check file exists
T4                                     os.rename() (fails: not found)
T5    Claim successful                  Claim failed (skip)
```

**Window**: <1ms (atomic rename on POSIX filesystem)

### Retry with Backoff

**Purpose**: Handle temporary failures gracefully

**Algorithm**:
```python
import time

def claim_with_retry(task_file: str, agent_name: str, max_retries: int = 3) -> bool:
    """
    Attempt to claim task with exponential backoff.

    Returns:
        True if claim successful, False otherwise
    """
    for attempt in range(max_retries):
        if claim_task(task_file, agent_name):
            return True

        # Exponential backoff: 100ms, 200ms, 400ms
        backoff = 0.1 * (2 ** attempt)
        time.sleep(backoff)

    log_error(f"Claim failed after {max_retries} retries: {task_file}")
    return False
```

---

## File Metadata

### Claim Metadata

**Added to file when claimed**:

```markdown
# Claimed Task: <task_id>

**Claimed By**: <agent_name>
**Claimed At**: <timestamp>
**Status**: processing

## Progress

<!-- Agent adds progress notes here -->
```

### Completion Metadata

**Added to file when completed**:

```markdown
## Completion

**Completed At**: <timestamp>
**Duration**: <seconds>
**Result**: <success/failure>
**Next State**: <Pending_Approval/Done/Rejected>
```

---

## Synchronization

### Git Sync Coordination

**Problem**: Git sync can cause conflicts during claim operations

**Solution**: Claim before sync, sync after processing

**Algorithm**:
```python
def sync_safe_claim_loop(agent_name: str):
    """
    Claim loop that coordinates with Git sync.
    """
    while True:
        # 1. Pull latest changes
        subprocess.run(["git", "pull", "origin", "main"])

        # 2. Claim tasks (atomic moves are local)
        claim_and_process_tasks(agent_name)

        # 3. Commit and push changes
        subprocess.run(["git", "add", "-A"])
        subprocess.run(["git", "commit", "-m" f"Agent {agent_name} updates"])
        subprocess.run(["git", "push", "origin", "main"])

        # 4. Wait for next interval
        time.sleep(30)
```

**Race Condition**: If cloud and local both pull, claim, and push simultaneously, Git will detect conflicts on the second push. Both agents will see the file removed from `Needs_Action/` (successful claim), but only one will successfully push. The other will encounter a Git conflict and must re-pull.

---

## Testing

### Test Script

**File**: `tests/integration/test-claim-by-move.sh`

```bash
#!/bin/bash

# 1. Create test task
echo "# Test Task" > /vault/Needs_Action/test-task.md

# 2. Start two agents simultaneously
agent-a --once &
agent-b --once &
wait

# 3. Verify only one agent claimed the task
if [ -f /vault/In_Progress/cloud/test-task.md ]; then
    if [ -f /vault/In_Progress/local/test-task.md ]; then
        echo "✗ Both agents claimed task (FAILED)"
        exit 1
    else
        echo "✓ Cloud agent claimed task (PASSED)"
    fi
elif [ -f /vault/In_Progress/local/test-task.md ]; then
    echo "✓ Local agent claimed task (PASSED)"
else
    echo "✗ No agent claimed task (FAILED)"
    exit 1
fi

# 4. Verify task removed from Needs_Action
if [ -f /vault/Needs_Action/test-task.md ]; then
    echo "✗ Task still in Needs_Action (FAILED)"
    exit 1
else
    echo "✓ Task removed from Needs_Action (PASSED)"
fi

echo "✓ All claim-by-move tests: PASSED"
```

---

## Monitoring

### Metrics

**Claim Metrics** (exposed via `/health` endpoint):

```json
{
  "coordination": {
    "agent_name": "cloud",
    "active_claims": 3,
    "total_claims": 142,
    "claim_conflicts_avoided": 12,
    "claim_success_rate": 0.98
  }
}
```

**Logs**:
- `/var/log/ai-employee/agent-<name>.log` - Claim operations

---

## Summary

This contract specifies:
- **Atomic move** operation for claiming tasks
- **Claim verification** to prevent processing unclaimed tasks
- **Release operation** to move tasks to next state
- **Race condition handling** with exponential backoff
- **Git sync coordination** to avoid conflicts
- **Testing strategy** to verify single-writer guarantee

The claim-by-move pattern ensures that only one agent processes each task, preventing duplicate work while maintaining simplicity and reliability.
