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

def create_todo(title):
    create_todo = """
    mutation {
  createTodo(title: "%s"){
          title
    }
  }
    """ % (title)
    return create_todo
