#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
SA_NAME="datadog-integration"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
KEY_FILE="config/keys/datadog-sa-key.json"

echo "🚀 Setting up Datadog GCP Integration for project: $PROJECT_ID"

# 1. Create Service Account
if ! gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; then
    echo "Creating service account: $SA_NAME..."
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="Datadog Integration Service Account"
else
    echo "Service account $SA_NAME already exists."
fi

# 2. Assign Roles
# Roles required by Datadog for metric collection
ROLES=(
    "roles/compute.viewer"
    "roles/monitoring.viewer"
    "roles/cloudasset.viewer"
    "roles/iam.serviceAccountTokenCreator"
)

echo "Assigning IAM roles..."
for role in "${ROLES[@]}"; do
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:$SA_EMAIL" \
        --role="$role" \
        --condition=None \
        --quiet > /dev/null
    echo "  - Assigned $role"
done

# 3. Generate Key
echo "Generating service account key..."
mkdir -p config/keys
if [ -f "$KEY_FILE" ]; then
    echo "  Key file already exists at $KEY_FILE. Skipping generation."
else
    gcloud iam service-accounts keys create "$KEY_FILE" \
        --iam-account="$SA_EMAIL"
    echo "  Key saved to $KEY_FILE"
fi

# 4. Enable APIs
echo "Enabling required APIs..."
gcloud services enable cloudasset.googleapis.com --quiet

echo "✅ Datadog Integration Setup Complete!"
echo "---------------------------------------------------"
echo "👉 NEXT STEP: Go to Datadog > Integrations > Google Cloud Platform"
echo "👉 Upload the file: $KEY_FILE"
echo "---------------------------------------------------"
