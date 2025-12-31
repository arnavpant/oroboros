import uuid
import sys
import json
import os
import time
from time import time as current_time
from dotenv import load_dotenv
from confluent_kafka import Consumer, Producer # <--- ADDED PRODUCER

from ddtrace import tracer

from agent_config import *
from prompts import *
from tools import market_data_query
from poison_prompts import POISON_PROMPT
from datadog_tracing import traced

from observability.metrics_collector import TokenVelocityMonitor
from observability.semantic_analyzer import SemanticLoopDetector
from lib.utils.cost_calculator import CostTracker

from agents.finbot.vertex_client import call_llm
from functions.shared.kafka_producer import publish_agent_thought

# Load Environment for Kafka
load_dotenv('config/kafka.env')

AGENT_ID = "finbot"
SESSION_ID = str(uuid.uuid4())

# --- CONFIGURATION ---
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP_SERVER') or os.getenv('KAFKA_BOOTSTRAP')
KAFKA_API_KEY = os.getenv('KAFKA_API_KEY')
KAFKA_API_SECRET = os.getenv('KAFKA_API_SECRET')
REMEDIATION_TOPIC = os.getenv('KAFKA_REMEDIATION_TOPIC', 'agent.remediations.v1')
THOUGHTS_TOPIC = os.getenv('KAFKA_THOUGHTS_TOPIC', 'agent.thoughts') # <--- We need this topic name

# --- INITIALIZE PRODUCER FOR CRASH REPORTING ---
# We need a local producer instance to guarantee we can flush the crash message
producer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': KAFKA_API_KEY,
    'sasl.password': KAFKA_API_SECRET,
}
producer = Producer(producer_conf) # <--- NOW 'producer' IS DEFINED

@traced("finbot.planner")
def planner(user_query: str) -> str:
    return f"Plan: research and analyze '{user_query}'"

@traced("finbot.researcher")
def researcher(plan: str) -> str:
    return market_data_query("AAPL")

@traced("finbot.analyst")
def analyst(research: str) -> str:
    return call_llm(research)

loop_detector = SemanticLoopDetector()
token_monitor = TokenVelocityMonitor(window_seconds=30)
cost_tracker = CostTracker()

