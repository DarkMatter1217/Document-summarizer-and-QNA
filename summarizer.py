import requests
import os
from dotenv import load_dotenv

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def summarize_with_perplexity(text, max_tokens=150):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Summarize the following content in under 150 words , Summary can be in points or in paragraph or mixture of both and the summary should be clean without any hyperlinks :\n\n{text[:4000]}"

    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
