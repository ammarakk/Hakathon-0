---
description: Finance watcher for monitoring banking APIs and CSV exports for transaction logging.
---

# COMMAND: Finance Watcher Implementation

## CONTEXT

The user needs to implement a finance watcher that:

- Monitors banking APIs for new transactions
- Processes CSV exports from bank statements
- Logs transactions in /Accounting/Current_Month.md
- Supports multiple banking integrations

## YOUR ROLE

Act as a Python developer with expertise in:

- Banking API integration (Plaid, GoCardless, etc.)
- CSV parsing and data validation
- Financial transaction categorization
- Secure credential handling

## OUTPUT STRUCTURE

Create a finance watcher implementation with:

1. **Banking API integration** (Plaid example)
2. **CSV import** for bank statements
3. **Transaction logging** in Accounting directory
4. **Categorization** with rules-based system
5. **Setup instructions** for banking services

## Step 1: Finance Watcher Implementation

```python
#!/usr/bin/env python3
"""
Finance Watcher - Monitor banking APIs and CSV exports

This watcher monitors financial transactions via banking APIs or CSV exports
and logs them in the Accounting directory for review and reconciliation.
"""

import asyncio
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

# Optional API imports (install as needed)
# import plaid
# from plaid.api import plaid_api
# from plaid.model.transactions_get_request import TransactionsGetRequest

from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FinanceWatcher")


class FinanceWatcher(BaseWatcher):
    """
    Watcher for monitoring financial transactions.

    Supports both banking API integration and CSV file monitoring
    for transaction logging and categorization.
    """

    def __init__(
        self,
        vault_path: Path,
        accounting_dir: Optional[Path] = None,
        check_interval: int = 3600,  # Check hourly
        api_mode: bool = False,
        csv_directories: Optional[List[Path]] = None,
        categorization_rules: Optional[Dict[str, List[str]]] = None
    ):
        """
        Initialize the finance watcher.

        Args:
            vault_path: Path to shared vault directory
            accounting_dir: Path to accounting directory (default: vault/Accounting)
            check_interval: Seconds between checks (default: 3600)
            api_mode: Use banking API if True, CSV mode if False
            csv_directories: List of directories to monitor for CSV files
            categorization_rules: Rules for auto-categorizing transactions
        """
        super().__init__(
            name="FinanceWatcher",
            vault_path=vault_path,
            check_interval=check_interval
        )
        self.accounting_dir = accounting_dir or (self.vault_path / "Accounting")
        self.accounting_dir.mkdir(parents=True, exist_ok=True)

        self.api_mode = api_mode
        self.csv_directories = csv_directories or []
        self.categorization_rules = categorization_rules or self._default_rules()

        # Transaction tracking
        self.seen_transactions: Dict[str, datetime] = {}
        self.current_month_file = self._get_current_month_file()

        # API client (initialized if api_mode is True)
        self.api_client = None

    def _default_rules(self) -> Dict[str, List[str]]:
        """Default categorization rules."""
        return {
            'Software & SaaS': ['github', 'aws', 'google', 'microsoft', 'adobe', 'slack', 'zoom'],
            'Office Expenses': ['staples', 'office depot', 'amazon business'],
            'Travel': ['airbnb', 'uber', 'lyft', 'airline', 'hotel', 'marriott', 'hilton'],
            'Marketing': ['facebook', 'google ads', 'linkedin', 'twitter'],
            'Utilities': ['electric', 'water', 'gas', 'internet', 'phone'],
            'Insurance': ['insurance', 'geico', 'progressive'],
            'Payroll': ['payroll', 'salary', 'wage'],
            'Legal & Professional': ['legal', 'attorney', 'accounting', 'consulting'],
            'Banking Fees': ['bank fee', 'atm fee', 'overdraft', 'wire transfer'],
            'Income': ['deposit', 'payment received', 'invoice paid', 'client'],
        }

    def _get_current_month_file(self) -> Path:
        """Get the current month's accounting file."""
        month_str = datetime.now().strftime("%Y_%m")
        filename = f"{month_str}.md"
        return self.accounting_dir / filename

    async def _setup_api_client(self):
        """Setup banking API client (example: Plaid)."""
        try:
            # Example with Plaid (requires: pip install plaid-python)
            # import plaid
            # from plaid.api import plaid_api
            # from plaid.model.transactions_get_request import TransactionsGetRequest
            # from plaid.model.country_code import CountryCode

            # configuration = plaid.Configuration(
            #     host=plaid.Environment.Sandbox,
            #     api_key={
            #         'clientId': os.getenv('PLAID_CLIENT_ID'),
            #         'secret': os.getenv('PLAID_SECRET'),
            #     }
            # )
            # api_client = plaid_api.PlaidApi(plaid.ApiClient(configuration))
            # self.api_client = api_client

            logger.info("Banking API client setup successful")
            return True

        except ImportError:
            logger.warning("Plaid SDK not installed. Run: pip install plaid-python")
            return False
        except Exception as e:
            logger.error(f"API client setup failed: {e}")
            return False

    async def check(self) -> List[Dict[str, Any]]:
        """
        Check for new transactions.

        Returns:
            List of transaction item dictionaries
        """
        items = []

        if self.api_mode:
            # Fetch from banking API
            items.extend(await self._fetch_from_api())
        else:
            # Parse from CSV files
            items.extend(await self._parse_csv_files())

        logger.info(f"Found {len(items)} new transactions")
        return items

    async def _fetch_from_api(self) -> List[Dict[str, Any]]:
        """Fetch transactions from banking API."""
        if not self.api_client:
            if not await self._setup_api_client():
                return []

        try:
            # Example with Plaid API
            # request = TransactionsGetRequest(
            #     access_token=os.getenv('PLAID_ACCESS_TOKEN'),
            #     start_date=(datetime.now() - timedelta(days=30)).date(),
            #     end_date=datetime.now().date(),
            # )
            # response = self.api_client.transactions_get(request)
            # transactions = response['transactions']

            # For now, return empty list (implement based on your API)
            logger.warning("API mode not fully implemented")
            return []

        except Exception as e:
            logger.error(f"Error fetching from API: {e}")
            return []

    async def _parse_csv_files(self) -> List[Dict[str, Any]]:
        """Parse transaction CSV files from monitored directories."""
        items = []

        for directory in self.csv_directories:
            directory = Path(directory)
            if not directory.exists():
                continue

            # Find CSV files modified in last 24 hours
            for csv_file in directory.glob("*.csv"):
                # Check if file was recently modified
                mtime = datetime.fromtimestamp(csv_file.stat().st_mtime)
                if datetime.now() - mtime > timedelta(days=1):
                    continue

                try:
                    transactions = self._parse_csv(csv_file)
                    items.extend(transactions)
                except Exception as e:
                    logger.error(f"Error parsing {csv_file}: {e}")

        return items

    def _parse_csv(self, csv_path: Path) -> List[Dict[str, Any]]:
        """
        Parse a bank statement CSV file.

        Expected CSV format (adjust based on your bank's format):
        Date, Description, Amount, Type, Balance

        Args:
            csv_path: Path to CSV file

        Returns:
            List of transaction dictionaries
        """
        transactions = []

        with open(csv_path, 'r', encoding='utf-8') as f:
            # Detect delimiter
            sample = f.read(1024)
            f.seek(0)
            delimiter = ',' if ',' in sample else '\t' if '\t' in sample else ';'

            reader = csv.DictReader(f, delimiter=delimiter)

            for row in reader:
                try:
                    # Normalize row keys
                    row = {k.strip().lower(): v for k, v in row.items()}

                    # Extract common fields (adjust based on your CSV format)
                    date_str = row.get('date') or row.get('transaction date') or row.get('datum')
                    description = row.get('description') or row.get('description') or row.get('beschreibung') or ''
                    amount_str = row.get('amount') or row.get('betrag') or '0'
                    trans_type = row.get('type') or row.get('transaction type') or 'unknown'

                    # Clean amount string
                    amount_str = amount_str.replace(',', '.').replace('€', '').replace('$', '').strip()
                    amount = float(amount_str) if amount_str else 0.0

                    # Create unique ID
                    transaction_id = f"{date_str}_{description[:30]}_{amount}".replace(' ', '_')
                    transaction_id = transaction_id.replace('/', '-')

                    # Skip if already seen
                    if transaction_id in self.seen_transactions:
                        continue

                    transaction = {
                        'id': f"finance_{hash(transaction_id) % 1000000:06d}",
                        'timestamp': date_str,
                        'source': 'BankCSV',
                        'data': {
                            'date': date_str,
                            'description': description,
                            'amount': amount,
                            'type': trans_type,
                            'csv_file': str(csv_path),
                        },
                        'metadata': {
                            'raw_row': row,
                        }
                    }

                    transactions.append(transaction)
                    self.seen_transactions[transaction_id] = datetime.now()

                except Exception as e:
                    logger.debug(f"Error parsing row: {e}")
                    continue

        return transactions

    async def process_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a transaction and categorize it.

        Args:
            item: Raw transaction item

        Returns:
            Processed transaction or None
        """
        description = item['data']['description'].lower()
        amount = item['data']['amount']
        trans_type = item['data']['type']

        # Categorize transaction
        category = self._categorize_transaction(description, amount)

        # Determine priority
        priority = 'high' if amount > 1000 else 'medium'

        return {
            'title': f"Transaction: {item['data']['description'][:50]}",
            'content': f"Amount: ${amount:,.2f}\nType: {trans_type}\nCategory: {category}",
            'action_type': 'transaction_review',
            'priority': priority,
            'metadata': {
                'source_id': item['id'],
                'date': item['data']['date'],
                'description': item['data']['description'],
                'amount': amount,
                'type': trans_type,
                'category': category,
                'csv_file': item['data'].get('csv_file', ''),
            }
        }

    def _categorize_transaction(self, description: str, amount: float) -> str:
        """
        Categorize a transaction based on description and amount.

        Args:
            description: Transaction description (lowercase)
            amount: Transaction amount

        Returns:
            Category name
        """
        # Check against rules
        for category, keywords in self.categorization_rules.items():
            if any(keyword in description for keyword in keywords):
                return category

        # Income detection
        if amount > 0:
            return 'Income'

        # Default category
        return 'Uncategorized'

    async def create_action_file(self, item: Dict[str, Any]) -> Path:
        """
        Create a transaction entry in the current month's accounting file.

        Args:
            item: Processed transaction item

        Returns:
            Path to the accounting file
        """
        # Ensure month file exists with header
        if not self.current_month_file.exists():
            self._create_month_file()

        # Append transaction to file
        with open(self.current_month_file, 'a', encoding='utf-8') as f:
            amount = item['metadata']['amount']
            amount_str = f"+${amount:,.2f}" if amount >= 0 else f"-${abs(amount):,.2f}"

            f.write(f"\n### {item['metadata']['date']} - {item['metadata']['description'][:50]}\n")
            f.write(f"**Amount:** {amount_str}  \n")
            f.write(f"**Category:** {item['metadata']['category']}  \n")
            f.write(f"**Type:** {item['metadata']['type']}  \n")
            f.write(f"**Status:** ❌ Unreviewed  \n")
            f.write(f"**Notes:**  \n")
            f.write("\n")

        logger.info(f"Logged transaction to {self.current_month_file}")

        # Also create individual action file for review
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_desc = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in item['metadata']['description'])
        action_filename = f"{timestamp}_transaction_{safe_desc[:30]}.md"
        action_filepath = self.needs_action_dir / action_filename

        content = f"""# {item['title']}

**Source:** Finance Watcher
**Date:** {item['metadata']['date']}
**Amount:** {item['metadata']['amount']:,.2f}
**Category:** {item['metadata']['category']}
**Type:** {item['metadata']['type']}
**Priority:** {item['priority'].upper()}

## Actions Required
- [ ] Verify transaction details
- [ ] Assign correct category if needed
- [ ] Add notes or receipt reference
- [ ] Mark as reviewed in Accounting file

## Notes
-

---
*Logged in: `{self.current_month_file.relative_to(self.vault_path)}`*
*Created by FinanceWatcher at {datetime.now().isoformat()}*
"""

        action_filepath.write_text(content, encoding='utf-8')
        return action_filepath

    def _create_month_file(self):
        """Create the current month's accounting file with header."""
        month_name = datetime.now().strftime("%B %Y")

        content = f"""# Accounting - {month_name}

**Period:** {datetime.now().strftime("%Y-%m")}
**Status:** Active

## Summary
- **Total Income:** $0.00
- **Total Expenses:** $0.00
- **Net:** $0.00

## Transactions

### Income

### Expenses

---

*Last updated: {datetime.now().isoformat()}*
"""

        self.current_month_file.write_text(content, encoding='utf-8')
        logger.info(f"Created new month file: {self.current_month_file}")


async def main():
    """Main entry point for running the finance watcher."""
    import os

    vault_path = Path(os.getenv("VAULT_PATH", "./vault"))
    csv_dirs = os.getenv("CSV_DIRECTORIES", "./bank_exports").split(",")

    watcher = FinanceWatcher(
        vault_path=vault_path,
        check_interval=3600,  # Check hourly
        api_mode=False,  # Set True for API mode
        csv_directories=[Path(d.strip()) for d in csv_dirs],
        categorization_rules={
            'Software & SaaS': ['github', 'aws', 'google', 'microsoft'],
            'Office Expenses': ['staples', 'office', 'amazon'],
            'Travel': ['airbnb', 'uber', 'hotel', 'airline'],
        }
    )

    await watcher.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Setup Instructions

### Prerequisites

1. **Install Dependencies**
```bash
# For API mode (Plaid example)
pip install plaid-python

