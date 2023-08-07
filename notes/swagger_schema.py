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
    },
    'collaborator': {
        'note_id': fields.Integer,
        'access_type': fields.String('read_only'),
        'collaborators': fields.List(fields.Integer)
    },
    'delete_collaborator': {
        'note_id': fields.Integer,
        'collaborators': fields.List(fields.Integer)
    },
    'label_m2m': {
        'note_id': fields.Integer,
        'labels': fields.List(fields.Integer)
    },
}


def get_model(name):
    return models.get(name) if models.get(name) else {}
