import json
import uuid

import requests

import urllib3

urllib3.disable_warnings()

authority: str | None = None
scope: str = "GIGACHAT_API_PERS"

AUTH_URI = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
MDLS_URI = "https://gigachat.devices.sberbank.ru/api/v1/models"
CHAT_URI = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

def get_token() -> tuple[str, str]:
    response = requests.post(
        AUTH_URI,
        data=f"scope={scope}",
        headers={
            "Authorization": f"Bearer {authority}", 
            "RqUID": str(uuid.uuid1()),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        verify=False)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)


def get_models(token: str) -> dict:
    response = requests.get(
        MDLS_URI, 
        headers={"Authorization": f"Bearer {token}"}, 
        verify=False)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)


def get_reply(token: str, model: str, prompt: str) -> dict:
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
    }
    response = requests.post(
        CHAT_URI,
        json=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        verify=False)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)
