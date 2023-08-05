import requests as http
from settings import settings


class AuthMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response, *args, **kwargs):
        # environ['CONTENT_TYPE'] = 'application/json'
        request = environ['werkzeug.request']
        if not request.headers.get('token'):
            return {'message': 'Jwt required', 'status': 401, 'data': {}}, 401
        res = http.post(f'{settings.base_url}:{settings.user_port}/authenticate/',
                        headers={'token': request.headers.get('token')})
        if res.status_code >= 400:
            return {'message': res.json()['message'], 'status': res.status_code, 'data': {}}, res.status_code
        request.json['user_id'] = res.json()['id']
        # print(dir(req))
        return self.app(environ, start_response)
