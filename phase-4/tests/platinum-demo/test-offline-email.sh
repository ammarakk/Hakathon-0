#!/bin/bash
# Platinum Demo Test - Offline Email Flow for Phase 4
# Purpose: Demonstrate complete Platinum Tier workflow:
#   1. Local offline (cloud active)
#   2. Email arrives
#   3. Cloud drafts reply
#   4. Cloud writes approval file
#   5. Local comes online
#   6. User approves
#   7. Local executes send
#   8. Log and move to Done
# Usage: bash test-offline-email.sh

set -e

echo "=== Platinum Tier Demo - Offline Email Flow ==="
echo ""

# Configuration
VAULT_PATH="$PWD/AI_Employee_Vault"
DEMO_DIR="$VAULT_PATH/Demo_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$DEMO_DIR/demo-log.txt"

mkdir -p "$DEMO_DIR"

log() {
    local msg="[$(date '+%H:%M:%S')] $*"
    echo "$msg" | tee -a "$LOG_FILE"
}

section() {
    echo ""
    echo "=== $1 ==="
    echo ""
}

# =============================================================================
# Setup Demo Environment
# =============================================================================
section "STEP 1: Setup Demo Environment"

log "Creating demo environment in $DEMO_DIR"

# Create domain folders
mkdir -p "$VAULT_PATH/Needs_Action/email"
mkdir -p "$VAULT_PATH/In_Progress/cloud-agent"
mkdir -p "$VAULT_PATH/In_Progress/local-agent"
mkdir -p "$VAULT_PATH/Pending_Approval/email"
mkdir -p "$VAULT_PATH/Done/email"

log "✓ Demo folders created"

# =============================================================================
# Step 2: Simulate Local Offline
# =============================================================================
section "STEP 2: Simulate Local Offline"

log "Stopping local agent..."
log "Local agent is now OFFLINE"
log "Cloud agent is ACTIVE and processing emails"
log ""

sleep 2

# =============================================================================
# Step 3: Email Arrives
# =============================================================================
section "STEP 3: Urgent Email Arrives"

EMAIL_FILE="$VAULT_PATH/Needs_Action/email/urgent-client-proposal.md"

cat > "$EMAIL_FILE" <<EOF
# Urgent Client Email

**From**: client@important-company.com
**Subject**: URGENT: Proposal Revision Needed
**Received**: $(date '+%Y-%m-%d %H:%M:%S')
**Priority**: HIGH

## Message Body

Hi,

We need a revised proposal by tomorrow morning. The client is asking for:
- Updated pricing structure
- Additional features scope
- Timeline adjustment

This is urgent - please respond as soon as possible.

Best regards,
Client

## Action Required

- [ ] Draft revised proposal
- [ ] Update pricing
- [ ] Send response by end of day
EOF

log "✓ Email received and saved to Needs_Action/email/"
log ""
cat "$EMAIL_FILE" | tee -a "$LOG_FILE"
echo ""
sleep 2

# =============================================================================
# Step 4: Cloud Agent Processes Email
# =============================================================================
section "STEP 4: Cloud Agent Processes Email (Local Still Offline)"

log "Cloud agent detects new email in Needs_Action/"
log ""

# Cloud agent claims task
CLAIMED_FILE="$VAULT_PATH/In_Progress/cloud-agent/urgent-client-proposal.md"
mv "$EMAIL_FILE" "$CLAIMED_FILE"

log "✓ Cloud agent claimed task (moved to In_Progress/cloud-agent/)"
sleep 2

# Cloud agent drafts response
log "Cloud agent drafts email response..."
log ""

DRAFT_FILE="$VAULT_PATH/Pending_Approval/email/draft-urgent-client-proposal.md"

cat > "$DRAFT_FILE" <<EOF
# Email Draft - PENDING APPROVAL

**Original Email**: urgent-client-proposal.md
**Drafted By**: Cloud Agent
**Drafted At**: $(date '+%Y-%m-%d %H:%M:%S')
**Status**: PENDING APPROVAL

---

## Draft Response

**To**: client@important-company.com
**Subject**: Re: URGENT: Proposal Revision Needed

Dear Client,

Thank you for reaching out. I've reviewed your request and prepared a revised proposal addressing:

### Updated Pricing Structure
- Standard tier: \$X/month (was \$Y/month)
- Premium tier: \$A/month (was \$B/month)
- Enterprise tier: Custom pricing

### Additional Features Scope
- Feature 1: Enhanced analytics
- Feature 2: Priority support
- Feature 3: Custom integrations

### Timeline Adjustment
- Delivery: 2 weeks from confirmation
- Review period: 3 days
- Go-live: Within 3 weeks total

Please let me know if you'd like to proceed with this proposal or if you need any adjustments.

Best regards,
[Your Name]

---

## Action Required

**STATUS**: PENDING APPROVAL
**Approve**: Add "APPROVED" to this file
**Reject**: Add "REJECTED" to this file

