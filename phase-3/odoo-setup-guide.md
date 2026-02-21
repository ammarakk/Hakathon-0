# Odoo Configuration Guide for Phase 3

**Date**: 2026-02-21
**Odoo Instance**: http://localhost:8069
**Database**: hakathon-00
**Master Password**: 8y82-ic5u-hspk
**Admin Email**: ammaraak79@gmail.com
**Admin Password**: Azeemi@1234

---

## Step 1: Login to Odoo

1. Open browser: http://localhost:8069
2. Select database: **hakathon-00**
3. Enter master password: `8y82-ic5u-hspk`
4. Login with:
   - Email: `ammaraak79@gmail.com`
   - Password: `Azeemi@1234`

⚠️ **IMPORTANT**: Change master password after first login!

---

## Step 2: Enable Required Modules (Task T009)

1. Click **Apps** menu (top navigation)
2. Remove default search filter if needed
3. Search for and install these modules:

### a. Invoicing
- Search: "Invoicing"
- Click **Install** on "Invoicing" app
- Wait for installation to complete

### b. Accounting
- Search: "Accounting"
- Click **Install** on "Accounting" app
- Wait for installation to complete

### c. Contacts
- Search: "Contacts"
- Click **Install** on "Contacts" app (may already be installed)
- Wait for installation to complete

**Verification**: You should see Invoicing, Accounting, and Contacts in the top menu

---

## Step 3: Create Test Customers (Task T010)

1. Click **Contacts** menu (top navigation)
2. Click **Create** button
3. Create these 3 customers:

### Customer 1: ABC Corp
- **Name**: ABC Corp
- **Email**: contact@abccorp.com
- **Phone**: +1-555-0100
- **Address**: 123 Business Ave, New York, NY 10001
- **Customer**: ✅ (checked)
- Click **Save**

### Customer 2: XYZ Ltd
- **Name**: XYZ Ltd
- **Email**: info@xyzltd.com
- **Phone**: +1-555-0200
- **Address**: 456 Commerce St, Los Angeles, CA 90001
- **Customer**: ✅ (checked)
- Click **Save**

### Customer 3: Startup Co
- **Name**: Startup Co
- **Email**: hello@startupco.com
- **Phone**: +1-555-0300
- **Address**: 789 Innovation Blvd, Austin, TX 78701
- **Customer**: ✅ (checked)
- Click **Save**

**Verification**: You should see all 3 customers in the Contacts list

---

## Step 4: Create Test Products (Task T011)

1. Click **Products** menu (under Invoicing or Accounting)
2. Click **Create** button
3. Create these 3 products:

### Product 1: Consulting Services
- **Product Name**: Consulting Services
- **Product Type**: Service
- **Sales Price**: 100.00
- **Unit of Measure**: Hour
- **Customer Lead Time**: 0 days
- Click **Save**

### Product 2: Software Development
- **Product Name**: Software Development
- **Product Type**: Service
- **Sales Price**: 150.00
- **Unit of Measure**: Hour
- **Customer Lead Time**: 0 days
- Click **Save**

### Product 3: Technical Support
- **Product Name**: Technical Support
- **Product Type**: Service
- **Sales Price**: 75.00
- **Unit of Measure**: Hour
- **Customer Lead Time**: 0 days
- Click **Save**

**Verification**: You should see all 3 products in the Products list

---

## Step 5: Create Draft Invoices (Task T012)

1. Click **Invoicing** menu (top navigation)
2. Click **Customers** → **Invoices**
3. Click **Create** button
4. Create these 2 draft invoices:

### Invoice #1 for ABC Corp
- **Customer**: ABC Corp
- **Invoice Date**: Today's date
- **Due Date**: 30 days from today
- **Invoice Lines**:
  - Product: Consulting Services
  - Quantity: 10 hours
  - Unit Price: $100.00
  - Total: $1,000.00
- **Status**: Draft (DO NOT click "Confirm" or "Validate")
- Click **Save**

### Invoice #2 for XYZ Ltd
- **Customer**: XYZ Ltd
- **Invoice Date**: Today's date
- **Due Date**: 30 days from today
- **Invoice Lines**:
  - Product: Software Development
  - Quantity: 10 hours
  - Unit Price: $150.00
  - Total: $1,500.00
- **Status**: Draft (DO NOT click "Confirm" or "Validate")
- Click **Save**

**Verification**: You should see 2 invoices in "Draft" status in the invoices list

⚠️ **IMPORTANT**: Do NOT post/validate these invoices yet! They must remain in Draft status for testing the draft → approve → post workflow.

---

## Completion Checklist

- [ ] T009: Modules enabled (Invoicing, Accounting, Contacts)
- [ ] T010: 3 customers created (ABC Corp, XYZ Ltd, Startup Co)
- [ ] T011: 3 products created (Consulting $100/hr, Software Dev $150/hr, Support $75/hr)
- [ ] T012: 2 draft invoices created (NOT posted)

---

## Next Steps

After completing these tasks:
1. Return to Claude Code session
2. Confirm completion: "Odoo configuration complete"
3. Proceed with Phase 3-10 implementation tasks

---

## Troubleshooting

### Issue: Can't find Apps menu
- **Solution**: Make sure you're logged in as admin user

### Issue: Module installation fails
- **Solution**: Check internet connection, try again

### Issue: Can't create products
- **Solution**: Make sure Products app is installed under Invoicing

### Issue: Invoice won't save as draft
- **Solution**: Make sure you click "Save" but NOT "Confirm" or "Validate"

---

**Guide Created**: 2026-02-21
**Phase**: 3 (Gold Tier)
**Status**: Ready for user execution
