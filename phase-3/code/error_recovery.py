#!/usr/bin/env python3
"""
Error Recovery and Graceful Degradation - Phase 3 Gold Tier

This module provides error handling patterns for watchers, MCP calls,
and Odoo integration. Implements exponential backoff retry logic.

Functions:
- with_retry(): Execute function with exponential backoff retry
- log_error(): Log error to vault error log
- safe_execute(): Execute function with error handling and logging

Usage:
    from error_recovery import with_retry, safe_execute

    result = with_retry(
        func=odoo_client.create_draft_invoice,
        max_retries=5,
        customer_id=1,
        line_items=[...]
    )

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
"""

import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Any, Dict
from functools import wraps

# Vault paths
VAULT_ROOT = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
LOGS_DIR = VAULT_ROOT / "Logs"
ERROR_LOG_FILE = LOGS_DIR / "errors.md"


# Configuration
MAX_RETRIES = 5
RETRY_DELAYS = [1, 2, 4, 8, 16]  # Exponential backoff: 1s, 2s, 4s, 8s, 16s


def with_retry(func: Callable,
               max_retries: int = MAX_RETRIES,
               retry_delays: list = None,
               silent: bool = False,
               **kwargs) -> Optional[Any]:
    """
    Execute function with exponential backoff retry logic

    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts (default: 5)
        retry_delays: List of delay seconds between retries (default: [1,2,4,8,16])
        silent: If True, don't log errors (default: False)
        **kwargs: Arguments to pass to func

    Returns:
        Result from func if successful, None if all retries failed

    Example:
        result = with_retry(
            func=odoo_client.create_draft_invoice,
            max_retries=3,
            customer_id=1,
            line_items=[...]
        )
    """
    if retry_delays is None:
        retry_delays = RETRY_DELAYS

    last_error = None

    for attempt in range(max_retries):
        try:
            result = func(**kwargs)
            if attempt > 0 and not silent:
                print(f"[OK] Success on retry {attempt + 1}/{max_retries}")
            return result

        except Exception as e:
            last_error = e
            current_delay = retry_delays[min(attempt, len(retry_delays) - 1)]

            if not silent:
                print(f"[WARNING]  Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"[RETRY] Retrying in {current_delay}s...")

            # Log error
            log_error(
                component=func.__name__,
                error_type=type(e).__name__,
                error_message=str(e),
                attempt=attempt + 1,
                stack_trace=traceback.format_exc() if not silent else None
            )

            # Wait before retry (unless this was the last attempt)
            if attempt < max_retries - 1:
                time.sleep(current_delay)

    # All retries failed
    if not silent:
        print(f"[ERROR] All {max_retries} attempts failed for {func.__name__}")
        log_error(
            component=func.__name__,
            error_type="MaxRetriesExceeded",
            error_message=f"Failed after {max_retries} attempts",
            final_error=str(last_error)
        )

    return None


def safe_execute(func: Callable,
                fallback_value: Any = None,
                log_to_file: bool = True,
                **kwargs) -> Any:
    """
    Execute function with error handling and logging

    If function fails, logs error and returns fallback_value instead of raising

    Args:
        func: Function to execute
        fallback_value: Value to return if function fails (default: None)
        log_to_file: If True, log errors to vault error log (default: True)
        **kwargs: Arguments to pass to func

    Returns:
        Result from func if successful, fallback_value if failed

    Example:
        result = safe_execute(
            func=odoo_client.read_partners,
            fallback_value=[],
            limit=100
        )
    """
    try:
        return func(**kwargs)

    except Exception as e:
        if log_to_file:
            log_error(
                component=func.__name__,
                error_type=type(e).__name__,
                error_message=str(e),
                stack_trace=traceback.format_exc()
            )

        print(f"[WARNING]  Error in {func.__name__}: {str(e)}")
        print(f"📦 Using fallback value: {fallback_value}")

        return fallback_value


def log_error(component: str,
              error_type: str,
              error_message: str,
              attempt: Optional[int] = None,
              stack_trace: Optional[str] = None,
              final_error: Optional[str] = None) -> bool:
    """
    Log error to vault error log

    Args:
        component: Component that encountered error
        error_type: Type of error
        error_message: Error message
        attempt: Attempt number if retrying
        stack_trace: Optional stack trace
        final_error: Final error if all retries failed

    Returns:
        bool: True if logged successfully
    """
    try:
        # Ensure Logs directory exists
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Create log entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log_entry = f"""## [{timestamp}] {component} - {error_type}

**Error Type**: {error_type}
**Error Message**: {error_message}
"""

        if attempt:
            log_entry += f"**Attempt**: {attempt}\n"

        if final_error:
            log_entry += f"**Final Error**: {final_error}\n"

        if stack_trace:
            log_entry += f"**Stack Trace**:\n```\n{stack_trace}\n```\n"

        log_entry += "**Resolved**: false\n\n---\n\n"

        # Append to error log file
        with open(ERROR_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        return True

    except Exception as e:
        print(f"[ERROR] Error writing to error log: {e}")
        return False


def retry_decorator(max_retries: int = MAX_RETRIES,
                   retry_delays: list = None,
                   silent: bool = False):
    """
    Decorator for adding retry logic to functions

    Usage:
        @retry_decorator(max_retries=3)
        def my_function():
            # Do something that might fail
            pass

    Args:
        max_retries: Maximum number of retry attempts
        retry_delays: List of delay seconds between retries
        silent: If True, don't log errors
    """
    if retry_delays is None:
        retry_delays = RETRY_DELAYS

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_error = e
                    current_delay = retry_delays[min(attempt, len(retry_delays) - 1)]

                    if not silent:
                        print(f"[WARNING]  {func.__name__} attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                        if attempt < max_retries - 1:
                            print(f"[RETRY] Retrying in {current_delay}s...")

                    # Log error
                    log_error(
                        component=func.__name__,
                        error_type=type(e).__name__,
                        error_message=str(e),
                        attempt=attempt + 1
                    )

                    # Wait before retry
                    if attempt < max_retries - 1:
                        time.sleep(current_delay)

            # All retries failed
            if not silent:
                print(f"[ERROR] {func.__name__} failed after {max_retries} attempts")
                log_error(
                    component=func.__name__,
                    error_type="MaxRetriesExceeded",
                    error_message=f"Failed after {max_retries} attempts",
                    final_error=str(last_error)
                )

            return None

        return wrapper
    return decorator


# Example usage and testing
if __name__ == "__main__":
    print("=== Error Recovery Test ===\n")

    # Test 1: Successful function
    print("Test 1: Successful function with retry...")
    def success_func():
        print("  [OK] Function succeeded")
        return "success"

    result = with_retry(func=success_func, max_retries=3)
    print(f"  Result: {result}\n")

    # Test 2: Failing function
    print("Test 2: Failing function with retry...")
    def failing_func():
        print("  [ERROR] Function failed")
        raise ValueError("Test error")

    result = with_retry(func=failing_func, max_retries=3, silent=True)
    print(f"  Result: {result}\n")

    # Test 3: Safe execute
    print("Test 3: Safe execute with fallback...")
    def safe_func():
        return "safe_result"

    result = safe_execute(func=safe_func, fallback_value="fallback")
    print(f"  Result: {result}\n")

    print("Test 4: Safe execute with error...")
    def unsafe_func():
        raise ValueError("Test error")

    result = safe_execute(func=unsafe_func, fallback_value="fallback", log_to_file=True)
    print(f"  Result: {result}\n")

    # Test 5: Decorator
    print("Test 5: Retry decorator...")
    @retry_decorator(max_retries=2, silent=True)
    def decorated_func():
        raise ValueError("Decorated function error")

    result = decorated_func()
    print(f"  Result: {result}\n")

    print("[OK] All error recovery tests completed")
    print(f"[FILE] Error log location: {ERROR_LOG_FILE}")
