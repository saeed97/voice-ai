import openai
import os

# API Key for OpenAI
API_KEY = "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"

import requests

def get_main_points(prompt):
    API_URL = "https://api.openai.com/v1/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.5,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    response = requests.post(API_URL, headers=headers, json=data)
    print(response.text)
    if response.status_code != 200:
        raise Exception("Failed to generate response.")
    response_text = response.json()["choices"][0]["text"]

    points = response_text.split("\n")[:3]
    return points

main_points = get_main_points(f"Three main points about love")
print(main_points)
