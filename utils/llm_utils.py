from openai import OpenAI
from config import settings

client = OpenAI(api_key=AIzaSyBstrHBTZ8Z6ndfnAw0nGggXRtY4XBRb4c)  # replace with your key

def generate_response(prompt: str, max_tokens=200) -> str:
    response = client.chat.completions.create(
        model="gemini-pro",  # your Google Gemini Pro model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content
