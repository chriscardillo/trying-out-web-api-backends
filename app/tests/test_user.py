import pytest
from tests import client, graphql_endpoint, site_secure
from tests.help import (basic_auth_header, extract_token, json_response,
                        register, login, update_user, delete_user)

@pytest.fixture(scope='module')
def current_user_header(client, graphql_endpoint):
    """Registering a user and getting back our token"""
    response = client.post(graphql_endpoint, data = dict(query=register("current", "user@app.com", "user")))
    registration_token = extract_token(response, 'register')
    registration_token_header = basic_auth_header(registration_token, "anytext")
    return registration_token_header

def test_update_user(client, graphql_endpoint, current_user_header):
    response = client.post(graphql_endpoint,
                           data = dict(query=update_user('mario')),
                           headers=current_user_header)
    response_json = json_response(response)
    assert response._status_code == 200
    assert response_json['data']['updateUser']['ok']

def test_confirmed_update(client, site_secure, current_user_header):
    response = client.get(site_secure, headers=current_user_header)
    assert response._status_code == 200
    assert 'mario' in str(response.data)

def test_password_header(client, site_secure):
    response = client.get(site_secure, headers=basic_auth_header('mario', 'user'))
    assert response._status_code == 200
    assert 'mario' in str(response.data)

def test_delete_user(client, graphql_endpoint, current_user_header):
    response = client.post(graphql_endpoint,
                           data = dict(query=delete_user()),
                           headers=current_user_header)
    response_json = json_response(response)
    assert response._status_code == 200
    assert response_json['data']['deleteUser']['ok']

def test_user_is_deleted(client, graphql_endpoint):
    response = client.post(graphql_endpoint, data = dict(query=login("mario", "user")))
    response_json = json_response(response)
    assert 'errors' in response_json.keys()
    assert response._status_code == 200
