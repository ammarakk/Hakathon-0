---
description: File system watcher using watchdog for handling file drops and auto-processing.
---

# COMMAND: File System Watcher Implementation

## CONTEXT

The user needs to implement a file system watcher that:

- Monitors directories for new file drops
- Automatically copies files to /Needs_Action
- Creates metadata .md files for each file
- Handles various file types (documents, images, etc.)

## YOUR ROLE

Act as a Python developer with expertise in:

- File system monitoring using watchdog
- Event-driven programming
- File operations and metadata extraction
- Async/await patterns

## OUTPUT STRUCTURE

Create a complete file system watcher implementation with:

1. **Watchdog-based directory monitoring**
2. **File processing pipeline** with metadata extraction
3. **Automatic copying** to Needs_Action
4. **Metadata file creation** with file info
5. **Setup instructions** for observer configuration

## Step 1: File System Watcher Implementation

```python
#!/usr/bin/env python3
"""
File System Watcher - Monitor directories for file drops

This watcher uses the watchdog library to monitor directories for new files,
automatically copying them to Needs_Action and creating metadata files.
"""

import asyncio
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import hashlib
import mimetypes

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FilesystemWatcher")


class FilesystemHandler(FileSystemEventHandler):
    """
    Handler for filesystem events.
    """

    def __init__(self, callback):
        """
        Initialize the handler.

        Args:
            callback: Async callback function to call when file is detected
        """
        super().__init__()
        self.callback = callback
        self.processed_files: Set[str] = set()
        self._loop = asyncio.get_event_loop()

    def on_created(self, event: FileSystemEvent):
        """Handle file/directory creation events."""
        if not event.is_directory:
            file_path = Path(event.src_path)

            # Skip temporary files and hidden files
            if file_path.name.startswith('.') or file_path.name.startswith('~'):
                return

            # Skip if already processed
            file_key = str(file_path.absolute())
            if file_key in self.processed_files:
                return

            logger.info(f"New file detected: {file_path}")

            # Add small delay to ensure file write is complete
            asyncio.run_coroutine_threadsafe(
                self._process_with_delay(file_path),
                self._loop
            )

    async def _process_with_delay(self, file_path: Path, delay: float = 1.0):
        """Wait before processing to ensure file write is complete."""
        await asyncio.sleep(delay)

        # Check if file still exists and has stable size
        if file_path.exists():
            try:
                # Get initial size
                initial_size = file_path.stat().st_size
                await asyncio.sleep(0.5)

                # Check size again
                final_size = file_path.stat().st_size

                # Only process if size is stable
                if initial_size == final_size:
                    await self.callback(file_path)
                    self.processed_files.add(str(file_path.absolute()))
                else:
                    # File still being written, retry later
                    logger.debug(f"File {file_path} still being written, will retry")

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")


class FilesystemWatcher(BaseWatcher):
    """
    Watcher for monitoring directories for new file drops.

    Uses watchdog to monitor specified directories and automatically
    process new files by copying them and creating metadata.
    """

    def __init__(
        self,
        vault_path: Path,
        watch_directories: List[Path],
        check_interval: int = 60,
        copy_files: bool = True,
        allowed_extensions: Optional[List[str]] = None,
        blocked_extensions: Optional[List[str]] = None
    ):
        """
        Initialize the filesystem watcher.

        Args:
            vault_path: Path to shared vault directory
            watch_directories: List of directories to monitor
            check_interval: Seconds between observer checks (default: 60)
            copy_files: Whether to copy files to Needs_Action (default: True)
            allowed_extensions: List of allowed extensions (None = all)
            blocked_extensions: List of blocked extensions (e.g., ['.tmp', '.part'])
        """
        super().__init__(
            name="FilesystemWatcher",
            vault_path=vault_path,
            check_interval=check_interval
        )
        self.watch_directories = [Path(d) for d in watch_directories]
        self.copy_files = copy_files
        self.allowed_extensions = allowed_extensions
        self.blocked_extensions = blocked_extensions or ['.tmp', '.part', '.crdownload']
        self.observer = None
        self.handler = None
        self.pending_items: List[Path] = []
        self._setup_watcher()

    def _setup_watcher(self):
        """Set up the watchdog observer."""
        self.observer = Observer()
        self.handler = FilesystemHandler(self._on_file_detected)

        for directory in self.watch_directories:
            if directory.exists():
                self.observer.schedule(self.handler, str(directory), recursive=True)
                logger.info(f"Watching directory: {directory}")
            else:
                logger.warning(f"Directory does not exist, will create: {directory}")
                directory.mkdir(parents=True, exist_ok=True)
                self.observer.schedule(self.handler, str(directory), recursive=True)

    async def _on_file_detected(self, file_path: Path):
        """
        Callback when a new file is detected.

        Args:
            file_path: Path to the detected file
        """
        self.pending_items.append(file_path)

    async def check(self) -> List[Dict[str, Any]]:
        """
        Check for new files (from pending items).

        Returns:
            List of file item dictionaries
        """
        if not self.pending_items:
            return []

        items = []
        processed = []

        for file_path in self.pending_items[:50]:  # Process in batches
            try:
                # Check file extension filters
                if not self._is_allowed_file(file_path):
                    logger.debug(f"File not allowed: {file_path}")
                    processed.append(file_path)
                    continue

                # Get file metadata
                stat = file_path.stat()
                file_hash = self._get_file_hash(file_path)

                item = {
                    'id': f"file_{file_hash[:16]}",
                    'timestamp': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'source': 'FileSystem',
                    'data': {
                        'file_path': str(file_path),
                        'file_name': file_path.name,
                        'file_size': stat.st_size,
                        'file_extension': file_path.suffix,
                    },
                    'metadata': {
                        'mime_type': mimetypes.guess_type(file_path)[0] or 'application/octet-stream',
                    }
                }

                items.append(item)
                processed.append(file_path)

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                processed.append(file_path)

        # Remove processed items from pending
        for item in processed:
            if item in self.pending_items:
                self.pending_items.remove(item)

        logger.info(f"Processed {len(items)} new files")
        return items

    def _is_allowed_file(self, file_path: Path) -> bool:
        """
        Check if file is allowed based on extension filters.

        Args:
            file_path: Path to file

        Returns:
            True if allowed, False otherwise
        """
        extension = file_path.suffix.lower()

        # Check blocked extensions
        if extension in self.blocked_extensions:
            return False

        # Check allowed extensions
        if self.allowed_extensions:
            return extension in self.allowed_extensions

        return True

    def _get_file_hash(self, file_path: Path) -> str:
        """
        Calculate SHA256 hash of file.

        Args:
            file_path: Path to file

        Returns:
            Hexadecimal hash string
        """
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    async def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a file item.

        Args:
            item: Raw file item

        Returns:
            Processed item or None
        """
        file_path = Path(item['data']['file_path'])
        file_name = item['data']['file_name']
        file_size = item['data']['file_size']
        mime_type = item['metadata']['mime_type']

        # Determine file category
        category = self._get_file_category(mime_type, file_path.suffix)

        # Determine action type
        action_type = self._get_action_type(category)

        return {
            'title': f"File Drop: {file_name}",
            'content': f"New file detected: {file_name}\nType: {mime_type}\nSize: {file_size:,} bytes",
            'action_type': action_type,
            'priority': self._get_priority(category),
            'metadata': {
                'source_id': item['id'],
                'file_path': str(file_path),
                'file_name': file_name,
                'file_size': file_size,
                'mime_type': mime_type,
                'category': category,
                'timestamp': item['timestamp'],
            }
        }

    def _get_file_category(self, mime_type: str, extension: str) -> str:
        """Determine file category based on mime type and extension."""
        if mime_type.startswith('image/'):
            return 'image'
        elif mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('audio/'):
            return 'audio'
        elif mime_type in ['application/pdf']:
            return 'document'
        elif extension in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp']:
            return 'document'
        elif extension in ['.txt', '.md', '.rst']:
            return 'text'
        elif extension in ['.zip', '.tar', '.gz', '.rar', '.7z']:
            return 'archive'
        elif extension in ['.csv', '.json', '.xml', '.yaml', '.yml']:
            return 'data'
        else:
            return 'other'

    def _get_action_type(self, category: str) -> str:
        """Determine action type based on file category."""
        action_map = {
            'document': 'document_review',
            'image': 'image_review',
            'data': 'data_processing',
            'archive': 'archive_extraction',
            'invoice': 'invoice_processing',
        }
        return action_map.get(category, 'file_review')

    def _get_priority(self, category: str) -> str:
        """Determine priority based on file category."""
        high_priority = ['invoice', 'payment', 'contract']
        if category in high_priority:
            return 'high'
        return 'medium'

    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create an action file and optionally copy the file.

        Args:
            item: Processed file item

        Returns:
            Path to created action file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_', '.') else '_' for c in item['metadata']['file_name'])

        # Create action file
        action_filename = f"{timestamp}_file_{safe_name[:40]}.md"
        action_filepath = self.needs_action_dir / action_filename

        # Copy file if enabled
        copied_to = ""
        if self.copy_files:
            files_dir = self.needs_action_dir / "files"
            files_dir.mkdir(exist_ok=True)

            destination = files_dir / f"{timestamp}_{safe_name}"
            try:
                shutil.copy2(item['metadata']['file_path'], destination)
                copied_to = f"\n**Copied to:** `{destination}`"
            except Exception as e:
                logger.error(f"Error copying file: {e}")

        content = f"""# {item['title']}

**Source:** File System Drop
**File:** {item['metadata']['file_name']}
**Type:** {item['metadata']['mime_type']}
**Category:** {item['metadata']['category']}
**Size:** {item['metadata']['file_size']:,} bytes
**Priority:** {item['priority'].upper()}
**Detected:** {item['metadata']['timestamp']}{copied_to}

## Description
{item['content']}

## Actions Required
- [ ] Review file content
- [ ] Determine required action
- [ ] Process or categorize appropriately

---
*Created by FilesystemWatcher at {datetime.now().isoformat()}*
"""

        action_filepath.write_text(content, encoding='utf-8')

        # Create metadata file next to copied file (if copied)
        if copied_to:
            metadata_path = Path(str(destination) + '.metadata.md')
            metadata_content = f"""# File Metadata

**Original Path:** `{item['metadata']['file_path']}`
**File Name:** {item['metadata']['file_name']}
**MIME Type:** {item['metadata']['mime_type']}
**Category:** {item['metadata']['category']}
**Size:** {item['metadata']['file_size']:,} bytes
**SHA256:** {item['metadata']['source_id'].replace('file_', '')}
**Detected:** {item['metadata']['timestamp']}
**Action File:** `{action_filepath}`

## Auto-Extracted Info
Created by FilesystemWatcher at {datetime.now().isoformat()}
"""
            metadata_path.write_text(metadata_content, encoding='utf-8')

        return action_filepath

    async def run(self):
        """
        Main run loop - start observer and check for new files.
        """
        logger.info(f"Starting watcher '{self.name}'")

        # Start the observer
        self.observer.start()

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
        """Cleanup observer resources."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        await super().cleanup()


async def main():
    """Main entry point for running the filesystem watcher."""
    import os

    vault_path = Path(os.getenv("VAULT_PATH", "./vault"))
    watch_dirs = os.getenv("WATCH_DIRECTORIES", "./drops").split(",")

    watcher = FilesystemWatcher(
        vault_path=vault_path,
        watch_directories=[Path(d.strip()) for d in watch_dirs],
        check_interval=10,
        copy_files=True,
        allowed_extensions=None,  # Allow all files
        blocked_extensions=['.tmp', '.part', '.crdownload']
    )

    await watcher.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Setup Instructions

### Prerequisites

1. **Install Dependencies**
```bash
pip install watchdog
```

2. **Create Watch Directories**
```bash
mkdir -p ./drops/documents
mkdir -p ./drops/invoices
mkdir -p ./drops/images
```

3. **Configure Environment**
```bash
export VAULT_PATH=/path/to/vault
export WATCH_DIRECTORIES="./drops/documents,./drops/invoices,./drops/images"
```

### Running the Watcher

```bash
python filesystem_watcher.py
```

### Configuration Options

```python
watcher = FilesystemWatcher(
    vault_path=vault_path,
    watch_directories=[
        Path('./drops/documents'),
        Path('./drops/invoices'),
        Path('./drops/images')
    ],
    check_interval=10,  # Check every 10 seconds
    copy_files=True,  # Copy files to Needs_Action/files
    allowed_extensions=None,  # All files
    blocked_extensions=['.tmp', '.part', '.crdownload']
)
```

### Advanced Configuration

**Only allow specific file types:**
```python
allowed_extensions=['.pdf', '.docx', '.xlsx', '.jpg', '.png']
```

**Custom priority logic:**
```python
def _get_priority(self, category: str) -> str:
    filename = item['metadata']['file_name'].lower()
    if 'urgent' in filename or 'invoice' in filename:
        return 'high'
    return 'medium'
```

## ACCEPTANCE CRITERIA

- Monitors specified directories for new files
- Copies files to Needs_Action/files directory
- Creates metadata files with complete file info
- Filters temporary and partial files
- Handles file write completion detection

## FOLLOW-UPS

- Add OCR support for scanned documents
- Implement duplicate file detection
- Add file content preview generation
- Support for watching network shares

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.
