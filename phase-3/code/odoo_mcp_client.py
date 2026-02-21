#!/usr/bin/env python3
"""
Odoo MCP Client - JSON-RPC Integration for Phase 3 Gold Tier

This module provides a Python client for interacting with Odoo Community Edition
via JSON-RPC API. It implements the draft -> approve -> post workflow required
for Gold Tier autonomous employee integration.

Functions:
- read_partners(): Read customer/partner records
- create_draft_invoice(): Create draft invoice (no approval needed)
- post_invoice(): Post draft invoice (requires prior approval)
- read_revenue(): Read revenue summary for CEO Briefing

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
Odoo Version: 19+ Community Edition
Database: hakathon-00
"""

import json
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime, date
import os
from dotenv import load_dotenv

# Load environment variables from credentials file
load_dotenv(os.path.join(os.path.dirname(__file__), '../secrets/.odoo_credentials'))


class OdooMCPClient:
    """
    Odoo JSON-RPC Client for MCP Integration

    This client connects to local Odoo Community Edition instance and provides
    methods for reading partners, creating draft invoices, posting invoices,
    and reading revenue data.
    """

    def __init__(self):
        """Initialize Odoo connection from environment variables"""
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'hakathon-00')
        self.username = os.getenv('ODOO_USER', 'admin')
        self.password = os.getenv('ODOO_PASSWORD', '')

        # JSON-RPC endpoints
        self.jsonrpc_url = f"{self.url}/jsonrpc"
        self.uid = None
        self._authenticate()

    def _authenticate(self) -> bool:
        """
        Authenticate with Odoo and store user ID

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "common",
                    "method": "login",
                    "args": [self.db, self.username, self.password]
                },
                "id": 1
            }

            response = requests.post(self.jsonrpc_url, json=payload)
            result = response.json()

            if 'result' in result and result['result']:
                self.uid = result['result']
                print(f"[OK] Authenticated to Odoo: {self.url} (DB: {self.db}, UID: {self.uid})")
                return True
            else:
                print(f"[ERROR] Odoo authentication failed: {result.get('error', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"[ERROR] Error connecting to Odoo: {str(e)}")
            return False

    def _execute_kw(self, model: str, method: str, domain: List = None,
                    fields: List = None, limit: int = None, **kwargs) -> Optional[Any]:
        """
        Execute Odoo model method

        Args:
            model: Odoo model name (e.g., 'res.partner', 'account.move')
            method: Method name (e.g., 'search_read', 'create')
            domain: Search domain (filters)
            fields: List of fields to retrieve
            limit: Maximum number of records
            **kwargs: Additional arguments

        Returns:
            Result from Odoo or None if error
        """
        if not self.uid:
            print("[ERROR] Not authenticated to Odoo")
            return None

        try:
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
                    ],
                    "kwargs": kwargs
                },
                "id": 2
            }

            # Add domain and fields if provided
            if domain is not None:
                payload['params']['args'].append(domain)
            if fields is not None:
                payload['params']['args'].append(fields)
            if limit is not None:
                payload['params']['args'].append(limit)

            response = requests.post(self.jsonrpc_url, json=payload)
            result = response.json()

            if 'error' in result:
                print(f"[ERROR] Odoo error: {result['error']}")
                return None

            return result.get('result')

        except Exception as e:
            print(f"[ERROR] Error executing Odoo method: {str(e)}")
            return None

    def read_partners(self, filters: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """
        Read customer/partner records from Odoo

        Args:
            filters: Optional filter dictionary (e.g., {'customer_rank': '>'})
            limit: Maximum number of partners to return (default: 100)

        Returns:
            List of partner dictionaries with name, email, phone
        """
        print(f"📖 Reading partners from Odoo (limit: {limit})...")

        # Build search domain for customers
        domain = [['customer_rank', '>', 0]]  # Only customers
        if filters:
            for key, value in filters.items():
                domain.append([key, '=', value])

        fields = ['name', 'email', 'phone', 'street', 'city', 'country_id']

        result = self._execute_kw(
            model='res.partner',
            method='search_read',
            domain=domain,
            fields=fields,
            limit=limit
        )

        if result is not None:
            print(f"[OK] Found {len(result)} partners")
            return result
        else:
            print(f"[ERROR] Failed to read partners")
            return []

    def create_draft_invoice(self, customer_id: int, line_items: List[Dict],
                           due_date: str, invoice_date: Optional[str] = None) -> Optional[Dict]:
        """
        Create draft invoice in Odoo

        Args:
            customer_id: Odoo partner ID
            line_items: List of line item dictionaries:
                [
                    {'product_id': 123, 'quantity': 10, 'price_unit': 100.0},
                    {'product_id': 124, 'quantity': 5, 'price_unit': 150.0}
                ]
            due_date: Due date in YYYY-MM-DD format
            invoice_date: Invoice date in YYYY-MM-DD format (default: today)

        Returns:
            Dictionary with invoice_id, status, total_amount, customer_name
        """
        print(f"[NOTE] Creating draft invoice for customer {customer_id}...")

        # Default to today if no invoice date provided
        if invoice_date is None:
            invoice_date = date.today().isoformat()

        # Build invoice lines
        invoice_lines = []
        for item in line_items:
            invoice_lines.append((0, 0, {
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'price_unit': item['price_unit'],
                'account_id': self._get_revenue_account_id(),
            }))

        # Create invoice
        invoice_data = {
            'move_type': 'out_invoice',  # Customer invoice
            'partner_id': customer_id,
            'invoice_date': invoice_date,
            'invoice_payment_term_id': self._get_payment_term_id(),
            'invoice_line_ids': invoice_lines,
        }

        result = self._execute_kw(
            model='account.move',
            method='create',
            **{'vals': invoice_data}
        )

        if result:
            print(f"[OK] Draft invoice created: ID {result}")

            # Calculate total
            total_amount = sum(item['quantity'] * item['price_unit'] for item in line_items)

            # Get customer name
            customer = self._execute_kw(
                model='res.partner',
                method='read',
                domain=[[customer_id]],
                fields=['name']
            )
            customer_name = customer[0]['name'] if customer else f"ID {customer_id}"

            return {
                'invoice_id': result,
                'status': 'draft',
                'total_amount': total_amount,
                'customer_name': customer_name,
                'invoice_date': invoice_date,
                'due_date': due_date
            }
        else:
            print(f"[ERROR] Failed to create draft invoice")
            return None

    def post_invoice(self, invoice_id: int) -> Optional[Dict]:
        """
        Post draft invoice to Odoo (requires prior approval)

        WARNING: This action posts the invoice to Odoo and makes it official.
        MUST have human approval before calling this method.

        Args:
            invoice_id: Odoo invoice ID

        Returns:
            Dictionary with invoice_id, status, posted_at, invoice_number
        """
        print(f"[WARNING]  Posting invoice {invoice_id} to Odoo...")

        # Verify invoice is in draft status
        invoice = self._execute_kw(
            model='account.move',
            method='read',
            domain=[[invoice_id]],
            fields=['state', 'move_type']
        )

        if not invoice:
            print(f"[ERROR] Invoice {invoice_id} not found")
            return None

        if invoice[0]['state'] != 'draft':
            print(f"[ERROR] Invoice {invoice_id} is not in draft status (current: {invoice[0]['state']})")
            return None

        # Post the invoice
        result = self._execute_kw(
            model='account.move',
            method='action_post',
            **{'ids': [invoice_id]}
        )

        if result is not None:
            posted_time = datetime.now().isoformat()

            # Get invoice number
            updated_invoice = self._execute_kw(
                model='account.move',
                method='read',
                domain=[[invoice_id]],
                fields=['name']
            )
            invoice_number = updated_invoice[0]['name'] if updated_invoice else f"INV-{invoice_id}"

            print(f"[OK] Invoice {invoice_id} posted successfully: {invoice_number}")

            return {
                'invoice_id': invoice_id,
                'status': 'posted',
                'posted_at': posted_time,
                'invoice_number': invoice_number
            }
        else:
            print(f"[ERROR] Failed to post invoice {invoice_id}")
            return None

    def read_revenue(self, month: int, year: int) -> Optional[Dict]:
        """
        Read revenue summary for CEO Briefing

        Args:
            month: Month (1-12)
            year: Year (e.g., 2026)

        Returns:
            Dictionary with total_revenue, outstanding, paid, top_customers
        """
        print(f"[MONEY] Reading revenue for {year}-{month:02d}...")

        # Search for invoices in the specified month
        domain = [
            ['move_type', '=', 'out_invoice'],
            ['invoice_date', '>=', f'{year}-{month:02d}-01'],
            ['invoice_date', '<=', f'{year}-{month:02d}-31'],
        ]

        fields = ['name', 'partner_id', 'amount_total', 'state', 'payment_state']

        invoices = self._execute_kw(
            model='account.move',
            method='search_read',
            domain=domain,
            fields=fields
        )

        if invoices is None:
            print(f"[ERROR] Failed to read revenue data")
            return None

        # Calculate revenue statistics
        total_revenue = sum(inv['amount_total'] for inv in invoices)
        outstanding = sum(inv['amount_total'] for inv in invoices if inv['payment_state'] not in ['paid', 'reversed'])
        paid = sum(inv['amount_total'] for inv in invoices if inv['payment_state'] in ['paid', 'reversed'])

        # Get top customers by revenue
        customer_revenue = {}
        for inv in invoices:
            customer_name = inv.get('partner_id', [False, 'Unknown'])[1]
            if customer_name not in customer_revenue:
                customer_revenue[customer_name] = 0
            customer_revenue[customer_name] += inv['amount_total']

        top_customers = sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)[:5]

        print(f"[OK] Revenue data: ${total_revenue:,.2f} total, ${outstanding:,.2f} outstanding")

        return {
            'month': month,
            'year': year,
            'total_revenue': total_revenue,
            'outstanding': outstanding,
            'paid': paid,
            'invoice_count': len(invoices),
            'top_customers': [
                {'name': name, 'revenue': rev}
                for name, rev in top_customers
            ]
        }

    def _get_revenue_account_id(self) -> int:
        """Get default revenue account ID (implementation-specific)"""
        # This would typically query the chart of accounts
        # For now, return a placeholder
        return 1  # TODO: Implement actual account lookup

    def _get_payment_term_id(self) -> int:
        """Get default payment term ID (implementation-specific)"""
        # This would typically query payment terms
        # For now, return a placeholder
        return 1  # TODO: Implement actual payment term lookup


# Example usage and testing
if __name__ == "__main__":
    print("=== Odoo MCP Client Test ===\n")

    # Initialize client
    client = OdooMCPClient()

    if client.uid:
        # Test 1: Read partners
        print("\n--- Test 1: Reading Partners ---")
        partners = client.read_partners(limit=10)
        for partner in partners[:3]:
            print(f"  - {partner['name']} ({partner.get('email', 'no email')})")

        # Test 2: Read revenue (current month)
        print("\n--- Test 2: Reading Revenue ---")
        today = date.today()
        revenue = client.read_revenue(today.month, today.year)
        if revenue:
            print(f"  Total Revenue: ${revenue['total_revenue']:,.2f}")
            print(f"  Outstanding: ${revenue['outstanding']:,.2f}")
            print(f"  Paid: ${revenue['paid']:,.2f}")
            print(f"  Invoices: {revenue['invoice_count']}")
            print(f"  Top Customers:")
            for customer in revenue['top_customers']:
                print(f"    - {customer['name']}: ${customer['revenue']:,.2f}")

        # Test 3: Create draft invoice (if customer and product exist)
        # Uncomment to test:
        # print("\n--- Test 3: Creating Draft Invoice ---")
        # draft = client.create_draft_invoice(
        #     customer_id=1,  # Replace with actual customer ID
        #     line_items=[
        #         {'product_id': 1, 'quantity': 10, 'price_unit': 100.0}
        #     ],
        #     due_date='2026-03-23'
        # )
        # if draft:
        #     print(f"  Draft ID: {draft['invoice_id']}")
        #     print(f"  Total: ${draft['total_amount']:,.2f}")

        print("\n[OK] All tests completed")
