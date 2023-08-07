from core import create_app, db
from flask import request
from settings import settings
from notes.models import Notes, Collaborator, NoteLabel
from flask_restx import Resource, Api
from core.middlewares import verify_token
from core.utils import exception_handler
from notes.swagger_schema import get_model
from notes import utils

app = create_app(settings.config_mode)

api = Api(app=app,
          default='Notes',
          title='Notes',
          default_label='API',
          security='Bearer',
          doc='/docs',
          authorizations={"Bearer": {"type": "apiKey", "in": "header", "name": "token"}})

api_model = lambda x: api.model(x, get_model(x))


@api.route('/notes')
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
        notes = list(map(lambda x: x.to_dict(), Notes.query.filter_by(user_id=kwargs.get('user_id'))))
        collab_notes = list(map(lambda x: Notes.query.get(x.note_id).to_dict(),
                                Collaborator.query.filter_by(user_id=kwargs.get('user_id'))))
        notes.extend(collab_notes)
        notes.sort(key=lambda x: x.get('id'))
        return {'message': 'Notes Retrieved', 'status': 200, 'data': notes}, 200

    @api.doc(body=api_model('note_update'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def put(self, *args, **kwargs):
        note = utils.check_note_accessibility(request.json.get('id'), request.json.get('user_id'))
        if not note:
            raise Exception('Access denied or note not found')
        [setattr(note, x, y) for x, y in request.json.items() if x != 'user_id']
        db.session.commit()
        return {'message': 'Note updated', 'status': 200, 'data': note.to_dict()}, 200

    @api.doc(params={'note_id': {'description': 'Provide note id to delete the note', 'required': True}})
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def delete(self, *args, **kwargs):
        note = Notes.query.filter_by(id=request.args.to_dict().get('note_id'), user_id=kwargs.get('user_id')).first()
        db.session.delete(note)
        db.session.commit()
        return {'message': 'Note deleted', 'status': 200, 'data': {}}, 200


@api.route('/notes/collaborator')
class CollaboratorRest(Resource):

    @api.doc(body=api_model('collaborator'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def post(self, *args, **kwargs):
        note = Notes.query.filter_by(id=request.json.get('note_id'), user_id=request.json.get('user_id')).first()
        if not note:
            raise Exception('Note not found')
        collab_obj = []
        for user in request.json.get('collaborators'):
            if user == request.json.get('user_id'):
                raise Exception('Trying to collaborate not with yourself')
            user_data = utils.fetch_user(user)
            if not user_data:
                raise Exception(f'User {user} not found')
            if Collaborator.query.filter_by(note_id=note.id, user_id=user_data['id']).first():
                raise Exception(f'Note {note.id} already shared with user {user}')
            collab_obj.append(Collaborator(note_id=note.id, user_id=user_data['id'],
                                           access_type=request.json.get('access_type')))
        db.session.add_all(collab_obj)
        db.session.commit()
        return {'message': 'Collaborator added', 'status': 200, 'data': {}}

    @api.doc(body=api_model('delete_collaborator'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def delete(self, *args, **kwargs):
        note = Notes.query.filter_by(id=request.json.get('note_id'), user_id=kwargs.get('user_id')).first()
        if not note:
            raise Exception('Note not found')
        collab_obj = []
        for user in request.json.get('collaborators'):
            user_data = utils.fetch_user(user)
            if not user_data:
                raise Exception(f'User {user} not found')
            collaborated_user = Collaborator.query.filter_by(note_id=note.id, user_id=user_data['id']).first()
            if not collaborated_user:
                raise Exception(f'Note {note.id} is not collaborated with user {user}')
            collab_obj.append(collaborated_user)
        [db.session.delete(x) for x in collab_obj]
        db.session.commit()
        return {'message': 'Collaborator deleted', 'status': 200, 'data': {}}


@api.route('/labelm2m')
class LabelAssociate(Resource):

    @api.doc(body=api_model('label_m2m'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def post(self, *args, **kwargs):
        note = Notes.query.filter_by(id=request.json.get('note_id'), user_id=request.json.get('user_id')).first()
        if not note:
            raise Exception('Note not found')
        label_data = utils.fetch_label(request.json.get('labels'))
        objs = [NoteLabel(note_id=note.id, label_id=i.get('id')) for i in label_data]
        db.session.add_all(objs)
        db.session.commit()
        return {'message': 'Label added to note', 'status': 200, 'data': {}}

    @api.doc(body=api_model('label_m2m'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def delete(self, *args, **kwargs):
        note = Notes.query.filter_by(id=request.json.get('note_id'), user_id=kwargs.get('user_id')).first()
        if not note:
            raise Exception('Note not found')
        NoteLabel.query.filter(NoteLabel.note_id == note.id,
                               NoteLabel.label_id.in_(request.json.get('labels'))
                               ).delete()
        db.session.commit()
        return {'message': 'Label removed from note', 'status': 200, 'data': {}}
