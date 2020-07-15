import pytest
from tests import client, graphql_endpoint, site_secure
from tests.help import (basic_auth_header, extract_token, json_response,
                        register, login, update_user, delete_user)

@pytest.fixture(scope='module')
def user1_header(client, graphql_endpoint):
    """Registering a user and getting back our token"""
    response = client.post(graphql_endpoint, data = dict(query=register("user1", "user1@app.com", "user")))
    registration_token = extract_token(response, 'register')
    registration_token_header = basic_auth_header(registration_token)
    return registration_token_header

@pytest.fixture(scope='module')
def user2_header(client, graphql_endpoint):
    """Registering a user and getting back our token"""
    response = client.post(graphql_endpoint, data = dict(query=register("user2", "user2@app.com", "user")))
    registration_token = extract_token(response, 'register')
    registration_token_header = basic_auth_header(registration_token)
    return registration_token_header

def test_different_headers(user1_header, user2_header):
    assert  user1_header != user2_header

def test_same_name_change(client, graphql_endpoint, user1_header):
    response = client.post(graphql_endpoint,
                           data = dict(query=update_user('UseR1')),
                           headers=user1_header)
    response_json = json_response(response)
    assert response._status_code == 200
    assert response_json['data']['updateUser']['ok']

def test_name_exists_error(client, graphql_endpoint, user1_header, user2_header):
    response = client.post(graphql_endpoint,
                           data = dict(query=update_user('USER1')),
                           headers=user2_header)
    response_json = json_response(response)
    assert response._status_code == 200
    assert 'errors' in response_json.keys()
    assert 'already exists' in response_json['errors'][0]['message']

def test_name_character_error(client, graphql_endpoint, user1_header, user2_header):
    response = client.post(graphql_endpoint,
                           data = dict(query=update_user('USER1!')),
                           headers=user2_header)
    response_json = json_response(response)
    assert response._status_code == 200
    assert 'errors' in response_json.keys()
    assert 'valid characters' in response_json['errors'][0]['message']
