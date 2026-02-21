---
description: Gmail watcher for monitoring unread important emails and creating action files.
---

# COMMAND: Gmail Watcher Implementation

## CONTEXT

The user needs to implement a Gmail watcher that:

- Monitors Gmail for unread important emails
- Creates action files in /Needs_Action directory
- Extracts email headers and content
- Integrates with Google Gmail API

## YOUR ROLE

Act as a Python developer with expertise in:

- Google APIs authentication and usage
- Email processing and MIME parsing
- Asynchronous programming
- File system operations

## OUTPUT STRUCTURE

Create a complete Gmail watcher implementation with:

1. **Gmail API Integration** with OAuth2 authentication
2. **Unread Email Detection** for important emails
3. **Action File Creation** with email metadata
4. **Error Handling** for API failures
5. **Setup Instructions** for Google credentials

## Step 1: Gmail Watcher Implementation

```python
#!/usr/bin/env python3
"""
Gmail Watcher - Monitor Gmail for unread important emails

This watcher connects to the Gmail API, monitors for unread emails,
and creates action files in the Needs_Action directory for important messages.
"""

import asyncio
import base64
import email
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from email.header import decode_header

import aiohttp
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GmailWatcher")

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher(BaseWatcher):
    """
    Watcher for monitoring Gmail unread important emails.

    Monitors the Gmail account for unread messages that are marked as important
    and creates action files in the Needs_Action directory.
    """

    def __init__(
        self,
        vault_path: Path,
        credentials_path: Optional[Path] = None,
        token_path: Optional[Path] = None,
        check_interval: int = 60,
        filters: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Gmail watcher.

        Args:
            vault_path: Path to shared vault directory
            credentials_path: Path to OAuth2 credentials JSON file
            token_path: Path to store/load OAuth2 token
            check_interval: Seconds between checks (default: 60)
            filters: Additional filters for email processing
        """
        super().__init__(
            name="GmailWatcher",
            vault_path=vault_path,
            check_interval=check_interval
        )
        self.credentials_path = credentials_path or Path.home() / '.gmail_credentials.json'
        self.token_path = token_path or Path.home() / '.gmail_token.json'
        self.filters = filters or {}
        self.service = None
        self.last_check_time = None

    async def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth2.

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            creds = None

            # Load existing token if available
            if self.token_path.exists():
                creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)

            # If there are no (valid) credentials, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not self.credentials_path.exists():
                        logger.error(f"Credentials file not found: {self.credentials_path}")
                        logger.error("Please download credentials from Google Cloud Console")
                        return False

                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_path), SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                # Save credentials for next run
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())

            # Build Gmail service
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API authentication successful")
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    async def check(self) -> List[Dict[str, Any]]:
        """
        Check for unread important emails.

        Returns:
            List of email item dictionaries
        """
        if not self.service:
            if not await self.authenticate():
                return []

        try:
            # Search for unread important emails
            query = 'is:unread is:important'
            results = self.service.users().messages().list(
                userId='me',
                q=query
            ).execute()

            messages = results.get('messages', [])
            logger.info(f"Found {len(messages)} unread important emails")

            items = []
            for msg in messages[:50]:  # Limit to 50 most recent
                try:
                    # Get full message details
                    msg_data = self.service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='full'
                    ).execute()

                    item = self._parse_message(msg_data)
                    if item:
                        items.append(item)

                except HttpError as e:
                    logger.error(f"Error fetching message {msg['id']}: {e}")

            return items

        except HttpError as e:
            logger.error(f"Gmail API error: {e}")
            return []

    def _parse_message(self, msg_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse Gmail message into standard item format.

        Args:
            msg_data: Raw Gmail message data

        Returns:
            Parsed item dictionary or None
        """
        try:
            msg_id = msg_data['id']
            payload = msg_data['payload']
            headers = {h['name']: h['value'] for h in payload.get('headers', [])}

            # Extract key headers
            subject = headers.get('Subject', '(No Subject)')
            from_email = headers.get('From', '')
            to_email = headers.get('To', '')
            date_str = headers.get('Date', '')

            # Parse email body
            body = self._extract_body(payload)

            return {
                'id': f"gmail_{msg_id}",
                'timestamp': date_str,
                'source': 'Gmail',
                'data': {
                    'message_id': msg_id,
                    'thread_id': msg_data.get('threadId', ''),
                    'snippet': msg_data.get('snippet', ''),
                },
                'metadata': {
                    'subject': subject,
                    'from': from_email,
                    'to': to_email,
                    'body': body,
                    'labels': msg_data.get('labelIds', []),
                }
            }

        except Exception as e:
            logger.error(f"Error parsing message {msg_data.get('id', 'unknown')}: {e}")
            return None

    def _extract_body(self, payload: Dict[str, Any]) -> str:
        """
        Extract email body from message payload.

        Args:
            payload: Gmail message payload

        Returns:
            Email body text
        """
        body = ''

        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        else:
            # Single part message
            if payload['mimeType'] == 'text/plain':
                data = payload['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

        return body[:10000]  # Limit body size

    async def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process an email item and extract relevant information.

        Args:
            item: Raw email item

        Returns:
            Processed item or None
        """
        metadata = item.get('metadata', {})

        # Apply filters
        subject = metadata.get('subject', '')
        from_email = metadata.get('from', '')

        # Check sender filter
        blocked_senders = self.filters.get('blocked_senders', [])
        if any(sender in from_email for sender in blocked_senders):
            logger.debug(f"Filtered email from blocked sender: {from_email}")
            return None

        # Check subject filter
        blocked_subjects = self.filters.get('blocked_subjects', [])
        if any(blocked.lower() in subject.lower() for blocked in blocked_subjects):
            logger.debug(f"Filtered email with blocked subject: {subject}")
            return None

        # Determine priority based on sender or keywords
        priority = self._determine_priority(subject, from_email)

        return {
            'title': subject,
            'content': metadata.get('body', ''),
            'action_type': 'email_response',
            'priority': priority,
            'metadata': {
                'source_id': item['id'],
                'from': from_email,
                'to': metadata.get('to', ''),
                'date': item['timestamp'],
                'snippet': item['data'].get('snippet', ''),
            }
        }

    def _determine_priority(self, subject: str, from_email: str) -> str:
        """
        Determine email priority based on content and sender.

        Args:
            subject: Email subject
            from_email: Sender email

        Returns:
            Priority level: high, medium, or low
        """
        # High priority keywords
        high_priority_keywords = ['urgent', 'asap', 'important', 'deadline']
        if any(kw in subject.lower() for kw in high_priority_keywords):
            return 'high'

        # High priority senders (customize as needed)
        high_priority_domains = ['@boss.com', '@client.com']
        if any(domain in from_email for domain in high_priority_domains):
            return 'high'

        return 'medium'

    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create an action file in the Needs_Action directory.

        Args:
            item: Processed email item

        Returns:
            Path to created action file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in item['title'])
        filename = f"{timestamp}_gmail_{safe_title[:50]}.md"
        filepath = self.needs_action_dir / filename

        content = f"""# {item['title']}

**Source:** Gmail
**From:** {item['metadata']['from']}
**To:** {item['metadata']['to']}
**Date:** {item['metadata']['date']}
**Priority:** {item['priority'].upper()}
**Source ID:** {item['metadata']['source_id']}

## Snippet
{item['metadata'].get('snippet', 'No preview available')}

## Full Content
{item['content']}

## Actions Required
- [ ] Review email
- [ ] Determine response needed
- [ ] Respond or archive

---
*Created by GmailWatcher at {datetime.now().isoformat()}*
"""

        filepath.write_text(content, encoding='utf-8')
        return filepath

    async def cleanup(self):
        """Cleanup Gmail service connection."""
        self.service = None
        await super().cleanup()


async def main():
    """Main entry point for running the Gmail watcher."""
    import os

    vault_path = Path(os.getenv("VAULT_PATH", "./vault"))
    credentials_path = Path(os.getenv("GMAIL_CREDENTIALS", "./credentials.json"))

    watcher = GmailWatcher(
        vault_path=vault_path,
        credentials_path=credentials_path
    )

    await watcher.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Setup Instructions

### Prerequisites

1. **Install Dependencies**
```bash
pip install google-api-python-client google-auth-oauthlib
```

2. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Gmail API:
     - Navigate to "APIs & Services" > "Library"
     - Search for "Gmail API" and enable it

3. **Create OAuth2 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop app"
   - Download the credentials JSON file

4. **Configure Environment**
```bash
# Set vault path
export VAULT_PATH=/path/to/vault

# Set credentials path
export GMAIL_CREDENTIALS=/path/to/credentials.json
```

### Running the Watcher

```bash
python gmail_watcher.py
```

First run will open a browser window for OAuth authentication. The token will be saved for subsequent runs.

### Configuration Options

Add filters in the watcher initialization:

```python
watcher = GmailWatcher(
    vault_path=vault_path,
    credentials_path=credentials_path,
    check_interval=120,  # Check every 2 minutes
    filters={
        'blocked_senders': ['noreply@', 'notifications@'],
        'blocked_subjects': ['[Newsletter]', '[Auto]'],
    }
)
```

## ACCEPTANCE CRITERIA

- Successfully authenticates with Gmail API
- Detects unread important emails
- Creates action files with complete metadata
- Handles API errors gracefully
- Supports custom filters

## FOLLOW-UPS

- Add support for label-based filtering
- Implement email marking as read after processing
- Add attachment handling
- Support multiple Gmail accounts

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.
