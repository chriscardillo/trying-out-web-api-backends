from tests.utils.requests import json_response

def check_success_message(response, message):
    response_json = json_response(response)
    assert response._status_code == 200, "status code was " + response._status_code + ", expected 200"
    assert 'errors' not in response_json.keys(), "errors block found in json response"
    assert message in str(response_json), "'" + message + "'" + " not in " + str(response_json)

def check_error_message(response, message, instructions=None):
    response_json = json_response(response)
    assert response._status_code == 200, "status code was " + response._status_code + ", expected 200"
    assert 'errors' in response_json.keys(), "expected errors block, found none"
    if instructions is None:
        instructions =  message + " not in " + str(response_json)
    assert message in response_json['errors'][0]['message'], instructions
