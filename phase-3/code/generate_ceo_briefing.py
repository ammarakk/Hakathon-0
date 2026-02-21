#!/usr/bin/env python3
"""
CEO Briefing Generator - Phase 3 Gold Tier

This script generates weekly Monday Morning CEO Briefings that provide:
- Revenue summary (from Odoo)
- Pending items (from vault)
- Bottlenecks and issues
- Actionable recommendations

Usage:
    python generate_ceo_briefing.py

Output:
    AI_Employee_Vault/CEO_Briefings/Briefing_YYYY-MM-DD.md

Author: AI Employee - Phase 3 Gold Tier
Created: 2026-02-21
Schedule: Every Monday 8:00 AM (via Task Scheduler or cron)
"""

import os
import json
from datetime import date, datetime, timedelta
from pathlib import Path
import glob

# Import Odoo client
try:
    from odoo_mcp_client import OdooMCPClient
except ImportError:
    print("[WARNING]  odoo_mcp_client not found, Odoo data will be skipped")
    OdooMCPClient = None

# Vault paths
VAULT_ROOT = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
CEO_BRIEFINGS_DIR = VAULT_ROOT / "CEO_Briefings"
NEEDS_ACTION_DIR = VAULT_ROOT / "Needs_Action"
PENDING_APPROVAL_DIR = VAULT_ROOT / "Pending_Approval"
PLANS_DIR = VAULT_ROOT / "Plans"
LOGS_DIR = VAULT_ROOT / "Logs"
ACCOUNTING_DIR = VAULT_ROOT / "Accounting"


