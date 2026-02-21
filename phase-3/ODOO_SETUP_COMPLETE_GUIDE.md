# Odoo Setup Guide - Phase 3 Gold Tier

**Auto-Generated**: 2026-02-21
**Purpose**: Complete Odoo configuration for Phase 3 testing
**Time Required**: 15-20 minutes

---

## Prerequisites

- [x] Odoo installed at http://localhost:8069
- [x] Database created: hakathon-00
- [x] Admin credentials configured
- [ ] **TODO**: Complete remaining setup steps below

---

## Step 1: Login to Odoo

1. Open browser: http://localhost:8069
2. Select database: **hakathon-00**
3. Email: **ammaraak79@gmail.com**
4. Password: **Azeemi@1234**

---

## Step 2: Enable Required Modules (T009)

### 2.1 Access Apps Menu
1. Click **Apps** (top navigation)
2. Remove "Apps" filter if needed

### 2.2 Install Accounting Module
1. Search for: **Accounting**
2. Click **Install** on "Accounting" by Odoo
3. Wait for installation (2-3 minutes)
4. Verify: "Invoicing" menu appears in left sidebar

### 2.3 Install Contacts Module
1. Search for: **Contacts**
2. Click **Install** on "Contacts" if not already installed
3. Verify: "Contacts" menu appears in left sidebar

**Verification Checklist**:
- [ ] Accounting module installed
- [ ] Contacts module installed
- [ ] Invoicing menu visible
- [ ] Customers menu visible under Sales

---

## Step 3: Create Test Customers (T010)

### Customer 1: ABC Corp

1. Go to **Sales** → **Customers** → **Create**
2. Fill in:
   - **Name**: ABC Corp
   - **Email**: contact@abccorp.com
   - **Phone**: +1-555-0101
   - **Address**:
     - Street: 123 Business St
     - City: New York
     - State: NY
     - Zip: 10001
     - Country: United States
3. Click **Save**

### Customer 2: XYZ Ltd

1. Click **Create** (in Customers list)
2. Fill in:
   - **Name**: XYZ Ltd
   - **Email**: info@xyzltd.com
   - **Phone**: +1-555-0102
   - **Address**:
     - Street: 456 Commerce Ave
     - City: Los Angeles
     - State: CA
     - Zip: 90001
     - Country: United States
3. Click **Save**

### Customer 3: Startup Co

1. Click **Create**
2. Fill in:
   - **Name**: Startup Co
   - **Email**: hello@startupco.com
   - **Phone**: +1-555-0103
   - **Address**:
     - Street: 789 Innovation Blvd
     - City: San Francisco
     - State: CA
     - Zip: 94101
     - Country: United States
3. Click **Save**

**Verification Checklist**:
- [ ] ABC Corp created (3 customers total in list)
- [ ] XYZ Ltd created
- [ ] Startup Co created

---

## Step 4: Create Test Products/Services (T011)

### Product 1: Consulting Services

1. Go to **Sales** → **Products** → **Create**
2. Fill in:
   - **Product Name**: Consulting Services
   - **Product Type**: Service (Consumable)
   - **Internal Reference**: CONS-001
   - **Sales Price**: 100.00
   - **Unit of Measure**: Hour
   - **Description**: Professional consulting services for business strategy and implementation
   - **Customer Taxes**: (leave empty for now)
3. Click **Save**

### Product 2: Software Development

1. Click **Create**
2. Fill in:
   - **Product Name**: Software Development
   - **Product Type**: Service (Consumable)
   - **Internal Reference**: DEV-001
   - **Sales Price**: 150.00
   - **Unit of Measure**: Hour
   - **Description**: Custom software development services including web and mobile applications
3. Click **Save**

### Product 3: Technical Support

1. Click **Create**
2. Fill in:
   - **Product Name**: Technical Support
   - **Product Type**: Service (Consumable)
   - **Internal Reference**: SUPP-001
   - **Sales Price**: 75.00
   - **Unit of Measure**: Hour
   - **Description**: Ongoing technical support and maintenance services
3. Click **Save**

**Verification Checklist**:
- [ ] Consulting Services created (price: $100.00)
- [ ] Software Development created (price: $150.00)
- [ ] Technical Support created (price: $75.00)

---

## Step 5: Create Draft Invoices (T012)

### Draft Invoice 1: ABC Corp

1. Go to **Sales** → **Invoices** → **Create**
2. Fill in:
   - **Customer**: ABC Corp
   - **Invoice Date**: 2026-02-15
   - **Product** (click "Add a line"):
     - Select: Consulting Services
     - Quantity: 10
     - Unit Price: 100.00
     - Description: Consulting services - February 2026
3. Click **Save** (DO NOT click Confirm/Validate)
4. Verify status shows: **Draft**

### Draft Invoice 2: XYZ Ltd

1. Click **Create** (in Invoices list)
2. Fill in:
   - **Customer**: XYZ Ltd
   - **Invoice Date**: 2026-02-18
   - **Product**:
     - Select: Software Development
     - Quantity: 20
     - Unit Price: 150.00
     - Description: Software development project - Phase 1
3. Click **Save** (DO NOT click Confirm/Validate)
4. Verify status shows: **Draft**

**Verification Checklist**:
- [ ] Invoice for ABC Corp: $1,000.00 (Draft status)
- [ ] Invoice for XYZ Ltd: $3,000.00 (Draft status)
- [ ] Both invoices in "Draft" status (NOT posted)

---

## Step 6: Verify Setup Complete

### Check Customers
1. Go to **Sales** → **Customers**
2. Should see: ABC Corp, XYZ Ltd, Startup Co

### Check Products
1. Go to **Sales** → **Products**
2. Should see: Consulting Services ($100), Software Development ($150), Technical Support ($75)

### Check Invoices
1. Go to **Sales** → **Invoices**
2. Filter by: **Draft**
3. Should see: 2 draft invoices totaling $4,000.00

### Test MCP Connection
1. Run: `python phase-3/code/odoo_mcp_client.py`
2. Should show: Connection successful
3. Should read customers and invoices

---

## Troubleshooting

**Problem**: Cannot install Accounting module
**Solution**: Make sure you have admin rights, restart Odoo service

**Problem**: Customer not saving
**Solution**: Fill all required fields (Name, Email at minimum)

**Problem**: Invoice status not "Draft"
**Solution**: Click "Save" only, DO NOT click "Confirm"

**Problem**: MCP connection fails
**Solution**:
1. Check Odoo is running: http://localhost:8069
2. Check credentials in phase-3/secrets/.odoo_credentials
3. Verify database name: hakathon-00

---

## Next Steps After Setup

1. ✅ Run test script: `python phase-3/code/test_implementation.py`
2. ✅ Verify MCP client can read customers
3. ✅ Test draft invoice creation via MCP
4. ✅ Test approval workflow
5. ✅ Complete Phase 3 verification

---

## Setup Completion Checklist

- [ ] Step 1: Login successful
- [ ] Step 2: Modules enabled (Accounting, Contacts)
- [ ] Step 3: 3 customers created
- [ ] Step 4: 3 products created
- [ ] Step 5: 2 draft invoices created
- [ ] Step 6: All verifications passed

**When all checkboxes marked**: Odoo setup complete, ready for Phase 3 testing!

---

*Generated by AI Employee - Phase 3 Gold Tier*
*Software Company Style: Automated Setup Guide*
