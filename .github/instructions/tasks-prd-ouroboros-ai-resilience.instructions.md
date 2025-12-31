---
name: Project_Tasks
applyTo: "**"
---

# Task List: Ouroboros AI Resilience Platform

**Based on**: `prd-ouroboros-ai-resilience.md`  
**Target Timeline**: 168 hours (7 days)  
**Current State**: Greenfield project - no existing infrastructure

---

## Current State Assessment

**Existing Infrastructure**: None - This is a new project from scratch.

**What Needs to Be Built**:
- Google Cloud Platform infrastructure (Vertex AI, Cloud Functions, Secret Manager)
- Datadog observability integration with LLM tracing
- Confluent Kafka event streaming setup
- Test AI agent ("FinBot") with intentional failure scenarios
- Autonomous remediation logic (Cloud Functions)
- Dashboard for monitoring and cost tracking
- Complete integration testing pipeline

**Architecture Pattern**: Event-driven microservices with serverless remediation layer

**Key Technologies**:
- **Backend**: Python 3.11+, Google Cloud SDK
- **AI Platform**: Google Vertex AI Agent Engine
- **Observability**: Datadog LLM Observability SDK, Datadog ASM
- **Event Streaming**: Confluent Kafka (Cloud)
- **Compute**: Google Cloud Functions (serverless)
- **Secrets**: Google Secret Manager
- **IaC**: Terraform (recommended) or gcloud CLI

---

## Relevant Files

### Infrastructure & Configuration
- `infrastructure/terraform/main.tf` - Main Terraform configuration for GCP resources
- `infrastructure/terraform/variables.tf` - Terraform variables for project configuration
- `infrastructure/terraform/outputs.tf` - Terraform outputs (service URLs, topic names, etc.)
- `infrastructure/gcp/enable-apis.sh` - Script to enable required GCP APIs
- `infrastructure/gcp/service-accounts.sh` - Script to create and configure service accounts
- `infrastructure/gcp/datadog-integration.sh` - Script to setup Datadog GCP integration
- `config/.env.example` - Environment variables template
- `config/.env` - Local environment variables (gitignored)
- `config/datadog.yaml` - Datadog agent configuration
- `config/kafka-topics.json` - Kafka topic definitions and schemas

### FinBot Test Agent
- `agents/finbot/agent_config.py` - Vertex AI agent configuration and initialization
- `agents/finbot/tools.py` - Custom tools for the FinBot agent (market data, portfolio analysis)
- `agents/finbot/prompts.py` - System instructions and prompt templates
- `agents/finbot/poison_prompts.py` - Test prompts designed to trigger infinite loops
- `agents/finbot/main.py` - Main agent execution entry point
- `agents/finbot/requirements.txt` - Python dependencies for FinBot

### Observability & Tracing
- `observability/datadog_tracer.py` - Datadog LLM Observability SDK integration
- `observability/metrics_collector.py` - Custom metrics collection (token velocity, cost tracking)
- `observability/semantic_analyzer.py` - Vector embedding and similarity calculation for loop detection
- `observability/monitors/loop_detection.json` - Datadog monitor configuration for semantic loops
- `observability/monitors/token_velocity.json` - Datadog monitor for token consumption anomalies
- `observability/monitors/cost_threshold.json` - Datadog monitor for session cost limits
- `observability/webhooks.py` - Webhook payload validation and routing logic

### Cloud Functions (Remediation)
- `functions/inject-antidote/main.py` - Cloud Function to inject system instruction override
- `functions/inject-antidote/requirements.txt` - Dependencies for antidote function
- `functions/inject-antidote/config.py` - Configuration for antidote logic
- `functions/circuit-breaker/main.py` - Cloud Function to suspend agents
- `functions/circuit-breaker/requirements.txt` - Dependencies for circuit breaker
- `functions/circuit-breaker/config.py` - Circuit breaker configuration
- `functions/shared/vertex_ai_client.py` - Shared Vertex AI API client utilities
- `functions/shared/kafka_producer.py` - Shared Kafka producer for remediation events

### Kafka Event Streaming
- `kafka/schemas/agent_thought.avsc` - Avro schema for agent thought events
- `kafka/schemas/remediation.avsc` - Avro schema for remediation events
- `kafka/producers/thought_logger.py` - Producer for agent thought stream
- `kafka/producers/remediation_logger.py` - Producer for remediation events
- `kafka/consumers/audit_consumer.py` - Consumer for audit trail processing
- `kafka/config.py` - Confluent Kafka configuration

