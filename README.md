# Ouroboros AI Resilience Platform

**Autonomous AI Resilience System for Enterprise Agent Infrastructure**

[![Status](https://img.shields.io/badge/status-in_development-yellow)]()
[![Phase](https://img.shields.io/badge/phase-1_infrastructure-blue)]()
[![Timeline](https://img.shields.io/badge/timeline-168h_hackathon-red)]()

---

## 🎯 Overview

Ouroboros is an autonomous AI resilience platform that detects and remediates catastrophic failure modes in enterprise AI agent systems. It acts as an **immune system for AI infrastructure**, automatically detecting infinite loops, semantic drift, and runaway costs—then healing them without human intervention.

**The Problem**: Multi-agent AI systems fail in unpredictable ways. A single trapped agent can burn **$3,000+ per hour** in API costs while grinding operations to a halt.

**The Solution**: Ouroboros combines deep observability (Datadog), generative AI (Google Vertex AI), and event-driven architecture (Confluent Kafka) to detect pathological behavior within **30 seconds** and execute autonomous remediation.

---

## ✨ Key Features

- **🔍 Autonomous Loop Detection**: Detects infinite reasoning loops using semantic similarity analysis (95% threshold, 5 consecutive turns)
- **💉 The Antidote**: Automatically injects system instruction overrides to break loops
- **⚡ Circuit Breaker**: Suspends agents exceeding cost thresholds ($100 limit)
- **📊 Real-Time Observability**: Full trace capture of agent reasoning with Datadog LLM Observability
- **🎨 Neon Dashboard**: Cyberpunk-themed Next.js dashboard with live remediation feed
- **🔄 Event Streaming**: Kafka-based audit trail for forensic analysis and replay
- **💰 Cost Prevention**: Prevents runaway API costs with token velocity monitoring

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OUROBOROS ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐      ┌──────────────┐      ┌────────────┐ │
│  │   Vertex AI │      │   Datadog    │      │  Confluent │ │
│  │ Agent Engine│─────▶│ Observability│─────▶│   Kafka    │ │
│  │  (Brain)    │      │  (Nervous    │      │ (Memory)   │ │
│  └─────────────┘      │   System)    │      └────────────┘ │
│         │             └──────────────┘             │        │
│         │                     │                    │        │
│         │                     ▼                    │        │
│         │             ┌──────────────┐             │        │
│         │             │   Webhook    │             │        │
│         │             │   Triggers   │             │        │
│         │             └──────────────┘             │        │
│         │                     │                    │        │
│         ▼                     ▼                    ▼        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Google Cloud Functions (Effector Arms)        │  │
│  │  ┌──────────────┐              ┌─────────────────┐   │  │
│  │  │inject-antidote│              │circuit-breaker  │   │  │
│  │  └──────────────┘              └─────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Design Philosophy**: Tripartite organism pattern
- **Brain** (Vertex AI): Agent reasoning and execution
- **Nervous System** (Datadog): Observability and alerting
- **Memory** (Kafka): Durable event log and audit trail

---

## 🚀 Quick Start

### Prerequisites

- Google Cloud Platform account with billing
- Datadog account (14-day trial acceptable)
- Confluent Cloud account (free tier)
- Python 3.11+, Node.js 18+, gcloud CLI

### Installation

```bash
# Clone the repository
cd /home/ugrads/majors/arnavpant27/oroboros

# Step 1: Create GCP project and enable billing
cd infrastructure/gcp
chmod +x create-project.sh
./create-project.sh

# Step 2: Load environment variables
source ../../config/gcp-project.env

# Step 3: Verify setup
gcloud projects describe $GCP_PROJECT_ID
```

**Next Steps**: See [SETUP.md](docs/SETUP.md) for complete installation guide.

---

## 📋 Project Structure

```
oroboros/
├── infrastructure/          # GCP and Terraform setup
│   ├── gcp/
│   │   ├── create-project.sh        # Task 1.1 ✅
│   │   ├── enable-apis.sh           # Task 1.2 (next)
│   │   └── service-accounts.sh      # Task 1.3 (next)
│   └── terraform/                   # IaC configuration
├── agents/                  # FinBot test agent
│   └── finbot/
│       ├── agent_config.py          # Vertex AI config
│       ├── tools.py                 # Custom tools
│       └── poison_prompts.py        # Test prompts
├── observability/          # Datadog integration
│   ├── datadog_tracer.py           # LLM tracing
│   ├── semantic_analyzer.py        # Loop detection
│   └── monitors/                   # Alert configs
├── functions/              # Cloud Functions (remediation)
│   ├── inject-antidote/            # The Antidote
│   └── circuit-breaker/            # Agent suspension
├── kafka/                  # Event streaming
│   ├── schemas/                    # Avro schemas
│   ├── producers/                  # Event publishers
│   └── consumers/                  # Audit processors
├── dashboard/              # Next.js frontend (neon theme)
│   ├── app/                        # App Router pages
│   ├── src/components/             # React components
│   └── tailwind.config.ts          # Neon theme config
├── api/                    # FastAPI backend
│   ├── routers/                    # API endpoints
│   └── services/                   # Business logic
├── tests/                  # Test suite
│   ├── unit/                       # Unit tests
│   ├── integration/                # E2E tests
│   └── load/                       # Load testing
├── config/                 # Configuration files
│   ├── gcp-project.env             # GCP settings ✅
│   └── .env.example                # Template
├── docs/                   # Documentation
│   └── SETUP.md                    # Setup guide ✅
└── tasks/                  # Project management
    ├── prd-ouroboros-ai-resilience.md
    └── tasks-prd-ouroboros-ai-resilience.md
```

---

## 🎯 Success Metrics (Demo Day)

- ✅ **Detection Speed**: <30 seconds from loop onset to detection
- ✅ **Remediation Success**: 3/3 auto-heals during live demo
- ✅ **Cost Savings**: Dashboard shows "$127 saved by auto-remediation"
- ✅ **Zero Human Intervention**: Fully autonomous healing

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Runtime** | Google Vertex AI Agent Engine | Multi-agent orchestration |
| **Observability** | Datadog LLM Observability | Trace capture & alerting |
| **Event Streaming** | Confluent Kafka | Durable audit log |
| **Remediation** | Google Cloud Functions | Serverless auto-healing |
| **Frontend** | Next.js 14 + React 18 | Neon cyberpunk dashboard |
| **Backend API** | FastAPI | Metrics & agent data |
| **Secrets** | Google Secret Manager | Secure credential storage |

---

## 📊 Current Status

**Phase**: 1 - Infrastructure Foundation (Hours 0-48)  
**Progress**: Task 1.1 Complete ✅

| Phase | Status | Tasks Complete |
|-------|--------|----------------|
| Phase 1: Infrastructure | 🟡 In Progress | 1/12 |
| Phase 2: Agent Development | ⚪ Not Started | 0/14 |
| Phase 3: Remediation | ⚪ Not Started | 0/14 |
| Phase 4: Kafka Streaming | ⚪ Not Started | 0/11 |
| Phase 5: Dashboard & Demo | ⚪ Not Started | 0/29 |

---

## 📖 Documentation

- [Setup Guide](docs/SETUP.md) - Step-by-step installation
- [PRD](tasks/prd-ouroboros-ai-resilience.md) - Product requirements
- [Task List](tasks/tasks-prd-ouroboros-ai-resilience.md) - Implementation roadmap
- Architecture Guide (coming in Phase 2)
- API Documentation (coming in Phase 3)
- Frontend Guide (coming in Phase 5)

---

## 🤝 Contributing

This is a hackathon project for the **AI Partner Catalyst** event.

**Development Workflow**:
1. Follow the task list in `tasks/tasks-prd-ouroboros-ai-resilience.md`
2. One sub-task at a time (per process guidelines)
3. Commit after each completed parent task
4. Run tests before committing

---

## 🔐 Security

- All secrets stored in Google Secret Manager
- Service accounts use least-privilege IAM roles
- No API keys committed to Git
- Audit logs enabled for all API calls

---

## 💰 Cost Estimate

**7-Day Hackathon Budget**: $25-60

| Service | Cost |
|---------|------|
| Vertex AI (Gemini 1.5 Pro) | $20-50 |
| Cloud Functions | $5-10 |
| Datadog Trial | $0 |
| Confluent Kafka Free Tier | $0 |

**Cost Control**: $100 circuit breaker prevents runaway costs

---

## 📅 Timeline

**Total**: 168 hours (7 days)

- **Phase 1** (Hours 0-48): Infrastructure setup
- **Phase 2** (Hours 49-96): Agent development & observability
- **Phase 3** (Hours 97-120): Autonomous remediation
- **Phase 4** (Hours 121-144): Kafka event streaming
- **Phase 5** (Hours 145-168): Dashboard & demo prep

---

## 📧 Contact

**Project**: Ouroboros AI Resilience Platform  
**Event**: AI Partner Catalyst Hackathon  
**Date**: December 22, 2025

---

## 📄 License

This is a hackathon POC project. Not licensed for production use.

---

**Built with ❤️ for the AI Partner Catalyst Hackathon**

*"The snake that eats its own tail—regenerating infinitely."*