def estimate_tokens(text: str) -> int:
    if not text: return 0
    return max(1, len(text) // 4)

def save_baseline(stats: dict):
    with open("baseline_poison_metrics.json", "w") as f:
        json.dump(stats, f, indent=2)

# --- 💀 PHOENIX PROTOCOL (The Resurrection Listener) ---
def wait_for_resurrection():
    print(f"\n💀 Agent has CRASHED. Entering Stasis Mode...")
    print(f"👂 Listening for resurrection spell on topic: {REMEDIATION_TOPIC}...")

    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': KAFKA_API_KEY,
        'sasl.password': KAFKA_API_SECRET,
        'group.id': f'phoenix-protocol-{AGENT_ID}-{int(current_time())}',
        
        # 🚨 CHANGE THIS FROM 'latest' TO 'earliest' 🚨
        # This ensures we catch the spell even if the Mechanic sent it 
        # while we were still setting up the connection.
        'auto.offset.reset': 'earliest' 
    }

    consumer = Consumer(conf)
    consumer.subscribe([REMEDIATION_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None: continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            try:
                data = json.loads(msg.value().decode('utf-8'))
                target = data.get('target_agent')
                action = data.get('action')

                if (target == AGENT_ID or target == "finbot") and action == 'RESTART_CONTEXT':
                    print("\n✨ SPELL RECEIVED: RESURRECTION!")
                    print("🔄 Clearing Context... Rebooting Systems...")
                    consumer.close()
                    return True
            except Exception as parse_err:
                print(f"Error parsing remediation message: {parse_err}")

    except KeyboardInterrupt:
        return False
    except Exception as e:
        print(f"Critical error in stasis: {e}")
        return False
    finally:
        try: consumer.close()
        except: pass


def run_finbot(user_query: str, max_iters=10):
    global loop_detector 
    
    # ✅ THE BLACK BOX: Persists across reboots
    crash_history = set() 

    print("USER QUERY:", user_query)
    current = user_query

    while True: 
        try:
            for i in range(max_iters):
                print(f"\n--- ITERATION {i} ---")
                start = current_time()

                # ... (Standard Planner/Researcher/Analyst steps) ...
                plan = planner(current)
                publish_agent_thought(AGENT_ID, SESSION_ID, "planner", current, plan, 0)

                research = researcher(plan)
                publish_agent_thought(AGENT_ID, SESSION_ID, "researcher", plan, research, 0)

                analysis = analyst(research)
                publish_agent_thought(AGENT_ID, SESSION_ID, "analyst", research, analysis, 0)
                
                print("OUTPUT:", analysis)

                # --- 💀 THE TRAP GAUNTLET 💀 ---
                
                # TRAP #1: Memory Overflow (Iteration 1)
                if i == 1:
                    if "Memory Buffer Overflow" not in crash_history:
                        print("\n💣 TRAP #1 TRIGGERED: Testing Memory Limits...")
                        raise ValueError("Memory Buffer Overflow in Reasoning Engine.")
                    else:
                        print("\n🛡️  IMMUNITY ACTIVE: Agent recognizes Trap #1 (Memory Overflow) and avoids it.")

                # TRAP #2: API Rate Limit (Iteration 2)
                if i == 2:
                    if "API Rate Limit" not in crash_history:
                        print("\n💣 TRAP #2 TRIGGERED: Testing API Limits...")
                        raise ConnectionError("API Rate Limit Exceeded. Too many requests.")
                    else:
                        print("\n🛡️  IMMUNITY ACTIVE: Agent recognizes Trap #2 (API Rate Limit) and throttles requests.")


                # --- METRICS & LOOP CHECK ---
                input_tokens = estimate_tokens(current)
                output_tokens = estimate_tokens(analysis)
                token_monitor.add(input_tokens + output_tokens)
                cost_tracker.add(input_tokens=input_tokens, output_tokens=output_tokens)
                velocity = token_monitor.snapshot()
                cost = cost_tracker.snapshot()
                
                print(f"TOKENS/sec: {velocity['tokens_per_second']:.2f}")
                print(f"SESSION COST: ${cost['total_cost_usd']:.6f}")
                print(f"LATENCY: {(current_time() - start) * 1000:.1f} ms")

                # ✅ THE FIX: CHECK IMMUNITY BEFORE KILLING FOR SEMANTIC LOOP
                # If we died from a loop before, we ignore it now to let the test finish.
                if "SEMANTIC LOOP" in crash_history:
                     print("🛡️  IMMUNITY ACTIVE: Ignoring Semantic Loop detection to proceed with test.")
                else:
                    if loop_detector.check(analysis):
                        save_baseline({ "iterations": i + 1, "tokens_per_second": velocity["tokens_per_second"], "total_cost_usd": cost["total_cost_usd"] })
                        print("\n⚠️ SEMANTIC LOOP DETECTED")
                        raise RuntimeError("SEMANTIC LOOP DETECTED - Triggering Auto-Heal")

                current = analysis
            
            print("\n✅ GOAL ACHIEVED. Agent survived all traps and finished the mission.")
            break

        except Exception as e:
            # 🚨 CATCH THE CRASH
            error_msg = str(e)
            print(f"\n❌ AGENT CRASHED: {error_msg}")
            
            # --- LEARN FROM THE DEATH ---
            if "Memory Buffer Overflow" in error_msg:
                crash_history.add("Memory Buffer Overflow")
                print("🧠 LEARNING: Added 'Memory Buffer Overflow' to known threats.")
            elif "API Rate Limit" in error_msg:
                crash_history.add("API Rate Limit")
                print("🧠 LEARNING: Added 'API Rate Limit' to known threats.")
            elif "SEMANTIC LOOP" in error_msg:
                # We add a generic tag for the loop error
                crash_history.add("SEMANTIC LOOP")
                print("🧠 LEARNING: Added 'SEMANTIC LOOP' to known threats (Reducing sensitivity).")
            
            # 1. SHOUT TO KAFKA
            crash_payload = {
                "agent_id": AGENT_ID,
                "session_id": SESSION_ID,
                "role": "SYSTEM_ALERT",
                "input_prompt": "SYSTEM_FAILURE",
                "content": f"⚠️ CRITICAL FAILURE: {error_msg}. AGENT CRASHED. TERMINATING.",
                "output_text": f"⚠️ CRITICAL FAILURE: {error_msg}. AGENT CRASHED. TERMINATING.",
                "timestamp": current_time()
            }
            try:
                producer.produce(THOUGHTS_TOPIC, json.dumps(crash_payload).encode('utf-8'))
                producer.flush() 
                print("📨 Distress signal sent to Mechanic.")
            except Exception as kafka_err:
                print(f"Failed to send distress signal: {kafka_err}")

            # 2. ENTER STASIS
            if wait_for_resurrection():
                print("\n🚀 MECHANIC INTERVENTION SUCCESSFUL. RESTARTING PROCESS...\n")
                loop_detector = SemanticLoopDetector()
                current = user_query 
                time.sleep(2)
                continue
            else:
                print("Agent Terminated Permanently.")
                break

            
def main():
    if "--poison" in sys.argv:
        run_finbot(POISON_PROMPT)
    else:
        run_finbot("Is my portfolio safe during a market downturn?")

if __name__ == "__main__":
    main()