from flask_restx import fields
from core.utils import DictField

models = {
    'note_schema': {
        'title': fields.String,
        'description': fields.String
    },
    'note_update': {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    },
    'response': {
        'message': fields.String,
        'status': fields.Integer,
        'data': DictField
    }
}


def get_model(name):
    return models.get(name) if models.get(name) else {}
