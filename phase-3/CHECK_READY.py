#!/usr/bin/env python3
"""
Simple check - Is everything ready?
"""

from pathlib import Path
import sys

print("="*70)
print("PHASE 3 READINESS CHECK")
print("="*70)
print()

all_ok = True

# 1. Credentials
print("1. Credentials:")
creds = ["phase-3/secrets/.odoo_credentials", "phase-3/secrets/.fb_credentials", "phase-3/secrets/.x_credentials"]
for cred in creds:
    exists = Path(cred).exists()
    status = "OK" if exists else "MISSING"
    print(f"   [{status}] {cred}")
    if not exists:
        all_ok = False

print()

# 2. Code modules
print("2. Code Modules:")
code_dir = Path("phase-3/code")
modules = ["odoo_mcp_client.py", "generate_ceo_briefing.py", "audit_logger.py"]
for mod in modules:
    exists = (code_dir / mod).exists()
    status = "OK" if exists else "MISSING"
    print(f"   [{status}] {mod}")
    if not exists:
        all_ok = False

print()

# 3. Code syntax check
print("3. Code Syntax:")
try:
    import ast
    for mod in modules:
        mod_path = code_dir / mod
        if mod_path.exists():
            with open(mod_path, 'r', encoding='utf-8') as f:
                try:
                    ast.parse(f.read())
                    print(f"   [OK] {mod} - Valid Python")
                except SyntaxError as e:
                    print(f"   [ERROR] {mod} - Line {e.lineno}: {e.msg}")
                    all_ok = False
except Exception as e:
    print(f"   [ERROR] {e}")
    all_ok = False

print()

# 4. Vault
print("4. Vault Structure:")
vault = ["AI_Employee_Vault/Dashboard.md", "AI_Employee_Vault/Company_Handbook.md"]
for item in vault:
    exists = Path(item).exists()
    status = "OK" if exists else "MISSING"
    print(f"   [{status}] {item}")
    if not exists:
        all_ok = False

print()

# 5. Odoo
print("5. Odoo:")
try:
    import requests
    response = requests.get("http://localhost:8069", timeout=3)
    if response.status_code == 200:
        print(f"   [OK] Odoo accessible (HTTP 200)")
    else:
        print(f"   [WARN] Odoo: HTTP {response.status_code}")
except:
    print(f"   [ERROR] Cannot reach Odoo")
    all_ok = False

print()
print("="*70)

if all_ok:
    print("STATUS: SYSTEM READY!")
    print()
    print("You can now:")
    print("  1. Fill .env files with actual credentials (if not done)")
    print("  2. Run: cd phase-3/code && python odoo_mcp_client.py")
    print("  3. Run: cd phase-3/code && python generate_ceo_briefing.py")
    print()
else:
    print("STATUS: NEEDS SETUP")
    print()
    print("Required:")
    print("  1. Fix syntax errors in code modules")
    print("  2. Install: pip install requests python-dotenv")
    print("  3. Configure credential files")
    print()

print("="*70)

sys.exit(0 if all_ok else 1)
