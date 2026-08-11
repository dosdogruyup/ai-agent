import os
from dotenv import load_dotenv
from openai import OpenAI



def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("API Key not found")

    client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            # "content": "Which model are you?"
        }
    ]
    
    response = client.chat.completions.create(messages=messages, model="openrouter/free")

        
    if not (response.usage.prompt_tokens == None or response.usage.completion_tokens == None):
        print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}\n\nUser prompt: {messages[0]["content"]}\nResponse: {response.choices[0].message.content}")
    else:
        raise RuntimeError("Token usage not found")
if __name__ == "__main__":
    main()
