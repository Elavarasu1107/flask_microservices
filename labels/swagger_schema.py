from flask_restx import fields
from core.utils import DictField

models = {
    'label_schema': {
        'name': fields.String,
        'color': fields.String
    },
    'label_update': {
        'id': fields.Integer,
        'name': fields.String,
        'color': fields.String
    },
    'response': {
        'message': fields.String,
        'status': fields.Integer,
        'data': DictField
    }
}


def get_model(name):
    return models.get(name) if models.get(name) else {}
