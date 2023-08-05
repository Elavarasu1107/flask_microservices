import json

from flask_restx import fields, Model
from core.utils import DictField


models = {
    'register_schema': {
        "username": fields.String,
        "password": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "email": fields.String,
        "phone": fields.Integer,
        "location": fields.String
    },
    'login_schema': {
        "username": fields.String,
        "password": fields.String
    },
    'login_response': {
        "access": fields.String,
        "refresh": fields.String
    },
    'response': {
        'message': fields.String,
        'status': fields.Integer,
        'data': DictField
    }
}


def get_model(name):
    return models.get(name) if models.get(name) else {}
