import pytest
from tests import client, site_secure
from tests.utils.graphql import register
from tests.utils.requests import gql_post
from tests.utils.user import generate_user
from tests.utils.response_checks import check_error_message, check_success_message

@pytest.fixture(scope="module")
def registered_user(client):
    return generate_user(client, "register", "user")

def test_authorized_registration_token(client, registered_user):
    secure = client.get(site_secure, headers=registered_user['token_header'])
    check_success_message(secure, "register")

def test_authorized_registration_creds(client, registered_user):
    secure = client.get(site_secure, headers=registered_user['creds_header'])
    check_success_message(secure, "register")

def test_bad_credentials(client):
    response = gql_post(client,
                        register,
                        username="Bad!",
                        email=("bad" + "@app.com"),
                        password="bad!")
    check_error_message(response, "valid characters")

def test_user_exists(client):
    response = gql_post(client,
                        register,
                        username="REGISTer",
                        email=("REGISTer" + "@app.com"),
                        password="bad!")
    check_error_message(response, "already exists")