### Dashboard & Frontend (Next.js)
- `dashboard/app/layout.tsx` - Root layout with neon theme
- `dashboard/app/globals.css` - Tailwind imports and neon CSS variables
- `dashboard/app/(dashboard)/layout.tsx` - Dashboard shell layout
- `dashboard/app/(dashboard)/page.tsx` - Main operations center page
- `dashboard/app/(dashboard)/agents/page.tsx` - Agent management view
- `dashboard/app/(dashboard)/analytics/page.tsx` - Cost & performance analytics
- `dashboard/app/(dashboard)/audit/page.tsx` - Kafka audit log viewer
- `dashboard/src/components/layout/DashboardShell.tsx` - Main dashboard container
- `dashboard/src/components/layout/Sidebar.tsx` - Navigation sidebar
- `dashboard/src/components/layout/StatusBar.tsx` - System status bar
- `dashboard/src/components/layout/NeonGrid.tsx` - Background grid effect
- `dashboard/src/components/agents/AgentCard.tsx` - Individual agent status card
- `dashboard/src/components/agents/AgentList.tsx` - Grid of agent cards
- `dashboard/src/components/agents/AgentFlowDiagram.tsx` - React Flow visualization
- `dashboard/src/components/metrics/KPICard.tsx` - Neon KPI cards
- `dashboard/src/components/metrics/TokenVelocityChart.tsx` - Token velocity heatmap
- `dashboard/src/components/metrics/CostSavingsCounter.tsx` - Animated cost counter
- `dashboard/src/components/metrics/LoopDetectionGraph.tsx` - Loop detection alert graph
- `dashboard/src/components/remediation/RemediationLog.tsx` - Real-time remediation stream
- `dashboard/src/components/remediation/AntidotePanel.tsx` - Antidote status display
- `dashboard/src/components/audit/KafkaEventStream.tsx` - Kafka event viewer
- `dashboard/src/components/audit/ThoughtTimeline.tsx` - Agent reasoning timeline
- `dashboard/src/components/ui/button.tsx` - Shadcn button (neon themed)
- `dashboard/src/components/ui/card.tsx` - Shadcn card (neon glass)
- `dashboard/src/components/ui/badge.tsx` - Shadcn badge (neon status)
- `dashboard/src/lib/api/agents.ts` - Agent API client functions
- `dashboard/src/lib/api/metrics.ts` - Metrics API client
- `dashboard/src/lib/api/kafka.ts` - Kafka consumer WebSocket client
- `dashboard/src/lib/constants.ts` - Frontend constants and thresholds
- `dashboard/src/lib/utils.ts` - Utility functions (cn, formatters)
- `dashboard/src/types/agent.ts` - Agent domain types
- `dashboard/src/types/metrics.ts` - Metrics types
- `dashboard/src/types/events.ts` - Kafka event types
- `dashboard/src/styles/neon-theme.css` - Neon CSS variables and glass panels
- `dashboard/src/styles/animations.css` - Neon animations (pulse, glow, flicker)
- `dashboard/tailwind.config.ts` - Tailwind config with neon extensions
- `dashboard/package.json` - Frontend dependencies
- `dashboard/next.config.js` - Next.js configuration

### Backend API (FastAPI for Dashboard)
- `api/main.py` - FastAPI application entry point
- `api/routers/agents.py` - Agent endpoints (list, get, update status)
- `api/routers/metrics.py` - Metrics endpoints (KPIs, charts data)
- `api/routers/kafka.py` - Kafka consumer WebSocket endpoint
- `api/services/datadog_client.py` - Datadog API client for metrics
- `api/services/vertex_client.py` - Vertex AI client for agent data
- `api/services/kafka_consumer.py` - Kafka consumer service
- `api/models/agent.py` - Pydantic models for agents
- `api/models/metrics.py` - Pydantic models for metrics
- `api/requirements.txt` - Backend API dependencies

### Testing & Demo
- `tests/unit/test_semantic_analyzer.py` - Unit tests for loop detection logic
- `tests/unit/test_antidote.py` - Unit tests for antidote Cloud Function
- `tests/unit/test_frontend_components.py` - Jest tests for React components
- `tests/integration/test_end_to_end_remediation.py` - E2E test: loop detection → webhook → remediation
- `tests/integration/test_kafka_flow.py` - Test Kafka event publishing and consumption
- `tests/integration/test_dashboard_api.py` - Test dashboard API endpoints
- `tests/load/simulate_multi_agent_loops.py` - Load test with 50+ simultaneous loops
- `tests/e2e/test_dashboard_ui.py` - Playwright E2E tests for dashboard
- `demo/run_poison_prompt.py` - Script to trigger demo failure scenario
- `demo/verify_remediation.py` - Script to verify auto-healing worked
- `demo/dashboard_demo.md` - Step-by-step demo script with screenshots

### Shared Libraries
- `lib/utils/cost_calculator.py` - Token-to-cost conversion utilities
- `lib/utils/embedding_utils.py` - Vector embedding generation and similarity
- `lib/utils/logger.py` - Structured logging configuration
- `lib/constants.py` - System-wide constants (thresholds, stage names, etc.)
- `requirements.txt` - Root Python dependencies
- `pyproject.toml` - Python project configuration (Poetry/setuptools)

### Documentation
- `docs/SETUP.md` - Step-by-step setup instructions
- `docs/ARCHITECTURE.md` - System architecture diagrams and explanations
- `docs/API.md` - Cloud Function and REST API documentation
- `docs/FRONTEND.md` - Dashboard development guide with neon theme reference
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `README.md` - Project overview and quick start

### Notes

- **Python Version**: All code uses Python 3.11+
- **Testing**: Use `pytest` for unit and integration tests
- **Deployment**: Use `gcloud functions deploy` for Cloud Functions
- **Kafka**: Confluent Cloud CLI (`confluent`) for topic management
- **Secrets**: Store API keys in Google Secret Manager, reference via environment variables
- **Monitoring**: Deploy Datadog monitors via API or Terraform

---

## Tasks

