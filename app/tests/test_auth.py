import pytest
from tests import client, graphql_endpoint, site_secure
from tests.help import (basic_auth_header, extract_token, json_response,
                        register, login, update_password)

# The order of these tests is very important
# Because we change the token with every new login
# or an update to the password

# Test a registered user against secure endpoint

@pytest.fixture(scope='module')
def registration_token(client, graphql_endpoint):
    """Registering a user and getting back our token"""
    response = client.post(graphql_endpoint, data = dict(query=register("PETER", "peter@app.com", "yoon")))
    registration_token = extract_token(response, 'register')
    return registration_token

@pytest.fixture(scope='module')
def registration_token_header(registration_token):
    """Turning the registration token into a basic http auth header"""
    registration_token_header = basic_auth_header(registration_token, "anytext")
    return registration_token_header

def test_registration_token(registration_token):
    """The registration token must exist"""
    assert registration_token is not None

def test_authorized_registration_token(client, site_secure, registration_token_header):
    """The registration token gets us into the secure endpoint"""
    secure = client.get(site_secure, headers=registration_token_header)
    assert secure._status_code == 200

def test_valid_characters_only(client, graphql_endpoint):
    response = client.post(graphql_endpoint, data = dict(query=register("BAD!", "bad@app.com", "bad")))
    response_json = json_response(response)
    assert response._status_code == 200
    assert 'errors' in response_json.keys()
    assert 'valid characters' in response_json['errors'][0]['message']

# Test a logged in user against secure endpoint

@pytest.fixture(scope='module')
def login_token(client, graphql_endpoint):
    """Logging in and receiving a new token"""
    response = client.post(graphql_endpoint, data = dict(query=login("peter", "yoon")))
    login_token = extract_token(response, 'login')
    return login_token

@pytest.fixture(scope='module')
def login_token_header(login_token):
    """Turning the login token into a basic http auth header"""
    login_token_header = basic_auth_header(login_token, "anytext")
    return login_token_header

def test_login_token(login_token, registration_token):
    """The login token must exist, and be different than the registration token"""
    assert login_token is not None
    assert login_token != registration_token

def test_authorized_login_token(client, site_secure, login_token_header):
    """The login token gets us into the secure endpoint"""
    secure = client.get(site_secure, headers=login_token_header)
    assert secure._status_code == 200

def test_registration_token_401(client, site_secure, registration_token_header):
    """The registration token no longer works"""
    secure = client.get(site_secure, headers=registration_token_header)
    assert secure._status_code == 401

# Test a password change

@pytest.fixture(scope='module')
def password_token(client, graphql_endpoint, login_token_header):
    """Logging in and receiving a new token"""
    response = client.post(graphql_endpoint,
                           data = dict(query=update_password("a_new_password")),
                           headers=login_token_header)
    password_token = extract_token(response, 'updatePassword')
    return password_token

@pytest.fixture(scope='module')
def password_token_header(password_token):
    """Turning the login token into a basic http auth header"""
    password_token_header = basic_auth_header(password_token, "anytext")
    return password_token_header

def test_password_token(login_token, registration_token, password_token):
    """The login token must exist, and be different than the registration token"""
    assert password_token is not None
    assert password_token != registration_token
    assert password_token != login_token

def test_authorized_password_token(client, site_secure, password_token_header):
    """The login token gets us into the secure endpoint"""
    secure = client.get(site_secure, headers=password_token_header)
    assert secure._status_code == 200

def test_login_token_401(client, site_secure, login_token_header):
    """The registration token no longer works"""
    secure = client.get(site_secure, headers=login_token_header)
    assert secure._status_code == 401
