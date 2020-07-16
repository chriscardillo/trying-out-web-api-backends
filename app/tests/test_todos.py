import pytest
from tests import client
from tests.utils.user import generate_user
from tests.utils.graphql import create_todo
from tests.utils.requests import gql_post, json_response
from tests.utils.response_checks import check_success_message

@pytest.fixture(scope="module")
def todo_user(client):
    return generate_user(client, "todos", "user")

def test_todo_creation(client, todo_user):
    response = gql_post(client,
                        create_todo,
                        headers=todo_user['token_header'],
                        title="Write some tests")
    check_success_message(response, "Write some tests")