- [ ] 1.0 **Phase 1: Infrastructure Foundation & GCP Setup (Hours 0-48)**
  - [x] 1.1 Create Google Cloud Project and enable billing
  - [x] 1.2 Enable required GCP APIs (Vertex AI, Cloud Functions, Secret Manager, Cloud Build)
  - [x] 1.3 Create service accounts with appropriate IAM roles
  - [x] 1.4 Set up Datadog organization and obtain API/App keys
  - [x] 1.5 Configure Datadog-GCP integration for metric collection
  - [ ] 1.6 Set up Confluent Cloud Kafka cluster (free tier)
  - [ ] 1.7 Create Kafka topics: `agent.thoughts.v1` and `agent.remediations.v1`
  - [ ] 1.8 Define Avro schemas for Kafka topics in Schema Registry
  - [ ] 1.9 Create project directory structure and initialize Git repository
  - [ ] 1.10 Set up environment variables and configuration files
  - [ ] 1.11 Install Python dependencies and verify local development environment
  - [ ] 1.12 Write infrastructure-as-code (Terraform) for reproducible deployment

- [ ] 2.0 **Phase 2: FinBot Test Agent Development & Observability Integration (Hours 49-96)**
  - [ ] 2.1 Design FinBot agent architecture (Planner, Researcher, Analyst pattern)
  - [ ] 2.2 Implement FinBot agent using Vertex AI Agent Builder Python SDK
  - [ ] 2.3 Create custom tools for FinBot (market data query, portfolio analysis)
  - [ ] 2.4 Write system instructions for each agent role
  - [ ] 2.5 Develop the "Poison Prompt" that triggers circular dependencies
  - [ ] 2.6 Integrate Datadog LLM Observability SDK (`ddtrace`) into agent code
  - [ ] 2.7 Configure trace capture for all agent interactions (input, output, tokens, latency)
  - [ ] 2.8 Add custom trace tags: `agent_id`, `session_id`, `user_query`
  - [ ] 2.9 Implement semantic loop detection logic using vector embeddings
  - [ ] 2.10 Build token velocity monitoring with rolling averages
  - [ ] 2.11 Create cost tracking module with real-time calculation
  - [ ] 2.12 Deploy FinBot to Vertex AI and verify basic functionality
  - [ ] 2.13 Test Poison Prompt and measure baseline failure metrics (time-to-failure, token burn rate)
  - [ ] 2.14 Verify traces appear in Datadog LLM Observability dashboard

- [ ] 3.0 **Phase 3: Autonomous Remediation System (The Antidote) (Hours 97-120)**
  - [ ] 3.1 Design Cloud Function architecture for remediation workflows
  - [ ] 3.2 Implement `inject-antidote` Cloud Function (HTTP trigger)
  - [ ] 3.3 Write logic to call Vertex AI `AgentServiceClient.update_agent()` with FieldMask
  - [ ] 3.4 Create the "Antidote" system instruction override text
  - [ ] 3.5 Implement verification logic to check for `TERMINATE_LOOP` output
  - [ ] 3.6 Implement `circuit-breaker` Cloud Function for agent suspension
  - [ ] 3.7 Add logic to update agent status to "SUSPENDED - Loop Detected"
  - [ ] 3.8 Implement cooldown and auto-restart logic (30-second delay)
  - [ ] 3.9 Build shared Vertex AI client library for Cloud Functions
  - [ ] 3.10 Deploy Cloud Functions to GCP with proper IAM permissions
  - [ ] 3.11 Test Cloud Functions locally using `curl` with mock payloads
  - [ ] 3.12 Configure Datadog webhooks to trigger Cloud Functions
  - [ ] 3.13 Create Datadog monitors with webhook triggers (token velocity, loop similarity, cost threshold)
  - [ ] 3.14 Test end-to-end flow: Run Poison Prompt → Datadog detects → Webhook fires → Antidote executes

- [ ] 4.0 **Phase 4: Kafka Event Streaming & Audit Trail (Hours 121-144)**
  - [ ] 4.1 Implement Kafka producer for agent thought events in FinBot
  - [ ] 4.2 Integrate thought event logging into agent execution flow (non-blocking async)
  - [ ] 4.3 Implement Kafka producer for remediation events in Cloud Functions
  - [ ] 4.4 Log remediation actions (timestamp, agent_id, failure_type, success, cost_saved)
  - [ ] 4.5 Create Kafka consumer for audit trail processing
  - [ ] 4.6 Implement event replay functionality for forensic analysis
  - [ ] 4.7 Set up Kafka retention policies (7 days for thought stream)
  - [ ] 4.8 Add error handling and retry logic for Kafka producers
  - [ ] 4.9 Test Kafka flow: Publish thought events → Verify in Confluent Cloud → Consume for audit
  - [ ] 4.10 Verify Schema Registry validates event schemas correctly
  - [ ] 4.11 Build sample analytics query using Kafka events (e.g., "Show all loops from last 24h")

