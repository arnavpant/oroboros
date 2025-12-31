# debug_models.py
import vertexai
from vertexai.generative_models import GenerativeModel
import os

PROJECT_ID = "ouroboros-ai-20251224005056"
LOCATION = "us-east4"

def test_models():
    print(f"🔍 Testing access for project: {PROJECT_ID} in {LOCATION}")
    
    # List of models to try, from newest to oldest
    models_to_test = [
        "gemini-1.5-flash-001",
        "gemini-1.5-flash",
        "gemini-1.5-pro-001",
        "gemini-1.0-pro",
        "gemini-3-flash-preview"
    ]

    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
    except Exception as e:
        print(f"❌ Critical: Vertex AI Init failed: {e}")
        return

    for model_name in models_to_test:
        print(f"\n--- Testing {model_name} ---")
        try:
            model = GenerativeModel(model_name)
            # Try a simple generation to prove access
            response = model.generate_content("Hello")
            print(f"✅ SUCCESS! Model '{model_name}' is working.")
            print(f"   Response: {response.text.strip()}")
            return  # Stop after finding the first working model
        except Exception as e:
            # We expect 404s here if the model isn't found
            error_str = str(e)
            if "404" in error_str:
                print(f"❌ 404 Not Found (Model unavailable)")
            elif "403" in error_str:
                print(f"⛔ 403 Permission Denied (API not enabled or IAM issue)")
            else:
                print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    test_models()