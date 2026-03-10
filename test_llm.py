import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": "Explain artificial intelligence",
        "stream": False
    }
)

print(response.json()["response"])