from flask import request
import requests as http
from settings import settings


def verify_token(function):
    def wrapper(*args, **kwargs):
        if not request.headers.get('token'):
            return {'message': 'Jwt required', 'status': 401, 'data': {}}, 401
        res = http.post(f'{settings.base_url}:{settings.user_port}/authenticate/',
                        headers={'token': request.headers.get('token')})
        if res.status_code >= 400:
            return {'message': res.json()['message'], 'status': res.status_code, 'data': {}}, res.status_code
        if request.method not in ['GET', 'DELETE']:
            request.json['user_id'] = res.json()['id']
        else:
            kwargs.update({'user_id': res.json()['id']})
        return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper
