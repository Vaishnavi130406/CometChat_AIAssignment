from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY was not found in .env")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Reply with exactly: API connection successful."
)

print(response.output_text)