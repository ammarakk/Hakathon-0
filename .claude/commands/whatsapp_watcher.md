---
description: WhatsApp watcher using Playwright for monitoring unread messages with keywords.
---

# COMMAND: WhatsApp Watcher Implementation

## CONTEXT

The user needs to implement a WhatsApp watcher that:

- Monitors WhatsApp Web for unread messages
- Searches for messages with specific keywords
- Creates action files for important messages
- Uses Playwright for browser automation

**IMPORTANT:** This implementation respects WhatsApp's Terms of Service. It only reads messages and does not automate sending, bulk messaging, or any prohibited activities.

## YOUR ROLE

Act as a Python developer with expertise in:

- Playwright browser automation
- Async/await patterns
- Web scraping and element selection
- Session management and persistence

## OUTPUT STRUCTURE

Create a complete WhatsApp watcher implementation with:

1. **Playwright-based WhatsApp Web monitoring**
2. **Unread message detection** with keyword filtering
3. **Session persistence** for QR code bypass
4. **Action file creation** for important messages
5. **Setup instructions** and compliance notes

## Step 1: WhatsApp Watcher Implementation

```python
#!/usr/bin/env python3
"""
WhatsApp Watcher - Monitor WhatsApp Web for unread messages

This watcher uses Playwright to monitor WhatsApp Web for unread messages
containing specific keywords and creates action files in Needs_Action.

COMPLIANCE: This implementation only READS messages. It does NOT:
- Send automated messages
- Perform bulk messaging
- Violate WhatsApp Terms of Service
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from playwright.async_api import async_playwright, Browser, Page, BrowserContext

from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WhatsAppWatcher")


class WhatsAppWatcher(BaseWatcher):
    """
    Watcher for monitoring WhatsApp Web unread messages.

    Uses Playwright to interact with WhatsApp Web, detecting unread messages
    that match specified keywords and creating action files.
    """

    def __init__(
        self,
        vault_path: Path,
        session_path: Optional[Path] = None,
        check_interval: int = 60,
        keywords: Optional[List[str]] = None,
        headless: bool = True,
        timeout_ms: int = 30000
    ):
        """
        Initialize the WhatsApp watcher.

        Args:
            vault_path: Path to shared vault directory
            session_path: Path to store browser session data
            check_interval: Seconds between checks (default: 60)
            keywords: List of keywords to filter messages (default: ['urgent', 'important'])
            headless: Run browser in headless mode (default: True)
            timeout_ms: Page load timeout in milliseconds (default: 30000)
        """
        super().__init__(
            name="WhatsAppWatcher",
            vault_path=vault_path,
            check_interval=check_interval
        )
        self.session_path = session_path or Path.home() / '.whatsapp_session'
        self.keywords = keywords or ['urgent', 'important', 'asap', 'help', 'please']
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_authenticated = False

    async def _setup_browser(self):
        """Set up Playwright browser with session persistence."""
        self.playwright = await async_playwright().start()

        # Launch browser with persistence
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        # Create context with session storage
        self.context = await self.browser.new_context(
            storage_state=str(self.session_path) if self.session_path.exists() else None,
            viewport={'width': 1280, 'height': 800}
        )

        self.page = await self.context.new_page()
        self.page.set_default_timeout(self.timeout_ms)

    async def _authenticate(self) -> bool:
        """
        Authenticate with WhatsApp Web.

        Returns:
            True if authenticated, False otherwise
        """
        try:
            await self.page.goto('https://web.whatsapp.com', wait_until='networkidle')

            # Check if QR code is present (not authenticated)
            qr_present = await self.page.query_selector('canvas[aria-label="Scan this QR code to link a device!"]')

            if qr_present:
                logger.warning("QR code detected. Please scan with WhatsApp mobile app.")
                logger.warning("Waiting for authentication...")

                # Wait for QR to be scanned (up to 2 minutes)
                try:
                    await self.page.wait_for_selector('div[contenteditable="true"][data-tab="3"]', timeout=120000)
                    logger.info("Authentication successful!")

                    # Save session for next time
                    await self.context.storage_state(path=str(self.session_path))
                    self.is_authenticated = True
                    return True

                except Exception as e:
                    logger.error(f"Authentication timeout: {e}")
                    return False
            else:
                # Already authenticated
                logger.info("Already authenticated (session restored)")
                self.is_authenticated = True
                return True

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False

    async def check(self) -> List[Dict[str, Any]]:
        """
        Check for unread messages with keywords.

        Returns:
            List of message item dictionaries
        """
        if not self.page or not self.is_authenticated:
            return []

        try:
            # Refresh the page to get latest messages
            await self.page.reload(wait_until='networkidle')
            await asyncio.sleep(2)  # Wait for messages to load

            items = []

            # Get all unread messages (identified by unread badge)
            unread_chats = await self.page.query_selector_all('span[aria-label*="unread messages"], span[aria-label*="mensajes sin leer"]')

            for chat_element in unread_chats[:20]:  # Limit to 20 most recent
                try:
                    # Get parent chat element
                    chat = await chat_element.query_selector('xpath=../..')
                    if not chat:
                        continue

                    # Extract chat info
                    sender = await self._extract_text(chat, 'span[title]')
                    message_preview = await self._extract_text(chat, 'span[copyable]')

                    # Get timestamp
                    timestamp_elem = await chat.query_selector('span[data-testid="msg-meta"]')
                    timestamp = await timestamp_elem.inner_text() if timestamp_elem else datetime.now().strftime("%H:%M")

                    # Get unread count
                    unread_badge = await chat_element.inner_text()

                    # Click to open chat and get full message
                    await chat.click()
                    await asyncio.sleep(1)

                    # Get last message
                    last_message = await self._get_last_message()

                    message_id = f"whatsapp_{datetime.now().timestamp()}_{sender.replace(' ', '_')}"

                    items.append({
                        'id': message_id,
                        'timestamp': timestamp,
                        'source': 'WhatsApp',
                        'data': {
                            'sender': sender,
                            'preview': message_preview,
                            'unread_count': unread_badge,
                        },
                        'metadata': {
                            'full_message': last_message,
                        }
                    })

                except Exception as e:
                    logger.error(f"Error processing chat: {e}")
                    continue

            logger.info(f"Found {len(items)} unread messages")
            return items

        except Exception as e:
            logger.error(f"Error checking messages: {e}")
            return []

    async def _extract_text(self, element, selector: str) -> str:
        """Extract text from element using selector."""
        try:
            elem = await element.query_selector(selector)
            return await elem.inner_text() if elem else ''
        except:
            return ''

    async def _get_last_message(self) -> str:
        """Get the last message in the current chat."""
        try:
            # Wait for messages to load
            await self.page.wait_for_selector('div[data-testid="msg-container"]', timeout=5000)

            # Get last message container
            messages = await self.page.query_selector_all('div[data-testid="msg-container"]')
            if messages:
                last_msg = messages[-1]

                # Try to get text content
                text_elem = await last_msg.query_selector('span.selectable-text')
                if text_elem:
                    return await text_elem.inner_text()

            return ''
        except:
            return ''

    async def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a WhatsApp message and check for keywords.

        Args:
            item: Raw message item

        Returns:
            Processed item or None if no keywords found
        """
        sender = item['data']['sender']
        full_message = item['metadata']['full_message']
        preview = item['data']['preview']

        # Combine message text for keyword search
        message_text = f"{preview} {full_message}".lower()

        # Check for keywords
        matched_keywords = [kw for kw in self.keywords if kw.lower() in message_text]

        if not matched_keywords:
            logger.debug(f"No keywords found in message from {sender}")
            return None

        # Determine priority
        priority = 'high' if 'urgent' in matched_keywords else 'medium'

        return {
            'title': f"WhatsApp from {sender}",
            'content': full_message or preview,
            'action_type': 'whatsapp_response',
            'priority': priority,
            'metadata': {
                'source_id': item['id'],
                'sender': sender,
                'matched_keywords': matched_keywords,
                'timestamp': item['timestamp'],
            }
        }

    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create an action file in the Needs_Action directory.

        Args:
            item: Processed message item

        Returns:
            Path to created action file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_sender = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in item['metadata']['sender'])
        filename = f"{timestamp}_whatsapp_{safe_sender[:30]}.md"
        filepath = self.needs_action_dir / filename

        keywords_str = ", ".join(item['metadata']['matched_keywords'])

        content = f"""# {item['title']}

**Source:** WhatsApp
**From:** {item['metadata']['sender']}
**Time:** {item['metadata']['timestamp']}
**Priority:** {item['priority'].upper()}
**Matched Keywords:** {keywords_str}

## Message
{item['content']}

## Actions Required
- [ ] Review message
- [ ] Determine response needed
- [ ] Reply via WhatsApp (manually)

⚠️ **Important:** Responses must be sent manually through WhatsApp app or web.
Do not automate responses as this may violate WhatsApp Terms of Service.

---
*Created by WhatsAppWatcher at {datetime.now().isoformat()}*
"""

        filepath.write_text(content, encoding='utf-8')
        return filepath

    async def cleanup(self):
        """Cleanup browser resources."""
        try:
            if self.context:
                # Save session state before closing
                await self.context.storage_state(path=str(self.session_path))
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

        await super().cleanup()


async def main():
    """Main entry point for running the WhatsApp watcher."""
    import os

    vault_path = Path(os.getenv("VAULT_PATH", "./vault"))
    session_path = Path(os.getenv("WHATSAPP_SESSION", "./whatsapp_session.json"))

    watcher = WhatsAppWatcher(
        vault_path=vault_path,
        session_path=session_path,
        check_interval=60,
        keywords=['urgent', 'important', 'asap', 'help', 'invoice', 'payment'],
        headless=True  # Set to False for first run to scan QR code
    )

    await watcher.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Setup Instructions

### Prerequisites

1. **Install Dependencies**
```bash
pip install playwright
playwright install chromium
```

2. **First-Time Setup**

For first run, set `headless=False` to scan QR code:
```bash
export VAULT_PATH=/path/to/vault
export WHATSAPP_SESSION=./whatsapp_session.json

