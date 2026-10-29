import os
import requests
from dotenv import load_dotenv

# Load variables from your .env file
load_dotenv()

# Change this if your .env uses GROQ_API_KEY instead of LLM_API_KEY
api_key = os.getenv("LLM_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: Could not find API key in .env file.")
    exit()

print("Fetching active models...")
url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("\n--- YOUR AVAILABLE MODELS ---")
    models = response.json().get("data", [])
    for model in models:
        print(f"- {model['id']}")
else:
    print(f"Error fetching models: {response.status_code}")
    print(response.text)