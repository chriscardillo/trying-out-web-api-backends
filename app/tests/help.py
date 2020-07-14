import json
import base64

######################
## Helper Functions ##
######################

def basic_auth_header(token):
    byte_token = base64.b64encode(bytes(token + ":" + 'anytext', 'ascii')).decode('ascii')
    basic_auth_header = {'Authorization': 'Basic ' + byte_token}
    return basic_auth_header

def extract_token(response, parent):
    token = json.loads(response.data.decode("UTF-8"))['data'][parent]['token']
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