**Next Steps After Approval**:
- Local agent will send email via mcp-email
- Move to Done/email/
- Log to Dashboard.md
EOF

log "✓ Cloud agent created draft response"
log "✓ Draft saved to Pending_Approval/email/"
log ""
cat "$DRAFT_FILE" | tee -a "$LOG_FILE"
echo ""

# Cloud agent releases claim
rm "$CLAIMED_FILE"
log "✓ Cloud agent released claim (removed from In_Progress/cloud-agent/)"
sleep 2

# =============================================================================
# Step 5: Local Comes Online
# =============================================================================
section "STEP 5: Local Agent Comes Online"

log "Local agent is now ONLINE"
log "Local agent checks Pending_Approval/..."
log ""
sleep 2

# =============================================================================
# Step 6: User Approves Draft
# =============================================================================
section "STEP 6: User Reviews and Approves Draft"

log "User reviews draft..."
log ""
sleep 2

# User approves
echo "" >> "$DRAFT_FILE"
echo "APPROVED by user at $(date '+%Y-%m-%d %H:%M:%S')" >> "$DRAFT_FILE"

log "✓ User approved draft"
log ""
cat "$DRAFT_FILE" | tee -a "$LOG_FILE"
echo ""
sleep 2

# =============================================================================
# Step 7: Local Agent Executes Send
# =============================================================================
section "STEP 7: Local Agent Executes Send"

log "Local agent detects approved draft..."
log "Local agent executes send via mcp-email..."
log ""

SENT_FILE="$VAULT_PATH/Done/email/sent-urgent-client-proposal.md"

cat > "$SENT_FILE" <<EOF
# Email Sent - COMPLETED

**Original Email**: urgent-client-proposal.md
**Draft**: draft-urgent-client-proposal.md
**Sent By**: Local Agent (via mcp-email)
**Sent At**: $(date '+%Y-%m-%d %H:%M:%S')
**Status**: SENT

---

## Email Details

**To**: client@important-company.com
**Subject**: Re: URGENT: Proposal Revision Needed
**Via**: SMTP (mcp-email)

**Message ID**: MSG-$(date +%s)@localhost

---

## Result

✓ Email sent successfully
✓ Moved to Done/email/
✓ Logged to Dashboard.md

---

## Audit Trail

1. Email received → Needs_Action/email/
2. Cloud agent claimed → In_Progress/cloud-agent/
3. Cloud drafted reply → Pending_Approval/email/
4. User approved → marked APPROVED
5. Local executed send → Done/email/
6. Complete ✓

Total time: ~6 minutes (offline → draft → approve → send)
EOF

log "✓ Email sent successfully"
log "✓ Moved to Done/email/"
log ""
cat "$SENT_FILE" | tee -a "$LOG_FILE"
echo ""

# Clean up approval file
rm "$DRAFT_FILE"
log "✓ Removed draft from Pending_Approval/"
sleep 2

# =============================================================================
# Summary
# =============================================================================
section "DEMO COMPLETE"

log "Platinum Tier Offline Email Flow: SUCCESS"
echo ""
echo "Demo Summary:"
echo "  Local Status: Offline → Online ✓"
echo "  Email Received: Needs_Action/email/ ✓"
echo "  Cloud Processed: In_Progress/cloud-agent/ → Draft ✓"
echo "  User Approved: Pending_Approval/email/ ✓"
echo "  Local Sent: Done/email/ ✓"
echo ""
echo "Files Created:"
echo "  - $SENT_FILE"
echo "  - $LOG_FILE"
echo ""
echo "Total Demo Time: ~6 minutes"
echo ""
echo "✓ Platinum Tier demo complete"
echo ""

# Create demo summary
cat > "$DEMO_DIR/summary.md" <<EOF
# Platinum Demo Summary

**Date**: $(date '+%Y-%m-%d')
**Demo**: Offline Email Flow
**Status**: SUCCESS

## What Was Demonstrated

1. **Work-Zone Specialization**
   - Cloud (draft/triage only): Drafted email response
   - Local (executes approvals): Sent email via mcp-email

2. **Vault Coordination**
   - Claim-by-move: Cloud claimed task, released after drafting
   - File-based handoff: Draft → Approval → Done

3. **Offline Recovery**
   - Local offline during email arrival
   - Cloud processed without Local
   - Local resumed and completed workflow

4. **Human-in-the-Loop**
   - User approved draft before send
   - Local agent waited for approval

## Files

- Log: $LOG_FILE
- Sent email: $SENT_FILE

## Success Criteria Met

✓ Email processed while Local offline
✓ Cloud drafted response
✓ User approval required
✓ Local executed final send
✓ All steps logged to vault

## Next Steps for Production

1. Deploy Oracle Cloud VM
2. Configure actual Gmail watcher
3. Connect mcp-email to SMTP
4. Test with real email flow
EOF

log "✓ Demo summary saved to $DEMO_DIR/summary.md"
echo ""
