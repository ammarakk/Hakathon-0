---
description: Security enforcement rules for AI Employee system.
---

# COMMAND: Security Rules

## CONTEXT

Enforce security rules for:

- Never syncing secrets (.env, tokens, sessions)
- Local-only handling of sensitive actions
- Cloud draft-only modes
- Credential management

## YOUR ROLE

Act as a security engineer with expertise in:

- Secret management
- Access control
- Data protection
- Compliance requirements

## RULES

### 1. Never Sync Secrets

```bash
# .gitignore - ALWAYS include these patterns

# Environment files
.env
.env.local
.env.*.local

# Credentials
credentials/
*.credentials.json
*token.json
*_key.pem
*_cert.pem

# Sessions
.session/
*.session.json
.whatsapp_session/
*_session/

# API Keys
*api_key*
*secret*
*password*

# Database
*.db
*.sqlite
*.sqlite3

# Logs (may contain sensitive data)
*.log
/logs/
```

```python
# security_validator.py

from pathlib import Path
import re


class SecurityValidator:
    """Validate that no secrets are being synced."""

    SENSITIVE_PATTERNS = [
        r'\.env$',
        r'token',
        r'secret',
        r'password',
        r'api[_-]?key',
        r'credential',
        r'\.session',
        r'auth',
        r'private[_-]?key',
        r'\.pem$',
        r'\.key$',
    ]

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.violations_log = vault_path / "Logs" / "security_violations.md"

    def check_for_secrets(self, filepath: Path) -> bool:
        """Check if file might contain secrets."""
        filename_lower = filepath.name.lower()

        # Check filename patterns
        for pattern in self.SENSITIVE_PATTERNS:
            if re.search(pattern, filename_lower):
                return True

        # Check file content for secret-like patterns
        if self._has_secret_content(filepath):
            return True

        return False

    def _has_secret_content(self, filepath: Path) -> bool:
        """Check file content for secret patterns."""
        secret_indicators = [
            ('API_KEY', '='),  # API_KEY=xxx
            ('SECRET', '='),   # SECRET=xxx
            ('TOKEN', '='),    # TOKEN=xxx
            ('password', ':'), # password:xxx
            ('Bearer ',),      # Bearer token
        ]

        try:
            content = filepath.read_text()[:1000]  # Check first 1000 chars

            for indicator in secret_indicators:
                if all(s.lower() in content.lower() for s in indicator):
                    return True

        except Exception:
            pass

        return False

    def validate_sync(self, files_to_sync: list) -> tuple[bool, list]:
        """Validate that no secret files are being synced."""
        violations = []

        for file in files_to_sync:
            if self.check_for_secrets(file):
                violations.append(file)

        if violations:
            self._log_violation(violations)

        return len(violations) == 0, violations

    def _log_violation(self, violations: list):
        """Log security violations."""
        self.violations_log.parent.mkdir(parents=True, exist_ok=True)

        entry = f"""
## Security Violation - {datetime.now().isoformat()}

Attempted to sync files containing secrets:

{chr(10).join(f"- {v}" for v in violations)}

**Action:** BLOCKED

---
"""

        with open(self.violations_log, 'a') as f:
            f.write(entry)
```

### 2. Local-Only Sensitive Actions

```python
# local_actions.py

from enum import Enum


class ActionLocation(Enum):
    """Where actions should be executed."""
    LOCAL_ONLY = "local_only"
    CLOUD_ONLY = "cloud_only"
    EITHER = "either"


LOCAL_ONLY_ACTIONS = {
    'whatsapp_watcher': ActionLocation.LOCAL_ONLY,  # Session must stay local
    'payment_approval': ActionLocation.LOCAL_ONLY,  # Requires human confirmation
    'secret_management': ActionLocation.LOCAL_ONLY, # Secrets never leave local
    'database_backup': ActionLocation.LOCAL_ONLY,   # Sensitive data
}

CLOUD_ONLY_ACTIONS = {
    'gmail_watcher': ActionLocation.CLOUD_ONLY,
    'filesystem_watcher': ActionLocation.CLOUD_ONLY,
    'reasoning_loop': ActionLocation.CLOUD_ONLY,
}

DRAFT_ONLY_ACTIONS = {
    'social_media_post': ActionLocation.LOCAL_ONLY,  # Drafts local, approve then send
    'email_send': ActionLocation.LOCAL_ONLY,         # Drafts local, approve then send
}


def validate_action_location(action: str, current_location: str) -> bool:
    """Validate if action can run at current location."""
    required = LOCAL_ONLY_ACTIONS.get(action)
    if required == ActionLocation.LOCAL_ONLY and current_location != 'local':
        raise SecurityError(f"{action} must run locally")

    required = CLOUD_ONLY_ACTIONS.get(action)
    if required == ActionLocation.CLOUD_ONLY and current_location != 'cloud':
        raise SecurityError(f"{action} must run in cloud")

    return True


class SecurityError(Exception):
    """Raised when security rule is violated."""
    pass
```

