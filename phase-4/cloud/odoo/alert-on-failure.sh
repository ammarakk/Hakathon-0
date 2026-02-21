#!/bin/bash
# Odoo Alert Script for Phase 4 - Platinum Tier
# Purpose: Send alerts when Odoo health check fails
# Usage: Called by health-check.sh on failure

ALERT_MESSAGE="$1"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/var/log/odoo/alerts.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Log alert
echo "[$TIMESTAMP] ALERT: $ALERT_MESSAGE" >> "$LOG_FILE"

# Option 1: Send email (configure if needed)
# echo "$ALERT_MESSAGE" | mail -s "Odoo Health Alert" admin@yourdomain.com

# Option 2: Write to vault for monitoring
VAULT_ALERT="/vault/Errors/odoo/health-alert-$(date +%Y%m%d-%H%M%S).md"
mkdir -p "$(dirname "$VAULT_ALERT")"
cat > "$VAULT_ALERT" <<EOF
# Odoo Health Alert

**Timestamp**: $TIMESTAMP
**Severity**: HIGH
**Service**: Odoo

## Alert Message

$ALERT_MESSAGE

## Action Required

1. Check Odoo status: \`sudo systemctl status odoo\`
2. Check Odoo logs: \`sudo tail -f /var/log/odoo/odoo.log\`
3. Run health check: \`sudo bash /opt/ai-employee/phase-4/cloud/odoo/health-check.sh\`
4. Restart if needed: \`sudo systemctl restart odoo\`

## System Status

- Host: $(hostname)
- Uptime: $(uptime -p)
- Load: $(uptime | awk -F'load average:' '{print $2}')
- Disk: $(df -h /var/lib/odoo | awk 'NR==2 {print $5 " used"}')
EOF

# Option 3: Send webhook (configure monitoring service)
# curl -X POST https://hooks.example.com/odoo-alert \
#   -H "Content-Type: application/json" \
#   -d "{\"message\": \"$ALERT_MESSAGE\", \"timestamp\": \"$TIMESTAMP\"}"

echo "Alert logged and written to vault: $VAULT_ALERT"
