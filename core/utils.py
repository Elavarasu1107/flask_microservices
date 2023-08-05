import json

from flask_restx import fields
from werkzeug.exceptions import Unauthorized


class DictField(fields.Raw):
    __schema_type__ = 'object'
    __schema_format__ = 'json'

    def format(self, value):
        if isinstance(value, bytes):
            return json.loads(value)
        return value


def exception_handler(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Unauthorized as ex:
            return {'message': str(ex), 'status': 401, 'data': {}}, 401
        except Exception as ex:
            return {'message': str(ex), 'status': 400, 'data': {}}, 400
    return wrapper

# def exception_handler(cls):
#     class ExceptionClass:
#
#         def __init__(self, *args, **kwargs):
#             self.instance = cls(*args, **kwargs)
#
#         def __getattribute__(self, item):
#             try:
#                 print('Hi')
#                 return super(ExceptionClass, self).__getattribute__(item)
#             except Unauthorized as ex:
#                 return {'message': str(ex), 'status': 401, 'data': {}}, 401
#             except Exception as ex:
#                 return {'message': str(ex), 'status': 400, 'data': {}}, 400
#     return ExceptionClass
