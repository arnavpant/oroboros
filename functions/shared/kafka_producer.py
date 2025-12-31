"""
Shared Kafka producer for remediation events.
Emits immutable audit records for every autonomous action.
"""

import json
import os
from datetime import datetime
from confluent_kafka import Producer


KAFKA_BOOTSTRAP = os.environ["KAFKA_BOOTSTRAP"]
KAFKA_API_KEY = os.environ["KAFKA_API_KEY"]
KAFKA_API_SECRET = os.environ["KAFKA_API_SECRET"]
KAFKA_TOPIC = os.environ.get(
    "KAFKA_REMEDIATION_TOPIC", "agent.remediations.v1"
)
KAFKA_THOUGHTS_TOPIC = os.environ.get(
    "KAFKA_THOUGHTS_TOPIC", "agent.thoughts.v1"
)


_conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP,
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": KAFKA_API_KEY,
    "sasl.password": KAFKA_API_SECRET,
    "linger.ms": 5,
}


_producer = Producer(_conf)


def publish_remediation_event(
    agent_id: str,
    session_id: str | None,
    action: str,
    failure_type: str,
    success: bool,
    cost_saved: float | None = None,
):
    """
    Emit a remediation event to Kafka.
    """
    event = {
        "agent_id": agent_id,
        "session_id": session_id,
        "action": action,
        "failure_type": failure_type,
        "success": success,
        "cost_saved": cost_saved,
        "timestamp": datetime.utcnow().isoformat(),
    }

    _producer.produce(
        topic=KAFKA_TOPIC,
        value=json.dumps(event).encode("utf-8"),
        key=agent_id.encode("utf-8"),
    )
    _producer.flush()


def publish_agent_thought(
    agent_id: str,
    session_id: str,
    role: str,
    input_prompt: str,
    output_text: str,
    token_count: int,
    tools_used: list = None
):
    """
    Emit an agent thought/step event to Kafka.
    """
    if tools_used is None:
        tools_used = []

    event = {
        "agent_id": agent_id,
        "session_id": session_id,
        "role": role,  # e.g., "planner", "researcher", "analyst"
        "input_prompt": input_prompt,
        "output_text": output_text,
        "token_count": token_count,
        "tools_used": tools_used,
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Use session_id as key to keep conversation steps ordered in the same partition
    _producer.produce(
        topic=KAFKA_THOUGHTS_TOPIC,
        value=json.dumps(event).encode("utf-8"),
        key=session_id.encode("utf-8"),
    )
    # Note: We rely on standard poll() usually, but for low volume 
    # immediate consistency in this POC, we can flush if needed, 
    # though it hurts throughput. For now, let's rely on linger.ms=5.
    _producer.poll(0)
