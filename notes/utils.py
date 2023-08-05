from settings import settings
import requests


def fetch_user(user_id: int):
    res = requests.get(f'{settings.base_url}:{settings.user_port}/retrieve/',
                       params={'user_id': user_id})
    if res.status_code >= 400:
        return None
    return res.json().get('data')
