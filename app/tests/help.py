import json
import base64

######################
## Helper Functions ##
######################

def basic_auth_header(token):
    byte_token = base64.b64encode(bytes(token + ":" + 'anytext', 'ascii')).decode('ascii')
    basic_auth_header = {'Authorization': 'Basic ' + byte_token}
    return basic_auth_header

def json_response(response):
    json_response = json.loads(response.data.decode("UTF-8"))
    return json_response

def extract_token(response, parent):
    token = json_response(response)['data'][parent]['token']
    return token

#####################
## GraphQL Helpers ##
#####################

def register(username, email, password):
    register = """
    mutation {
      register(username: "%s", email: "%s", password: "%s"){
              token
        }
      }
    """ % (username, email, password)
    return register

def login(username, password):
    login = """
    mutation {
  login(username: "%s", password: "%s"){
          token
    }
  }
    """ % (username, password)
    return login

def update_password(password):
    update_password = """
    mutation {
  updatePassword(password: "%s"){
          token
    }
  }
    """ % (password)
    return update_password

# Only username for now..
def update_user(username):
    update_user = """
    mutation {
  updateUser(username: "%s"){
          ok
    }
  }
    """ % (username)
    return update_user

def delete_user():
    delete_user = """
    mutation {
  deleteUser{
          ok
    }
  }
    """
    return delete_user
