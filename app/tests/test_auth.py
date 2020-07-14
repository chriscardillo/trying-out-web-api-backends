import json
import base64
import pytest
from tests import (client, graphql_endpoint,
                   registration, login)

# The order of these tests is very important
# Because we change the token with every new login
# or an update to the password

def test_client(client):
    """The client exists"""
    assert client is not None

def test_open(client):
    """The open endpoint delivers a response"""
    site = client.get('/site/')
    assert site._status_code == 200
    assert 'site' in str(site.data)

def test_closed(client):
    """The closed endpoint delivers a 401 without any authorization"""
    secure = client.get('/site/secure')
    assert secure._status_code == 401

@pytest.fixture(scope='module')
def registration_token(client, graphql_endpoint):
    """Registering a user and getting back our token"""
    response = client.post(graphql_endpoint, data = dict(query=registration("peter", "peter@app.com", "yoon")))
    registration_token = json.loads(response.data.decode("UTF-8"))['data']['register']['token']
    return registration_token

@pytest.fixture(scope='module')
def registration_token_header(registration_token):
    """Turning the registration token into a basic http auth header"""
    byte_token = base64.b64encode(bytes(registration_token + ":" + 'anytext', 'ascii')).decode('ascii')
    registration_token_header = {'Authorization': 'Basic ' + byte_token}
    return registration_token_header

def test_registration_token(registration_token):
    """The registration token must exist"""
    assert registration_token is not None

def test_authorized_registration_token(client, registration_token_header):
    """The registration token gets us into the secure endpoint"""
    secure = client.get('/site/secure', headers=registration_token_header)
    assert secure._status_code == 200

@pytest.fixture(scope='module')
def login_token(client, graphql_endpoint):
    """Logging in and receiving a new token"""
    response = client.post(graphql_endpoint, data = dict(query=login("peter", "yoon")))
    login_token = json.loads(response.data.decode("UTF-8"))['data']['login']['token']
    return login_token

@pytest.fixture(scope='module')
def login_token_header(login_token):
    """Turning the login token into a basic http auth header"""
    byte_token = base64.b64encode(bytes(login_token + ":" + 'anytext', 'ascii')).decode('ascii')
    login_token_header = {'Authorization': 'Basic ' + byte_token}
    return login_token_header

def test_login_token(login_token, registration_token):
    """The login token must exist, and be different than the registration token"""
    assert login_token is not None
    assert login_token != registration_token

def test_authorized_login_token(client, login_token_header):
    """The login token gets us into the secure endpoint"""
    secure = client.get('/site/secure', headers=login_token_header)
    assert secure._status_code == 200

def test_registration_token_401(client, registration_token_header):
    """The registration token no longer works"""
    secure = client.get('/site/secure', headers=registration_token_header)
    assert secure._status_code == 401