### 3. Cloud Draft-Only Mode

```python
# cloud_draft_mode.py

from pathlib import Path
import json


class CloudDraftManager:
    """Manage cloud draft-only mode for sensitive actions."""

    def __init__(self, vault_path: Path, location: str = 'cloud'):
        self.vault_path = vault_path
        self.location = location
        self.pending_dir = vault_path / "Pending_Approval"

    def create_draft(self, action_type: str, content: dict) -> Path:
        """Create a draft for local approval."""
        if self.location != 'cloud':
            raise SecurityError("Draft creation only happens in cloud")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"draft_{timestamp}_{action_type}.md"
        filepath = self.pending_dir / filename

        draft_content = f"""# Draft: {action_type}

**Created:** {datetime.now().isoformat()}
**Status:** DRAFT - Requires Local Approval
**Created by:** cloud

## Content

```json
{json.dumps(content, indent=2)}
```

## Actions Required

⚠️ This action was created in the cloud and requires local approval.

To approve:
1. Review the content above
2. Change status from "DRAFT" to "APPROVED"
3. Add your name to "Approved by"
4. The action will execute on next sync

---
"""
        filepath.write_text(draft_content)
        return filepath

    def execute_approved_drafts(self):
        """Execute drafts that have been approved locally."""
        if self.location != 'local':
            raise SecurityError("Draft execution only happens locally")

        for draft_file in self.pending_dir.glob("draft_*.md"):
            content = draft_file.read_text()

            # Check if approved
            if "**Status:** APPROVED" in content:
                # Extract action details and execute
                self._execute_draft(draft_file, content)

    def _execute_draft(self, draft_file: Path, content: str):
        """Execute an approved draft."""
        # Parse action from content
        # Execute action
        # Move to Done

        draft_file.unlink()
```

### 4. Credential Management

```python
# credential_manager.py

import os
from pathlib import Path
import json
from cryptography.fernet import Fernet


class CredentialManager:
    """Manage credentials securely."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.credential_file = vault_path / ".credentials" / "encrypted.enc"
        self.key_file = vault_path / ".credentials" / "key.enc"

        # NEVER sync these files
        self._ensure_gitignore()

    def _ensure_gitignore(self):
        """Ensure credential files are in .gitignore."""
        gitignore = self.vault_path / ".gitignore"
        content = gitignore.read_text() if gitignore.exists() else ""

        required = ['.credentials/', '*.enc']

        for line in required:
            if line not in content:
                content += f"\n{line}\n"

        gitignore.write_text(content)

    def store_credential(self, service: str, credential: dict):
        """Store encrypted credential."""
        key = self._get_or_create_key()
        fernet = Fernet(key)

        # Encrypt credential
        encrypted = fernet.encrypt(json.dumps(credential).encode())

        # Store
        self.credential_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.credential_file, 'ab') as f:
            f.write(f"{service}:".encode() + encrypted + b"\n")

    def get_credential(self, service: str) -> dict:
        """Retrieve and decrypt credential."""
        key = self._get_or_create_key()
        fernet = Fernet(key)

        with open(self.credential_file, 'rb') as f:
            for line in f:
                if line.startswith(f"{service}:".encode()):
                    encrypted = line.split(b":", 1)[1].strip()
                    decrypted = fernet.decrypt(encrypted)
                    return json.loads(decrypted.decode())

        raise FileNotFoundError(f"Credential not found: {service}")

    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key."""
        if self.key_file.exists():
            return self.key_file.read_bytes()

        # Create new key
        key = Fernet.generate_key()
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        self.key_file.write_bytes(key)
        self.key_file.chmod(0o600)  # Owner read/write only

        return key
```

## ACCEPTANCE CRITERIA

- .gitignore prevents secret syncing
- Sensitive actions validated by location
- Cloud creates drafts, local executes
- Credentials encrypted at rest

## FOLLOW-UPS

- Add secret scanning in CI/CD
- Implement credential rotation
- Add audit logging for access
- Create security dashboard
