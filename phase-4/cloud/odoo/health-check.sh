#!/bin/bash
# Odoo Health Check Script for Phase 4 - Platinum Tier
# Purpose: Monitor Odoo service health, database connection, and HTTP endpoint
# Usage: Can be run manually or via monitoring service

set -e

echo "=== Odoo Health Check - Phase 4 Platinum Tier ==="
echo ""

# Configuration
ODOO_HOST="localhost"
ODOO_PORT=8069
ODOO_URL="http://${ODOO_HOST}:${ODOO_PORT}"
ODOO_DB_NAME="odoo"
ODOO_DB_USER="odoo"
LOG_FILE="/var/log/odoo/health-check.log"
ALERT_SCRIPT="/opt/ai-employee/phase-4/cloud/odoo/alert-on-failure.sh"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $*"
    # Optionally send alert
    if [ -f "$ALERT_SCRIPT" ]; then
        bash "$ALERT_SCRIPT" "Odoo health check failed: $*"
    fi
    exit 1
}

# Counters
ERRORS=0
WARNINGS=0

# ==============================================================================
# Check 1: Odoo HTTP Endpoint
# ==============================================================================
echo "Check 1: Testing Odoo HTTP endpoint..."

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$ODOO_URL" 2>/dev/null || echo "000")

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "302" ]; then
    log "✓ Odoo HTTP endpoint responding (status: $HTTP_STATUS)"
else
    log "✗ ERROR: Odoo HTTP endpoint not responding (status: $HTTP_STATUS)"
    ERRORS=$((ERRORS + 1))
fi

# ==============================================================================
# Check 2: PostgreSQL Connection
# ==============================================================================
echo "Check 2: Testing PostgreSQL connection..."

if pg_isready -U $ODOO_DB_USER -d $ODOO_DB_NAME > /dev/null 2>&1; then
    log "✓ PostgreSQL connection successful"
else
    log "✗ ERROR: PostgreSQL connection failed"
    ERRORS=$((ERRORS + 1))
fi

# ==============================================================================
# Check 3: Odoo Process Status
# ==============================================================================
echo "Check 3: Checking Odoo process..."

ODOO_PID=$(pgrep -f "odoo-bin" | head -1)

if [ -n "$ODOO_PID" ]; then
    log "✓ Odoo process running (PID: $ODOO_PID)"

    # Check process uptime
    UPTIME=$(ps -p "$ODOO_PID" -o etimes=)
    log "  Uptime: $UPTIME"

    # Check memory usage
    MEM_USAGE=$(ps -p "$ODOO_PID" -o rss=)
    MEM_MB=$((MEM_USAGE / 1024))
    log "  Memory: ${MEM_MB}MB"
else
    log "✗ ERROR: Odoo process not running"
    ERRORS=$((ERRORS + 1))
fi

# ==============================================================================
# Check 4: System Resources
# ==============================================================================
echo "Check 4: Checking system resources..."

# Disk space
DISK_USAGE=$(df -h /var/lib/odoo | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_AVAILABLE=$(df -h /var/lib/odoo | awk 'NR==2 {print $4}')

log "  Disk usage: $DISK_USAGE"
log "  Available: $DISK_AVAILABLE"

# Check if disk space is low (<10% available)
DISK_PERCENT=$(df /var/lib/odoo | awk 'NR==2 {print $5}' | sed 's/%//')
if [ ${DISK_PERCENT%.*} -lt 10 ]; then
    log "⚠ WARNING: Low disk space (${DISK_PERCENT}% used)"
    WARNINGS=$((WARNINGS + 1))
fi

# ==============================================================================
# Check 5: Recent Odoo Logs
# ==============================================================================
echo "Check 5: Checking Odoo logs for errors..."

ODOO_LOG="/var/log/odoo/odoo.log"

if [ -f "$ODOO_LOG" ]; then
    # Count errors in last 100 lines
    RECENT_ERRORS=$(tail -100 "$ODOO_LOG" 2>/dev/null | grep -i "error" | wc -l)

    if [ "$RECENT_ERRORS" -gt 0 ]; then
        log "⚠ WARNING: Found $RECENT_ERRORS errors in recent logs"
        log "  Run: tail -100 $ODOO_LOG | grep -i error"

        # Check if errors are recent (within last 10 minutes)
        RECENT_ERROR_COUNT=$(tail -100 "$ODOO_LOG" 2>/dev/null | grep -i "error" | grep -c "$(date '+%Y-%m-%d %H')" || true)
        if [ "$RECENT_ERROR_COUNT" -gt 5 ]; then
            log "  ⚠ HIGH error rate in current hour"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        log "✓ No errors found in recent logs"
    fi
else
    log "⚠ WARNING: Odoo log file not found at $ODOO_LOG"
    WARNINGS=$((WARNINGS + 1))
fi

# ==============================================================================
# Summary
# ==============================================================================
echo ""
echo "=== Odoo Health Check Summary ==="
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✓ All checks PASSED"
    echo ""
    echo "Odoo Status: Healthy"
    echo "HTTP: $ODOO_URL"
    echo "Database: Connected"
    echo "Process: Running (PID: $ODOO_PID)"
    echo ""
else
    echo "✗ $ERRORS check(s) FAILED"
    echo ""
    echo "Action Required:"
    if ! pgrep -f "odoo-bin" > /dev/null; then
        echo "  - Restart Odoo: sudo systemctl restart odoo"
    fi
    if [ "$HTTP_STATUS" != "200" ] && [ "$HTTP_STATUS" != "302" ]; then
        echo "  - Check Nginx: sudo systemctl status nginx"
    fi
    echo ""
fi

if [ $WARNINGS -gt 0 ]; then
    echo "⚠ $WARNINGS warning(s)"
    echo ""
fi

# Log health status to log file
if [ $ERRORS -eq 0 ]; then
    log "Health Status: Healthy"
else
    log "Health Status: Degraded"
fi

echo "Health check log: $LOG_FILE"
echo ""

# Exit with appropriate code
if [ $ERRORS -eq 0 ]; then
    exit 0
else
    exit 1
fi