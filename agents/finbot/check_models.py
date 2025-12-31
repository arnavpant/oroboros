import vertexai
from vertexai.preview.generative_models import GenerativeModel

PROJECT_ID = "ouroboros-ai-20251224005056"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

try:
    model = GenerativeModel("gemini-3-flash-preview")
    print("✅ gemini-pro is available!")
except Exception as e:
    print(f"❌ gemini-pro failed: {e}")

try:
    model = GenerativeModel("gemini-1.5-flash-001")
    print("✅ gemini-1.5-flash-001 is available!")
except Exception as e:
    print(f"❌ gemini-1.5-flash-001 failed: {e}")
