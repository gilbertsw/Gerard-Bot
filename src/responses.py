import helper.file_helper as file_helper
from config.app_config import config
import openai

openai.api_key = config.OPENAI_API_KEY

# Container that act as chatGPT knowledge
messages = []

# Add default system prompt to messages
messages.append({"role": "system", "content": file_helper.get_persona()})

def get_open_api_response(message: str) -> str:
    # Add user message to messages
    messages.append({"role": "user", "content": message})

    # Hit chatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]

    print("\n" + reply + "\n") # Debug

    # Add chatGPT reply to messages
    messages.append({"role": "assistant", "content": reply})

    return reply

def get_response(message: str) -> str:
    response = get_open_api_response(message)
    print(response) # Debug
    return response
