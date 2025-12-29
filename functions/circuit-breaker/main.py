import time
from flask import Request, jsonify

from functions.shared.vertex_ai_client import suspend_agent, resume_agent
from functions.shared.kafka_producer import publish_remediation_event


COOLDOWN_SECONDS = 30


def circuit_breaker(request: Request):
    """
    Immediately suspend an agent, then auto-resume after cooldown.
    """
    try:
        payload = request.get_json(force=True)

        agent_id = payload.get("agent_id")
        session_id = payload.get("session_id")
        failure_type = payload.get("failure_type", "RUNAWAY_AGENT")

        if not agent_id:
            return jsonify({"error": "agent_id missing"}), 400

        # Hard stop
        suspend_agent(agent_id)

        publish_remediation_event(
            agent_id=agent_id,
            session_id=session_id,
            action="AGENT_SUSPENDED",
            failure_type=failure_type,
            success=True,
        )

        # Cooldown
        time.sleep(COOLDOWN_SECONDS)

        # Auto-resume
        resume_agent(agent_id)

        publish_remediation_event(
            agent_id=agent_id,
            session_id=session_id,
            action="AGENT_RESUMED",
            failure_type="COOLDOWN_COMPLETE",
            success=True,
        )

        return jsonify({
            "status": "SUSPENDED_AND_RESUMED",
            "agent_id": agent_id,
            "cooldown_seconds": COOLDOWN_SECONDS,
        }), 200

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "error": str(e),
        }), 500
