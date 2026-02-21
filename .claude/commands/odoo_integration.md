---
description: Odoo JSON-RPC MCP server for accounting integration with local approval workflow.
---

# COMMAND: Odoo Integration (MCP Server)

## CONTEXT

The user needs to create an MCP server for Odoo Community integration that:

- Connects via JSON-RPC to Odoo 19+
- Creates draft accounting actions
- Requires local approval before posting
- Integrates with the vault sync system

## YOUR ROLE

Act as a Python/Node.js developer with expertise in:

- Odoo JSON-RPC API
- Accounting workflow design
- MCP server implementation
- Approval pattern integration

## Step 1: Odoo MCP Server (Python)

```python
#!/usr/bin/env python3
"""
Odoo MCP Server - JSON-RPC integration for accounting

Provides MCP tools for creating accounting entries in Odoo
with local approval before posting.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict
import os
import requests
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("odoo_mcp")

# Odoo configuration
ODOO_URL = os.getenv("ODOO_URL", "http://localhost:8069")
ODOO_DB = os.getenv("ODOO_DB", "odoo")
ODOO_USER = os.getenv("ODOO_USER", "admin")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", "admin")


class OdooClient:
    """Odoo JSON-RPC client."""

    def __init__(self, url: str, db: str, user: str, password: str):
        self.url = url
        self.db = db
        self.user = user
        self.password = password
        self.uid = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Odoo."""
        endpoint = urljoin(self.url, "/jsonrpc")
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "login",
                "args": [self.db, self.user, self.password]
            },
            "id": 1
        }

        response = requests.post(endpoint, json=payload)
        result = response.json()

        if result.get("error"):
            raise Exception(f"Authentication failed: {result['error']}")

        self.uid = result["result"]
        logger.info(f"Authenticated as {self.user} (UID: {self.uid})")

    def call(self, model: str, method: str, args: list = None, kwargs: dict = None):
        """Call an Odoo model method."""
        endpoint = urljoin(self.url, "/jsonrpc")
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
                    args or [],
                    kwargs or {}
                ]
            },
            "id": 2
        }

        response = requests.post(endpoint, json=payload)
        result = response.json()

        if result.get("error"):
            raise Exception(f"Odoo error: {result['error']}")

        return result["result"]

    def search_read(self, model: str, domain: list = None, fields: list = None):
        """Search and read records."""
        return self.call(model, "search_read", args=[domain or []], kwargs={"fields": fields or []})

    def create(self, model: str, values: dict):
        """Create a new record."""
        return self.call(model, "create", args=[values])

    def write(self, model: str, record_id: int, values: dict):
        """Update a record."""
        return self.call(model, "write", args=[[record_id], values])

    def button_action(self, model: str, record_id: int, method: str):
        """Call a button/action method on a record."""
        return self.call(model, method, args=[[record_id]])


# Initialize Odoo client
odoo_client = None


def get_client():
    """Get or create Odoo client."""
    global odoo_client
    if odoo_client is None:
        odoo_client = OdooClient(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD)
    return odoo_client


# MCP Tools

def create_vendor_bill(description: str, amount: float, partner_id: int = None, account_id: int = None) -> dict:
    """
    Create a draft vendor bill in Odoo.

    Args:
        description: Bill description
        amount: Bill amount
        partner_id: Vendor partner ID (optional)
        account_id: Account ID for the line (optional)

    Returns:
        Dictionary with bill ID and status
    """
    client = get_client()

    # Get default account if not specified
    if account_id is None:
        accounts = client.search_read(
            "account.account",
            [["account_type", "=", "liability_payable"]],
            ["id", "name"]
        )
        if accounts:
            account_id = accounts[0]["id"]
        else:
            return {
                "success": False,
                "error": "No default payable account found"
            }

    # Create bill
    bill_values = {
        "move_type": "in_invoice",
        "state": "draft",  # Draft state, requires approval
        "date": datetime.now().strftime("%Y-%m-%d"),
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "journal_id": 1,  # Default purchase journal
    }

    if partner_id:
        bill_values["partner_id"] = partner_id

    # Create invoice line
    line_values = {
        "name": description,
        "price_unit": amount,
        "account_id": account_id,
    }

    try:
        bill_id = client.create("account.move", bill_values)

        # Add line
        client.write("account.move", bill_id, {
            "invoice_line_ids": [(0, 0, line_values)]
        })

        logger.info(f"Created draft vendor bill: {bill_id}")

        return {
            "success": True,
            "bill_id": bill_id,
            "state": "draft",
            "message": f"Vendor bill created as draft. Requires approval before posting."
        }

    except Exception as e:
        logger.error(f"Error creating vendor bill: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def post_vendor_bill(bill_id: int) -> dict:
    """
    Post a draft vendor bill (after approval).

    Args:
        bill_id: Vendor bill ID

    Returns:
        Dictionary with result
    """
    client = get_client()

    try:
        # Post the bill
        client.button_action("account.move", bill_id, "action_post")

        logger.info(f"Posted vendor bill: {bill_id}")

        return {
            "success": True,
            "bill_id": bill_id,
            "state": "posted",
            "message": "Vendor bill posted successfully"
        }

    except Exception as e:
        logger.error(f"Error posting vendor bill: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def create_journal_entry(description: str, debit: float, credit: float, debit_account: int, credit_account: int) -> dict:
    """
    Create a draft journal entry.

    Args:
        description: Entry description
        debit: Debit amount
        credit: Credit amount
        debit_account: Debit account ID
        credit_account: Credit account ID

    Returns:
        Dictionary with entry ID and status
    """
    client = get_client()

    entry_values = {
        "state": "draft",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "journal_id": 1,  # Default journal
        "line_ids": [
            (0, 0, {
                "name": description,
                "debit": debit,
                "credit": 0,
                "account_id": debit_account,
            }),
            (0, 0, {
                "name": description,
                "debit": 0,
                "credit": credit,
                "account_id": credit_account,
            }),
        ]
    }

    try:
        entry_id = client.create("account.move", entry_values)

        logger.info(f"Created draft journal entry: {entry_id}")

        return {
            "success": True,
            "entry_id": entry_id,
            "state": "draft",
            "message": "Journal entry created as draft. Requires approval before posting."
        }

    except Exception as e:
        logger.error(f"Error creating journal entry: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_account_by_code(code: str) -> dict:
    """
    Find an account by its code.

    Args:
        code: Account code (e.g., "1010")

    Returns:
        Dictionary with account info
    """
    client = get_client()

    try:
        accounts = client.search_read(
            "account.account",
            [["code", "=", code]],
            ["id", "code", "name"]
        )

        if accounts:
            return {
                "success": True,
                "account": accounts[0]
            }
        else:
            return {
                "success": False,
                "error": f"Account not found: {code}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_partners(name: str = None) -> dict:
    """
    Search for partners (vendors/customers).

    Args:
        name: Optional name filter

    Returns:
        Dictionary with list of partners
    """
    client = get_client()

    try:
        domain = []
        if name:
            domain.append(["name", "ilike", name])

        partners = client.search_read(
            "res.partner",
            domain,
            ["id", "name", "supplier_rank", "customer_rank"]
        )

        return {
            "success": True,
            "partners": partners
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# MCP Server Response Generator

def mcp_response(content: str, is_error: bool = False) -> str:
    """Generate MCP response."""
    response = {
        "content": [
            {
                "type": "text",
                "text": content
            }
        ]
    }
    if is_error:
        response["isError"] = True
    return json.dumps(response)


# Main MCP Handler

def handle_tool_call(tool_name: str, arguments: dict) -> str:
    """Handle MCP tool calls."""
    try:
        if tool_name == "create_vendor_bill":
            result = create_vendor_bill(
                description=arguments["description"],
                amount=arguments["amount"],
                partner_id=arguments.get("partner_id"),
                account_id=arguments.get("account_id")
            )
            return mcp_response(json.dumps(result, indent=2))

        elif tool_name == "post_vendor_bill":
            result = post_vendor_bill(arguments["bill_id"])
            return mcp_response(json.dumps(result, indent=2))

        elif tool_name == "create_journal_entry":
            result = create_journal_entry(
                description=arguments["description"],
                debit=arguments["debit"],
                credit=arguments["credit"],
                debit_account=arguments["debit_account"],
                credit_account=arguments["credit_account"]
            )
            return mcp_response(json.dumps(result, indent=2))

        elif tool_name == "get_account_by_code":
            result = get_account_by_code(arguments["code"])
            return mcp_response(json.dumps(result, indent=2))

        elif tool_name == "get_partners":
            result = get_partners(arguments.get("name"))
            return mcp_response(json.dumps(result, indent=2))

        else:
            return mcp_response(f"Unknown tool: {tool_name}", is_error=True)

    except Exception as e:
        logger.exception("Error handling tool call")
        return mcp_response(f"Error: {str(e)}", is_error=True)


def main():
    """Main MCP server loop."""
    import sys

    logger.info("Odoo MCP Server starting...")

    # stdio communication with MCP host
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if request.get("method") == "tools/call":
                result = handle_tool_call(
                    request["params"]["name"],
                    request["params"].get("arguments", {})
                )
                print(result, flush=True)

        except json.JSONDecodeError:
            continue
        except Exception as e:
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
```

## Step 2: Configuration

```bash
# .env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USER=admin
ODOO_PASSWORD=admin
```

## Step 3: MCP Configuration

```json
// ~/.config/claude/mcp_settings.json
{
  "mcpServers": {
    "odoo": {
      "command": "python",
      "args": ["/path/to/odoo_mcp_server.py"],
      "env": {
        "ODOO_URL": "http://localhost:8069",
        "ODOO_DB": "your_db",
        "ODOO_USER": "your_user",
        "ODOO_PASSWORD": "your_password"
      }
    }
  }
}
```

## ACCEPTANCE CRITERIA

- Connects to Odoo via JSON-RPC
- Creates draft accounting entries
- Requires approval before posting
- Supports vendor bills and journal entries

## FOLLOW-UPS

- Add payment processing
- Implement invoice reconciliation
- Create reporting functions
- Add multi-company support
