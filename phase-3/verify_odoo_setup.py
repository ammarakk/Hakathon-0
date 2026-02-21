#!/usr/bin/env python3
"""
Odoo Setup Verification Script

Run this after completing manual Odoo setup to verify everything is ready.
"""

import sys
from pathlib import Path

# Add code directory
code_dir = Path(__file__).parent / "phase-3" / "code"
sys.path.insert(0, str(code_dir))

try:
    from odoo_mcp_client import OdooMCPClient

    print("="*70)
    print(" ODOO SETUP VERIFICATION")
    print("="*70)
    print()

    client = OdooMCPClient()

    if client.uid:
        print("[OK] Odoo authenticated successfully")
        print()

        # Test read partners
        print("[TEST] Reading customers...")
        partners = client.read_partners(limit=10)
        if partners:
            print(f"[OK] Found {len(partners)} customers")
            for partner in partners[:3]:
                print(f"  - {partner.get('name', 'Unknown')}")
        else:
            print("[WARNING] No customers found")

        print()

        # Test read invoices
        print("[TEST] Reading draft invoices...")
        # This would need implementation in odoo_mcp_client.py
        print("[NOTE] Invoice reading requires additional implementation")

        print()
        print("="*70)
        print("VERIFICATION COMPLETE")
        print("="*70)
        print()
        print("[NEXT] Run full test suite:")
        print("  python phase-3/code/test_implementation.py")

    else:
        print("[ERROR] Odoo authentication failed")
        print("[ACTION] Check:")
        print("  1. Odoo is running at http://localhost:8069")
        print("  2. Database 'hakathon-00' exists")
        print("  3. Credentials in phase-3/secrets/.odoo_credentials")

except Exception as e:
    print(f"[ERROR] Verification failed: {e}")
