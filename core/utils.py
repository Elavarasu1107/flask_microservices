import json

from flask_restx import fields
from werkzeug.exceptions import Unauthorized
import logging

logger = logging.getLogger('file_logger')


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
            logger.exception(str(ex))
            return {'message': str(ex), 'status': 401, 'data': {}}, 401
        except Exception as ex:
            logger.exception(str(ex))
            return {'message': str(ex), 'status': 400, 'data': {}}, 400
    wrapper.__name__ = function.__name__
    return wrapper
