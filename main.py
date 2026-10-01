import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions
from prompts import system_prompt


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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt,}
    ]
    response = client.chat.completions.create(messages=messages, model="openrouter/free", tools=available_functions)
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            if tool_call.type == "function":
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")

    elif response.usage and args.verbose:
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
