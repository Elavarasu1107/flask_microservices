from core import create_app, db
from flask import request
from settings import settings
from flask_restx import Resource, Api
from core.middlewares import verify_token
from labels.models import Label
from core.utils import exception_handler
from labels.swagger_schema import get_model

app = create_app(settings.config_mode)

api = Api(app=app,
          default='Label',
          title='Label',
          default_label='API',
          security='Bearer',
          doc='/docs',
          authorizations={"Bearer": {"type": "apiKey", "in": "header", "name": "token"}})

api_model = lambda x: api.model(x, get_model(x))


@api.route('/label')
class LabelRest(Resource):
    @api.doc(body=api_model('label_schema'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def post(self, *args, **kwargs):
        label = Label(**request.json)
        db.session.add(label)
        db.session.commit()
        label = Label.query.get(label.id)
        return {'message': 'Label created', 'status': 201, 'data': label.to_dict()}, 201

    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def get(self, *args, **kwargs):
        labels = list(map(lambda x: x.to_dict(), Label.query.filter_by(user_id=kwargs.get('user_id'))))
        return {'message': 'Label Retrieved', 'status': 200, 'data': labels}, 200

    @api.doc(body=api_model('label_update'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def put(self, *args, **kwargs):
        label = Label.query.filter_by(id=request.json.get('id'), user_id=request.json.get('user_id')).first()
        [setattr(label, x, y) for x, y in request.json.items()]
        db.session.commit()
        return {'message': 'Label updated', 'status': 200, 'data': label.to_dict()}, 200

    @api.doc(params={'label_id': {'description': 'Provide label id to delete the label', 'required': True}})
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    @verify_token
    def delete(self, *args, **kwargs):
        label = Label.query.filter_by(id=request.args.to_dict().get('label_id'), user_id=kwargs.get('user_id')).first()
        db.session.delete(label)
        db.session.commit()
        return {'message': 'Label deleted', 'status': 200, 'data': {}}, 200


@app.post('/retrieve/')
@exception_handler
def retrieve_label():
    objs = []
    for label in request.json.get('label_id'):
        obj = Label.query.filter_by(id=label).first()
        if not obj:
            return {'message': f'Label {label} not found', 'status': 400, 'data': {}}, 400
        objs.append(obj.to_dict())
    return {'message': 'Label fetched successfully', 'status': 200, 'data': objs}