- [ ] 5.0 **Phase 5: Dashboard, Integration Testing & Demo Preparation (Hours 145-168)**
  - [ ] 5.1 Set up Next.js 14 project with TypeScript and Tailwind CSS (neon theme)
  - [ ] 5.2 Configure Tailwind with neon color extensions and custom animations
  - [ ] 5.3 Create neon glass panel CSS classes and background effects
  - [ ] 5.4 Build DashboardShell layout component with sidebar navigation
  - [ ] 5.5 Implement AgentCard component with neon status indicators
  - [ ] 5.6 Create AgentList grid component with responsive layout
  - [ ] 5.7 Build KPI cards widget (Agents Monitored, Loops Detected, Cost Saved, Remediations)
  - [ ] 5.8 Implement TokenVelocityChart with Recharts and neon styling
  - [ ] 5.9 Create LoopDetectionGraph with alert visualization and neon magenta theme
  - [ ] 5.10 Build CostSavingsCounter with animated CountUp and neon green glow
  - [ ] 5.11 Implement RemediationLog stream component with real-time updates
  - [ ] 5.12 Create KafkaEventStream viewer for audit trail
  - [ ] 5.13 Build ThoughtTimeline component for agent reasoning replay
  - [ ] 5.14 Add neon-pulse animations to status indicators
  - [ ] 5.15 Implement hover effects with glow on all interactive elements
  - [ ] 5.16 Connect dashboard to backend APIs (agents, metrics, Kafka consumers)
  - [ ] 5.17 Add Framer Motion page transitions with blur effects
  - [ ] 5.18 Test responsive layouts on mobile, tablet, and desktop
  - [ ] 5.19 Deploy dashboard to Vercel or GCP Cloud Run
  - [ ] 5.20 Write comprehensive integration test suite for E2E flows
  - [ ] 5.21 Run load test: Simulate 50+ agents, verify UI handles concurrent updates
  - [ ] 5.22 Measure and document key metrics (detection speed, remediation success rate)
  - [ ] 5.23 Create demo script with step-by-step narration and visual cues
  - [ ] 5.24 Record backup demo video showing full loop detection → remediation flow
  - [ ] 5.25 Prepare "Before/After" comparison slides (cost burn, time-to-resolution)
  - [ ] 5.26 Test demo flow end-to-end at least 3 times with live dashboard
  - [ ] 5.27 Create fallback plan and troubleshooting checklist for demo
  - [ ] 5.28 Polish presentation deck with architecture diagrams and live demo setup
  - [ ] 5.29 Final verification: Run Poison Prompt, confirm auto-heal within 30 seconds, verify dashboard shows cost savings in real-time

---

## Implementation Notes

### Critical Path Dependencies
1. **GCP Setup** → **Agent Development** → **Observability** → **Remediation** → **Dashboard**
2. Kafka can be developed in parallel with Phase 3 (Remediation)
3. Testing should happen incrementally after each phase

### Key Success Criteria (Demo Day)
- ✅ Detect infinite loop within 30 seconds
- ✅ Auto-remediate without human intervention
- ✅ Dashboard shows "$127 saved by auto-remediation"
- ✅ 3/3 successful auto-heals during presentation

### Risk Mitigation
- **Cold Start Issue**: Pre-warm Cloud Functions before demo
- **Network Latency**: Test webhook reliability, have manual trigger as backup
- **Datadog Trial Limits**: Monitor trial usage, upgrade if needed
- **Kafka Free Tier**: Stay within throughput limits (avoid log spam)

### Development Best Practices
- Commit frequently with descriptive messages
- Use feature branches for major components
- Write tests alongside implementation (TDD where possible)
- Document environment setup in `docs/SETUP.md` as you go
- Keep secrets in Secret Manager, never commit to Git
- Use structured logging for all components (JSON format)
- Tag all resources with `project:ouroboros` for cost tracking

---

## Frontend Development Reference

### Design Philosophy for Ouroboros Dashboard

