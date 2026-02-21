# Company Handbook

## Rules of Engagement

### Communication Style
- Be polite in all communications
- Use professional yet friendly tone
- Be concise but thorough
- Avoid jargon unless necessary

### Approval Thresholds
- **Payments >$500**: Require human approval
- **Email sends**: Require human review
- **Social media posts**: Require human approval
- **File deletions**: Require human confirmation

### Workflow
1. Watchers detect items → create files in /Needs_Action/
2. Process items systematically
3. Move completed items to /Done/
4. Archive processed items regularly

### Privacy & Security
- Never share credentials
- Keep .env files local-only
- Don't log sensitive information
- Ask for approval on uncertain actions

---

## Gold Tier: Cross-Domain Integration

### Domain Rules
- **Personal Domain**: Gmail, WhatsApp, banking alerts, personal tasks
- **Business Domain**: Social media, Odoo accounting, client projects, invoices
- **Unified Reasoning**: Both domains processed in single Plan.md with clear labels

### Cross-Domain Task Linking
- Personal client communications → Link to business Odoo invoices
- Business project completion → Include personal follow-up tasks if relevant
- Banking alerts → May trigger business expense categorization

### Task Prioritization
- **Business tasks prioritized by default** (client deadlines > personal messages)
- **Urgent personal items** (family emergencies) → Override business tasks
- **Domain labeling**: All tasks in Plan.md must have [Personal] or [Business] prefix

---

## Gold Tier: Odoo Accounting Integration

### Odoo Workflow
- **System**: Odoo Community Edition (local, port 8069)
- **Database**: hakathon-00
- **Access**: http://localhost:8069

### Draft → Approve → Post Pattern
1. **Draft Creation**: Claude creates draft invoice via MCP
2. **Draft Details**: Written to /Pending_Approval/ with invoice summary
3. **Human Approval**: User reviews draft in vault
4. **Post to Odoo**: After approval, MCP posts invoice to Odoo
5. **Confirmation**: Posted invoice details logged to audit log

### Odoo Approval Rules
- **ALL invoice postings** require human approval
- **ALL payment validations** require human approval
- **Draft invoices**: Safe to create automatically (no financial commitment)
- **Posted invoices**: Only after explicit user approval

### Revenue Tracking
- Weekly CEO Briefing scans Odoo for revenue data
- Outstanding invoices tracked separately from paid
- Top customers identified from revenue data

---

## Gold Tier: Social Media Integration

### Social Platform Approval
- **ALL social posts** require human approval (draft → approve → post)
- **Platforms**: LinkedIn, Facebook, Instagram, Twitter/X
- **Test Accounts Only**: Use business/test accounts during development

### Social Follow-Up Rules
- Business project completion → Consider social announcement post
- Invoice sent → Optional: "Project completed" social post
- New client engaged → Optional: "Welcome" post (with approval)

### Post Generation
- Claude generates platform-appropriate content
- Drafts saved to /Pending_Approval/ with platform tag
- Summary appended to /Done/ after posting

---

*Version: 2.0 - Gold Tier*
*Updated: 2026-02-21*
