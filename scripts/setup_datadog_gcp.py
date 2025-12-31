import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")
DD_SITE = os.getenv("DD_SITE", "datadoghq.com")

KEY_FILE = "config/keys/datadog-sa-key.json"

def setup_integration():
    if not os.path.exists(KEY_FILE):
        print(f"Error: Key file not found at {KEY_FILE}")
        return

    with open(KEY_FILE, "r") as f:
        sa_key = json.load(f)

    url = f"https://api.{DD_SITE}/api/v1/integration/gcp"
    
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY
    }

    # The payload is essentially the service account key JSON
    # plus any optional configuration like host_filters
    payload = sa_key
    payload["host_filters"] = ""
    payload["automute"] = True

    print(f"Sending request to {url}...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Successfully configured Datadog GCP Integration!")
        print(response.json())
    elif response.status_code == 400 and "already exists" in response.text:
         print("⚠️ Integration already exists. Updating...")
         # Try update if needed, or just report success
         print(response.text)
    else:
        print(f"❌ Failed to configure integration. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    setup_integration()