#### Core Aesthetic - Neon Cyberpunk Theme
- **Glassmorphism Design Language**: Modern, premium feel with frosted glass effects on pure black
- **Pure Black Theme**: Solid black (#000000) background with neon glass overlays
- **Neon Gradients**: Cyan-to-magenta, green-to-cyan, and purple-to-pink gradients for actions and highlights
- **Smooth Animations**: Framer Motion for page transitions and micro-interactions with glow effects
- **Modern Typography**: Inter font family, clean hierarchy with neon accents

#### Visual Principles
1. **Neon on Black**: High contrast neon colors on pure black background
2. **Depth through glow**: Glass panels with neon borders and outer glow effects
3. **Fluid motion**: Smooth transitions with trail effects and pulsing glows
4. **Sharp rounding**: Medium border radii (8px-16px) for tech aesthetic
5. **Color as status**: Neon colors indicate system health (cyan=healthy, magenta=alert, red=critical)

---

### Tech Stack

#### Core Framework
- **Next.js 14.1.0**: App Router (not Pages Router)
- **React 18.2.0**: Latest stable with hooks
- **TypeScript 5**: Full type safety

#### UI & Styling
- **Tailwind CSS 3.4.17**: Utility-first styling with custom neon utilities
- **Shadcn/ui**: "New York" style variant (customized for neon theme)
- **Radix UI**: Accessible component primitives
- **Lucide React**: Icon library
- **Framer Motion 11.0.3**: Animation library with glow animations
- **class-variance-authority**: Component variant management
- **tailwind-merge + clsx**: Dynamic className composition

#### Charts & Visualization
- **Recharts 2.12.0**: Analytics charts with neon styling
- **React Flow**: For agent workflow visualization

#### Other Libraries
- **date-fns 3.3.1**: Date manipulation
- **Sonner 1.4.0**: Toast notifications with neon styling

---

### Color Palette - Neon Cyberpunk

#### Background & Base
```css
/* Main background: Pure black with subtle noise texture */
--bg-primary: #000000;
--bg-secondary: #0a0a0a;
--bg-tertiary: #111111;

/* Overlay gradient for depth */
background: radial-gradient(ellipse at top, rgba(0, 255, 255, 0.05) 0%, #000000 50%);
```

#### Neon Glass System Colors
```css
--glass-bg: rgba(255, 255, 255, 0.02);
--glass-border: rgba(0, 255, 255, 0.3);  /* Cyan border */
--glass-glow: 0 0 20px rgba(0, 255, 255, 0.3);
--glass-inner-glow: inset 0 0 20px rgba(0, 255, 255, 0.1);
```

#### Neon Brand Colors
```css
--neon-cyan: #00ffff;           /* Primary neon cyan */
--neon-magenta: #ff00ff;        /* Alert/warning magenta */
--neon-green: #00ff88;          /* Success/healthy green */
--neon-red: #ff0055;            /* Critical/danger red */
--neon-purple: #9d00ff;         /* Secondary purple */
--neon-yellow: #ffff00;         /* Caution yellow */
--neon-orange: #ff6600;         /* Warning orange */
```

#### Agent Status Colors (Neon)
```css
--status-healthy: #00ff88;      /* Neon green */
--status-warning: #ffff00;      /* Neon yellow */
--status-looping: #ff00ff;      /* Neon magenta */
--status-suspended: #ff0055;    /* Neon red */
--status-healing: #00ffff;      /* Neon cyan (pulsing) */
```

#### Text Colors
```css
--text-primary: #ffffff;        /* Pure white */
--text-secondary: #b3b3b3;      /* Light gray */
--text-muted: #666666;          /* Medium gray */
--text-neon-cyan: #00ffff;      /* Neon cyan for emphasis */
--text-neon-magenta: #ff00ff;   /* Neon magenta for alerts */
```

---

### Typography

#### Font Family
```css
font-family: 'Inter', 'JetBrains Mono', monospace, system-ui, -apple-system, sans-serif;
```

#### Scale
- **Dashboard Title**: 5xl (48px), font-black, text-white with cyan text-shadow
- **Section Title**: 3xl (30px), font-bold, text-white with subtle glow
- **Card Title**: xl (20px), font-semibold, text-neon-cyan
- **Metric Value**: 4xl (36px), font-black, text-white
- **Body**: base (16px), font-medium, text-white/90
- **Small**: sm (14px), text-gray-400
- **Code/Mono**: xs (12px), font-mono, text-neon-cyan

---

### Spacing & Layout

#### Radius Values
```css
--radius-xs: 4px;
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;
```

#### Common Patterns
- **Large panels**: rounded-2xl (16px)
- **Medium cards**: rounded-xl (12px)
- **Small cards/buttons**: rounded-lg (8px)
- **Input fields**: rounded-md (6px)
- **Badges**: rounded-full (pill shape)

#### Padding Scale
- **Dashboard margins**: p-6 (24px)
- **Card padding**: p-5 (20px)
- **Compact card**: p-3 (12px)
- **Button padding**: px-6 py-2.5
- **Section spacing**: space-y-6

---

### Glassmorphism Effects - Neon Style

#### Primary Neon Glass Panel
```css
.neon-glass-panel {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.2),
    inset 0 0 20px rgba(0, 255, 255, 0.05);
}
```

#### Neon Glass Variants
```css
/* Healthy Status - Cyan */
.neon-glass-cyan {
  border: 1px solid rgba(0, 255, 255, 0.4);
  box-shadow: 
    0 0 30px rgba(0, 255, 255, 0.3),
    inset 0 0 20px rgba(0, 255, 255, 0.1);
}

/* Alert Status - Magenta */
.neon-glass-magenta {
  border: 1px solid rgba(255, 0, 255, 0.4);
  box-shadow: 
    0 0 30px rgba(255, 0, 255, 0.3),
    inset 0 0 20px rgba(255, 0, 255, 0.1);
}

/* Critical Status - Red */
.neon-glass-red {
  border: 1px solid rgba(255, 0, 85, 0.4);
  box-shadow: 
    0 0 30px rgba(255, 0, 85, 0.3),
    inset 0 0 20px rgba(255, 0, 85, 0.1);
}

/* Success Status - Green */
.neon-glass-green {
  border: 1px solid rgba(0, 255, 136, 0.4);
  box-shadow: 
    0 0 30px rgba(0, 255, 136, 0.3),
    inset 0 0 20px rgba(0, 255, 136, 0.1);
}
```

#### Hover Effects - Neon Glow
```css
.neon-glass-hover:hover {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 
    0 0 40px rgba(0, 255, 255, 0.4),
    inset 0 0 30px rgba(0, 255, 255, 0.15);
  transform: translateY(-2px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

### Animations - Neon Effects

#### Page Transitions
```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.95, filter: "blur(10px)" }}
  animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
  exit={{ opacity: 0, scale: 0.95, filter: "blur(10px)" }}
  transition={{ duration: 0.4, ease: [0.4, 0, 0.2, 1] }}
