from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

import os

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
else:
    raise ValueError("No OpenAI API Key found. Please set the OPENAI_API_KEY environment variable.")

def get_openai_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model="gpt-3.5-turbo"
            )
        response_text = chat_completion.choices[0].message['content'] if chat_completion.choices else "No response generated."
        return response_text
    except Exception as e:
        raise Exception(f"Failed to get response from OpenAI: {e}")
