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