# Run with visible browser for QR scan
python whatsapp_watcher.py  # Edit: headless=False in script first
```

3. **Scan QR Code**
   - Open WhatsApp on your mobile device
   - Go to Settings > Linked Devices
   - Tap "Link a Device"
   - Scan the QR code in the browser window

4. **Subsequent Runs**
After successful authentication, the session is saved. Set `headless=True`:
```bash
python whatsapp_watcher.py
```

### Configuration Options

```python
watcher = WhatsAppWatcher(
    vault_path=vault_path,
    session_path=session_path,
    check_interval=120,  # Check every 2 minutes
    keywords=['urgent', 'important', 'invoice', 'payment', 'client'],
    headless=True,
    timeout_ms=30000
)
```

## Compliance with WhatsApp Terms of Service

✅ **ALLOWED by this implementation:**
- Reading messages (manual monitoring)
- Personal account use
- Creating action files for manual review
- Session-based authentication

❌ **NOT ALLOWED (this implementation does NOT do):**
- Sending automated messages
- Bulk messaging or spam
- Creating multiple fake accounts
- Using unofficial APIs
- Scraping at scale

⚠️ **IMPORTANT:** Use this watcher for legitimate business purposes only. Misuse may result in account suspension.

## ACCEPTANCE CRITERIA

- Successfully authenticates with WhatsApp Web
- Detects unread messages with keywords
- Creates action files with complete metadata
- Persists session for re-authentication
- Handles network errors gracefully

## FOLLOW-UPS

- Add support for media message detection
- Implement message archiving after processing
- Add support for multiple WhatsApp accounts
- Create WhatsApp-specific response templates

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.
