import pytest
from tests import client, site_secure
from tests.utils.graphql import login
from tests.utils.requests import gql_post
from tests.utils.user import generate_user, update_user_password, login_user
from tests.utils.response_checks import check_success_message, check_error_message

@pytest.fixture(scope="module")
def password_user(client):
    return generate_user(client, "updatePassword", "user")

def test_update_password(client, password_user):
    # New password generates a new token
    new_password_creds = update_user_password(client,
                                              password_user['token_header'],
                                              "my_new_password")
    assert new_password_creds['token'] != password_user['token']

    # Old token no longer works
    secure = client.get(site_secure, headers=password_user['token_header'])
    assert secure._status_code == 401

    # New token works
    secure = client.get(site_secure, headers=new_password_creds['token_header'])
    assert secure._status_code == 200

    # Old password does not work
    login_check = gql_post(client,
                           login,
                           username="updatePassword",
                           password="user")
    check_error_message(login_check, "Incorrect username or password")

    # New password does work
    login_check = login_user(client, "UPDATEPASSWORD", "my_new_password")
    assert login_check['token'] is not None
