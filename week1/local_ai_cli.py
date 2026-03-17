import requests

def ask_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            # "model": "mistral",
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data["response"]


def main():
    question = "can you give me plan become Agentic AI in 1 month give me plan for week 1 and week2 etc,,"

    answer = ask_llm(question)

    print("\nAI Response:\n")
    print(answer)


if __name__ == "__main__":
    main()