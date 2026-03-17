import requests

history = []

SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer clearly and briefly.
"""


def ask_llm(question):

    global history

    history.append(f"User: {question}")

    context = SYSTEM_PROMPT + "\n".join(history)
    print(context)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": context,
            "stream": False
        }
    )

    answer = response.json()["response"]

    history.append(f"AI: {answer}")

    return answer


def chat():

    print("AI Assistant (type 'exit' to quit)\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = ask_llm(question)

        print("\nAI:", answer)


if __name__ == "__main__":
    chat()