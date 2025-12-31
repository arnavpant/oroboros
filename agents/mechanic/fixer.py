import os
import json
import time
from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv

# Load environment
load_dotenv('config/kafka.env')

# Configuration
KAFKA_CONFIG = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET'),
    'group.id': 'mechanic-ops-v1',  # Unique group for the mechanic
    'auto.offset.reset': 'latest'   # Only care about NEW errors
}


TRIGGER_PHRASES = [
    "SEMANTIC LOOP DETECTED", 
    "TERMINATE", 
    "CRITICAL FAILURE", 
    "AGENT CRASHED", 
    "FAIL" 
]


THOUGHTS_TOPIC = os.getenv('KAFKA_THOUGHTS_TOPIC')
REMEDIATION_TOPIC = os.getenv('KAFKA_REMEDIATION_TOPIC')

def start_mechanic():
    print("🔧 Ouroboros Mechanic is ONLINE.")
    print("👀 Watching for: 'FAIL', 'TERMINATE', 'LOOP DETECTED'...")

    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([THOUGHTS_TOPIC])
    
    # We also need a producer to announce when we fix things
    producer = Producer(KAFKA_CONFIG)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None: continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # Decode the thought
            data = json.loads(msg.value().decode('utf-8'))
            
            # 🔍 THE DIAGNOSIS LOGIC 🔍
            # We look for specific keywords in the agent's output that signal trouble
            content = data.get('content', '') or data.get('output_text', '')
            
            if any(phrase in content for phrase in TRIGGER_PHRASES):
                print(f"\n🚨 FAILURE DETECTED in Agent {data.get('agent_id')}!")
                print(f"   Reason: {content[:100]}...")
                
                # 🛠️ THE FIX (Simulation for now)
                print("   ⚡ ACTIVATING REMEDIATION PROTOCOL...")
                
                remediation_event = {
                    "event": "AUTO_HEAL",
                    "target_agent": data.get('agent_id'),
                    "action": "RESTART_CONTEXT",
                    "status": "SUCCESS",
                    "timestamp": time.time()
                }
                
                # Announce the fix to the network (so the Dashboard sees it)
                producer.produce(
                    REMEDIATION_TOPIC,
                    key="mechanic",
                    value=json.dumps(remediation_event)
                )
                producer.flush()
                print("   ✅ SYSTEM RESTORED. Waiting for next anomaly.\n")

    except KeyboardInterrupt:
        print("🔧 Mechanic shutting down.")
    finally:
        consumer.close()

if __name__ == "__main__":
    start_mechanic()