>
```

#### Neon Pulse Animation
```css
@keyframes neon-pulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(0, 255, 255, 0.6);
  }
}

.neon-pulse {
  animation: neon-pulse 2s ease-in-out infinite;
}
```

#### Neon Glow Text
```css
.neon-text-cyan {
  color: #00ffff;
  text-shadow: 
    0 0 10px rgba(0, 255, 255, 0.8),
    0 0 20px rgba(0, 255, 255, 0.6),
    0 0 30px rgba(0, 255, 255, 0.4);
}

.neon-text-magenta {
  color: #ff00ff;
  text-shadow: 
    0 0 10px rgba(255, 0, 255, 0.8),
    0 0 20px rgba(255, 0, 255, 0.6),
    0 0 30px rgba(255, 0, 255, 0.4);
}
```

#### Available Animations
- **neon-pulse**: 2s infinite (status indicators)
- **neon-flicker**: 3s infinite (subtle flicker effect)
- **data-flow**: 4s infinite (flowing data streams)
- **scan-line**: 2s infinite (CRT scan effect)
- **glow-in**: 0.5s ease-out (entrance glow)

---

### Project Structure - Ouroboros Dashboard

```
ouroboros-dashboard/
├── app/                          # Next.js App Router
│   ├── (dashboard)/              # Dashboard route group
│   │   ├── layout.tsx            # Dashboard shell with sidebar
│   │   ├── page.tsx              # Main operations center
│   │   ├── agents/               # Agent management
│   │   ├── analytics/            # Cost & performance analytics
│   │   ├── audit/                # Kafka audit log viewer
│   │   └── settings/             # System configuration
│   ├── globals.css               # Tailwind + neon theme
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Landing/redirect
├── src/
│   ├── components/
│   │   ├── layout/               # Layout components
│   │   │   ├── DashboardShell.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── StatusBar.tsx
│   │   │   └── NeonGrid.tsx      # Background grid effect
│   │   ├── agents/               # Agent components
│   │   │   ├── AgentCard.tsx     # Individual agent status
│   │   │   ├── AgentList.tsx     # Grid of agents
│   │   │   └── AgentFlowDiagram.tsx  # React Flow visualization
│   │   ├── metrics/              # Metrics widgets
│   │   │   ├── KPICard.tsx       # Neon KPI cards
│   │   │   ├── TokenVelocityChart.tsx
│   │   │   ├── CostSavingsCounter.tsx
│   │   │   └── LoopDetectionGraph.tsx
│   │   ├── remediation/          # Remediation components
│   │   │   ├── RemediationLog.tsx
│   │   │   ├── AntidotePanel.tsx
│   │   │   └── CircuitBreakerStatus.tsx
│   │   ├── audit/                # Audit trail
│   │   │   ├── KafkaEventStream.tsx
│   │   │   ├── ThoughtTimeline.tsx
│   │   │   └── EventReplay.tsx
│   │   └── ui/                   # Shadcn UI (neon themed)
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── badge.tsx
│   │       ├── progress.tsx
│   │       └── chart.tsx
│   ├── lib/
│   │   ├── api/                  # API client
│   │   │   ├── agents.ts         # Agent API calls
│   │   │   ├── metrics.ts        # Metrics fetching
│   │   │   └── kafka.ts          # Kafka consumer client
│   │   ├── constants.ts          # Thresholds & config
│   │   └── utils.ts              # Utility functions
│   ├── types/
│   │   ├── agent.ts              # Agent domain types
│   │   ├── metrics.ts            # Metrics types
│   │   └── events.ts             # Kafka event types
│   └── styles/
│       ├── neon-theme.css        # Neon CSS variables
│       └── animations.css        # Neon animations
├── public/
│   └── noise-texture.png         # Subtle noise overlay
├── tailwind.config.ts            # Neon color extensions
└── package.json
```

---

### Core Components - Ouroboros Specific

#### 1. Agent Status Card
```tsx
<div className="neon-glass-panel neon-glass-hover rounded-xl p-5">
  {/* Agent Icon with Status Glow */}
  <div className={`relative w-12 h-12 rounded-lg ${statusGlow}`}>
    <Bot className="w-6 h-6 text-white" />
    {/* Pulsing status indicator */}
    <div className={`absolute -top-1 -right-1 w-4 h-4 rounded-full ${statusColor} neon-pulse`} />
  </div>
  
  {/* Agent Info */}
  <div className="mt-4">
    <h3 className="text-lg font-semibold text-white">{agentName}</h3>
    <p className="text-sm text-gray-400">{agentType}</p>
  </div>
  
  {/* Status Badge */}
  <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium ${statusStyle}`}>
    <Activity className="w-3 h-3" />
    {status}
  </span>
  
  {/* Metrics */}
  <div className="grid grid-cols-2 gap-3 mt-4">
    <div>
      <p className="text-xs text-gray-500">Tokens/min</p>
      <p className="text-xl font-bold text-neon-cyan">{tokensPerMin}</p>
    </div>
    <div>
      <p className="text-xs text-gray-500">Cost</p>
      <p className="text-xl font-bold text-neon-green">${cost}</p>
    </div>
  </div>
</div>
```

