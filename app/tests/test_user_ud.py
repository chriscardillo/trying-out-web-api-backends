import pytest
from tests import client, site_secure
from tests.utils.requests import gql_post
from tests.utils.user import generate_user
from tests.utils.graphql import update_user, delete_user
from tests.utils.response_checks import check_success_message, check_error_message

@pytest.fixture(scope = "module")
def unchanged_user(client):
    return generate_user(client, "unchanged", "user")

@pytest.fixture(scope = "module")
def updated_user(client):
    return generate_user(client, "original", "user")

def test_update_user(client, unchanged_user, updated_user):
    # User gets name updated
    response = gql_post(client,
                        update_user,
                        headers=updated_user['token_header'],
                        username="updated")

    check_success_message(response, "True")

    # We get the username at an endpoint
    secure = client.get(site_secure, headers=updated_user['token_header'])
    check_success_message(secure, "updated")

    # User can adjust casing their own name
    response = gql_post(client,
                        update_user,
                        headers=updated_user['token_header'],
                        username="UPDATED")

    secure = client.get(site_secure, headers=updated_user['token_header'])
    check_success_message(secure, "UPDATED")

    # The user can't take someone else's name
    response = gql_post(client,
                        update_user,
                        headers=updated_user['token_header'],
                        username="UNCHANGED")
    check_error_message(response, "Username or email already exists", "The user shouldn't be able to take someone else's name.")

# test deleting a user
