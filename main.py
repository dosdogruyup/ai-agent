import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key not found")
    client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list=[
        {
            "role": "user",
            "content": args.user_prompt,
            # "content": "Which model are you?"
        }
    ]
    response = client.chat.completions.create(messages=messages, model="openrouter/free")

    if response.usage and args.verbose:
        print(
            f"Prompt tokens: {response.usage.prompt_tokens}\n\n"
            f"Response tokens: {response.usage.completion_tokens}\n\n\n"
            f"User prompt: {messages[0]["content"]}\n\n"
            f"Response: {response.choices[0].message.content}"
        )
    elif response.usage and not args.verbose:
        print(f"Response: {response.choices[0].message.content}")
    else:
        raise RuntimeError("Token usage not found")

if __name__ == "__main__":
    main()
