import pytest
import responses

from core import db, create_app
from flask_restx import Api

from settings import settings
from user import views as us, models
from notes import views as ns


@pytest.fixture()
def user_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    api = Api(app)
    api.add_resource(us.LoginUser, '/login/')
    api.add_resource(us.RegisterUser, '/user/')
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def note_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    api = Api(app)
    api.add_resource(ns.NotesRest, '/notes')
    api.add_resource(ns.CollaboratorRest, '/notes/collaborator')
    api.add_resource(ns.LabelAssociate, '/labelm2m')
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def user_client(user_app):
    return user_app.test_client()


@pytest.fixture()
def note_client(note_app):
    return note_app.test_client()


@pytest.fixture()
def token(user_client, user_app):
    data = {
        "username": "appu",
        "password": "password",
        "first_name": "Elavarasu",
        "last_name": "Appusamy",
        "email": "elavarasu.107@gmail.com",
        "phone": "9087654321",
        "location": "Salem"
    }
    response = user_client.post('/user/', json=data, headers={'content_type': 'application/json'})
    with user_app.app_context():
        user = models.User.query.get(response.json['data']['id'])
        user.is_verified = True
        db.session.commit()
    data = {
        "username": "appu",
        "password": "password"
    }
    response = user_client.post('/login/', json=data, headers={'content_type': 'application/json'})
    return response.json['data']['access']


@pytest.fixture()
def authenticate_user(token):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as res:
        res = responses.add(
            method=responses.POST,
            url=f'{settings.base_url}:{settings.user_port}/authenticate/',
            headers={'token': token},
            json={'id': 1, 'username': 'appu', 'first_name': 'Elavarasu', 'last_name': 'Appusamy',
                  'email': 'elavarasu.107@gmail.com', 'phone': 9087654321, 'location': 'salem',
                  'is_superuser': False, 'is_verified': True}
        )
        yield res
