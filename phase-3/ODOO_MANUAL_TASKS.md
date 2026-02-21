# Odoo Manual Setup Tasks - Phase 3

**Note**: Yeh tasks manually Odoo interface mein complete karni padengi kyunki ye Odoo GUI ke tasks hain.

---

## T009: Enable Odoo Modules

**Status**: PENDING (Manual action required in Odoo)

**Steps**:
1. Open browser: http://localhost:8069
2. Login with:
   - Email: ammaraak79@gmail.com
   - Password: Azeemi@1234
3. Click "Apps" menu (top navigation)
4. Search for and install these modules:
   - **Invoicing** (account)
   - **Accounting** (account)
   - **Contacts** (contacts)

**Verification**:
- [ ] Invoicing app appears in Apps list with "Installed" status
- [ ] Accounting app appears in Apps list with "Installed" status
- [ ] Contacts app appears in Apps list with "Installed" status

---

## T010: Create Test Customers

**Status**: PENDING (Manual action required in Odoo)

**Steps**:
1. Open http://localhost:8069
2. Click "Sales" → "Customers" → "Create"
3. Create 3 customers:

**Customer 1: ABC Corp**
- Name: ABC Corp
- Email: contact@abccorp.com
- Phone: +1-555-0101
- Address: 123 Business St, New York, NY 10001

**Customer 2: XYZ Ltd**
- Name: XYZ Ltd
- Email: info@xyzltd.com
- Phone: +1-555-0102
- Address: 456 Commerce Ave, Los Angeles, CA 90001

**Customer 3: Startup Co**
- Name: Startup Co
- Email: hello@startupco.com
- Phone: +1-555-0103
- Address: 789 Innovation Blvd, San Francisco, CA 94101

**Verification**:
- [ ] 3 customers visible in Sales → Customers list
- [ ] All customers have complete contact information

---

## T011: Create Test Products

**Status**: PENDING (Manual action required in Odoo)

**Steps**:
1. Open http://localhost:8069
2. Click "Sales" → "Products" → "Create"
3. Create 3 products/services:

**Product 1: Consulting Services**
- Product Name: Consulting Services
- Product Type: Service
- Sales Price: 100.00
- Unit: Hour
- Internal Reference: CONS-001
- Description: Professional consulting services

**Product 2: Software Development**
- Product Name: Software Development
- Product Type: Service
- Sales Price: 150.00
- Unit: Hour
- Internal Reference: DEV-001
- Description: Custom software development

**Product 3: Support**
- Product Name: Technical Support
- Product Type: Service
- Sales Price: 75.00
- Unit: Hour
- Internal Reference: SUPP-001
- Description: Ongoing technical support services

**Verification**:
- [ ] 3 products visible in Sales → Products list
- [ ] All products have correct pricing

---

## T012: Create Test Draft Invoices

**Status**: PENDING (Manual action required in Odoo)

**Steps**:
1. Open http://localhost:8069
2. Click "Sales" → "Invoices" → "Create"
3. Create 2 draft invoices:

**Invoice 1: ABC Corp - Consulting**
- Customer: ABC Corp
- Invoice Date: 2026-02-15
- Product Line: Consulting Services - 10 hours - $100.00/hr
- Total: $1,000.00
- **Status**: DRAFT (do NOT post/validate)

**Invoice 2: XYZ Ltd - Software Development**
- Customer: XYZ Ltd
- Invoice Date: 2026-02-18
- Product Line: Software Development - 20 hours - $150.00/hr
- Total: $3,000.00
- **Status**: DRAFT (do NOT post/validate)

**Verification**:
- [ ] 2 draft invoices visible in Sales → Invoices (filter: Draft)
- [ ] Invoice 1: $1,000.00 for ABC Corp
- [ ] Invoice 2: $3,000.00 for XYZ Ltd
- [ ] Both invoices in "Draft" status (not posted)

---

## Notes

- Yeh tasks manually Odoo web interface mein complete karni padengi
- Database already created: hakathon-00
- Admin credentials already configured
- MCP client code ready - bas test data create karna baaki hai
- Draft invoices zaroori hai kyunki unhe approval workflow test karna hai

---

**Next Step**: After completing these manual tasks, run T033 (Odoo MCP test) to verify connection.
