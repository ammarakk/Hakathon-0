#!/bin/bash
# Oracle Cloud Setup Script for Phase 4 - Platinum Tier
# This script documents the steps to provision Oracle Cloud Always Free VM
#
# NOTE: This is a documentation/reference script. Actual execution requires
# manual steps through Oracle Cloud Console or OCI CLI.

set -e

echo "=== Oracle Cloud Setup - Phase 4 Platinum Tier ==="
echo ""
echo "This script documents the Oracle Cloud Always Free VM provisioning"
echo ""

# ============================================================================
# PREREQUISITES
# ============================================================================
echo "PREREQUISITES:"
echo "1. Oracle Cloud Account (free tier): https://www.oracle.com/cloud/free/"
echo "2. Credit card (verification only, no charges for Always Free)"
echo "3. SSH key pair for authentication"
echo ""

# ============================================================================
# STEP 1: Create Oracle Cloud Account
# ============================================================================
echo "STEP 1: Create Oracle Cloud Account"
echo "1. Visit: https://www.oracle.com/cloud/free/"
echo "2. Sign up with email"
echo "3. Verify credit card (for identity verification only)"
echo "4. Wait for account activation (usually 5-10 minutes)"
echo ""

# ============================================================================
# STEP 2: Create Virtual Cloud Network (VCN)
# ============================================================================
echo "STEP 2: Create Virtual Cloud Network"
echo "Using OCI CLI or Console:"
echo ""
echo "oci network vcn create --compartment-id \$COMPARTMENT_ID"
echo "  --cidr-block 10.0.0.0/16"
echo "  --display-name 'ai-employee-vcn'"
echo ""
echo "Or via Console:"
echo "1. Networking → Virtual Cloud Networks"
echo "2. Start VCN Wizard"
echo "3. VCN Name: ai-employee-vcn"
echo "4. CIDR Block: 10.0.0.0/16"
echo "5. Create VCN"
echo ""

# ============================================================================
# STEP 3: Create Security List with Firewall Rules
# ============================================================================
echo "STEP 3: Configure Security List (Firewall Rules)"
echo ""
echo "Required Ingress Rules:"
echo "  - SSH:      TCP 22    from Your IP"
echo "  - HTTP:     TCP 80    from 0.0.0.0/0"
echo "  - HTTPS:    TCP 443   from 0.0.0.0/0"
echo "  - Health:   TCP 8080  from 0.0.0.0/0"
echo "  - Odoo:     TCP 8069  from 0.0.0.0/0 (or restrict to your IP)"
echo ""
echo "Via Console:"
echo "1. Networking → Virtual Cloud Networks → ai-employee-vcn"
echo "2. Security Lists → Default Security List"
echo "3. Add Ingress Rules:"
echo "   - Source: 0.0.0.0/0, IP Protocol: TCP, Dest Port: 22"
echo "   - Source: 0.0.0.0/0, IP Protocol: TCP, Dest Port: 80"
echo "   - Source: 0.0.0.0/0, IP Protocol: TCP, Dest Port: 443"
echo "   - Source: 0.0.0.0/0, IP Protocol: TCP, Dest Port: 8080"
echo "   - Source: 0.0.0.0/0, IP Protocol: TCP, Dest Port: 8069"
echo ""

# ============================================================================
# STEP 4: Create Compute Instance (VM)
# ============================================================================
echo "STEP 4: Provision Compute Instance"
echo ""
echo "OCI CLI Command:"
echo ""
echo "oci compute instance launch --compartment-id \$COMPARTMENT_ID"
echo "  --shape 'VM.Standard.E4.Flex'"
echo "  --shape-config '{\"ocpus\": 4, \"memoryInGBs\": 24}'"
echo "  --source-details '{\"sourceType\": \"image\", \"bootVolumeSizeInGBs\": 50}'"
echo "  --image-id \$UBUNTU_22_04_IMAGE_ID"
echo "  --display-name 'ai-employee-cloud'"
echo "  --ssh-authorized-keys-file ~/.ssh/id_ed25519.pub"
echo "  --subnet-id \$SUBNET_ID"
echo "  --assign-public-ip true"
echo ""
echo "Via Console:"
echo "1. Compute → Instances → Create Instance"
echo "2. Name: ai-employee-cloud"
echo "3. Shape: VM.Standard.E4.Flex (Always Free eligible)"
echo "   - OCPUs: 4 (Always Free limit)"
echo "   - Memory: 24 GB (Always Free limit)"
echo "4. Image: Ubuntu 22.04 Minimal"
echo "5. SSH Key: Upload your public key (~/.ssh/id_ed25519.pub)"
echo "6. Networking: Use existing VCN (ai-employee-vcn)"
echo "7. Create Instance"
echo ""

# ============================================================================
# STEP 5: Verify Instance Creation
# ============================================================================
echo "STEP 5: Verify Instance Creation"
echo ""
echo "Wait for instance to be in 'Running' state (~2-3 minutes)"
echo ""
echo "Get Public IP:"
echo "oci compute instance list --compartment-id \$COMPARTMENT_ID"
echo "  --query 'data[?contains(\"display-name\", \`ai-employee-cloud\`)].\"public-ip\" [0]'"
echo ""
echo "Test SSH Connection:"
echo "ssh -i ~/.ssh/id_ed25519 ubuntu@<PUBLIC_IP>"
echo ""

# ============================================================================
# SUMMARY
# ============================================================================
echo "=== SUMMARY ==="
echo ""
echo "Oracle Cloud Always Free VM provisioned with:"
echo "  - 4 OCPUs (ARM architecture)"
echo "  - 24 GB RAM"
echo "  - Ubuntu 22.04 Minimal"
echo "  - Public IP address"
echo "  - Security rules configured"
echo ""
echo "Next Steps:"
echo "  1. Run install-dependencies.sh"
echo "  2. Run security-hardening.sh"
echo "  3. Setup vault structure"
echo ""
echo "Estimated Monthly Cost: $0 (Always Free tier)"
echo ""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================
echo "=== TROUBLESHOOTING ==="
echo ""
echo "If instance creation fails:"
echo "  - Verify Always Free limits not exceeded"
echo "  - Check compartment permissions"
echo "  - Ensure SSH key is in correct format (OpenSSH)"
echo ""
echo "If SSH connection fails:"
echo "  - Verify security list rules allow port 22 from your IP"
echo "  - Check instance is in 'Running' state"
echo "  - Verify using correct SSH key and username (ubuntu)"
echo ""
echo "For more help, see: phase-4/docs/troubleshooting.md"
echo ""
