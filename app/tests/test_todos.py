import pytest
from tests import client
from tests.utils.user import generate_user
from tests.utils.requests import gql_post, json_response
from tests.utils.graphql import (create_todo, update_todo, delete_todo,
                                 tag_todo)
from tests.utils.response_checks import check_success_message, check_error_message

@pytest.fixture(scope="module")
def todo_user(client):
    return generate_user(client, "todo", "user")

@pytest.fixture(scope="module")
def not_my_todo_user(client):
    return generate_user(client, "not_my_todo", "user")

@pytest.fixture(scope="module")
def updated_todo(client, todo_user):
    response = gql_post(client,
                        create_todo,
                        headers=todo_user['token_header'],
                        title="Change my todo")
    return json_response(response)['data']['createTodo']

# Todo Crud

def test_todo_creation(client, todo_user):
    response = gql_post(client,
                        create_todo,
                        headers=todo_user['token_header'],
                        title="Write some tests")
    check_success_message(response, "Write some tests")

def test_unauthorized_todo(client):
    response = gql_post(client,
                        create_todo,
                        title="Write some tests")
    # This is janky, should be check error...
    check_success_message(response, "None")

def test_update_todo(client, todo_user, updated_todo):
    response = gql_post(client,
                        update_todo,
                        headers=todo_user['token_header'],
                        id = updated_todo['id'],
                        title="My new todo title!")
    check_success_message(response, "My new todo title!")

def test_user_specific_todos(client, not_my_todo_user, updated_todo):
    response = gql_post(client,
                        update_todo,
                        headers=not_my_todo_user['token_header'],
                        id = updated_todo['id'],
                        title="The title shouldn't change!")
    check_error_message(response, "Todo not owned by current user")

def test_user_specific_todo_deletion(client, not_my_todo_user, updated_todo):
    response = gql_post(client,
                        delete_todo,
                        headers=not_my_todo_user['token_header'],
                        id = updated_todo['id'])
    check_error_message(response, "Todo not owned by current user")

def test_delete_todo(client, todo_user, updated_todo):
    response = gql_post(client,
                        delete_todo,
                        headers=todo_user['token_header'],
                        id = updated_todo['id'])
    check_success_message(response, "True")

# Todo Tags

@pytest.fixture(scope="module")
def tagged_todo(client, todo_user):
    response = gql_post(client,
                        create_todo,
                        headers=todo_user['token_header'],
                        title="Tag my todo")
    return json_response(response)['data']['createTodo']

def test_tag_todo(client, todo_user, tagged_todo):
    response = gql_post(client,
                        tag_todo,
                        headers=todo_user['token_header'],
                        id = tagged_todo['id'],
                        tag = "myradtag")
    check_success_message(response, "True")

def test_tag_exists(client, todo_user, tagged_todo):
    response = gql_post(client,
                        tag_todo,
                        headers=todo_user['token_header'],
                        id = tagged_todo['id'],
                        tag = "myradtag")
    check_error_message(response, "Tag already exists on todo.")

def test_user_specific_tags(client, not_my_todo_user, tagged_todo):
    response = gql_post(client,
                        tag_todo,
                        headers=not_my_todo_user['token_header'],
                        id = tagged_todo['id'],
                        tag = "myinvalidtag")
    check_error_message(response, "Todo not owned by current user.")
