---
description: Base watcher template with abstract methods and run loop for all watchers.
---

# COMMAND: Base Watcher Template

## CONTEXT

The user needs to create a base template for all watcher agents that:

- Provides a common structure for monitoring external systems
- Defines abstract methods that specific watchers must implement
- Implements the run loop for continuous monitoring
- Handles error recovery and graceful shutdown

## YOUR ROLE

Act as a Python software architect with expertise in:

- Abstract base classes and inheritance patterns
- Asynchronous programming and event loops
- Observer pattern implementation
- Error handling and recovery strategies

## OUTPUT STRUCTURE

Create a base watcher template that includes:

1. **Abstract Base Class** with required methods
2. **Run Loop** implementation with configurable intervals
3. **Error Handling** with retry logic
4. **Graceful Shutdown** support
5. **Logging** and observability hooks

## Step 1: Create Base Watcher Class

```python
#!/usr/bin/env python3
"""
Base Watcher - Abstract template for all watcher agents

All specific watchers (Gmail, WhatsApp, etc.) must inherit from this class
and implement the abstract methods defined below.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BaseWatcher")


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher agents.

    Attributes:
        name (str): Human-readable watcher name
        check_interval (int): Seconds between checks
        vault_path (Path): Path to the shared vault directory
        running (bool): Control flag for the run loop
    """

    def __init__(
        self,
        name: str,
        vault_path: Path,
        check_interval: int = 60
    ):
        """
        Initialize the base watcher.

        Args:
            name: Human-readable name for this watcher
            vault_path: Path to shared vault directory
            check_interval: Seconds between monitoring checks (default: 60)
        """
        self.name = name
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.running = False
        self._setup_paths()

    def _setup_paths(self):
        """Create required directory structure in vault."""
        self.needs_action_dir = self.vault_path / "Needs_Action"
        self.pending_approval_dir = self.vault_path / "Pending_Approval"
        self.updates_dir = self.vault_path / "Updates"

        # Create directories if they don't exist
        for directory in [self.needs_action_dir, self.pending_approval_dir, self.updates_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info(f"Watcher '{self.name}' initialized with vault at {self.vault_path}")

    @abstractmethod
    async def check(self) -> List[Dict[str, Any]]:
        """
        Check for new items from the monitored system.

        This method MUST be implemented by each specific watcher.

        Returns:
            List of dictionaries, each containing:
                - id: Unique identifier for the item
                - timestamp: When the item was created/modified
                - source: Source system name
                - data: Raw data from the source
                - metadata: Additional context (headers, sender, etc.)
        """
        pass

    @abstractmethod
    async def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single item and extract relevant information.

        This method MUST be implemented by each specific watcher.

        Args:
            item: Item dictionary from check()

        Returns:
            Processed item dictionary with:
                - title: Brief title/description
                - content: Main content/body
                - action_type: Type of action needed
                - priority: Priority level (low/medium/high)
                - metadata: Additional context
            Or None if item should be ignored
        """
        pass

    @abstractmethod
    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create an action file in the Needs_Action directory.

        This method MUST be implemented by each specific watcher.

        Args:
            item: Processed item from process_item()

        Returns:
            Path to the created action file
        """
        pass

    async def validate_item(self, item: Dict[str, Any]) -> bool:
        """
        Validate that an item meets minimum requirements.

        Override this method to add custom validation logic.

        Args:
            item: Item to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ['id', 'timestamp', 'source', 'data']
        return all(field in item for field in required_fields)

    async def filter_item(self, item: Dict[str, Any]) -> bool:
        """
        Filter items based on custom criteria.

        Override this method to add custom filtering logic.
        Return True to process the item, False to skip it.

        Args:
            item: Item to filter

        Returns:
            True to process, False to skip
        """
        return True

    async def handle_item(self, item: Dict[str, Any]) -> Optional[Path]:
        """
        Handle a single item through the full pipeline.

        Args:
            item: Raw item from check()

        Returns:
            Path to action file if created, None otherwise
        """
        try:
            # Validate item
            if not await self.validate_item(item):
                logger.warning(f"Invalid item: {item.get('id', 'unknown')}")
                return None

            # Filter item
            if not await self.filter_item(item):
                logger.debug(f"Filtered out item: {item.get('id', 'unknown')}")
                return None

            # Process item
            processed = await self.process_item(item)
            if not processed:
                return None

            # Create action file
            action_path = await self.create_action_file(processed)
            logger.info(f"Created action file: {action_path}")
            return action_path

        except Exception as e:
            logger.error(f"Error handling item {item.get('id', 'unknown')}: {e}")
            return None

    async def run_once(self) -> int:
        """
        Run a single check cycle.

        Returns:
            Number of action files created
        """
        logger.info(f"Running check cycle for {self.name}")

        try:
            items = await self.check()
            logger.info(f"Found {len(items)} items")

            created_count = 0
            for item in items:
                result = await self.handle_item(item)
                if result:
                    created_count += 1

            logger.info(f"Created {created_count} action files")
            return created_count

        except Exception as e:
            logger.error(f"Error in check cycle: {e}")
            return 0

    async def run(self):
        """
        Main run loop - continuously check for new items.
        """
        logger.info(f"Starting watcher '{self.name}'")
        self.running = True

        # Set up signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))

        try:
            while self.running:
                await self.run_once()
                logger.debug(f"Waiting {self.check_interval} seconds until next check")
                await asyncio.sleep(self.check_interval)

        except Exception as e:
            logger.error(f"Fatal error in run loop: {e}")
        finally:
            await self.cleanup()

    async def stop(self):
        """
        Stop the watcher gracefully.
        """
        logger.info(f"Stopping watcher '{self.name}'")
        self.running = False

    async def cleanup(self):
        """
        Cleanup resources before shutdown.

        Override this method to add custom cleanup logic.
        """
        logger.info(f"Cleanup for watcher '{self.name}'")


def create_watcher(watcher_type: str, **kwargs) -> BaseWatcher:
    """
    Factory function to create specific watcher instances.

    Args:
        watcher_type: Type of watcher to create ('gmail', 'whatsapp', etc.)
        **kwargs: Arguments to pass to the watcher constructor

    Returns:
        Instance of the specified watcher

    Raises:
        ValueError: If watcher_type is unknown
    """
    watchers = {
        # 'gmail': GmailWatcher,
        # 'whatsapp': WhatsAppWatcher,
        # 'filesystem': FilesystemWatcher,
    }

    watcher_class = watchers.get(watcher_type.lower())
    if not watcher_class:
        raise ValueError(f"Unknown watcher type: {watcher_type}")

    return watcher_class(**kwargs)


async def main():
    """
    Example main function to run a watcher.
    """
    import os

    vault_path = Path(os.getenv("VAULT_PATH", "./vault"))
    # watcher = GmailWatcher(vault_path=vault_path)
    # await watcher.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Usage Instructions

### Creating a Specific Watcher

To create a specific watcher (e.g., Gmail, WhatsApp):

1. **Inherit from `BaseWatcher`**
2. **Implement all abstract methods**:
   - `check()` - Fetch items from the source
   - `process_item()` - Extract relevant information
   - `create_action_file()` - Create the action file in Needs_Action

3. **Override optional methods**:
   - `validate_item()` - Add custom validation
   - `filter_item()` - Add custom filtering
   - `cleanup()` - Add custom cleanup

### Example Skeleton

```python
from base_watcher import BaseWatcher
from pathlib import Path
from typing import Dict, Any, List

class MyWatcher(BaseWatcher):
    """Custom watcher implementation."""

    def __init__(self, vault_path: Path, **kwargs):
        super().__init__(
            name="MyWatcher",
            vault_path=vault_path,
            check_interval=kwargs.get('check_interval', 60)
        )
        # Add custom initialization here

    async def check(self) -> List[Dict[str, Any]]:
        """Check for new items."""
        # Your implementation here
        pass

    async def process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single item."""
        # Your implementation here
        pass

    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """Create action file."""
        # Your implementation here
        pass
```

## Step 3: Running a Watcher

```bash
# Set vault path
export VAULT_PATH=/path/to/vault

# Run the watcher
python gmail_watcher.py
```

## ACCEPTANCE CRITERIA

- BaseWatcher class is abstract and cannot be instantiated directly
- All abstract methods are clearly documented
- Run loop supports graceful shutdown via SIGTERM/SIGINT
- Error handling prevents crashes on individual item failures
- Logging provides visibility into watcher operations

## FOLLOW-UPS

- Add metrics collection (items processed, errors, etc.)
- Implement backoff strategy for failed API calls
- Add health check endpoint for monitoring

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: `misc`

2) Generate Title: "Base Watcher Template Creation"

3) Create and Fill PHR using agent-native tools
