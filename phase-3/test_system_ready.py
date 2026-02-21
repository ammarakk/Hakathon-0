#!/usr/bin/env python3
"""
Quick Test - Is Phase 3 System Ready to Run?
"""

import sys
import os
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path("phase-3/code")))

print("="*70)
print("PHASE 3 SYSTEM READINESS CHECK")
print("="*70)
print()

# Check 1: Credential files exist
print("1. Credential Files (.env):")
creds = [
    "phase-3/secrets/.odoo_credentials",
    "phase-3/secrets/.fb_credentials",
    "phase-3/secrets/.x_credentials"
]

for cred in creds:
    if Path(cred).exists():
        print(f"   [OK] {cred}")
    else:
        print(f"   [MISSING] {cred}")

print()

# Check 2: Code modules exist
print("2. Code Modules:")
code_dir = Path("phase-3/code")
modules = [
    "odoo_mcp_client.py",
    "generate_ceo_briefing.py",
    "audit_logger.py"
]

for mod in modules:
    mod_path = code_dir / mod
    if mod_path.exists():
        print(f"   [OK] {mod}")
    else:
        print(f"   [MISSING] {mod}")

print()

# Check 3: Can import modules
print("3. Can Import Modules:")
try:
    sys.path.insert(0, "phase-3/code")
    from odoo_mcp_client import OdooMCPClient
    print("   [OK] odoo_mcp_client imported")
except Exception as e:
    print(f"   [ERROR] odoo_mcp_client: {e}")

try:
    from generate_ceo_briefing import generate_ceo_briefing
    print("   [OK] generate_ceo_briefing imported")
except Exception as e:
    print(f"   [ERROR] generate_ceo_briefing: {e}")

try:
    from audit_logger import log_audit
    print("   [OK] audit_logger imported")
except Exception as e:
    print(f"   [ERROR] audit_logger: {e}")

print()

# Check 4: Vault structure
print("4. Vault Structure:")
vault_items = [
    "AI_Employee_Vault/Dashboard.md",
    "AI_Employee_Vault/Company_Handbook.md"
]

for item in vault_items:
    if Path(item).exists():
        print(f"   [OK] {item}")
    else:
        print(f"   [MISSING] {item}")

print()

# Check 5: Odoo accessibility
print("5. Odoo Accessibility:")
try:
    import requests
    response = requests.get("http://localhost:8069", timeout=3)
    if response.status_code in [200, 303]:
        print(f"   [OK] Odoo running (HTTP {response.status_code})")
    else:
        print(f"   [WARNING] Odoo responded with HTTP {response.status_code}")
except Exception as e:
    print(f"   [ERROR] Cannot reach Odoo: {e}")

print()
print("="*70)
print("READINESS STATUS:")
print()

# Summary
all_ok = True

# Count OKs
ok_count = 0
total_checks = 0

# Credential files
for cred in creds:
    total_checks += 1
    if Path(cred).exists():
        ok_count += 1

# Code modules
for mod in modules:
    total_checks += 1
    if (code_dir / mod).exists():
        ok_count += 1

# Vault files
for item in vault_items:
    total_checks += 1
    if Path(item).exists():
        ok_count += 1

print(f"Checks: {ok_count}/{total_checks} passed")

if ok_count == total_checks:
    print()
    print("✅ SYSTEM IS READY!")
    print()
    print("Next steps:")
    print("  1. Fill in credential files (if not done)")
    print("  2. Run: python phase-3/code/odoo_mcp_client.py")
    print("  3. Run: python phase-3/code/generate_ceo_briefing.py")
    print()
else:
    print()
    print("⚠️  System needs setup:")
    print("  1. Create missing files")
    print("  2. Install dependencies: pip install requests python-dotenv")
    print("  3. Configure credentials")
    print()

print("="*70)
