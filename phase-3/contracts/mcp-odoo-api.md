# MCP Odoo API Contract

**Version**: 1.0.0
**Protocol**: JSON-RPC over HTTP
**Base URL**: http://localhost:8069/jsonrpc
**Authentication**: Username/Password (Basic Auth)

---

## Overview

This MCP server provides tools for interacting with a self-hosted Odoo Community Edition instance. All actions that modify data (create, update, delete) create drafts first and require approval via `/Pending_Approval/` workflow.

**Security Notes**:
- Credentials stored in `phase-3/secrets/.odoo_credentials`
- Draft invoices can be created autonomously
- Posting invoices requires human approval
- Reading data (customers, invoices) does not require approval

---

## Tools

### 1. read_odoo_partners

**Description**: Read customer/partner records from Odoo

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "filters": {
      "type": "object",
      "description": "Optional filters (Odoo domain syntax)",
      "properties": {
        "is_company": {
          "type": "boolean",
          "description": "Filter for companies (true) or individuals (false)"
        },
        "customer_rank": {
          "type": "integer",
          "description": "Filter by customer rank (>0 for customers)"
        }
      }
    },
    "limit": {
      "type": "integer",
      "description": "Maximum number of records to return",
      "default": 100
    },
    "offset": {
      "type": "integer",
      "description": "Number of records to skip",
      "default": 0
    }
  }
}
```

**Output Schema**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "partner_id": {
        "type": "integer",
        "description": "Odoo partner ID"
      },
      "name": {
        "type": "string",
        "description": "Partner name"
      },
      "email": {
        "type": "string",
        "description": "Email address"
      },
      "phone": {
        "type": "string",
        "description": "Phone number"
      },
      "is_company": {
        "type": "boolean"
      },
      "customer_rank": {
        "type": "integer"
      }
    }
  }
}
```

**Example Request**:
```python
read_odoo_partners(
    filters={"is_company": true, "customer_rank": 1},
    limit=50
)
```

**Example Response**:
```json
[
  {
    "partner_id": 456,
    "name": "ABC Corp",
    "email": "contact@abccorp.com",
    "phone": "+1-555-1234",
    "is_company": true,
    "customer_rank": 1
  }
]
```

**Errors**:
- `OdooConnectionError`: Cannot connect to Odoo
- `AuthenticationError`: Invalid credentials
- `PermissionError`: User lacks read permission

---

### 2. create_odoo_draft_invoice

**Description**: Create a draft invoice in Odoo (does NOT post)

**Input Schema**:
```json
{
  "type": "object",
  "required": ["customer_id", "line_items", "due_date"],
  "properties": {
    "customer_id": {
      "type": "integer",
      "description": "Odoo partner ID for customer"
    },
    "line_items": {
      "type": "array",
      "description": "Invoice line items",
      "items": {
        "type": "object",
        "required": ["product_id", "quantity", "price_unit"],
        "properties": {
          "product_id": {
            "type": "integer",
            "description": "Odoo product ID"
          },
          "quantity": {
            "type": "number",
            "description": "Quantity"
          },
          "price_unit": {
            "type": "number",
            "description": "Unit price"
          },
          "description": {
            "type": "string",
            "description": "Line item description"
          }
        }
      }
    },
    "due_date": {
      "type": "string",
      "format": "date",
      "description": "Invoice due date (YYYY-MM-DD)"
    },
    "invoice_date": {
      "type": "string",
      "format": "date",
      "description": "Invoice date (YYYY-MM-DD), defaults to today"
    }
  }
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "invoice_id": {
      "type": "integer",
      "description": "Odoo invoice ID"
    },
    "status": {
      "type": "string",
      "enum": ["draft"],
      "description": "Invoice status (always draft)"
    },
    "total_amount": {
      "type": "number",
      "description": "Total invoice amount"
    },
    "customer_name": {
      "type": "string",
      "description": "Customer name"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation timestamp"
    }
  }
}
```

**Example Request**:
```python
create_odoo_draft_invoice(
    customer_id=456,
    line_items=[
        {
            "product_id": 123,
            "quantity": 10,
            "price_unit": 100.00,
            "description": "Consulting Services"
        }
    ],
    due_date="2026-03-20"
)
```

**Example Response**:
```json
{
  "invoice_id": 123,
  "status": "draft",
  "total_amount": 1000.00,
  "customer_name": "ABC Corp",
  "created_at": "2026-02-20T10:30:00Z"
}
```

**Errors**:
- `ValidationError`: Missing required fields
- `CustomerNotFoundError`: customer_id does not exist
- `ProductNotFoundError`: product_id does not exist
- `OdooConnectionError`: Cannot connect to Odoo

**Approval Required**: ✅ YES - Must create `/Pending_Approval/` request before posting

---

### 3. post_odoo_invoice

**Description**: Post a draft invoice to Odoo (requires prior approval)

**Input Schema**:
```json
{
  "type": "object",
  "required": ["invoice_id"],
  "properties": {
    "invoice_id": {
      "type": "integer",
      "description": "Odoo invoice ID to post"
    }
  }
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "invoice_id": {
      "type": "integer"
    },
    "status": {
      "type": "string",
      "enum": ["posted"]
    },
    "posted_at": {
      "type": "string",
      "format": "date-time"
    },
    "invoice_number": {
      "type": "string",
      "description": "Assigned invoice number (e.g., INV/2026/001)"
    }
  }
}
```

**Example Request**:
```python
post_odoo_invoice(invoice_id=123)
```

**Example Response**:
```json
{
  "invoice_id": 123,
  "status": "posted",
  "posted_at": "2026-02-20T11:00:00Z",
  "invoice_number": "INV/2026/001"
}
```

