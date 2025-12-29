import vertexai
from vertexai.preview.generative_models import GenerativeModel

vertexai.init(project="ouroboros-ai-20251224005056", location="us-central1")

model = GenerativeModel("gemini-2.0-flash-lite")

def call_llm(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
