"""
Shared Vertex AI Agent client utilities.
Used by all remediation Cloud Functions.
"""

import os
from google.cloud import aiplatform
from google.protobuf.field_mask_pb2 import FieldMask
from google.cloud.aiplatform_v1.services.agent_service import AgentServiceClient
from google.cloud.aiplatform_v1.types import agent as agent_types


PROJECT_ID = os.environ["GCP_PROJECT"]
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")


def _client() -> AgentServiceClient:
    return AgentServiceClient(
        client_options={"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
    )


def _agent_name(agent_id: str) -> str:
    return f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{agent_id}"


def update_agent_instruction(agent_id: str, system_instruction: str):
    """
    Safely update ONLY the system instruction using FieldMask.
    """
    client = _client()

    agent = agent_types.Agent(
        name=_agent_name(agent_id),
        system_instruction=system_instruction,
    )

    update_mask = FieldMask(paths=["system_instruction"])

    return client.update_agent(
        agent=agent,
        update_mask=update_mask,
    )


def suspend_agent(agent_id: str):
    """
    Suspend an agent immediately (hard stop).
    """
    client = _client()
    return client.pause_agent(name=_agent_name(agent_id))


def resume_agent(agent_id: str):
    """
    Resume a previously suspended agent.
    """
    client = _client()
    return client.resume_agent(name=_agent_name(agent_id))
