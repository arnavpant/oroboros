import json
import os
from flask import Request, jsonify

from functions.inject_antidote.config import ANTIDOTE_INSTRUCTION
from functions.shared.vertex_ai_client import update_agent_instruction
from functions.shared.kafka_producer import publish_remediation_event


def inject_antidote(request: Request):
    """
    Datadog webhook → inject antidote into Vertex AI agent.
    """
    try:
        payload = request.get_json(force=True)

        agent_id = payload.get("agent_id")
        session_id = payload.get("session_id")
        failure_type = payload.get("failure_type", "SEMANTIC_LOOP")

        if not agent_id:
            return jsonify({"error": "agent_id missing"}), 400

        # Inject antidote
        update_agent_instruction(
            agent_id=agent_id,
            system_instruction=ANTIDOTE_INSTRUCTION,
        )

        # Emit Kafka remediation event
        publish_remediation_event(
            agent_id=agent_id,
            session_id=session_id,
            action="ANTIDOTE_INJECTED",
            failure_type=failure_type,
            success=True,
        )

        return jsonify({
            "status": "ANTIDOTE_INJECTED",
            "agent_id": agent_id,
        }), 200

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "error": str(e),
        }), 500
