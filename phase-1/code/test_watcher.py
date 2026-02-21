#!/usr/bin/env python3
"""
Manual test for FilesystemWatcher (Phase 1)

This script manually tests the watcher by simulating a file drop.
"""
import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from base_watcher import BaseWatcher
from datetime import datetime
from typing import Dict, Any, List, Optional

class MockFilesystemWatcher(BaseWatcher):
    """Simplified watcher for manual testing."""

    async def check(self) -> List[Dict[str, Any]]:
        """Return test file data."""
        return [{
            'id': 'test_001',
            'timestamp': datetime.now().isoformat(),
            'source': 'filesystem',
            'data': {
                'file_path': str(Path(__file__).parent.parent.parent / 'test_drop_folder' / 'test_file.txt'),
                'file_name': 'test_file.txt',
                'file_size': 43,
                'file_extension': '.txt',
            },
            'metadata': {
                'mime_type': 'text/plain',
            }
        }]

    async def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process the test item."""
        return {
            'title': f"File Drop: {item['data']['file_name']}",
            'content': f"Test file detected via manual trigger\nSize: {item['data']['file_size']} bytes",
            'action_type': 'file_review',
            'priority': 'medium',
            'metadata': {
                'source_id': item['id'],
                'file_path': item['data']['file_path'],
                'file_name': item['data']['file_name'],
                'file_size': item['data']['file_size'],
                'mime_type': item['metadata']['mime_type'],
                'category': 'text',
                'timestamp': item['timestamp'],
            }
        }

    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """Create action file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = item['metadata']['file_name']

        action_filename = f"{timestamp}_filesystem_{safe_name}.md"
        action_filepath = self.needs_action_dir / action_filename

        content = f"""---
type: action_item
source: filesystem
timestamp: {item['metadata']['timestamp']}
priority: {item['priority']}
---
# {item['title']}

**Source**: {item['metadata'].get('source', 'filesystem')}
**Detected**: {item['metadata']['timestamp']}
**Priority**: {item['priority'].upper()}

## Content

{item['content']}

**File Path**: `{item['metadata']['file_path']}`
**File Size**: {item['metadata']['file_size']:,} bytes
**MIME Type**: {item['metadata']['mime_type']}
**Category**: {item['metadata']['category']}

## Actions Required
- [ ] Review file content
- [ ] Determine required action
- [ ] Process or categorize appropriately

---
*Created by FilesystemWatcher (manual test) at {datetime.now().isoformat()}*
"""

        action_filepath.write_text(content, encoding='utf-8')
        print(f"✓ Created action file: {action_filepath}")
        return action_filepath


async def main():
    """Run manual test."""
    import sys
    import os

    # Import test_config
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from test_config import VAULT_PATH

    print("=" * 60)
    print("FilesystemWatcher Manual Test (Phase 1)")
    print("=" * 60)
    print(f"\nVault Path: {VAULT_PATH}")
    print(f"Needs_Action: {VAULT_PATH / 'Needs_Action'}")

    # Create watcher
    watcher = MockFilesystemWatcher(
        name="MockFilesystemWatcher",
        vault_path=VAULT_PATH,
        check_interval=60
    )

    print("\nRunning one check cycle...")
    await watcher.run_once()

    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

    # List created files
    needs_action = VAULT_PATH / "Needs_Action"
    if needs_action.exists():
        files = list(needs_action.glob("*.md"))
        print(f"\nFiles in Needs_Action: {len(files)}")
        for f in files:
            print(f"  - {f.name}")


if __name__ == "__main__":
    asyncio.run(main())
