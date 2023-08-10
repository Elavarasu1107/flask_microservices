import pytest
import responses


@responses.activate
def test_create_note_successful(note_client, token, authenticate_user):
    data = {
        "title": "RDBMS",
        "description": "Postgresql"
    }
    response = note_client.post('/notes', json=data, headers={'content_type': 'application/json', 'token': token})
    assert response.status_code == 201


@responses.activate
def test_create_note_unsuccessful(note_client, token, authenticate_user):
    response = note_client.post('/notes', headers={'content_type': 'application/json', 'token': token})
    assert response.status_code == 415
