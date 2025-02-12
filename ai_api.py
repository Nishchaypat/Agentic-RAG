from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import requests
from typing import Optional
import json
import os
load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "57a0a7ce-81e6-4430-a570-5c38766b3ffd"
FLOW_ID = "cc661ea7-8534-4eb7-97da-740121bdb533"
APPLICATION_TOKEN = "AstraCS:vAERjEmCXtKPYqzehSPOihdW:0f82b54a11a248c3c2b3a2dd7aadb2d659c7c159802b48a737356d22e401b9e4"
ENDPOINT = "ask-ai-v2"

question = "Build abs and back muscles"
profile = "Tim; Male; 25 years old; 5'10; 180lbs; Exercise 3 times a week; 1 hour per session; 1 year of experience; no injuries"

def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)

def ask_ai(question: str, profile: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    tweaks = {
        "TextInput-GesrA": {
            "input_value": question
        },
        "TextInput-4MiiN": {
            "input_value": profile
        },
    }

    payload = {
        "tweaks": tweaks,
        "flow_id": FLOW_ID
    }

    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    response = response.json()  # Return the JSON response
    return response['outputs'][0]['outputs'][0]['results']['text']['data']['text']

def get_macros(profile, goals):
    TWEAKS = {
        "TextInput-PR5Jb": {
            "input_value": ", ".join(goals)
        },
        "TextInput-PrfY9": {
            "input_value": dict_to_string(profile)
        }
    }
    return run_flow("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)


def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    
    return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
# try:
#     result = ask_ai(question, profile)
#     print(result)
# except requests.exceptions.RequestException as e:
#     print(f"Error occurred: {e}")


#print(get_macros(profile, question))
