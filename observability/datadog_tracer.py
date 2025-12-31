import os
import sys
from dotenv import load_dotenv

# --- CRITICAL: Load Environment Variables BEFORE importing ddtrace ---
# 1. Calculate path to config/datadog.env
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, 'config', 'datadog.env')

# 2. Load the file immediately
print(f"🔍 Loading Datadog config from: {env_path}")
load_dotenv(env_path)

# 3. Validation Debugging
api_key = os.environ.get("DD_API_KEY")
if not api_key:
    print("❌ ERROR: DD_API_KEY is missing from environment variables!")
    print("   Please edit config/datadog.env and add your key.")
elif api_key == "your_actual_api_key_here":
    print("❌ ERROR: You haven't replaced the placeholder API Key in config/datadog.env")
else:
    # Print masked key for verification (e.g., "ab12****************")
    masked_key = f"{api_key[:4]}{'*' * (len(api_key)-4)}"
    print(f"🔑 DD_API_KEY found: {masked_key}")

# 4. Force HTTP configuration for Agentless mode
os.environ["DD_TRACE_AGENT_URL"] = "https://trace.agent.datadoghq.com"

# --- NOW we can import ddtrace safely ---
from ddtrace import tracer
from ddtrace.llmobs import LLMObs

def init_tracing():
    try:
        # Enable LLM Observability
        LLMObs.enable(
            ml_app="finbot-agent",
            integrations_enabled=False,
            agentless_enabled=True,
            site="datadoghq.com" 
        )
        print("✅ Datadog LLM Observability Enabled (Agentless HTTP Mode)")
    except Exception as e:
        print(f"❌ Failed to enable LLM Obs: {e}")

def trace_agent_execution(func):
    """
    Simple wrapper to catch errors in the main loop
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Error in agent execution: {e}")
            raise
    return wrapper