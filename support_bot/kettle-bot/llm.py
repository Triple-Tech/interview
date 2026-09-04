import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "openai")
MODEL = os.getenv("MODEL")


def ask(messages, system):
    if PROVIDER == "openai":
        return ask_openai(messages, system)
    else:
        return ask_anthropic(messages, system)


def ask_openai(messages, system):
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}] + messages,
        max_completion_tokens=600,
        reasoning_effort="low",
    )
    return resp.choices[0].message.content


def ask_anthropic(messages, system):
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=system,
        messages=messages,
    )
    return resp.content[0].text
