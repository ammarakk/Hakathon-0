#!/usr/bin/env python3
"""
Base Watcher - Abstract template for all watcher agents (Phase 1 Simplified)

All specific watchers must inherit from this class and implement the abstract methods.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BaseWatcher")


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher agents.
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

        Returns:
            List of item dictionaries
        """
        pass

    @abstractmethod
    async def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single item and extract relevant information.

        Args:
            item: Item dictionary from check()

        Returns:
            Processed item dictionary or None if item should be ignored
        """
        pass

    @abstractmethod
    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create an action file in the Needs_Action directory.

        Args:
            item: Processed item dictionary

        Returns:
            Path to created action file
        """
        pass

    async def run_once(self):
        """
        Execute one monitoring cycle.
        """
        logger.info(f"Checking {self.name} for new items...")

        # Check for new items
        raw_items = await self.check()

        if not raw_items:
            logger.info(f"No new items found by {self.name}")
            return

        logger.info(f"Found {len(raw_items)} new items")

        # Process each item
        for raw_item in raw_items:
            try:
                # Process the item
                processed = await self.process_item(raw_item)

                if not processed:
                    logger.debug(f"Item ignored: {raw_item.get('id')}")
                    continue

                # Create action file
                action_file = await self.create_action_file(processed)
                logger.info(f"Created action file: {action_file}")

            except Exception as e:
                logger.error(f"Error processing item {raw_item.get('id')}: {e}")

    async def run(self):
        """
        Main run loop - continuously check for new items.
        """
        logger.info(f"Starting watcher '{self.name}'")
        self.running = True

        try:
            while self.running:
                await self.run_once()
                await asyncio.sleep(self.check_interval)

        except Exception as e:
            logger.error(f"Fatal error in run loop: {e}")
        finally:
            await self.cleanup()

    async def stop(self):
        """Stop the watcher gracefully."""
        logger.info(f"Stopping watcher '{self.name}'")
        self.running = False

    async def cleanup(self):
        """Cleanup resources."""
        logger.info(f"Cleanup for watcher '{self.name}'")
