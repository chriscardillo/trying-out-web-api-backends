from tests.utils.graphql import register, login, update_password
from tests.utils.requests import gql_post, extract_token, basic_auth_header

def generate_user(client, username, password):
    response = gql_post(client,
                        register,
                        username=username,
                        email=(username + "@app.com"),
                        password=password)
    token = extract_token(response, 'register')
    token_header = basic_auth_header(token)
    creds_header = basic_auth_header(username, password)
    return {"token": token, "token_header": token_header, "creds_header": creds_header}

def login_user(client, username, password):
    response = gql_post(client,
                        login,
                        username=username,
                        password=password)
    token = extract_token(response, 'login')
    token_header = basic_auth_header(token)
    creds_header = basic_auth_header(username, password)
    return {"token": token, "token_header": token_header, "creds_header": creds_header}

def update_user_password(client, user_header, new_password):
    response = gql_post(client,
                        update_password,
                        headers=user_header,
                        password=new_password)
    token = extract_token(response, 'updatePassword')
    token_header = basic_auth_header(token)
    return {"token": token, "token_header": token_header}
