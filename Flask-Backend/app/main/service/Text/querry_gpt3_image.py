
import os
import openai
import requests
import json
import logging
from .gpt3_validation import get_request_result

log = logging.getLogger(__name__)

TOKEN = os.getenv("OPENAI_API_KEY")


def querry_qpt3_image(data: dict):
    """Querring GPT3"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': TOKEN
    }
    body={ 
        "model": "text-davinci-003",
        "prompt": data['prompt'],
        "n": data['n'],
        "size": data['size']
    }
    url = "https://api.openai.com/v1/completions"
    log.info(f"Body request for url {url}:  {body}")

    request = requests.get(url, headers=headers, data=body)
    log.info(f"\nRequest reponse: {request.text}")
    print(request.text)
    return get_request_result(request)

