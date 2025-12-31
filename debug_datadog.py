import os
import sys
import logging
from dotenv import load_dotenv

# 1. Setup Debug Logging
logging.basicConfig(level=logging.DEBUG)

# 2. Load Config
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, 'config', 'datadog.env')
load_dotenv(env_path)

print(f"--- Debugging Datadog Connection ---")

# 3. Force Agentless Mode
os.environ["DD_LLMOBS_AGENTLESS_ENABLED"] = "1"
os.environ["DD_LLMOBS_ENABLED"] = "1"
os.environ["DD_API_KEY"] = os.getenv("DD_API_KEY") # Ensure env var is set for the SDK

from ddtrace.llmobs import LLMObs

def test_connection():
    try:
        # Enable LLM Obs
        LLMObs.enable(ml_app="connection-test")
        
        print("\n1. Starting Workflow...")
        # 👇 CRITICAL FIX: We must start a workflow context
        with LLMObs.workflow(name="debug_connection_check") as span:
            
            print("2. Annotating test trace...")
            LLMObs.annotate(
                span=span, # Explicitly link to the span
                input_data="Test input from debug script",
                output_data="Test output from debug script",
                metadata={"test": "true"}
            )
            
            print("3. Workflow closing...")
        
        # Force Flush
        print("4. Flushing to Datadog (Wait for 200 OK)...")
        success = LLMObs.flush()
        
        print(f"\n5. Flush result: {success}")
        print("Done. Check dashboard for 'connection-test' app.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()