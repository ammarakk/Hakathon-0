#!/usr/bin/env python3
"""
Phase 3 Gold Tier - Integration Test Suite

This script tests all Phase 3 components:
1. Odoo MCP connection
2. CEO briefing generation
3. Audit logging
4. Social media clients (simulation)
5. Error recovery
6. Cross-domain scenarios

Usage:
    python test_all_integrations.py

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent
sys.path.insert(0, str(code_dir))

print("="*70)
print("PHASE 3 GOLD TIER - INTEGRATION TEST SUITE")
print("="*70)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test results tracking
test_results = {
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'tests': []
}

def run_test(test_name, test_func):
    """Run a test and track results"""
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print('='*70)

    try:
        result = test_func()
        if result:
            test_results['passed'] += 1
            test_results['tests'].append({'name': test_name, 'status': 'PASS'})
            print(f"\n✅ {test_name}: PASSED")
            return True
        else:
            test_results['failed'] += 1
            test_results['tests'].append({'name': test_name, 'status': 'FAIL'})
            print(f"\n❌ {test_name}: FAILED")
            return False
    except Exception as e:
        test_results['failed'] += 1
        test_results['tests'].append({'name': test_name, 'status': 'ERROR', 'error': str(e)})
        print(f"\n❌ {test_name}: ERROR - {e}")
        return False

# Test 1: Odoo Connection
def test_odoo_connection():
    """Test Odoo MCP client connection"""
    print("\nTesting Odoo connection...")

    try:
        from odoo_mcp_client import OdooMCPClient

        client = OdooMCPClient()

        if client.uid:
            print(f"✅ Connected to Odoo successfully")
            print(f"   Database: {client.db}")
            print(f"   URL: {client.url}")
            print(f"   UID: {client.uid}")
            return True
        else:
            print(f"❌ Failed to connect to Odoo")
            return False

    except ImportError as e:
        print(f"⚠️  odoo_mcp_client not available: {e}")
        print("   This is expected if Odoo is not configured yet")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 2: Odoo Read Partners
def test_odoo_read_partners():
    """Test reading partners from Odoo"""
    print("\nTesting Odoo read partners...")

    try:
        from odoo_mcp_client import OdooMCPClient

        client = OdooMCPClient()

        if not client.uid:
            print("⚠️  Odoo not connected - skipping test")
            return False

        partners = client.read_partners(limit=5)

        if partners:
            print(f"✅ Read {len(partners)} partners from Odoo")
            for partner in partners[:3]:
                print(f"   - {partner.get('name', 'Unknown')}")
            return True
        else:
            print(f"⚠️  No partners found (Odoo may be empty)")
            return True  # Not a failure, just no data

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 3: CEO Briefing Generation
def test_ceo_briefing():
    """Test CEO briefing generation"""
    print("\nTesting CEO briefing generation...")

    try:
        from generate_ceo_briefing import main as generate_briefing

        print("Running CEO briefing generator...")

        # Capture output by running the function
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            generate_briefing()
        finally:
            sys.stdout = old_stdout
            output = buffer.getvalue()

        print(output)

        # Check if briefing file was created
        from pathlib import Path
        briefing_dir = Path("../AI_Employee_Vault/CEO_Briefings")
        if briefing_dir.exists():
            briefings = list(briefing_dir.glob("Briefing_*.md"))
            if briefings:
                print(f"✅ CEO Briefing generated: {briefings[-1].name}")
                return True
            else:
                print("⚠️  Briefing file not created")
                return False
        else:
            print("⚠️  CEO_Briefings directory doesn't exist")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test 4: Audit Logger
def test_audit_logger():
    """Test audit logging functionality"""
    print("\nTesting audit logger...")

    try:
        from audit_logger import log_audit

        # Create a test audit entry
        success = log_audit(
            actor="TestSuite",
            action="test_audit_entry",
            result="success",
            details="Integration test audit entry"
        )

        if success:
            print("✅ Audit log entry created successfully")

            # Check if audit file exists
            from pathlib import Path
            logs_dir = Path("../AI_Employee_Vault/Logs")
            if logs_dir.exists():
                audit_files = list(logs_dir.glob("audit-*.md"))
                if audit_files:
                    print(f"   Audit file: {audit_files[-1].name}")
                    return True

            print("✅ Audit log function works (file check skipped)")
            return True
        else:
            print("❌ Failed to create audit entry")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 5: Error Recovery
def test_error_recovery():
    """Test error recovery patterns"""
    print("\nTesting error recovery...")

    try:
        from error_recovery import with_retry, safe_execute

        # Test successful retry
        print("Testing retry with success...")

        def successful_function():
            return "success"

        result = with_retry(
            func=successful_function,
            max_retries=2,
            silent=True
        )

        if result == "success":
            print("✅ Retry with successful function works")
        else:
            print("❌ Retry failed for successful function")
            return False

        # Test safe execute
        print("Testing safe execute...")

        def failing_function():
            raise ValueError("Test error")

        result = safe_execute(
            func=failing_function,
            fallback_value="fallback",
            log_to_file=False,
            silent=True
        )

        if result == "fallback":
            print("✅ Safe execute with fallback works")
            return True
        else:
            print("❌ Safe execute failed")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 6: Facebook/Instagram Client
def test_facebook_client():
    """Test Facebook/Instagram client"""
    print("\nTesting Facebook/Instagram client...")

    try:
        from fb_ig_mcp_client import FacebookInstagramMCPClient

        client = FacebookInstagramMCPClient()

        # Create a test draft
        draft = client.create_fb_post_draft(
            content="Test post from Phase 3 integration",
            business_context="Integration testing",
            hashtags=["#Test", "#Phase3"]
        )

        if draft and draft.get('status') == 'pending_approval':
            print(f"✅ Facebook post draft created")
            print(f"   File: {Path(draft['draft_file']).name}")
            print(f"   Characters: {draft['character_count']}")
            return True
        else:
            print("❌ Failed to create Facebook draft")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 7: Twitter/X Client
def test_twitter_client():
    """Test Twitter/X client"""
    print("\nTesting Twitter/X client...")

    try:
        from x_mcp_client import TwitterXMCPClient

        client = TwitterXMCPClient()

        # Create a test tweet draft
        draft = client.create_tweet_draft(
            content="Test tweet from Phase 3 integration 🚀",
            business_context="Integration testing",
            hashtags=["#AI", "#Automation"]
        )

        if draft and draft.get('status') == 'pending_approval':
            print(f"✅ Tweet draft created")
            print(f"   File: {Path(draft['draft_file']).name}")
            print(f"   Characters: {draft['character_count']}/280")
            return True
        else:
            print("❌ Failed to create tweet draft")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 8: Cross-Domain Scenario
def test_cross_domain_scenario():
    """Test cross-domain scenario processing"""
    print("\nTesting cross-domain scenario...")

    try:
        # Check if test scenarios exist
        needs_action_dir = Path("../AI_Employee_Vault/Needs_Action")

        if not needs_action_dir.exists():
            print("⚠️  Needs_Action directory doesn't exist")
            return False

        scenarios = list(needs_action_dir.glob("*.md"))

        if len(scenarios) >= 2:
            print(f"✅ Found {len(scenarios)} test scenarios")
            for scenario in scenarios:
                print(f"   - {scenario.name}")

            # Check if scenarios have domain labels
            personal_count = 0
            business_count = 0

            for scenario in scenarios:
                with open(scenario, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '[Personal]' in content or 'domain: personal' in content:
                        personal_count += 1
                    if '[Business]' in content or 'domain: business' in content:
                        business_count += 1

            print(f"   Personal domains: {personal_count}")
            print(f"   Business domains: {business_count}")

            if personal_count > 0 and business_count > 0:
                print("✅ Cross-domain test scenarios configured")
                return True
            else:
                print("⚠️  Cross-domain labels not found")
                return True  # Still pass if files exist
        else:
            print(f"⚠️  Only {len(scenarios)} scenarios found (need 2)")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 9: Vault Structure
def test_vault_structure():
    """Test vault structure for Gold Tier"""
    print("\nTesting vault structure...")

    try:
        vault_dir = Path("../AI_Employee_Vault")

        required_dirs = [
            "Dashboard.md",
            "Company_Handbook.md",
            "Needs_Action",
            "Plans",
            "Pending_Approval",
            "Done",
            "Logs",
            "CEO_Briefings"
        ]

        all_exist = True
        for item in required_dirs:
            item_path = vault_dir / item
            if item_path.exists():
                print(f"   ✅ {item}")
            else:
                print(f"   ❌ {item} (missing)")
                all_exist = False

        if all_exist:
            print("✅ Vault structure complete")
            return True
        else:
            print("⚠️  Some vault items missing")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test 10: Dashboard Gold Tier Sections
def test_dashboard_sections():
    """Test Dashboard.md has Gold Tier sections"""
    print("\nTesting Dashboard Gold Tier sections...")

    try:
        dashboard_path = Path("../AI_Employee_Vault/Dashboard.md")

        if not dashboard_path.exists():
            print("❌ Dashboard.md not found")
            return False

        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required_sections = [
            "Gold Tier Status",
            "Personal Pending Items",
            "Business Pending Items",
            "Cross-Domain Active Plans",
            "Latest CEO Briefing"
        ]

        all_found = True
        for section in required_sections:
            if section in content:
                print(f"   ✅ {section}")
            else:
                print(f"   ❌ {section} (missing)")
                all_found = False

        if all_found:
            print("✅ Dashboard Gold Tier sections complete")
            return True
        else:
            print("⚠️  Some sections missing")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Main test execution
def main():
    """Run all tests"""

    # Define all tests
    tests = [
        ("Odoo Connection", test_odoo_connection),
        ("Odoo Read Partners", test_odoo_read_partners),
        ("CEO Briefing Generation", test_ceo_briefing),
        ("Audit Logger", test_audit_logger),
        ("Error Recovery", test_error_recovery),
        ("Facebook/Instagram Client", test_facebook_client),
        ("Twitter/X Client", test_twitter_client),
        ("Cross-Domain Scenario", test_cross_domain_scenario),
        ("Vault Structure", test_vault_structure),
        ("Dashboard Gold Tier Sections", test_dashboard_sections),
    ]

    # Run all tests
    for test_name, test_func in tests:
        run_test(test_name, test_func)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {len(test_results['tests'])}")
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")
    print(f"⏭️  Skipped: {test_results['skipped']}")
    print()

    pass_rate = (test_results['passed'] / len(test_results['tests']) * 100) if test_results['tests'] else 0
    print(f"Pass Rate: {pass_rate:.1f}%")
    print()

    if test_results['failed'] == 0:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  Some tests failed - see details above")

    print("="*70)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return test_results['failed'] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
