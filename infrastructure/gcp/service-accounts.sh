#!/bin/bash
# Ouroboros AI Resilience Platform - Service Account Setup
# Task 1.3: Create service accounts with IAM roles

set -e

# Color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   Ouroboros AI Resilience Platform - IAM Setup        ║${NC}"
echo -e "${CYAN}║   Task 1.3: Create Service Accounts                   ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ -z "$GCP_PROJECT_ID" ]; then
    echo "Error: GCP_PROJECT_ID not set. Run 'source ../../config/gcp-project.env'"
    exit 1
fi

# 1. Agent Runner Service Account
SA_NAME="ouroboros-agent-runner"
SA_EMAIL="$SA_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"
echo -e "${CYAN}Creating $SA_NAME...${NC}"

if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$GCP_PROJECT_ID" &>/dev/null; then
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="Ouroboros Agent Runner" \
        --project="$GCP_PROJECT_ID"
    echo -e "${GREEN}✓ Created $SA_NAME${NC}"
else
    echo -e "${GREEN}✓ $SA_NAME already exists${NC}"
fi

# Grant roles to Agent Runner
# Needs Vertex AI User role
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.user" \
    --condition=None &>/dev/null
echo -e "${GREEN}✓ Granted roles/aiplatform.user to $SA_NAME${NC}"


# 2. Remediation Service Account (Cloud Functions)
SA_NAME="ouroboros-remediation"
SA_EMAIL="$SA_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"
echo -e "${CYAN}Creating $SA_NAME...${NC}"

if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$GCP_PROJECT_ID" &>/dev/null; then
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="Ouroboros Remediation Function" \
        --project="$GCP_PROJECT_ID"
    echo -e "${GREEN}✓ Created $SA_NAME${NC}"
else
    echo -e "${GREEN}✓ $SA_NAME already exists${NC}"
fi

# Grant roles to Remediation SA
# Needs to invoke Vertex AI and manage agents
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.user" \
    --condition=None &>/dev/null
# Needs to write logs
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/logging.logWriter" \
    --condition=None &>/dev/null
echo -e "${GREEN}✓ Granted roles to $SA_NAME${NC}"


# 3. Kafka Producer Service Account
SA_NAME="ouroboros-kafka-producer"
SA_EMAIL="$SA_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"
echo -e "${CYAN}Creating $SA_NAME...${NC}"

if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$GCP_PROJECT_ID" &>/dev/null; then
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="Ouroboros Kafka Producer" \
        --project="$GCP_PROJECT_ID"
    echo -e "${GREEN}✓ Created $SA_NAME${NC}"
else
    echo -e "${GREEN}✓ $SA_NAME already exists${NC}"
fi

# Grant roles to Kafka Producer
# Needs Secret Manager Access to get Kafka credentials
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/secretmanager.secretAccessor" \
    --condition=None &>/dev/null
echo -e "${GREEN}✓ Granted roles to $SA_NAME${NC}"

echo ""
echo -e "${GREEN}✅ Task 1.3 Complete: Service Accounts Created${NC}"
