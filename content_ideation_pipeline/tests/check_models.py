from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("🔎 Scanning available models...")
try:
    # We will just print the object as a string to be 100% safe
    for m in client.models.list():
        print(f"✅ Found: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")