import requests
from colorama import Fore
import json

def fetch_tags():
    url = "http://127.0.0.1:11434/api/tags"
    formatted_models = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for index, model in enumerate(data.get('models', []), start=1):
            formatted_models.append(f"[{Fore.LIGHTYELLOW_EX}{index}{Fore.RESET}] {model['name']}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return formatted_models
    
def chat(model, messages, tools=None, stream=True, options=None):
    url = "http://127.0.0.1:11434/api/chat"

    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
    }

    if tools:
        payload["tools"] = tools

    if options:
        payload["options"] = options

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        if not stream:
            return response.json()
        
        responses = []
        for line in response.iter_lines():
            if line:
                responses.append(json.loads(line))
        
        return responses

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
