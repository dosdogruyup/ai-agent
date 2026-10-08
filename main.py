import argparse
import os
import sys
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from call_function import available_functions, call_function
from prompts import system_prompt


def message_create(client: OpenAI, messages: list[ChatCompletionMessageParam], args: argparse.Namespace) -> None | str:
    response = client.chat.completions.create(messages=messages, model="openrouter/free", tools=available_functions)
    message = response.choices[0].message

    messages.append(cast(ChatCompletionMessageParam, message.model_dump()))

    if message.tool_calls:
        call_results: list[ChatCompletionMessageParam] = []
        if args.verbose:
            print(message.content)
        for tool_call in message.tool_calls:
            call_results.append(call_function(tool_call, args.verbose))
        messages.extend(call_results)
        return None
    else:
        return message.content

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

    messages: list[ChatCompletionMessageParam]=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt,}
    ]

    for _ in range(20):
        result = message_create(client, messages, args)
        if result is not None:
            print(f"\nFinal Response: {result}")
            return

    print("Max iterations reached without a final response")
    sys.exit(1)

if __name__ == "__main__":
    main()
