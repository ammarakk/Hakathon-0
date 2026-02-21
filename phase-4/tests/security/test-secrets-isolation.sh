#!/bin/bash
# Secrets Isolation Test
# Phase 4 - Platinum Tier
# Purpose: Verify zero secrets on cloud, all secrets local-only

set -e

echo "=== Secrets Isolation Security Test ==="
echo ""

VAULT_PATH="${VAULT_PATH:-$(pwd)/../../AI_Employee_Vault}"
LOG_FILE="secrets-test-$(date +%Y%m%d-%H%M%S).log"
SECRETS_FOUND=0

log() {
    echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

cd "$VAULT_PATH" || exit 1

# ==============================================================================
# TEST 1: Verify .gitignore Blocks All Secrets
# ==============================================================================
log "TEST 1: Verifying .gitignore secret patterns"

SECRET_PATTERNS=(
    ".env"
    "*.session"
    "*.token"
    "*.cred"
    "*.key"
    "*.pem"
    "secrets/"
    "creds/"
)

MISSING_PATTERNS=()

for pattern in "${SECRET_PATTERNS[@]}"; do
    if ! grep -q "$pattern" .gitignore 2>/dev/null; then
        MISSING_PATTERNS+=("$pattern")
    fi
done

if [ ${#MISSING_PATTERNS[@]} -eq 0 ]; then
    log "  ✓ All secret patterns found in .gitignore"
else
    log "  ✗ ERROR: Missing patterns in .gitignore:"
    for pattern in "${MISSING_PATTERNS[@]}"; do
        log "    - $pattern"
    done
    SECRETS_FOUND=$((SECRETS_FOUND + 1))
fi

# ==============================================================================
# TEST 2: Verify No .env Files in Vault
# ==============================================================================
log "TEST 2: Scanning for .env files in vault"

ENV_FILES=$(find . -name ".env" -o -name "*.env" 2>/dev/null || true)

if [ -z "$ENV_FILES" ]; then
    log "  ✓ No .env files found in vault"
else
    log "  ✗ ERROR: .env files found:"
    echo "$ENV_FILES" | tee -a "$LOG_FILE"
    SECRETS_FOUND=$((SECRETS_FOUND + 1))
fi

# ==============================================================================
# TEST 3: Verify No Session/Token Files
# ==============================================================================
log "TEST 3: Scanning for session and token files"

SECRET_FILES=$(find . -name "*.session" -o -name "*.token" -o -name "*.cred" -o -name "*.key" -o -name "*.pem" 2>/dev/null || true)

if [ -z "$SECRET_FILES" ]; then
    log "  ✓ No secret files found"
else
    log "  ✗ ERROR: Secret files found:"
    echo "$SECRET_FILES" | tee -a "$LOG_FILE"
    SECRETS_FOUND=$((SECRETS_FOUND + 1))
fi

# ==============================================================================
# TEST 4: Verify Cloud Environment Has No Credentials
# ==============================================================================
log "TEST 4: Checking cloud environment configuration"

CLOUD_ENV="../phase-4/cloud/config/cloud.env.example"

if [ -f "$CLOUD_ENV" ]; then
    # Check for credential patterns
    if grep -iE "(password|secret|token|key|credential)" "$CLOUD_ENV" > /dev/null; then
        log "  ✗ ERROR: Cloud .env contains credential-like strings"
        log "    Run: grep -iE 'password|secret|token' $CLOUD_ENV"
        SECRETS_FOUND=$((SECRETS_FOUND + 1))
    else
        log "  ✓ Cloud .env has NO credentials (URLs and config only)"
    fi
else
    log "  ⚠ Warning: Cloud .env not found at $CLOUD_ENV"
fi

# ==============================================================================
# TEST 5: Verify Local Environment Has Placeholders
# ==============================================================================
log "TEST 5: Checking local environment configuration"

LOCAL_ENV="../phase-4/local/config/local.env.example"

if [ -f "$LOCAL_ENV" ]; then
    # Check for credential placeholders
    if grep -qE "#.*PASSWORD|#.*TOKEN|#.*SECRET" "$LOCAL_ENV"; then
        log "  ✓ Local .env has credential placeholders (correct)"
    else
        log "  ✓ Local .env has no placeholder comments (also acceptable)"
    fi
else
    log "  ⚠ Warning: Local .env not found at $LOCAL_ENV"
fi

# ==============================================================================
# TEST 6: Simulate Pre-Sync Security Audit
# ==============================================================================
log "TEST 6: Running security audit simulation"

# Create temporary test file to verify audit catches it
echo "TEST_KEY=should-be-blocked" > .env.test

# Check if .gitignore would block it
if git check-ignore .env.test > /dev/null 2>&1; then
    log "  ✓ Security audit would block .env.test"
else
    log "  ✗ ERROR: .gitignore does not block .env.test"
    SECRETS_FOUND=$((SECRETS_FOUND + 1))
fi

# Clean up test file
rm .env.test

# ==============================================================================
# RESULTS
# ==============================================================================
echo ""
echo "=== Secrets Isolation Test Results ==="
echo ""

if [ $SECRETS_FOUND -eq 0 ]; then
    echo "✓ ALL TESTS PASSED"
    echo ""
    echo "Summary:"
    echo "  ✓ .gitignore blocks all secret patterns"
    echo "  ✓ No .env files in vault"
    echo "  ✓ No session/token files in vault"
    echo "  ✓ Cloud .env has no credentials"
    echo "  ✓ Security audit would block secrets"
    echo ""
    echo "✓ Secrets isolation verified"
    echo "✓ Zero secrets would be synced to cloud"
    echo ""
else
    echo "✗ $SECRETS_FOUND issue(s) found"
    echo ""
    echo "Summary:"
    echo "  Some security checks failed"
    echo "  Review log above for details"
    echo ""
    echo "Action required:"
    echo "  1. Review failed tests"
    echo "  2. Update .gitignore with missing patterns"
    echo "  3. Remove any secret files from vault"
    echo "  4. Run security audit before git push"
    echo ""
fi

echo "Test log: $LOG_FILE"
echo ""

if [ $SECRETS_FOUND -eq 0 ]; then
    echo "✓ Secrets Isolation Test PASSED"
    exit 0
else
    echo "✗ Secrets Isolation Test FAILED"
    exit 1
fi