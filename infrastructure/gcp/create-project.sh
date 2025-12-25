#!/bin/bash
# Ouroboros AI Resilience Platform - GCP Project Setup Script
# This script creates a new GCP project and enables billing
# 
# Prerequisites:
# - gcloud CLI installed and authenticated (gcloud auth login)
# - Billing account access
# - Organization/folder permissions (if applicable)

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   Ouroboros AI Resilience Platform - GCP Setup        ║${NC}"
echo -e "${CYAN}║   Task 1.1: Create Project and Enable Billing         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration variables
PROJECT_ID="${PROJECT_ID:-ouroboros-ai-$(date +%Y%m%d%H%M%S)}"
PROJECT_NAME="${PROJECT_NAME:-Ouroboros AI}"
REGION="${REGION:-us-central1}"
ZONE="${ZONE:-us-central1-a}"

echo -e "${YELLOW}📋 Project Configuration:${NC}"
echo "  Project ID:   $PROJECT_ID"
echo "  Project Name: $PROJECT_NAME"
echo "  Region:       $REGION"
echo "  Zone:         $ZONE"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: gcloud CLI is not installed${NC}"
    echo "   Please install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✓ gcloud CLI found${NC}"

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}⚠ Not authenticated. Running: gcloud auth login${NC}"
    gcloud auth login
fi

ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
echo -e "${GREEN}✓ Authenticated as: $ACTIVE_ACCOUNT${NC}"

# List available billing accounts
echo ""
echo -e "${YELLOW}📊 Fetching available billing accounts...${NC}"
BILLING_ACCOUNTS=$(gcloud billing accounts list --format="table(name,displayName,open)" 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error fetching billing accounts${NC}"
    echo "   Make sure you have billing permissions"
    exit 1
fi

echo "$BILLING_ACCOUNTS"
echo ""

# Prompt for billing account (or use environment variable)
if [ -z "$BILLING_ACCOUNT_ID" ]; then
    echo -e "${YELLOW}Please enter your Billing Account ID:${NC}"
    echo "(Format: XXXXXX-XXXXXX-XXXXXX)"
    read -r BILLING_ACCOUNT_ID
fi

# Validate billing account
if ! gcloud billing accounts describe "$BILLING_ACCOUNT_ID" &> /dev/null; then
    echo -e "${RED}❌ Invalid billing account: $BILLING_ACCOUNT_ID${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Billing account validated: $BILLING_ACCOUNT_ID${NC}"

# Create the project
echo ""
echo -e "${CYAN}🔨 Creating GCP project: $PROJECT_ID${NC}"

if gcloud projects describe "$PROJECT_ID" &> /dev/null; then
    echo -e "${YELLOW}⚠ Project $PROJECT_ID already exists${NC}"
    read -p "Do you want to use this existing project? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Aborted. Please choose a different PROJECT_ID${NC}"
        exit 1
    fi
else
    gcloud projects create "$PROJECT_ID" \
        --name="$PROJECT_NAME" \
        --set-as-default

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Project created successfully${NC}"
    else
        echo -e "${RED}❌ Failed to create project${NC}"
        exit 1
    fi
fi

# Link billing account to project
echo ""
echo -e "${CYAN}💳 Linking billing account to project...${NC}"

gcloud billing projects link "$PROJECT_ID" \
    --billing-account="$BILLING_ACCOUNT_ID"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Billing enabled successfully${NC}"
else
    echo -e "${RED}❌ Failed to enable billing${NC}"
    exit 1
fi

# Set default project
gcloud config set project "$PROJECT_ID"
gcloud config set compute/region "$REGION"
gcloud config set compute/zone "$ZONE"

echo -e "${GREEN}✓ Default project set to: $PROJECT_ID${NC}"

# Save project configuration
CONFIG_FILE="../../config/gcp-project.env"
echo ""
echo -e "${CYAN}💾 Saving configuration to $CONFIG_FILE${NC}"

cat > "$CONFIG_FILE" <<EOF
# Ouroboros GCP Project Configuration
# Generated on: $(date)

export GCP_PROJECT_ID="$PROJECT_ID"
export GCP_PROJECT_NAME="$PROJECT_NAME"
export GCP_REGION="$REGION"
export GCP_ZONE="$ZONE"
export GCP_BILLING_ACCOUNT="$BILLING_ACCOUNT_ID"

# Source this file to set environment variables:
# source config/gcp-project.env
EOF

echo -e "${GREEN}✓ Configuration saved${NC}"

# Display summary
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              Setup Complete! 🎉                         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Project Details:${NC}"
echo "  📦 Project ID:        $PROJECT_ID"
echo "  💳 Billing Account:   $BILLING_ACCOUNT_ID"
echo "  🌍 Region:            $REGION"
echo "  📍 Zone:              $ZONE"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Source the config file: ${CYAN}source config/gcp-project.env${NC}"
echo "  2. Run Task 1.2: ${CYAN}./infrastructure/gcp/enable-apis.sh${NC}"
echo "  3. Verify project: ${CYAN}gcloud projects describe $PROJECT_ID${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: You can view your project in the console:${NC}"
echo "   https://console.cloud.google.com/home/dashboard?project=$PROJECT_ID"
echo ""
