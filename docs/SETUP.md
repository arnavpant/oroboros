# Ouroboros AI Resilience Platform - Setup Guide

**Last Updated**: December 22, 2025  
**Timeline**: 168 hours (7 days)  
**Current Phase**: Phase 1 - Infrastructure Foundation

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Infrastructure Setup](#phase-1-infrastructure-setup)
3. [Phase 2: Agent Development](#phase-2-agent-development)
4. [Phase 3: Remediation System](#phase-3-remediation-system)
5. [Phase 4: Kafka Streaming](#phase-4-kafka-streaming)
6. [Phase 5: Dashboard & Demo](#phase-5-dashboard--demo)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have the following:

### Required Software

- **Google Cloud SDK** (`gcloud` CLI)
  - Install: https://cloud.google.com/sdk/docs/install
  - Version: Latest stable
  
- **Python 3.11+**
  - Check: `python3 --version`
  - Install: https://www.python.org/downloads/

- **Node.js 18+** (for Dashboard)
  - Check: `node --version`
  - Install: https://nodejs.org/

- **Git**
  - Check: `git --version`

- **Terraform** (optional, for IaC)
  - Install: https://developer.hashicorp.com/terraform/downloads

### Required Accounts

- **Google Cloud Platform**
  - Active GCP account with billing enabled
  - Organization admin access (or project creator permissions)
  - Billing account with available credits

- **Datadog**
  - Free trial or active subscription
  - LLM Observability enabled
  - API and App keys

- **Confluent Cloud**
  - Free tier account
  - Kafka cluster access

### Local Environment

```bash
# Clone the repository (if not already done)
cd /home/ugrads/majors/arnavpant27/oroboros

# Verify prerequisites
gcloud --version
python3 --version
node --version
git --version
```

---

## Phase 1: Infrastructure Setup

### Task 1.1: Create Google Cloud Project and Enable Billing ✅

**Objective**: Set up the foundational GCP project for Ouroboros

**Steps**:

1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Run the project creation script**:
   ```bash
   cd infrastructure/gcp
   chmod +x create-project.sh
   ./create-project.sh
   ```

   The script will:
   - Create a new GCP project with ID: `ouroboros-ai-resilience-<timestamp>`
   - Link your billing account
   - Set default region to `us-central1`
   - Save configuration to `config/gcp-project.env`

3. **Load environment variables**:
   ```bash
   source ../../config/gcp-project.env
   echo $GCP_PROJECT_ID  # Verify it's set
   ```

4. **Verify project creation**:
   ```bash
   gcloud projects describe $GCP_PROJECT_ID
   ```

   Expected output:
   ```
   createTime: '2025-12-22T...'
   lifecycleState: ACTIVE
   name: Ouroboros AI Resilience Platform
   projectId: ouroboros-ai-resilience-...
   ```

5. **Check billing status**:
   ```bash
   gcloud billing projects describe $GCP_PROJECT_ID
   ```

   Expected output should show: `billingEnabled: true`

**Configuration File**: `config/gcp-project.env`

```bash
export GCP_PROJECT_ID="ouroboros-ai-resilience-1234567890"
export GCP_PROJECT_NAME="Ouroboros AI Resilience Platform"
export GCP_REGION="us-central1"
export GCP_ZONE="us-central1-a"
export GCP_BILLING_ACCOUNT="XXXXXX-XXXXXX-XXXXXX"
```

**Troubleshooting**:

- **Error: "User does not have permission to create projects"**
  - Solution: Ask your organization admin for `resourcemanager.projects.create` permission
  - Alternative: Have admin create the project and grant you owner access

- **Error: "Billing account not found"**
  - Solution: Run `gcloud billing accounts list` to find your billing account ID
  - Ensure you have `billing.accounts.get` permission

- **Error: "Project ID already exists"**
  - Solution: Project IDs are globally unique. The script generates a unique ID with timestamp
  - You can set a custom ID: `export PROJECT_ID=ouroboros-yourname` before running

**Success Criteria**:
- ✅ GCP project created and active
- ✅ Billing enabled and linked
- ✅ Configuration file generated
- ✅ Default region/zone set to `us-central1`/`us-central1-a`

**Estimated Time**: 10-15 minutes

---

### Task 1.2: Enable Required GCP APIs ✅

**Objective**: Enable all necessary Google Cloud APIs for the platform

**APIs to Enable**:
- Vertex AI API (`aiplatform.googleapis.com`) - Agent runtime with Gemini models
- Cloud Functions API (`cloudfunctions.googleapis.com`) - Autonomous remediation logic
- Secret Manager API (`secretmanager.googleapis.com`) - Secure credential storage
- Cloud Build API (`cloudbuild.googleapis.com`) - Function deployment pipeline
- Cloud Resource Manager API (`cloudresourcemanager.googleapis.com`) - Project management
- IAM API (`iam.googleapis.com`) - Service account management
- Cloud Logging API (`logging.googleapis.com`) - Audit trails and debugging
- Cloud Monitoring API (`monitoring.googleapis.com`) - Metrics collection

**Steps**:

1. **Ensure environment variables are loaded**:
   ```bash
   source config/gcp-project.env
   echo $GCP_PROJECT_ID  # Should display your project ID
   ```

2. **Run the API enablement script**:
   ```bash
   cd infrastructure/gcp
   chmod +x enable-apis.sh
   ./enable-apis.sh
   ```

   The script will:
   - Verify project is active and billing is enabled
   - Enable all 8 required APIs
   - Verify critical APIs (Vertex AI, Cloud Functions, Secret Manager)
   - Save API state to `config/apis-enabled.txt`
   - Wait 30 seconds for API propagation

3. **Verify APIs are enabled**:
   ```bash
   gcloud services list --enabled --filter="aiplatform OR cloudfunctions"
   ```

   Expected output should show:
   ```
   NAME                              TITLE
   aiplatform.googleapis.com         Vertex AI API
   cloudfunctions.googleapis.com     Cloud Functions API
   secretmanager.googleapis.com      Secret Manager API
   ...
   ```

4. **Test Vertex AI access**:
   ```bash
   gcloud ai models list --region=$GCP_REGION 2>&1 | head -5
   ```

   If successful, you should see model listings (or "Listed 0 items" if none deployed yet)

**What Each API Does**:

| API | Purpose in Ouroboros | Phase Used |
|-----|---------------------|------------|
| **Vertex AI** | Runs FinBot agent with Gemini 1.5 Pro, handles agent updates for remediation | Phase 2, 3 |
| **Cloud Functions** | Hosts `inject-antidote` and `circuit-breaker` serverless functions | Phase 3 |
| **Secret Manager** | Stores Datadog API keys, Kafka credentials securely (no .env files!) | Phase 1-5 |
| **Cloud Build** | Builds and deploys Cloud Functions from source code | Phase 3 |
| **IAM** | Creates service accounts with least-privilege permissions | Phase 1 |
| **Logging** | Captures function execution logs, agent traces | Phase 2-5 |
| **Monitoring** | Collects metrics for cost tracking and performance | Phase 4-5 |

**Troubleshooting**:

- **Error: "Billing is not enabled on this project"**
  - Solution: Complete Task 1.1 first or run `gcloud billing projects link $GCP_PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT`

- **Error: "User does not have permission to enable APIs"**
  - Solution: You need `serviceusage.services.enable` permission
  - Ask project owner to grant you `roles/serviceusage.serviceUsageAdmin`

- **Error: "API enablement failed for aiplatform.googleapis.com"**
  - Solution: Check quota limits in [Quotas page](https://console.cloud.google.com/iam-admin/quotas)
  - Some organizations restrict Vertex AI access - contact admin

- **Warning: "API may take time to propagate"**
  - This is normal! The script waits 30 seconds automatically
  - If issues persist, wait 2-3 minutes before proceeding

**Success Criteria**:
- ✅ All 8 APIs enabled without errors
- ✅ Critical APIs verified (Vertex AI, Cloud Functions, Secret Manager)
- ✅ API state saved to `config/apis-enabled.txt`
- ✅ `gcloud services list --enabled` shows all required APIs

**Cost Impact**:
- **API enablement**: $0 (free to enable)
- **API usage**: Billed separately in later phases
  - Vertex AI: ~$20-50 for hackathon
  - Cloud Functions: ~$5-10
  - Other APIs: Minimal (<$1)

**Estimated Time**: 5-10 minutes (including propagation wait)

---

### Task 1.3: Create Service Accounts with IAM Roles

**Objective**: Set up service accounts for agent execution and Cloud Functions

**Service Accounts**:
- `ouroboros-agent-runner@...` (for Vertex AI agents)
- `ouroboros-remediation@...` (for Cloud Functions)
- `ouroboros-kafka-producer@...` (for event streaming)

**Steps**: See `infrastructure/gcp/service-accounts.sh` (Task 1.3)

---

## Quick Start Commands

```bash
# Complete Phase 1 setup in sequence
cd /home/ugrads/majors/arnavpant27/oroboros

# Task 1.1: Create project
infrastructure/gcp/create-project.sh
source config/gcp-project.env

# Task 1.2: Enable APIs (when ready)
# infrastructure/gcp/enable-apis.sh

# Task 1.3: Create service accounts (when ready)
# infrastructure/gcp/service-accounts.sh

# Verify setup
gcloud config list
gcloud projects describe $GCP_PROJECT_ID
```

---

## Environment Variables Reference

All environment variables are stored in `config/gcp-project.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `GCP_PROJECT_ID` | Unique GCP project identifier | `ouroboros-ai-resilience-1703260800` |
| `GCP_PROJECT_NAME` | Human-readable project name | `Ouroboros AI Resilience Platform` |
| `GCP_REGION` | Default compute region | `us-central1` |
| `GCP_ZONE` | Default compute zone | `us-central1-a` |
| `GCP_BILLING_ACCOUNT` | Billing account ID | `01234A-56789B-CDEFGH` |

**Always source this file** before running commands:
```bash
source config/gcp-project.env
```

---

## Security Best Practices

1. **Never commit secrets to Git**:
   - `config/gcp-project.env` is git-ignored
   - Use Google Secret Manager for API keys

2. **Use least-privilege IAM**:
   - Service accounts have minimal required permissions
   - No owner roles on service accounts

3. **Enable audit logging**:
   - All API calls are logged via Cloud Audit Logs
   - Review logs regularly: `gcloud logging read`

4. **Rotate credentials**:
   - Service account keys should be rotated every 90 days
   - Use Workload Identity when possible (Phase 3 feature)

---

## Cost Management

**Expected Costs** (7-day hackathon):

| Service | Estimated Cost |
|---------|----------------|
| Vertex AI (Gemini 1.5 Pro) | $20-50 |
| Cloud Functions | $5-10 |
| Datadog Trial | $0 (14-day trial) |
| Confluent Kafka Free Tier | $0 |
| **Total** | **$25-60** |

**Cost Control Measures**:
- Set up budget alerts at $50 and $75
- Use `$100` circuit breaker (REQ-REM-02)
- Monitor token consumption daily

**Set a budget alert**:
```bash
# Create budget (after Task 1.2)
gcloud billing budgets create \
  --billing-account=$GCP_BILLING_ACCOUNT \
  --display-name="Ouroboros Hackathon Budget" \
  --budget-amount=100 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=75 \
  --threshold-rule=percent=90
```

---

## Next Steps

After completing Task 1.1:

1. ✅ **Verify** project is active: `gcloud projects list`
2. ➡️ **Proceed** to Task 1.2: Enable APIs
3. 📖 **Read** the PRD: `tasks/prd-ouroboros-ai-resilience.md`
4. 🎯 **Review** task list: `tasks/tasks-prd-ouroboros-ai-resilience.md`

---

## Support & Resources

- **GCP Documentation**: https://cloud.google.com/docs
- **Vertex AI Agents**: https://cloud.google.com/vertex-ai/docs/agents
- **Datadog LLM Observability**: https://docs.datadoghq.com/llm_observability/
- **Confluent Kafka**: https://docs.confluent.io/cloud/

---

**Last Updated**: December 22, 2025  
**Status**: Task 1.1 Complete ✅