#### 2. Loop Detection Alert Graph
```tsx
<div className="neon-glass-magenta rounded-xl p-6">
  <div className="flex items-center justify-between mb-4">
    <h3 className="text-xl font-bold text-white flex items-center gap-2">
      <AlertTriangle className="w-5 h-5 text-neon-magenta" />
      Loop Detection Status
    </h3>
    <span className="text-xs text-gray-400 font-mono">{timestamp}</span>
  </div>
  
  {/* Recharts Area Chart with neon styling */}
  <ResponsiveContainer width="100%" height={200}>
    <AreaChart data={loopData}>
      <defs>
        <linearGradient id="loopGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ff00ff" stopOpacity={0.8} />
          <stop offset="100%" stopColor="#ff00ff" stopOpacity={0} />
        </linearGradient>
      </defs>
      <Area 
        type="monotone" 
        dataKey="similarity" 
        stroke="#ff00ff" 
        strokeWidth={2}
        fill="url(#loopGradient)" 
      />
    </AreaChart>
  </ResponsiveContainer>
  
  {/* Alert threshold line */}
  <div className="mt-2 text-xs text-gray-400">
    Alert Threshold: <span className="text-neon-magenta font-mono">95%</span>
  </div>
</div>
```

#### 3. Cost Savings Counter (Animated)
```tsx
<div className="neon-glass-green rounded-xl p-6">
  <div className="flex items-center gap-3 mb-4">
    <div className="w-12 h-12 rounded-lg bg-neon-green/20 flex items-center justify-center">
      <DollarSign className="w-6 h-6 text-neon-green" />
    </div>
    <div>
      <h4 className="text-sm text-gray-400">Cost Saved Today</h4>
      <p className="text-4xl font-black text-neon-green neon-text-green">
        <CountUp end={costSaved} prefix="$" duration={2} />
      </p>
    </div>
  </div>
  
  {/* Savings breakdown */}
  <div className="space-y-2">
    <div className="flex justify-between text-sm">
      <span className="text-gray-400">Loops prevented</span>
      <span className="text-white font-mono">{loopsPrevented}</span>
    </div>
    <div className="flex justify-between text-sm">
      <span className="text-gray-400">Avg. cost/loop</span>
      <span className="text-white font-mono">${avgCostPerLoop}</span>
    </div>
  </div>
</div>
```

#### 4. Remediation Log Stream
```tsx
<div className="neon-glass-panel rounded-xl p-6 h-96 overflow-y-auto">
  <h3 className="text-xl font-bold text-white mb-4">Recent Remediations</h3>
  
  <div className="space-y-3">
    {remediations.map((event, idx) => (
      <motion.div
        key={event.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: idx * 0.1 }}
        className="neon-glass-hover rounded-lg p-4 border-l-4 border-neon-cyan"
      >
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <Zap className="w-4 h-4 text-neon-cyan" />
            <div>
              <p className="text-sm font-semibold text-white">{event.action}</p>
              <p className="text-xs text-gray-400 font-mono">{event.agent_id}</p>
            </div>
          </div>
          <span className={`text-xs px-2 py-1 rounded-full ${event.success ? 'bg-neon-green/20 text-neon-green' : 'bg-neon-red/20 text-neon-red'}`}>
            {event.success ? 'Success' : 'Failed'}
          </span>
        </div>
        
        <div className="mt-2 text-xs text-gray-500">
          {event.timestamp} • Saved ${event.cost_saved}
        </div>
      </motion.div>
    ))}
  </div>
</div>
```

#### 5. Token Velocity Heatmap
```tsx
<div className="neon-glass-panel rounded-xl p-6">
  <h3 className="text-xl font-bold text-white mb-4">Token Velocity by Agent</h3>
  
  <div className="grid grid-cols-4 gap-2">
    {agents.map((agent) => (
      <div
        key={agent.id}
        className={`rounded-lg p-3 transition-all ${getVelocityColor(agent.velocity)}`}
        title={`${agent.name}: ${agent.velocity} tokens/min`}
      >
        <p className="text-xs text-white/80 truncate">{agent.name}</p>
        <p className="text-lg font-bold text-white font-mono">{agent.velocity}</p>
      </div>
    ))}
  </div>
  
  {/* Legend */}
  <div className="flex items-center gap-4 mt-4 text-xs">
    <div className="flex items-center gap-1">
      <div className="w-3 h-3 rounded bg-neon-green/30" />
      <span className="text-gray-400">Normal</span>
    </div>
    <div className="flex items-center gap-1">
      <div className="w-3 h-3 rounded bg-neon-yellow/30" />
      <span className="text-gray-400">Warning</span>
    </div>
    <div className="flex items-center gap-1">
      <div className="w-3 h-3 rounded bg-neon-red/30" />
      <span className="text-gray-400">Critical</span>
    </div>
  </div>
</div>
```

---

### Gradient Patterns - Neon Style

#### Primary Action Gradients
```css
/* Cyan to Magenta */
background: linear-gradient(to right, #00ffff, #ff00ff);

/* Green to Cyan */
background: linear-gradient(to right, #00ff88, #00ffff);

/* Purple to Pink */
background: linear-gradient(to right, #9d00ff, #ff00ff);

/* Red to Orange */
background: linear-gradient(to right, #ff0055, #ff6600);
```

