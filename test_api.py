import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load API key from vault
load_dotenv("/mnt/scratch/vault/central_keys.env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("🔍 Testing Evolution Studio API connection...")
print()

# Test message
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say 'Evolution Studio API is connected!' in a tech-savvy way."}
    ]
)

print(message.content[0].text)
print()
print("✅ API connection successful!")
print(f"📊 Tokens used: {message.usage.input_tokens} in, {message.usage.output_tokens} out")
