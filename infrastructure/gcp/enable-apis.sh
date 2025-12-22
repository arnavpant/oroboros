#!/bin/bash
# Ouroboros AI Resilience Platform - Enable GCP APIs Script
# This script enables all required Google Cloud APIs for the platform
# 
# Prerequisites:
# - GCP project created (Task 1.1 complete)
# - gcloud CLI authenticated
# - Billing enabled on the project
# - Project environment variables loaded (source config/gcp-project.env)

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   Ouroboros AI Resilience Platform - API Setup        ║${NC}"
echo -e "${CYAN}║   Task 1.2: Enable Required GCP APIs                  ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if project environment variables are loaded
if [ -z "$GCP_PROJECT_ID" ]; then
    echo -e "${RED}❌ Error: GCP_PROJECT_ID not set${NC}"
    echo "   Please run: source ../../config/gcp-project.env"
    exit 1
fi

echo -e "${YELLOW}📋 Project Configuration:${NC}"
echo "  Project ID: $GCP_PROJECT_ID"
echo "  Region:     $GCP_REGION"
echo ""

# Verify project exists and is active
echo -e "${CYAN}🔍 Verifying project status...${NC}"
if ! gcloud projects describe "$GCP_PROJECT_ID" --format="value(lifecycleState)" 2>/dev/null | grep -q "ACTIVE"; then
    echo -e "${RED}❌ Project $GCP_PROJECT_ID is not active or doesn't exist${NC}"
    echo "   Please run Task 1.1 first: ./create-project.sh"
    exit 1
fi

echo -e "${GREEN}✓ Project is active${NC}"

# Verify billing is enabled
echo -e "${CYAN}💳 Checking billing status...${NC}"
BILLING_ENABLED=$(gcloud billing projects describe "$GCP_PROJECT_ID" --format="value(billingEnabled)" 2>/dev/null || echo "false")

if [ "$BILLING_ENABLED" != "True" ]; then
    echo -e "${RED}❌ Billing is not enabled on this project${NC}"
    echo "   APIs cannot be enabled without billing"
    echo "   Please complete Task 1.1 or manually enable billing"
    exit 1
fi

echo -e "${GREEN}✓ Billing is enabled${NC}"
echo ""

# Define required APIs
declare -A APIS
APIS=(
    ["aiplatform.googleapis.com"]="Vertex AI API (Agent Engine, Gemini Models)"
    ["cloudfunctions.googleapis.com"]="Cloud Functions API (Remediation Logic)"
    ["secretmanager.googleapis.com"]="Secret Manager API (Credential Storage)"
    ["cloudbuild.googleapis.com"]="Cloud Build API (Function Deployment)"
    ["cloudresourcemanager.googleapis.com"]="Cloud Resource Manager API (Project Management)"
    ["iam.googleapis.com"]="IAM API (Service Account Management)"
    ["logging.googleapis.com"]="Cloud Logging API (Audit Trails)"
    ["monitoring.googleapis.com"]="Cloud Monitoring API (Metrics)"
)

echo -e "${CYAN}🔨 Enabling APIs...${NC}"
echo ""

# Track progress
TOTAL_APIS=${#APIS[@]}
CURRENT=0
ENABLED_COUNT=0
ALREADY_ENABLED=0
FAILED_COUNT=0

# Enable each API
for api in "${!APIS[@]}"; do
    ((CURRENT++))
    description="${APIS[$api]}"
    
    echo -e "${MAGENTA}[$CURRENT/$TOTAL_APIS]${NC} ${api}"
    echo "         ${description}"
    
    # Check if already enabled
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" 2>/dev/null | grep -q "$api"; then
        echo -e "         ${YELLOW}⚠ Already enabled${NC}"
        ((ALREADY_ENABLED++))
    else
        # Enable the API
        if gcloud services enable "$api" --project="$GCP_PROJECT_ID" 2>/dev/null; then
            echo -e "         ${GREEN}✓ Enabled successfully${NC}"
            ((ENABLED_COUNT++))
        else
            echo -e "         ${RED}✗ Failed to enable${NC}"
            ((FAILED_COUNT++))
        fi
    fi
    
    echo ""
done

# Summary
echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              API Enablement Summary                    ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓ Newly Enabled:      $ENABLED_COUNT${NC}"
echo -e "${YELLOW}⚠ Already Enabled:    $ALREADY_ENABLED${NC}"

if [ $FAILED_COUNT -gt 0 ]; then
    echo -e "${RED}✗ Failed:             $FAILED_COUNT${NC}"
    echo ""
    echo -e "${RED}⚠ Warning: Some APIs failed to enable${NC}"
    echo "  This may cause issues in later phases"
    echo "  Check permissions and billing status"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All APIs enabled successfully!${NC}"

# Verify critical APIs
echo ""
echo -e "${CYAN}🔍 Verifying critical APIs...${NC}"

CRITICAL_APIS=(
    "aiplatform.googleapis.com"
    "cloudfunctions.googleapis.com"
    "secretmanager.googleapis.com"
)

ALL_CRITICAL_ENABLED=true

for api in "${CRITICAL_APIS[@]}"; do
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" 2>/dev/null | grep -q "$api"; then
        echo -e "${GREEN}✓${NC} $api"
    else
        echo -e "${RED}✗${NC} $api - ${RED}CRITICAL API NOT ENABLED${NC}"
        ALL_CRITICAL_ENABLED=false
    fi
done

echo ""

if [ "$ALL_CRITICAL_ENABLED" = false ]; then
    echo -e "${RED}❌ Critical APIs are missing${NC}"
    echo "   Cannot proceed without these APIs"
    exit 1
fi

# Save API enablement state
CONFIG_FILE="../../config/apis-enabled.txt"
echo -e "${CYAN}💾 Saving API state to $CONFIG_FILE${NC}"

cat > "$CONFIG_FILE" << EOF
# Ouroboros GCP APIs - Enabled on $(date)
# Project: $GCP_PROJECT_ID

EOF

for api in "${!APIS[@]}"; do
    echo "$api" >> "$CONFIG_FILE"
done

echo -e "${GREEN}✓ API state saved${NC}"

# Display next steps
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              Setup Complete! 🎉                         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Enabled APIs Summary:${NC}"
echo "  🤖 Vertex AI API         → Agent runtime (FinBot)"
echo "  ⚡ Cloud Functions API   → Autonomous remediation"
echo "  🔐 Secret Manager API    → Secure credential storage"
echo "  🔨 Cloud Build API       → Function deployment"
echo "  👥 IAM API               → Service account management"
echo "  📊 Logging/Monitoring    → Observability stack"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Verify APIs: ${CYAN}gcloud services list --enabled${NC}"
echo "  2. Run Task 1.3: ${CYAN}./infrastructure/gcp/service-accounts.sh${NC}"
echo "  3. Test Vertex AI: ${CYAN}gcloud ai models list --region=$GCP_REGION${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: APIs may take 1-2 minutes to fully propagate${NC}"
echo ""
echo -e "${YELLOW}📊 View enabled APIs in console:${NC}"
echo "   https://console.cloud.google.com/apis/dashboard?project=$GCP_PROJECT_ID"
echo ""

# Optional: Wait for API propagation
echo -e "${YELLOW}⏳ Waiting 30 seconds for API propagation...${NC}"
sleep 30
echo -e "${GREEN}✓ Ready to proceed${NC}"
echo ""
