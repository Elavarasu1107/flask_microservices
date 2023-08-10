from user.models import User
import pytest
from core import db

register_data = {
    "username": "appu",
    "password": "password",
    "first_name": "Elavarasu",
    "last_name": "Appusamy",
    "email": "elavarasu.107@gmail.com",
    "phone": "9087654321",
    "location": "Salem"
}


def test_user_register_successful(user_client):
    response = user_client.post('/user/', json=register_data, headers={'content_type': 'application/json'})
    assert response.status_code == 201


def test_user_register_unsuccessful(user_client):
    response = user_client.post('/user/', json={}, headers={'content_type': 'application/json'})
    assert response.status_code == 400


def test_login_successful(user_client, user_app):
    response = user_client.post('/user/', json=register_data, headers={'content_type': 'application/json'})
    with user_app.app_context():
        user = User.query.get(response.json['data']['id'])
        user.is_verified = True
        db.session.commit()
    data = {
        "username": "appu",
        "password": "password"
    }
    response = user_client.post('/login/', json=data, headers={'content_type': 'application/json'})
    assert response.status_code == 200


def test_login_unsuccessful(user_client, user_app):
    response = user_client.post('/user/', json=register_data, headers={'content_type': 'application/json'})
    with user_app.app_context():
        user = User.query.get(response.json['data']['id'])
        user.is_verified = True
        db.session.commit()
    data = {
        "username": "app",
        "password": "password"
    }
    response = user_client.post('/login/', json=data, headers={'content_type': 'application/json'})
    assert response.status_code == 401