**Errors**:
- `InvoiceNotFoundError`: invoice_id does not exist
- `InvalidStateError`: Invoice not in draft state
- `PostingError`: Odoo rejected posting (e.g., missing fields)
- `ApprovalRequiredError`: Called without prior approval

**Prerequisite**: ✅ MUST have approval in `/Pending_Approval/`

---

### 4. read_odoo_invoices

**Description**: Read invoices from Odoo (for CEO Briefing generation)

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "date_range": {
      "type": "object",
      "properties": {
        "start_date": {
          "type": "string",
          "format": "date"
        },
        "end_date": {
          "type": "string",
          "format": "date"
        }
      }
    },
    "status": {
      "type": "string",
      "enum": ["draft", "posted", "paid", "all"],
      "default": "all"
    },
    "limit": {
      "type": "integer",
      "default": 100
    }
  }
}
```

**Output Schema**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "invoice_id": {
        "type": "integer"
      },
      "invoice_number": {
        "type": "string"
      },
      "customer_name": {
        "type": "string"
      },
      "total_amount": {
        "type": "number"
      },
      "status": {
        "type": "string",
        "enum": ["draft", "posted", "paid"]
      },
      "invoice_date": {
        "type": "string",
        "format": "date"
      },
      "due_date": {
        "type": "string",
        "format": "date"
      }
    }
  }
}
```

**Example Request**:
```python
read_odoo_invoices(
    date_range={"start_date": "2026-02-01", "end_date": "2026-02-29"},
    status="posted"
)
```

**Example Response**:
```json
[
  {
    "invoice_id": 100,
    "invoice_number": "INV/2026/001",
    "customer_name": "ABC Corp",
    "total_amount": 1500.00,
    "status": "posted",
    "invoice_date": "2026-02-15",
    "due_date": "2026-03-15"
  }
]
```

**Errors**: None (empty array if no invoices found)

---

### 5. read_odoo_revenue

**Description**: Read revenue summary for CEO Briefing

**Input Schema**:
```json
{
  "type": "object",
  "required": ["month", "year"],
  "properties": {
    "month": {
      "type": "integer",
      "minimum": 1,
      "maximum": 12,
      "description": "Month (1-12)"
    },
    "year": {
      "type": "integer",
      "description": "Year (e.g., 2026)"
    }
  }
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "total_revenue": {
      "type": "number",
      "description": "Total revenue from posted invoices"
    },
    "outstanding_amount": {
      "type": "number",
      "description": "Total amount of unpaid (posted) invoices"
    },
    "paid_amount": {
      "type": "number",
      "description": "Total amount of paid invoices"
    },
    "invoice_count": {
      "type": "integer",
      "description": "Number of posted invoices"
    },
    "top_customers": {
      "type": "array",
      "description": "Top 3 customers by revenue",
      "items": {
        "type": "object",
        "properties": {
          "customer_name": {
            "type": "string"
          },
          "revenue": {
            "type": "number"
          }
        }
      }
    }
  }
}
```

**Example Request**:
```python
read_odoo_revenue(month=2, year=2026)
```

**Example Response**:
```json
{
  "total_revenue": 12500.00,
  "outstanding_amount": 4500.00,
  "paid_amount": 8000.00,
  "invoice_count": 8,
  "top_customers": [
    {"customer_name": "ABC Corp", "revenue": 5000.00},
    {"customer_name": "XYZ Ltd", "revenue": 3500.00},
    {"customer_name": "Startup Co", "revenue": 2000.00}
  ]
}
```

**Errors**: None (zero values if no data)

---

## Error Handling

All MCP tools follow this error response format:

```json
{
  "error": {
    "code": "ErrorCode",
    "message": "Human-readable error description",
    "details": {
      "odoorpc_error": "Original Odoo error message"
    }
  }
}
```

**Error Codes**:
- `OdooConnectionError`: Cannot connect to http://localhost:8069
- `AuthenticationError`: Invalid username/password
- `PermissionError`: User lacks required permission
- `ValidationError`: Invalid input data
- `NotFoundError`: Record does not exist
- `InvalidStateError`: Invalid state transition
- `ApprovalRequiredError`: Action requires prior approval

---

## Rate Limits

- **Read operations**: 60 requests per minute
- **Write operations**: 30 requests per minute
- **Retry**: Exponential backoff (1s, 2s, 4s, 8s, 16s)

---

## Testing

### Test Script

```python
# phase-3/code/test_odoo_mcp.py

from mcp_odoo_client import OdooMCPClient
import os
from dotenv import load_dotenv

load_dotenv('phase-3/secrets/.odoo_credentials')

client = OdooMCPClient(
    url=os.getenv('ODOO_URL'),
    db=os.getenv('ODOO_DB'),
    user=os.getenv('ODOO_USER'),
    password=os.getenv('ODOO_PASSWORD')
)

# Test 1: Read partners
print("Testing read_odoo_partners...")
partners = client.read_odoo_partners(limit=5)
print(f"Found {len(partners)} partners")

# Test 2: Create draft invoice
print("\nTesting create_odoo_draft_invoice...")
invoice = client.create_odoo_draft_invoice(
    customer_id=partners[0]['partner_id'],
    line_items=[{
        "product_id": 1,  # Use actual product ID
        "quantity": 5,
        "price_unit": 100.00,
        "description": "Test Service"
    }],
    due_date="2026-03-20"
)
print(f"Created draft invoice {invoice['invoice_id']}")

# Test 3: Read revenue
print("\nTesting read_odoo_revenue...")
revenue = client.read_odoo_revenue(month=2, year=2026)
print(f"Total revenue: ${revenue['total_revenue']}")

print("\n✅ All tests passed!")
```

---

**Status**: ✅ API contract complete
**Implementation**: Phase 3 code/odoo_mcp_client.py
