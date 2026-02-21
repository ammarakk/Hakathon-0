---
description: Error recovery and graceful degradation patterns for watchers and agents.
---

# COMMAND: Error Handling & Recovery

## CONTEXT

Implement robust error handling patterns for:

- Watcher failure recovery
- Retry logic with exponential backoff
- Graceful degradation
- Error logging and alerting

## YOUR ROLE

Act as a reliability engineer with expertise in:

- Error handling patterns
- Resilience engineering
- Monitoring and alerting
- Fault tolerance

## PATTERNS

### 1. Watcher Error Handler

```python
#!/usr/bin/env python3
"""
Error handling utilities for watchers and agents.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Any
import functools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("error_recovery")


class ErrorHandler:
    """Centralized error handling and logging."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.error_log = vault_path / "Logs" / "errors.md"
        self.error_log.parent.mkdir(parents=True, exist_ok=True)

    def log_error(self, component: str, error: Exception, context: dict = None):
        """Log error to file."""
        timestamp = datetime.now().isoformat()
        context_str = "\n".join(f"  {k}: {v}" for k, v in (context or {}).items())

        entry = f"""
## [{timestamp}] {component}

**Error Type:** {type(error).__name__}
**Message:** {str(error)}

{f'**Context:**\n{context_str}' if context else ''}

---
"""

        with open(self.error_log, 'a') as f:
            f.write(entry)

        logger.error(f"[{component}] {error}")

    def log_warning(self, component: str, message: str, context: dict = None):
        """Log warning to file."""
        timestamp = datetime.now().isoformat()

        entry = f"""
## [{timestamp}] {component} - WARNING

**Message:** {message}

---
"""

        with open(self.error_log, 'a') as f:
            f.write(entry)

        logger.warning(f"[{component}] {message}")


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential: bool = True
):
    """Decorator for retry with exponential backoff."""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = base_delay
            last_error = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay:.1f}s: {e}")
                        await asyncio.sleep(delay)
                        if exponential:
                            delay = min(delay * 2, max_delay)
                    else:
                        logger.error(f"All {max_retries} retries failed")

            raise last_error

        return wrapper
    return decorator


class CircuitBreaker:
    """Circuit breaker pattern for failing services."""

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        recovery_timeout: float = 30.0
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.recovery_timeout = recovery_timeout

        self.failures = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half_open

    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == "open":
            if asyncio.get_event_loop().time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half_open"
                logger.info("Circuit breaker entering half-open state")
            else:
                raise Exception("Circuit breaker is OPEN - service unavailable")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call."""
        self.failures = 0
        if self.state == "half_open":
            self.state = "closed"
            logger.info("Circuit breaker closed - service recovered")

    def _on_failure(self):
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = asyncio.get_event_loop().time()

        if self.failures >= self.failure_threshold:
            self.state = "open"
            logger.error(f"Circuit breaker OPEN after {self.failures} failures")


class GracefulWatcher:
    """Base watcher with graceful degradation."""

    def __init__(self, name: str, vault_path: Path, error_handler: ErrorHandler):
        self.name = name
        self.vault_path = vault_path
        self.error_handler = error_handler
        self.consecutive_errors = 0
        self.max_consecutive_errors = 10
        self.circuit_breaker = CircuitBreaker()

    async def run_safe(self, func: Callable, *args, **kwargs):
        """Run function with error handling."""
        try:
            result = await self.circuit_breaker.call(func, *args, **kwargs)
            self.consecutive_errors = 0
            return result

        except Exception as e:
            self.consecutive_errors += 1

            self.error_handler.log_error(
                component=self.name,
                error=e,
                context={'consecutive_errors': self.consecutive_errors}
            )

            if self.consecutive_errors >= self.max_consecutive_errors:
                self.error_handler.log_warning(
                    component=self.name,
                    message=f"Too many consecutive errors ({self.consecutive_errors}). Pausing.",
                )
                await asyncio.sleep(60)  # Pause for 1 minute

            return None

    def is_degraded(self) -> bool:
        """Check if watcher is in degraded state."""
        return self.circuit_breaker.state == "open"


# Example: Enhanced Gmail Watcher with Error Handling

class SafeGmailWatcher:
    """Gmail watcher with comprehensive error handling."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.error_handler = ErrorHandler(vault_path)
        self.graceful = GracefulWatcher("GmailWatcher", vault_path, self.error_handler)

    @retry_with_backoff(max_retries=3, base_delay=2.0)
    async def fetch_messages(self):
        """Fetch messages with retry."""
        # Simulated API call
        raise Exception("API timeout")

    async def run(self):
        """Run watcher with error handling."""
        while True:
            messages = await self.graceful.run_safe(self.fetch_messages)

            if messages is None and self.graceful.is_degraded():
                logger.warning("GmailWatcher degraded - using cached data")

            await asyncio.sleep(60)
```

## ACCEPTANCE CRITERIA

- Retry logic with exponential backoff
- Circuit breaker pattern
- Comprehensive error logging
- Graceful degradation on failure

## FOLLOW-UPS

- Add health check endpoints
- Implement alerting for critical errors
- Create error dashboard
- Add metrics collection