def scan_vault_pending_items() -> dict:
    """
    Scan vault for pending items

    Returns:
        dict with counts and details
    """
    pending = {
        'needs_action': [],
        'pending_approval': [],
        'active_plans': [],
        'overdue': []
    }

    # Scan /Needs_Action/
    if NEEDS_ACTION_DIR.exists():
        for file in NEEDS_ACTION_DIR.glob("*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract priority and source
                    priority = 'medium'
                    source = 'unknown'
                    for line in content.split('\n')[:20]:
                        if 'priority:' in line.lower():
                            priority = line.split(':')[1].strip()
                        if 'source:' in line.lower():
                            source = line.split(':')[1].strip()

                    pending['needs_action'].append({
                        'file': file.name,
                        'source': source,
                        'priority': priority
                    })
            except Exception as e:
                print(f"[WARNING]  Error reading {file.name}: {e}")

    # Scan /Pending_Approval/
    if PENDING_APPROVAL_DIR.exists():
        for file in PENDING_APPROVAL_DIR.glob("*.md"):
            pending['pending_approval'].append({
                'file': file.name,
                'type': 'approval_required'
            })

    # Scan /Plans/ for active plans
    if PLANS_DIR.exists():
        for file in PLANS_DIR.glob("Plan_*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check if plan has incomplete tasks
                    if '- [ ]' in content or '- [  ]' in content:
                        pending['active_plans'].append({
                            'file': file.name,
                            'status': 'in_progress'
                        })
            except Exception as e:
                print(f"[WARNING]  Error reading {file.name}: {e}")

    # Identify overdue items (older than 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    for item in pending['needs_action']:
        file_path = NEEDS_ACTION_DIR / item['file']
        if file_path.stat().st_mtime < week_ago.timestamp():
            pending['overdue'].append(item)

    return pending


def scan_odoo_revenue() -> dict:
    """
    Scan Odoo for revenue data

    Returns:
        dict with revenue summary
    """
    if OdooMCPClient is None:
        return {
            'total_revenue': 0,
            'outstanding': 0,
            'paid': 0,
            'invoice_count': 0,
            'top_customers': [],
            'error': 'Odoo client not available'
        }

    try:
        client = OdooMCPClient()
        if not client.uid:
            return {
                'total_revenue': 0,
                'outstanding': 0,
                'paid': 0,
                'invoice_count': 0,
                'top_customers': [],
                'error': 'Odoo authentication failed'
            }

        # Get current month revenue
        today = date.today()
        revenue = client.read_revenue(today.month, today.year)

        if revenue:
            return revenue
        else:
            return {
                'total_revenue': 0,
                'outstanding': 0,
                'paid': 0,
                'invoice_count': 0,
                'top_customers': [],
                'error': 'Failed to read revenue'
            }

    except Exception as e:
        return {
            'total_revenue': 0,
            'outstanding': 0,
            'paid': 0,
            'invoice_count': 0,
            'top_customers': [],
            'error': str(e)
        }


def identify_bottlenecks(pending: dict, revenue: dict) -> list:
    """
    Identify bottlenecks and issues

    Args:
        pending: Pending items from scan_vault_pending_items()
        revenue: Revenue data from scan_odoo_revenue()

    Returns:
        list of bottleneck descriptions
    """
    bottlenecks = []

    # Check for overdue items
    if pending['overdue']:
        bottlenecks.append({
            'severity': 'high',
            'issue': f"{len(pending['overdue'])} overdue items in /Needs_Action/",
            'impact': 'Customer satisfaction at risk',
            'recommendation': 'Review overdue items immediately and prioritize responses'
        })

    # Check for pending approvals
    if len(pending['pending_approval']) > 5:
        bottlenecks.append({
            'severity': 'medium',
            'issue': f"{len(pending['pending_approval'])} items awaiting approval",
            'impact': 'Workflow bottleneck',
            'recommendation': 'Review approval queue and process or reject pending items'
        })

    # Check for outstanding invoices
    if revenue.get('outstanding', 0) > 5000:
        bottlenecks.append({
            'severity': 'high',
            'issue': f"${revenue['outstanding']:,.2f} in outstanding invoices",
            'impact': 'Cash flow risk',
            'recommendation': 'Follow up on unpaid invoices, consider payment reminders'
        })

    # Check for too many active plans
    if len(pending['active_plans']) > 5:
        bottlenecks.append({
            'severity': 'medium',
            'issue': f"{len(pending['active_plans'])} active plans (recommend: 3-5 max)",
            'impact': 'Diluted focus',
            'recommendation': 'Complete or consolidate active plans to improve focus'
        })

    return bottlenecks


def generate_recommendations(pending: dict, revenue: dict, bottlenecks: list) -> dict:
    """
    Generate actionable recommendations

    Args:
        pending: Pending items
        revenue: Revenue data
        bottlenecks: Identified bottlenecks

    Returns:
        dict with high/medium/low priority recommendations
    """
    recommendations = {
        'high': [],
        'medium': [],
        'low': []
    }

    # High priority recommendations
    if pending['overdue']:
        recommendations['high'].append(
            "[HIGH] Process all overdue items in /Needs_Action/ immediately"
        )

    if revenue.get('outstanding', 0) > 5000:
        recommendations['high'].append(
            f"[HIGH] Follow up on ${revenue['outstanding']:,.2f} outstanding invoices"
        )

    if revenue.get('total_revenue', 0) < 5000 and date.today().day >= 20:
        recommendations['high'].append(
            "[HIGH] Monthly revenue below target - consider outreach to past clients"
        )

    # Medium priority recommendations
    if len(pending['pending_approval']) > 3:
        recommendations['medium'].append(
            f"[MEDIUM] Review and process {len(pending['pending_approval'])} pending approvals"
        )

    if len(pending['needs_action']) > 10:
        recommendations['medium'].append(
            f"[MEDIUM] {len(pending['needs_action'])} items in /Needs_Action/ - batch similar tasks"
        )

    if revenue.get('invoice_count', 0) < 3 and date.today().day >= 25:
        recommendations['medium'].append(
            "[MEDIUM] Low invoice count this month - review project pipeline"
        )

    # Low priority recommendations
    recommendations['low'].append(
        "[LOW] Review and update Company_Handbook.md if rules have changed"
    )

    recommendations['low'].append(
        "[LOW] Archive completed items from /Done/ to keep vault clean"
    )

    if len(pending['active_plans']) == 0:
        recommendations['low'].append(
            "[LOW] No active plans - consider initiating new business development"
        )

    return recommendations


def generate_briefing_markdown(briefing_date: date, pending: dict, revenue: dict,
                               bottlenecks: list, recommendations: dict) -> str:
    """
    Generate CEO Briefing markdown content

    Args:
        briefing_date: Date of the briefing
        pending: Pending items
        revenue: Revenue data
        bottlenecks: Identified bottlenecks
        recommendations: Actionable recommendations

    Returns:
        Markdown content for briefing
    """
    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    month_name = month_names[briefing_date.month]

    content = f"""# CEO Briefing: {briefing_date.strftime('%B %d, %Y')}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Week**: Week {briefing_date.isocalendar()[1]} of {briefing_date.year}
**Status**: Weekly Business and Accounting Audit

---

## Executive Summary

This weekly briefing provides an overview of business performance, pending items, bottlenecks, and actionable recommendations for the week ahead.

---

## Revenue Summary ({month_name} {briefing_date.year})

### Financial Overview

| Metric | Amount |
|--------|--------|
| Total Revenue | ${revenue.get('total_revenue', 0):,.2f} |
| Outstanding Invoices | ${revenue.get('outstanding', 0):,.2f} |
| Paid Invoices | ${revenue.get('paid', 0):,.2f} |
| Total Invoices | {revenue.get('invoice_count', 0)} |

### Top Customers

"""

    if revenue.get('top_customers'):
        for i, customer in enumerate(revenue['top_customers'], 1):
            content += f"{i}. **{customer['name']}**: ${customer['revenue']:,.2f}\n"
    else:
        content += "No customer data available (Odoo may not be configured)\n"

    content += "\n---\n\n"

    content += """## Pending Items

### Needs Action Queue

| Source | Count | Priority |
|--------|-------|----------|
"""

    # Count by source
    source_counts = {}
    for item in pending['needs_action']:
        source = item['source']
        source_counts[source] = source_counts.get(source, 0) + 1

    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        content += f"| {source.title()} | {count} | {'High' if source_counts.get(source, 0) > 5 else 'Medium'} |\n"

    content += f"""
| **Total** | **{len(pending['needs_action'])}** | - |

### Pending Approvals

- **{len(pending['pending_approval'])}** items awaiting human approval
- Location: `/Pending_Approval/`
- **Action Required**: Review and approve/reject

### Active Plans

- **{len(pending['active_plans'])}** active plans in progress
- Location: `/Plans/`
- Status: Multi-step autonomous execution

---

## Bottlenecks and Issues

"""

    if bottlenecks:
        for bottleneck in bottlenecks:
            severity_marker = {'high': '[HIGH]', 'medium': '[MEDIUM]', 'low': '[LOW]'}
            marker = severity_marker.get(bottleneck['severity'], '[INFO]')

            content += f"""
### {marker} {bottleneck['issue']}

**Severity**: {bottleneck['severity'].title()}
**Impact**: {bottleneck['impact']}
**Recommendation**: {bottleneck['recommendation']}

"""
    else:
        content += "\n[OK] No critical bottlenecks identified - System operating smoothly\n\n"

    content += "---\n\n## Recommendations\n\n"

    # High priority
    if recommendations['high']:
        content += "### [HIGH] High Priority (This Week)\n\n"
        for rec in recommendations['high']:
            content += f"- {rec}\n"
        content += "\n"

    # Medium priority
    if recommendations['medium']:
        content += "### [MEDIUM] Medium Priority (This Week)\n\n"
        for rec in recommendations['medium']:
            content += f"- {rec}\n"
        content += "\n"

    # Low priority
    if recommendations['low']:
        content += "### [LOW] Low Priority (When Time Permits)\n\n"
        for rec in recommendations['low']:
            content += f"- {rec}\n"
        content += "\n"

    content += "---\n\n"

    # Add audit log entry
    content += "## Briefing Metadata\n\n"
    content += f"- **Generated By**: AI Employee (Phase 3 Gold Tier)\n"
    content += f"- **Generation Time**: {datetime.now().isoformat()}\n"
    content += f"- **Odoo Status**: {'[OK] Connected' if revenue.get('total_revenue') > 0 or revenue.get('invoice_count', 0) > 0 else '[WARNING] Not configured'}\n"
    content += f"- **Vault Status**: [OK] Scanned\n"
    content += f"- **Next Briefing**: {(briefing_date + timedelta(days=7)).strftime('%B %d, %Y')}\n"

    content += "\n---\n\n"

    content += "*End of CEO Briefing*"

    return content


def main():
    """Main execution function"""
    print("[REPORT] Generating CEO Briefing...")

    # Create CEO_Briefings directory if it doesn't exist
    CEO_BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)

    # Use today's date (or most recent Monday)
    today = date.today()
    monday = today - timedelta(days=today.weekday())

    briefing_filename = f"Briefing_{monday.strftime('%Y-%m-%d')}.md"
    briefing_path = CEO_BRIEFINGS_DIR / briefing_filename

    print(f"[FILE] Briefing will be saved to: {briefing_path}")

    # Scan vault for pending items
    print("[SCAN] Scanning vault for pending items...")
    pending = scan_vault_pending_items()
    print(f"  - {len(pending['needs_action'])} items in /Needs_Action/")
    print(f"  - {len(pending['pending_approval'])} items in /Pending_Approval/")
    print(f"  - {len(pending['active_plans'])} active plans")
    print(f"  - {len(pending['overdue'])} overdue items")

    # Scan Odoo for revenue
    print("[MONEY] Scanning Odoo for revenue data...")
    revenue = scan_odoo_revenue()
    if revenue.get('error'):
        print(f"  [WARNING]  Odoo error: {revenue['error']}")
    else:
        print(f"  - Total Revenue: ${revenue['total_revenue']:,.2f}")
        print(f"  - Outstanding: ${revenue['outstanding']:,.2f}")
        print(f"  - Paid: ${revenue['paid']:,.2f}")
        print(f"  - Invoices: {revenue['invoice_count']}")

    # Identify bottlenecks
    print("[TOOL] Identifying bottlenecks...")
    bottlenecks = identify_bottlenecks(pending, revenue)
    print(f"  - {len(bottlenecks)} bottlenecks identified")

    # Generate recommendations
    print("[IDEA] Generating recommendations...")
    recommendations = generate_recommendations(pending, revenue, bottlenecks)
    total_recs = (len(recommendations['high']) +
                  len(recommendations['medium']) +
                  len(recommendations['low']))
    print(f"  - {total_recs} recommendations generated")

    # Generate markdown content
    print("[NOTE] Generating briefing markdown...")
    content = generate_briefing_markdown(monday, pending, revenue, bottlenecks, recommendations)

    # Write briefing to file
    print(f"[SAVE] Writing briefing to {briefing_path}...")
    with open(briefing_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] CEO Briefing generated successfully!")
    print(f"[FILE] Location: {briefing_path}")
    print(f"[DATE] Date: {monday.strftime('%B %d, %Y')}")

    # Print summary
    print("\n" + "="*60)
    print("BRIEFING SUMMARY")
    print("="*60)
    print(f"Date: {monday.strftime('%B %d, %Y')}")
    print(f"Revenue: ${revenue['total_revenue']:,.2f} ({revenue['invoice_count']} invoices)")
    print(f"Pending Items: {len(pending['needs_action'])}")
    print(f"Bottlenecks: {len(bottlenecks)}")
    print(f"Recommendations: {total_recs}")
    print("="*60)


if __name__ == "__main__":
    main()
