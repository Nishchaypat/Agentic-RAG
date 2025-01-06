from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import asyncio

load_dotenv()

def ask_ai(question, profile):
  TWEAKS = {
    "AstraVectorStoreComponent": {
        "user_id": "jWptGwJhkTEpEGGLEYewDYey"
    },
    "TextInput-GesrA": {
      "input_value": question
    },
    "TextInput-4MiiN": {
      "input_value": profile
    },
  }

  result = run_flow_from_json(flow="AskAIV2.json",
                              input_value="message",
                              fallback_to_env_vars=True,
                              tweaks=TWEAKS)

  return result[0].ouputs[0].result['text'].data['text']

question = "I need to know the best way to build abs and back muscles"
profile = "Male; 25; 5'10; 180lbs; 3 times a week; 1 hour per session; 1 year of experience; no injuries"
print(ask_ai(question, profile))
