#!/usr/bin/env python3
"""
Odoo Auto-Setup Script - Phase 3 Gold Tier

Automatically completes Odoo setup tasks:
- T009: Enable modules
- T010: Create test customers
- T011: Create test products
- T012: Create draft invoices

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load credentials
load_dotenv(Path(__file__).parent.parent / "secrets" / ".odoo_credentials")

ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'hakathon-00')
ODOO_USER = os.getenv('ODOO_USER', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', '')


class OdooAutoSetup:
    """Automated Odoo setup via JSON-RPC"""

    def __init__(self):
        self.url = ODOO_URL
        self.db = ODOO_DB
        self.uid = None
        self.password = ODOO_PASSWORD

    def authenticate(self):
        """Authenticate with Odoo"""
        print("[AUTH] Connecting to Odoo...")

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "login",
                "args": [self.db, ODOO_USER, self.password]
            },
            "id": 1
        }

        try:
            response = requests.post(f"{self.url}/jsonrpc", json=payload)
            result = response.json()

            if 'result' in result and result['result']:
                self.uid = result['result']
                print(f"[OK] Authenticated successfully (UID: {self.uid})")
                return True
            else:
                print(f"[ERROR] Authentication failed: {result}")
                return False

        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return False

    def call_odoo(self, model, method, domain=None, fields=None, data=None):
        """Generic Odoo RPC call"""
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    model,
                    method,
                    domain or [],
                    fields or {}
                ]
            },
            "id": 1
        }

        if data:
            payload['params']['args'].append(data)

        response = requests.post(f"{self.url}/jsonrpc", json=payload)
        return response.json()

    def check_module_installed(self, module_name):
        """Check if module is installed"""
        result = self.call_odoo(
            'ir.module.module',
            'search',
            domain=[[['name', '=', module_name], ['state', '=', 'installed']]]
        )
        return len(result.get('result', [])) > 0

    def enable_module(self, module_name):
        """Enable Odoo module"""
        print(f"[MODULE] Checking {module_name}...")

        if self.check_module_installed(module_name):
            print(f"  [OK] {module_name} already installed")
            return True

        # Find module
        result = self.call_odoo(
            'ir.module.module',
            'search',
            domain=[[['name', '=', module_name]]]
        )

        module_ids = result.get('result', [])
        if not module_ids:
            print(f"  [WARNING] Module {module_name} not found")
            return False

        # Install module
        print(f"  [INSTALLING] {module_name}...")
        result = self.call_odoo(
            'ir.module.module',
            'button_immediate_install',
            data=[module_ids]
        )

        if 'error' in result:
            print(f"  [ERROR] Failed to install {module_name}: {result['error']}")
            return False

        print(f"  [OK] {module_name} installed successfully")
        return True

    def create_customer(self, name, email, phone, street, city):
        """Create a customer"""
        print(f"[CUSTOMER] Creating: {name}")

        result = self.call_odoo(
            'res.partner',
            'create',
            data={
                'name': name,
                'email': email,
                'phone': phone,
                'street': street,
                'city': city,
                'supplier_rank': 0,
                'customer_rank': 1
            }
        )

        if 'result' in result:
            customer_id = result['result']
            print(f"  [OK] Customer created (ID: {customer_id})")
            return customer_id
        else:
            print(f"  [ERROR] Failed to create customer: {result}")
            return None

    def create_product(self, name, code, price, description):
        """Create a product/service"""
        print(f"[PRODUCT] Creating: {name}")

        result = self.call_odoo(
            'product.template',
            'create',
            data={
                'name': name,
                'default_code': code,
                'list_price': price,
                'detailed_type': 'service',
                'description': description
            }
        )

        if 'result' in result:
            product_id = result['result']
            print(f"  [OK] Product created (ID: {product_id})")
            return product_id
        else:
            print(f"  [ERROR] Failed to create product: {result}")
            return None

    def create_draft_invoice(self, customer_id, line_items):
        """Create draft invoice"""
        print(f"[INVOICE] Creating draft invoice...")

        # Create invoice
        invoice_data = {
            'move_type': 'out_invoice',
            'partner_id': customer_id,
            'invoice_date': '2026-02-21',
            'state': 'draft'
        }

        result = self.call_odoo(
            'account.move',
            'create',
            data=invoice_data
        )

        if 'result' not in result:
            print(f"  [ERROR] Failed to create invoice: {result}")
            return None

        invoice_id = result['result']

        # Add line items
        for product_id, quantity, price in line_items:
            line_result = self.call_odoo(
                'account.move.line',
                'create',
                data={
                    'move_id': invoice_id,
                    'product_id': product_id,
                    'quantity': quantity,
                    'price_unit': price
                }
            )

        print(f"  [OK] Draft invoice created (ID: {invoice_id})")
        return invoice_id


def main():
    """Run all auto-setup tasks"""
    print("="*70)
    print(" ODOO AUTO-SETUP - Phase 3 Gold Tier")
    print(" Software Company Style: Fully Automated")
    print("="*70)
    print()

    setup = OdooAutoSetup()

    # Authenticate
    if not setup.authenticate():
        print("\n[FAILED] Cannot proceed without authentication")
        print("[ACTION] Check Odoo is running at http://localhost:8069")
        print("[ACTION] Verify credentials in phase-3/secrets/.odoo_credentials")
        return

    print()

    # T009: Enable modules
    print("-"*70)
    print("T009: Enabling Odoo Modules")
    print("-"*70)

    modules = ['account', 'contacts']
    for module in modules:
        setup.enable_module(module)
        print()

    # T010: Create test customers
    print("-"*70)
    print("T010: Creating Test Customers")
    print("-"*70)

    customers = [
        {
            'name': 'ABC Corp',
            'email': 'contact@abccorp.com',
            'phone': '+1-555-0101',
            'street': '123 Business St',
            'city': 'New York, NY 10001'
        },
        {
            'name': 'XYZ Ltd',
            'email': 'info@xyzltd.com',
            'phone': '+1-555-0102',
            'street': '456 Commerce Ave',
            'city': 'Los Angeles, CA 90001'
        },
        {
            'name': 'Startup Co',
            'email': 'hello@startupco.com',
            'phone': '+1-555-0103',
            'street': '789 Innovation Blvd',
            'city': 'San Francisco, CA 94101'
        }
    ]

    customer_ids = []
    for customer in customers:
        cust_id = setup.create_customer(**customer)
        if cust_id:
            customer_ids.append(cust_id)
    print()

    # T011: Create test products
    print("-"*70)
    print("T011: Creating Test Products/Services")
    print("-"*70)

    products = [
        {
            'name': 'Consulting Services',
            'code': 'CONS-001',
            'price': 100.0,
            'description': 'Professional consulting services'
        },
        {
            'name': 'Software Development',
            'code': 'DEV-001',
            'price': 150.0,
            'description': 'Custom software development'
        },
        {
            'name': 'Technical Support',
            'code': 'SUPP-001',
            'price': 75.0,
            'description': 'Ongoing technical support services'
        }
    ]

    product_ids = []
    for product in products:
        prod_id = setup.create_product(**product)
        if prod_id:
            # Get actual product.product id (not template)
            result = setup.call_odoo(
                'product.product',
                'search',
                domain=[[['product_tmpl_id', '=', prod_id]]]
            )
            if 'result' in result and result['result']:
                product_ids.append(result['result'][0])
    print()

    # T012: Create draft invoices
    print("-"*70)
    print("T012: Creating Draft Invoices")
    print("-"*70)

    if len(customer_ids) >= 2 and len(product_ids) >= 2:
        # Invoice 1: ABC Corp - Consulting
        invoice1 = setup.create_draft_invoice(
            customer_ids[0],
            [(product_ids[0], 10, 100.0)]
        )

        # Invoice 2: XYZ Ltd - Software Development
        invoice2 = setup.create_draft_invoice(
            customer_ids[1],
            [(product_ids[1], 20, 150.0)]
        )

        print()
        print("="*70)
        print(" SUMMARY")
        print("="*70)
        print(f"Customers Created: {len(customer_ids)}/3")
        print(f"Products Created: {len(product_ids)}/3")
        print(f"Draft Invoices: 2")
        print()
        print("[SUCCESS] Odoo auto-setup complete!")
        print("[NEXT] Verify at http://localhost:8069")
        print("="*70)

    else:
        print("[ERROR] Not enough customers or products created")
        print(f"  Customers: {len(customer_ids)}, Products: {len(product_ids)}")


if __name__ == "__main__":
    main()
