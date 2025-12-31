import os
import json
import time
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv('config/kafka.env')

# Setup the "Shout" mechanism
conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET'),
}

producer = Producer(conf)
topic = os.getenv('KAFKA_THOUGHTS_TOPIC')

print(f"💣 Injecting FAILURE signal into {topic}...")

# The fake "Death Message"
death_rattle = {
    "agent_id": "TEST_DUMMY_AGENT",
    "role": "SYSTEM_ALERT",
    "timestamp": time.time(),
    "content": "CRITICAL ERROR: ⚠️ SEMANTIC LOOP DETECTED in reasoning chain. TERMINATE IMMEDIATELY."
}

producer.produce(topic, value=json.dumps(death_rattle))
producer.flush()

print("✅ Signal sent! Check your Mechanic terminal.")