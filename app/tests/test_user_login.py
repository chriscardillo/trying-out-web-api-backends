import pytest
from tests import client, site_secure
from tests.utils.user import generate_user, login_user
from tests.utils.requests import gql_post, json_response, extract_token
from tests.utils.response_checks import check_success_message, check_error_message

@pytest.fixture(scope="module")
def my_login_user(client):
    return generate_user(client, "login", "user")

def test_login_user(client, my_login_user):
    # New login generates a new token
    new_login_creds = login_user(client,
                                    "login",
                                    "user")
    assert new_login_creds['token'] != my_login_user['token']

    # Old token no longer works
    secure = client.get(site_secure, headers=my_login_user['token_header'])
    assert secure._status_code == 401

    # New token works
    secure = client.get(site_secure, headers=new_login_creds['token_header'])
    assert secure._status_code == 200
