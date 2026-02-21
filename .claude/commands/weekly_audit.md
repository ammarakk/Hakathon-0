---
description: Weekly business and accounting audit to generate CEO Briefing reports.
---

# COMMAND: Weekly CEO Briefing & Audit

## CONTEXT

Generate weekly CEO Briefing reports by analyzing:

- Accounting transactions and revenue
- Pending action items
- Task completion status
- Business bottlenecks and risks
- Recommendations for the week

## YOUR ROLE

Act as a business analyst with expertise in:

- Financial analysis
- Business metrics
- Executive reporting
- Strategic recommendations

## IMPLEMENTATION

```python
#!/usr/bin/env python3
"""
Weekly CEO Briefing Generator

Analyzes vault data and generates executive summary reports.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weekly_audit")


class WeeklyCEOBriefing:
    """Generate weekly executive briefing."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.accounting_dir = vault_path / "Accounting"
        self.needs_action_dir = vault_path / "Needs_Action"
        self.plans_dir = vault_path / "Plans"
        self.done_dir = vault_path / "Done"
        self.logs_dir = vault_path / "Logs"
        self.updates_dir = vault_path / "Updates"

    def analyze_accounting(self) -> Dict:
        """Analyze accounting records."""
        transactions = []
        total_income = 0
        total_expenses = 0

        for file in self.accounting_dir.glob("*.md"):
            content = file.read_text()
            # Extract transactions
            for match in re.finditer(r'\$\s*([\d,]+\.?\d*)', content):
                amount = float(match.group(1).replace(',', ''))
                if 'income' in content.lower() or 'revenue' in content.lower():
                    total_income += amount
                else:
                    total_expenses += amount

        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net': total_income - total_expenses,
            'profit_margin': (total_income - total_expenses) / total_income * 100 if total_income > 0 else 0
        }

    def count_pending_actions(self) -> Dict:
        """Count and categorize pending actions."""
        actions = {
            'total': 0,
            'high_priority': 0,
            'by_source': {}
        }

        for file in self.needs_action_dir.glob("*.md"):
            content = file.read_text()
            actions['total'] += 1

            # Check priority
            if '**priority:** high' in content.lower():
                actions['high_priority'] += 1

            # Extract source
            source_match = re.search(r'\*\*source:\*\*\s*(\w+)', content, re.IGNORECASE)
            if source_match:
                source = source_match.group(1)
                actions['by_source'][source] = actions['by_source'].get(source, 0) + 1

        return actions

    def identify_bottlenecks(self) -> List[str]:
        """Identify business bottlenecks."""
        bottlenecks = []

        # Check high priority items
        for file in self.needs_action_dir.glob("*.md"):
            content = file.read_text()
            if '**priority:** high' in content.lower():
                bottlenecks.append(f"High priority item: {file.stem}")

        # Check old pending items
        week_ago = datetime.now() - timedelta(days=7)
        for file in self.needs_action_dir.glob("*.md"):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime < week_ago:
                bottlenecks.append(f"Stale item: {file.stem} (from {mtime.strftime('%Y-%m-%d')})")

        return bottlenecks[:10]  # Top 10

    def generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate business recommendations."""
        recommendations = []

        # Financial recommendations
        if analysis['accounting']['profit_margin'] < 20:
            recommendations.append("⚠️ Review pricing strategy - margin below 20%")

        if analysis['actions']['high_priority'] > 5:
            recommendations.append("⚡ Address high priority items - backlog growing")

        if len(analysis['bottlenecks']) > 10:
            recommendations.append("🔄 Consider automation for recurring bottlenecks")

        recommendations.append("📊 Schedule monthly financial review")
        recommendations.append("💬 Conduct team sync on blocking issues")

        return recommendations

    def generate_briefing(self) -> str:
        """Generate full CEO briefing."""
        week_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        week_end = datetime.now().strftime("%Y-%m-%d")

        accounting = self.analyze_accounting()
        actions = self.count_pending_actions()
        bottlenecks = self.identify_bottlenecks()

        analysis = {
            'accounting': accounting,
            'actions': actions,
            'bottlenecks': bottlenecks
        }

        recommendations = self.generate_recommendations(analysis)

        briefing = f"""# Monday Morning CEO Briefing

**Week:** {week_start} to {week_end}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 Financial Summary

| Metric | Value |
|--------|-------|
| Total Income | ${accounting['total_income']:,.2f} |
| Total Expenses | ${accounting['total_expenses']:,.2f} |
| Net Profit | ${accounting['net']:,.2f} |
| Profit Margin | {accounting['profit_margin']:.1f}% |

---

## 📋 Action Items Overview

- **Total Pending:** {actions['total']}
- **High Priority:** {actions['high_priority']}

**By Source:**
{chr(10).join(f"- {s}: {c}" for s, c in actions['by_source'].items())}

---

## 🚧 Bottlenecks & Blockers

{chr(10).join(f"{i+1}. {b}" for i, b in enumerate(bottlenecks[:5]))}

---

## 💡 Recommendations

{chr(10).join(f"{i+1}. {r}" for i, r in enumerate(recommendations))}

---

## 📈 This Week's Focus

1. Address high-priority items
2. Review financial performance
3. Clear stale action items
4. Update strategic plans

---

*Generated by WeeklyCEOBriefing*
"""

        return briefing

    def save_briefing(self) -> Path:
        """Save briefing to Updates directory."""
        filename = f"CEO_Briefing_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = self.updates_dir / filename
        filepath.write_text(self.generate_briefing())
        logger.info(f"CEO Briefing saved: {filepath}")
        return filepath


async def main():
    """Generate weekly briefing."""
    vault_path = Path("./vault")
    briefing_gen = WeeklyCEOBriefing(vault_path)
    filepath = briefing_gen.save_briefing()
    print(f"✓ Briefing generated: {filepath}")


if __name__ == "__main__":
    asyncio.run(main())
```

## ACCEPTANCE CRITERIA

- Analyzes accounting transactions
- Counts and categorizes pending actions
- Identifies bottlenecks
- Generates actionable recommendations
- Creates formatted CEO briefing

## FOLLOW-UPS

- Add trend analysis over weeks
- Include employee productivity metrics
- Add competitor tracking
- Create action item tracking
