import json

from settings import settings
import requests


def fetch_user(user_id: int):
    res = requests.get(f'{settings.base_url}:{settings.user_port}/retrieve/',
                       params={'user_id': user_id})
    if res.status_code >= 400:
        return None
    return res.json().get('data')


def fetch_label(label_id: list):
    res = requests.post(f'{settings.base_url}:{settings.label_port}/retrieve/',
                        json={'label_id': label_id}, headers={'content_type': 'application/json'})
    if res.status_code >= 400:
        data = json.loads(res.content)
        raise Exception(data.get('message'))
    return res.json().get('data')
