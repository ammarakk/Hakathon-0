#!/usr/bin/env python3
"""
Phase 3 Implementation Testing Script
Tests all remaining Phase 3 tasks automatically

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add code directory to path
CODE_DIR = Path(__file__).parent
sys.path.insert(0, str(CODE_DIR))

# Import all modules
try:
    import odoo_mcp_client
    import generate_ceo_briefing
    import audit_logger
    import error_recovery
    import fb_ig_mcp_client
    import x_mcp_client
    print("[OK] All modules imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import modules: {e}")
    sys.exit(1)


def test_cross_domain_integration():
    """
    T018-T024: Test cross-domain integration
    """
    print("\n" + "="*60)
    print("TEST: Cross-Domain Integration (T018-T024)")
    print("="*60)

    vault_root = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
    needs_action_dir = vault_root / "Needs_Action"

    # Check test scenarios exist
    test_files = [
        "whatsapp_call_mom.md",
        "gmail_project_completed.md"
    ]

    for test_file in test_files:
        test_path = needs_action_dir / test_file
        if test_path.exists():
            print(f"[OK] Test file exists: {test_file}")
        else:
            print(f"[WARNING] Test file missing: {test_file}")

    print("\n[NOTE] Manual verification required:")
    print("  1. Trigger Claude reasoning on both test items")
    print("  2. Verify unified Plan.md creation")
    print("  3. Check tasks labeled [Personal] and [Business]")
    print("  4. Verify business tasks prioritized first")


def test_odoo_mcp_connection():
    """
    T033: Test Odoo MCP connection
    """
    print("\n" + "="*60)
    print("TEST: Odoo MCP Connection (T033)")
    print("="*60)

    try:
        client = odoo_mcp_client.OdooMCPClient()
        print(f"[OK] Odoo client initialized")
        print(f"     URL: {client.url}")
        print(f"     DB: {client.db}")

        # Test connection by reading partners
        if client.uid:
            print("[OK] Odoo authenticated successfully")
            print("[NOTE] Manual test: create draft invoice via MCP")
            print("  Run: python -c \"from odoo_mcp_client import *; client = OdooMCPClient(); print(client.read_partners(limit=5))\"")
        else:
            print("[WARNING] Odoo not authenticated - check credentials")

    except Exception as e:
        print(f"[ERROR] Odoo connection failed: {e}")


def test_ceo_briefing_generation():
    """
    T065-T067: Test CEO briefing generation
    """
    print("\n" + "="*60)
    print("TEST: CEO Briefing Generation (T065-T067)")
    print("="*60)

    try:
        # Import and run
        from generate_ceo_briefing import main

        print("[RUNNING] Generating CEO Briefing...")
        main()

        # Check if briefing was created
        vault_root = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
        ceo_dir = vault_root / "CEO_Briefings"

        if ceo_dir.exists():
            briefings = list(ceo_dir.glob("Briefing_*.md"))
            if briefings:
                latest = max(briefings, key=lambda p: p.stat().st_mtime)
                print(f"[OK] CEO Briefing created: {latest.name}")
                print(f"     Location: {latest}")
            else:
                print("[WARNING] No briefing files found")
        else:
            print("[WARNING] CEO_Briefings directory not found")

    except Exception as e:
        print(f"[ERROR] CEO briefing generation failed: {e}")


def test_audit_logging():
    """
    T077-T079: Test audit logging
    """
    print("\n" + "="*60)
    print("TEST: Audit Logging (T077-T079)")
    print("="*60)

    try:
        # Generate sample audit entries
        from audit_logger import (
            log_watcher_trigger,
            log_action_item_created,
            log_plan_created,
            log_mcp_call,
            log_approval_requested
        )

        print("[GENERATING] Sample audit entries...")

        # Generate 10 different event types
        log_watcher_trigger("GmailWatcher", "gmail", 3)
        log_action_item_created("GmailWatcher", "Needs_Action/email_001.md", "gmail")
        log_plan_created("Plans/Plan_2026-02-21.md", 5, ["Personal", "Business"])
        log_mcp_call("mcp-odoo", "create_draft_invoice", "success", "Draft invoice ID: 123")
        log_approval_requested("post_invoice", "Pending_Approval/invoice_123.md")

        print("[OK] Generated 5 audit entries")

        # Check audit log file
        vault_root = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
        logs_dir = vault_root / "Logs"
        audit_file = logs_dir / f"audit-{datetime.now().strftime('%Y-%m-%d')}.md"

        if audit_file.exists():
            print(f"[OK] Audit log file exists: {audit_file.name}")

            # Count entries
            with open(audit_file, 'r', encoding='utf-8') as f:
                content = f.read()
                entry_count = content.count("## [")
                print(f"[OK] Found {entry_count} audit entries")
        else:
            print(f"[WARNING] Audit log not found: {audit_file}")

    except Exception as e:
        print(f"[ERROR] Audit logging test failed: {e}")


def test_social_media_clients():
    """
    T051-T057: Test social media clients
    """
    print("\n" + "="*60)
    print("TEST: Social Media Clients (T051-T057)")
    print("="*60)

    try:
        # Test Facebook/Instagram client
        fb_client = fb_ig_mcp_client.FacebookInstagramMCPClient()
        print("[OK] Facebook/Instagram client initialized")

        # Test Twitter/X client
        x_client = x_mcp_client.TwitterXMCPClient()
        print("[OK] Twitter/X client initialized")

        print("\n[NOTE] Manual verification required:")
        print("  1. Create business event test in /Needs_Action/")
        print("  2. Trigger Claude to generate social drafts")
        print("  3. Verify drafts for LinkedIn, FB, IG, X")
        print("  4. Test approval → post workflow")

    except Exception as e:
        print(f"[ERROR] Social media client test failed: {e}")


def test_error_recovery():
    """
    T044-T046: Test error recovery
    """
    print("\n" + "="*60)
    print("TEST: Error Recovery (T044-T046)")
    print("="*60)

    try:
        # Test retry logic
        from error_recovery import with_retry

        # Test 1: Successful function
        def success_func():
            return "success"

        result = with_retry(func=success_func, max_retries=3, silent=True)
        if result == "success":
            print("[OK] Retry with successful function works")

        # Test 2: Failing function
        def failing_func():
            raise ValueError("Test error")

        result = with_retry(func=failing_func, max_retries=3, silent=True)
        if result is None:
            print("[OK] Retry handles failures gracefully")

        print("\n[NOTE] Manual verification required:")
        print("  1. Stop Odoo service")
        print("  2. Trigger invoice creation")
        print("  3. Verify error logged to /Logs/errors.md")
        print("  4. Verify other components continue")
        print("  5. Restart Odoo, verify recovery")

    except Exception as e:
        print(f"[ERROR] Error recovery test failed: {e}")


def main():
    """Run all Phase 3 tests"""
    print("="*70)
    print(" PHASE 3 GOLD TIER - IMPLEMENTATION TESTING")
    print(" Automated Test Suite")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Code Directory: {CODE_DIR}")

    # Run all tests
    test_cross_domain_integration()
    test_odoo_mcp_connection()
    test_ceo_briefing_generation()
    test_audit_logging()
    test_social_media_clients()
    test_error_recovery()

    print("\n" + "="*70)
    print(" TEST SUITE COMPLETE")
    print("="*70)
    print("\n[SUMMARY]")
    print("  - Automated tests: COMPLETE")
    print("  - Manual tests: See notes above")
    print("  - Odoo GUI tasks: See ODOO_MANUAL_TASKS.md")
    print("\n[NEXT STEPS]")
    print("  1. Complete Odoo GUI tasks (T009-T012)")
    print("  2. Run manual verification tests")
    print("  3. Verify all deliverables complete")


if __name__ == "__main__":
    main()
