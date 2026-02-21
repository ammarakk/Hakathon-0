#!/bin/bash
# Security Audit Script for Phase 4 - Platinum Tier
# Purpose: Pre-sync secret scanning to prevent credentials from being committed
# Usage: Run before git push (integrated into sync-daemon.sh)

set -e

echo "=== Phase 4 Security Audit ==="
echo "Scanning for secrets and sensitive files..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
SECRETS_FOUND=0
FILES_SCANNED=0

# Secret file patterns to check
SECRET_PATTERNS=(
    "\.env$"
    "\.env\."
    "\.session$"
    "\.token$"
    "\.cred$"
    "\.credentials$"
    "\.key$"
    "\.pem$"
    "\.cert$"
    "\.crt$"
    "\.der$"
    "\.keystore$"
    "\.jks$"
    "\.p12$"
    "\.pfx$"
    "secrets/"
    "creds/"
    "credentials/"
    "tokens/"
    "auth/"
    "WhatsApp/"
    "whatsapp/"
    "banking/"
    "payments/"
    "financial/"
)

# Content patterns to check within files
CONTENT_PATTERNS=(
    "AWS_ACCESS_KEY_ID"
    "AWS_SECRET_ACCESS_KEY"
    "AKIA[0-9A-Z]{16}"
    "Bearer\s+[A-Za-z0-9\-._~+/]+=*"
    "Authorization:\s*Bearer"
    "password\s*=\s*['\"][^'\"]+['\"]"
    "PASSWORD\s*=\s*['\"][^'\"]+['\"]"
    "api_key\s*=\s*['\"][^'\"]+['\"]"
    "API_KEY\s*=\s*['\"][^'\"]+['\"]"
    "secret\s*=\s*['\"][^'\"]+['\"]"
    "SECRET\s*=\s*['\"][^'\"]+['\"]"
    "token\s*=\s*['\"][^'\"]+['\"]"
    "TOKEN\s*=\s*['\"][^'\"]+['\"]"
)

# Get list of files to check
# If files are staged for commit, check those
# Otherwise, check all untracked/modified files
if git diff --cached --quiet >/dev/null 2>&1; then
    # No staged files, check working directory
    FILES_TO_CHECK=$(git ls-files --others --modified --exclude-standard)
else
    # Check staged files
    FILES_TO_CHECK=$(git diff --cached --name-only)
fi

# Scan each file
for file in $FILES_TO_CHECK; do
    FILES_SCANNED=$((FILES_SCANNED + 1))

    # Check file name patterns
    for pattern in "${SECRET_PATTERNS[@]}"; do
        if echo "$file" | grep -qE "$pattern"; then
            echo -e "${RED}SECURITY ALERT: Secret file detected: $file${NC}"
            echo "  Pattern matched: $pattern"
            SECRETS_FOUND=$((SECRETS_FOUND + 1))
        fi
    done

    # Check file content (if it's a text file)
    if [ -f "$file" ] && file "$file" | grep -qE "text|ASCII|UTF-8"; then
        for pattern in "${CONTENT_PATTERNS[@]}"; do
            if grep -qE "$pattern" "$file" 2>/dev/null; then
                echo -e "${YELLOW}WARNING: Potential secret content in: $file${NC}"
                echo "  Pattern matched: $pattern"
                echo "  Line(s):"
                grep -nE "$pattern" "$file" | head -3 | sed 's/^/    /'
                SECRETS_FOUND=$((SECRETS_FOUND + 1))
            fi
        done
    fi
done

# Special check: Verify .gitignore exists and contains essential patterns
if [ -f ".gitignore" ]; then
    echo "Checking .gitignore..."

    REQUIRED_PATTERNS=(
        ".env"
        "*.session"
        "*.token"
        "*.key"
        "*.pem"
        "secrets/"
        "creds/"
    )

    for pattern in "${REQUIRED_PATTERNS[@]}"; do
        if ! grep -qF "$pattern" .gitignore; then
            echo -e "${YELLOW}WARNING: .gitignore missing pattern: $pattern${NC}"
        fi
    done
else
    echo -e "${RED}ERROR: .gitignore not found!${NC}"
    SECRETS_FOUND=$((SECRETS_FOUND + 1))
fi

# Report results
echo ""
echo "=== Scan Summary ==="
echo "Files scanned: $FILES_SCANNED"
echo "Secrets found: $SECRETS_FOUND"
echo ""

if [ $SECRETS_FOUND -eq 0 ]; then
    echo -e "${GREEN}✓ Security audit PASSED - No secrets detected${NC}"
    echo ""
    echo "Safe to proceed with git push."
    exit 0
else
    echo -e "${RED}✗ Security audit FAILED - $SECRETS_FOUND issue(s) found${NC}"
    echo ""
    echo "Action required:"
    echo "1. Remove secret files from Git staging:"
    echo "   git reset HEAD <secret-file>"
    echo ""
    echo "2. Add to .gitignore if not already present:"
    echo "   echo '<secret-file>' >> .gitignore"
    echo ""
    echo "3. Rotate any exposed credentials"
    echo ""
    echo "4. Re-run audit before pushing"
    echo ""
    echo "BLOCKING git push for security reasons."
    exit 1
fi
