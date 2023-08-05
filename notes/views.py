from core import create_app, db
from flask import request
from settings import settings
from notes.models import Notes
from flask_restx import Resource, Api
import requests as http
from core.utils import exception_handler
from notes.swagger_schema import get_model

app = create_app(settings.config_mode)

api = Api(app=app,
          default='Notes',
          title='Notes',
          default_label='API',
          security='Bearer',
          authorizations={"Bearer": {"type": "apiKey", "in": "header", "name": "token"}})

api_model = lambda x: api.model(x, get_model(x))


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
            kwargs.update({'user': res.json()['id']})
        return function(*args, **kwargs)
    return wrapper


@api.route('/notes/')
class NotesRest(Resource):
    @api.doc(body=api_model('note_schema'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def post(self, *args, **kwargs):
        note = Notes(**request.json)
        db.session.add(note)
        db.session.commit()
        note = Notes.query.get(note.id)
        return {'message': 'Note created', 'status': 201, 'data': note.to_dict()}, 201

    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def get(self, *args, **kwargs):
        notes = list(map(lambda x: x.to_dict(), Notes.query.filter_by(user_id=kwargs.get('user'))))
        return {'message': 'Notes Retrieved', 'status': 200, 'data': notes}, 200

    @api.doc(body=api_model('note_update'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def put(self, *args, **kwargs):
        note = Notes.query.filter_by(id=request.json.get('id'), user_id=request.json.get('user_id')).first()
        [setattr(note, x, y) for x, y in request.json.items()]
        db.session.commit()
        return {'message': 'Note updated', 'status': 200, 'data': note.to_dict()}, 200

    @api.doc(params={'note_id': {'description': 'Provide note id to delete the note', 'required': True}})
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def delete(self, *args, **kwargs):
        note = Notes.query.filter_by(id=request.args.to_dict().get('note_id'), user_id=kwargs.get('user')).first()
        db.session.delete(note)
        db.session.commit()
        return {'message': 'Note deleted', 'status': 200, 'data': {}}, 200