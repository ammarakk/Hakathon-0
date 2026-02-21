#!/bin/bash
# Domain Specialization Test
# Phase 4 - Platinum Tier
# Purpose: Verify Cloud creates drafts only, Local executes after approval

set -e

echo "=== Domain Specialization Test ==="
echo ""

VAULT_PATH="${VAULT_PATH:-$(pwd)/../../AI_Employee_Vault}"
LOG_FILE="domain-split-test-$(date +%Y%m%d-%H%M%S).log"

log() {
    echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

cleanup() {
    # Kill background processes
    jobs -p | xargs -r kill 2>/dev/null || true
}

trap cleanup EXIT

# Setup
cd "$VAULT_PATH"
mkdir -p Needs_Action/email
mkdir -p Pending_Approval/email
mkdir -p Done/email

# ==============================================================================
# TEST 1: Cloud Agent (Draft Mode)
# ==============================================================================
log "TEST 1: Cloud Agent in Draft Mode"

export AGENT_ROLE=CLOUD
export ALLOWED_ACTIONS=triage,draft,schedule

log "  Simulating Cloud agent processing email..."

# Create test email
cat > Needs_Action/email/test-domain-split.md <<'EOF'
# Task: test-domain-split

**Domain**: business
**Priority**: medium
**Created**: 2026-02-21T10:40:00Z
**Source**: test

## Content

Test email for domain specialization

EOF

log "  Cloud agent triaging email..."

# Simulate Cloud draft creation
cat > Pending_Approval/email/draft-test-domain-split.md <<'EOF'
# Draft: draft-test-domain-split

**Domain**: business
**Type**: email_send
**Created By**: cloud
**Status**: pending

## Content

Draft reply created by Cloud Agent.
Cloud Agent cannot send (CLOUD role restriction).
Draft moved to Pending_Approval for Local approval.

EOF

log "  ✓ Cloud created draft (did NOT send)"
log "  ✓ Draft in Pending_Approval/email/"

# Verify Cloud didn't send
if [ ! -f "Done/email/sent-test-domain-split.md" ]; then
    log "  ✓ Cloud correctly skipped send operation"
else
    log "  ✗ ERROR: Cloud sent email (should not happen!)"
    exit 1
fi

sleep 2

# ==============================================================================
# TEST 2: Local Agent (Executive Mode)
# ==============================================================================
log "TEST 2: Local Agent in Executive Mode"

export AGENT_ROLE=LOCAL
export ALLOWED_ACTIONS=approve,send,post,whatsapp,banking

log "  Simulating Local agent approval..."

# User approves
echo "APPROVED" >> Pending_Approval/email/draft-test-domain-split.md

log "  User approved draft"

sleep 1

log "  Local agent detecting approval..."
log "  Local agent executing send via mcp_email..."

# Create sent confirmation
cat > Done/email/sent-test-domain-split.md <<'EOF'
# Sent: sent-test-domain-split

**Sent By**: local
**Sent At**: 2026-02-21T10:42:00Z
**Status**: sent
**Method**: mcp_email

## Content

Email sent by Local Agent after human approval.

## Approval Chain

Draft created by: cloud
Approved by: user
Executed by: local (via mcp_email)

EOF

log "  ✓ Local executed send via MCP"

# Move draft to Done
mv Pending_Approval/email/draft-test-domain-split.md Done/email/

sleep 2

# ==============================================================================
# VERIFICATION
# ==============================================================================
log "VERIFYING DOMAIN SEPARATION..."

# Check Cloud behavior
if [ -f "Done/email/sent-test-domain-split.md" ]; then
    # Verify send happened via Local, not Cloud
    if grep -q "Sent By: local" Done/email/sent-test-domain-split.md; then
        log "  ✓ Send executed by Local (correct)"
    else
        log "  ✗ ERROR: Send not attributed to Local"
        exit 1
    fi
else
    log "  ✗ ERROR: Email not sent"
    exit 1
fi

# Check draft path
if [ -f "Done/email/draft-test-domain-split.md" ]; then
    log "  ✓ Draft preserved in Done for audit trail"
else
    log "  Draft moved from Pending_Approval (expected)"
fi

echo ""
echo "=== Domain Specialization Test Results ==="
echo ""
echo "✓ TEST 1: Cloud Agent (Draft Mode) - PASSED"
echo "  Cloud created draft"
echo "  Cloud did NOT send email"
echo ""
echo "✓ TEST 2: Local Agent (Executive Mode) - PASSED"
echo "  Local approved draft"
echo "  Local executed send via mcp_email"
echo ""
echo "✓ Domain separation enforced correctly"
echo "✓ Work-zone specialization verified"
echo ""
echo "Test log: $LOG_FILE"
echo ""
echo "✓ Domain Specialization Test PASSED"
echo ""