#### Button Variants
```tsx
// Primary (Cyan gradient with glow)
<Button className="bg-gradient-to-r from-cyan-500 to-blue-500 hover:shadow-[0_0_30px_rgba(0,255,255,0.5)]">

// Danger (Red gradient with glow)
<Button className="bg-gradient-to-r from-red-500 to-pink-500 hover:shadow-[0_0_30px_rgba(255,0,85,0.5)]">

// Success (Green gradient with glow)
<Button className="bg-gradient-to-r from-green-500 to-cyan-500 hover:shadow-[0_0_30px_rgba(0,255,136,0.5)]">

// Ghost (Border only with hover glow)
<Button className="border border-cyan-500/50 hover:border-cyan-500 hover:shadow-[0_0_20px_rgba(0,255,255,0.3)]">
```

---

### Status Badge System - Neon

```tsx
// Healthy Agent
<span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-neon-green/20 border border-neon-green/50 text-neon-green text-xs font-medium">
  <Activity className="w-3 h-3" />
  HEALTHY
</span>

// Looping Agent
<span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-neon-magenta/20 border border-neon-magenta/50 text-neon-magenta text-xs font-medium neon-pulse">
  <AlertTriangle className="w-3 h-3" />
  LOOPING
</span>

// Suspended Agent
<span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-neon-red/20 border border-neon-red/50 text-neon-red text-xs font-medium">
  <XCircle className="w-3 h-3" />
  SUSPENDED
</span>

// Healing Agent
<span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-neon-cyan/20 border border-neon-cyan/50 text-neon-cyan text-xs font-medium neon-pulse">
  <Zap className="w-3 h-3" />
  HEALING
</span>
```

---

### Responsive Design

#### Breakpoints (Same as reference)
```typescript
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

#### Grid Patterns for Dashboard
```tsx
// Agent grid - responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">

// Metrics row
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

// Two-column analytics
<div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
```

---

### Key Differences from CareerPilot Reference

#### What's Changed:
1. **Background**: Pure black (#000000) instead of blue gradient
2. **Colors**: Neon cyan/magenta/green instead of blue/purple
3. **Borders**: Neon glowing borders instead of subtle glass
4. **Typography**: Added monospace for metrics and IDs
5. **Animations**: Added neon-pulse, flicker, and glow effects
6. **Shadows**: Outer glow instead of traditional drop shadows

#### What Stays the Same:
1. **Tech Stack**: Next.js, React, TypeScript, Tailwind, Shadcn/ui
2. **Component Structure**: Layout system, component organization
3. **Animation Library**: Framer Motion
4. **Chart Library**: Recharts (with neon styling)
5. **File Organization**: Same directory structure pattern

---

### Implementation Priority for Ouroboros Dashboard

1. **Phase 1: Core Layout** (Hours 145-150)
   - Set up Next.js project with neon theme
   - Create DashboardShell and Sidebar
   - Implement neon glass panel styles
   - Add background effects (noise texture, radial gradient)

2. **Phase 2: Agent Components** (Hours 151-156)
   - Build AgentCard with status indicators
   - Implement AgentList grid
   - Add status badges with neon glow

3. **Phase 3: Metrics & Charts** (Hours 157-162)
   - Create KPI cards (cost saved, loops detected, agents monitored)
   - Build TokenVelocityChart with Recharts
   - Implement LoopDetectionGraph with alert visualization
   - Add CostSavingsCounter with animated numbers

4. **Phase 4: Remediation & Audit** (Hours 163-166)
   - Build RemediationLog stream component
   - Implement Kafka event viewer
   - Add ThoughtTimeline for agent reasoning replay

5. **Phase 5: Polish & Animation** (Hours 167-168)
   - Add entrance animations for all components
   - Implement neon-pulse for status indicators
   - Add hover effects with glow
   - Test responsive layouts

---

### Tailwind Config Extensions for Neon Theme

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        neon: {
          cyan: '#00ffff',
          magenta: '#ff00ff',
          green: '#00ff88',
          red: '#ff0055',
          purple: '#9d00ff',
          yellow: '#ffff00',
          orange: '#ff6600',
        }
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(0, 255, 255, 0.3)',
        'neon-magenta': '0 0 20px rgba(255, 0, 255, 0.3)',
        'neon-green': '0 0 20px rgba(0, 255, 136, 0.3)',
        'neon-red': '0 0 20px rgba(255, 0, 85, 0.3)',
      },
      animation: {
        'neon-pulse': 'neon-pulse 2s ease-in-out infinite',
        'neon-flicker': 'neon-flicker 3s infinite',
      },
      keyframes: {
        'neon-pulse': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 255, 255, 0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(0, 255, 255, 0.6)' },
        },
        'neon-flicker': {
          '0%, 100%': { opacity: '1' },
          '41%': { opacity: '1' },
          '42%': { opacity: '0.8' },
          '43%': { opacity: '1' },
          '45%': { opacity: '0.9' },
          '46%': { opacity: '1' },
        },
      },
    },
  },
}
```

---

**This frontend reference is specifically tailored for the Ouroboros AI Resilience Platform dashboard. All UI components should follow this neon cyberpunk aesthetic on pure black background. Use this as the definitive design guide for all frontend development tasks.**
