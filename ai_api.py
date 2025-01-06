import requests

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "57a0a7ce-81e6-4430-a570-5c38766b3ffd"
FLOW_ID = "cc661ea7-8534-4eb7-97da-740121bdb533"
APPLICATION_TOKEN = "AstraCS:vAERjEmCXtKPYqzehSPOihdW:0f82b54a11a248c3c2b3a2dd7aadb2d659c7c159802b48a737356d22e401b9e4"
ENDPOINT = "ask-ai-v2"


def ask_ai(question: str, profile: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    # Define the tweaks for the question and profile inputs
    tweaks = {
        "TextInput-GesrA": {
            "input_value": question
        },
        "TextInput-4MiiN": {
            "input_value": profile
        },
    }

    # Prepare the payload with tweaks
    payload = {
        "tweaks": tweaks,
        "flow_id": FLOW_ID
    }

    # Add headers with the application token for authentication
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()  # Return the JSON response


# Example usage
question = "I need to know the best way to build abs and back muscles"
profile = "Male; 25; 5'10; 180lbs; 3 times a week; 1 hour per session; 1 year of experience; no injuries"

try:
    result = ask_ai(question, profile)
    print(result['outputs'][0]['outputs'][0]['results']['text']['data']['text'])
except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")