# For CSV mode only
# No additional dependencies needed
```

2. **Create Directory Structure**
```bash
mkdir -p ./vault/Accounting
mkdir -p ./bank_exports
```

3. **Configure Environment**
```bash
export VAULT_PATH=/path/to/vault
export CSV_DIRECTORIES="./bank_exports,./another_bank/exports"

# For API mode
export PLAID_CLIENT_ID=your_client_id
export PLAID_SECRET=your_secret
export PLAID_ACCESS_TOKEN=your_access_token
```

### CSV File Format

The watcher expects CSV files with these columns (case-insensitive):
- `Date` - Transaction date
- `Description` - Transaction description
- `Amount` - Transaction amount (positive for income, negative for expenses)
- `Type` - Transaction type (optional)
- `Balance` - Account balance (optional)

Example:
```csv
Date,Description,Amount,Type,Balance
2024-01-15,Amazon Web Services,-150.00,Debit,5000.00
2024-01-16,Client Payment,2500.00,Credit,7500.00
```

### Running the Watcher

```bash
# CSV mode
python finance_watcher.py

# API mode (requires credentials)
# Edit script to set api_mode=True
python finance_watcher.py
```

## Configuration Examples

### Custom Categorization Rules

```python
watcher = FinanceWatcher(
    vault_path=vault_path,
    categorization_rules={
        'Software & SaaS': ['github', 'aws', 'digitalocean', 'heroku'],
        'Marketing': ['facebook', 'google ads', 'linkedin ads'],
        'Payroll': ['payroll', 'salary', 'wage'],
        'Client Payments': ['client', 'invoice', 'payment received'],
    }
)
```

### API Integration (Plaid Example)

```python
# Set api_mode=True in watcher initialization
watcher = FinanceWatcher(
    vault_path=vault_path,
    api_mode=True,
    check_interval=3600
)
```

## ACCEPTANCE CRITERIA

- Monitors CSV directories for new bank exports
- Logs transactions in monthly accounting file
- Categorizes transactions based on rules
- Prevents duplicate transaction logging
- Handles various CSV formats

## FOLLOW-UPS

- Add support for Plaid API integration
- Implement receipt attachment matching
- Create monthly summary reports
- Add transaction approval workflow

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.
