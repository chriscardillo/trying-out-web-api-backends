import json
import base64
from tests import graphql_endpoint

def json_response(response):
    json_response = json.loads(response.data.decode("UTF-8"))
    return json_response

def extract_token(response, parent):
    token = json_response(response)['data'][parent]['token']
    return token

def basic_auth_header(username_or_token, password=None):
    if password is None:
        password = "anytext"
    byte_encoding = base64.b64encode(bytes(username_or_token + ":" + password, 'ascii')).decode('ascii')
    basic_auth_header = {'Authorization': 'Basic ' + byte_encoding}
    return basic_auth_header

def gql_post(client, func, headers=None, **kwargs):
    response = client.post(graphql_endpoint,
                           data = dict(query=func(**kwargs)),
                           headers=headers)
    return response
