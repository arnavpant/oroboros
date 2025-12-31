import vertexai
from vertexai.generative_models import GenerativeModel
# 👇 THIS WAS MISSING
from .tools import finbot_tools  

PROJECT_ID = "ouroboros-ai-20251224005056"
LOCATION = "us-central1"

def init_vertex():
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print(f"✅ Vertex AI Initialized for {PROJECT_ID}")
    except Exception as e:
        print(f"❌ Failed to initialize Vertex AI: {e}")
        print("💡 Tip: Run 'gcloud auth application-default login' if this persists.")

def get_model():
    # Using the working model from your list
    model_name = "gemini-2.0-flash-001" 
    
    try:
        # Load the model with tools attached
        model = GenerativeModel(
            model_name,
            tools=[finbot_tools],
        )
        return model
    except Exception as e:
        print(f"❌ Error loading model '{model_name}': {e}")
        return None