from core import create_app, db
from flask import request
from user.models import User
from user import auth
from werkzeug.exceptions import Unauthorized
from settings import settings
from flask_restx import Api, Resource
from user import swagger_schemas
from core.utils import exception_handler
from tasks import send_mail

app = create_app(settings.config_mode)
api = Api(app,
          title='User',
          ordered=True,
          default='User',
          default_label='API')

api_model = lambda x: api.model(x, swagger_schemas.get_model(x))


@api.route('/signup/')
class RegisterUser(Resource):
    @api.doc(body=api_model('register_schema'))
    @api.marshal_with(fields=api_model('response'), code=201)
    @exception_handler
    def post(self):
        request.json['password'] = auth.set_password(request.json['password'])
        user = User(**request.json)
        db.session.add(user)
        db.session.commit()
        user = User.query.get(user.id)
        message = f'{request.host_url}verify?' \
                  f'token={auth.access_token({"user": user.id}, aud=auth.Audience.register.value)}'
        send_mail.delay(payload={'recipient': user.email, 'message': message})
        return {'message': 'User Registered', 'status': 201, 'data': user.to_dict()}, 201


@api.route('/login/')
class LoginUser(Resource):
    @api.doc(body=api_model('login_schema'))
    @api.marshal_with(fields=api_model('response'), code=200)
    @exception_handler
    def post(self):
        user = auth.authenticate(request.json)
        if not user:
            raise Unauthorized(description='Invalid Credentials')
        return {'message': 'Login successful', 'status': 200, 'data': {
            'access': auth.access_token({'user': user.id}, aud=auth.Audience.login.value),
            'refresh': auth.refresh_token({'user': user.id}, aud=auth.Audience.login.value)
        }}, 200


@api.route('/verify')
class VerifyUser(Resource):
    @api.doc(params={'token': {'required': True, 'description': 'Pass jwt token verify registered user'}})
    @api.marshal_with(fields=api_model('response'), code=200)
    @exception_handler
    def get(self):
        token = request.args.to_dict().get('token')
        if not token:
            raise Exception('Token required to verify user registration')
        user = auth.api_key_authenticate(token, auth.Audience.register.value)
        if not user:
            raise Exception('User not found to verify')
        user.is_verified = True
        db.session.commit()
        return {'message': 'User verified successfully', 'status': 200, 'data': {}}, 200


@app.post('/authenticate/')
@exception_handler
def authenticate_user():
    token = request.headers.get('token')
    if not token:
        raise Unauthorized(description='Token not found')
    user = auth.api_key_authenticate(token, auth.Audience.login.value)
    return user


@app.get('/retrieve/')
@exception_handler
def abc():
    user = User.query.filter_by(id=request.args.get('user_id')).first()
    return {'message': 'User retrieved', 'status': 200, 'data': user.to_dict()}
