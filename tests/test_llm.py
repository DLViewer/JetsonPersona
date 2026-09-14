import requests


LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"


def ask_llm(message: str) -> str:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": message,
            }
        ]
    }

    response = requests.post(
        LLM_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def main():
    print("JetsonPersona LLM Test")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            break

        if not user_input:
            continue

        try:
            reply = ask_llm(user_input)
            print(f"JetsonPersona: {reply}\n")

        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()
