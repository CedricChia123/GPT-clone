from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

from .schema.responses import APIError
from .schema.conversation_schema import Prompt

import os

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
else:
    raise ValueError(
        "No OpenAI API Key found. Please set the OPENAI_API_KEY environment variable."
    )


def prompt_to_dict(prompt):
    return {"role": prompt.role.value, "content": prompt.content}


def get_openai_response(prompt, context=None, params=None):
    messages = []
    if context:
        messages.extend([prompt_to_dict(item) for item in context])
    messages.append(prompt)
    chat_completion = client.chat.completions.create(
        messages=messages, model="gpt-3.5-turbo", **(params or {})
    )
    response_text = (
        chat_completion.choices[0].message.content
        if chat_completion.choices and chat_completion.choices[0].message
        else "No response generated."
    )
    tokens_used = chat_completion.usage.total_tokens
    return {
        "response": Prompt(role="assistant", content=response_text),
        "tokens_used": tokens_used,
    }
