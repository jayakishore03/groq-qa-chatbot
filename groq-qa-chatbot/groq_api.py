import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = "Your api key"  # Replace with your actual Groq API key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"  # or "gemma-7b-it"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def ask_groq(question: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer the following question:"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 2000:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"
