###################
## Token Actions ##
###################

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

##################
## User Actions ##
##################

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

##################
## Todo Actions ##
##################

def create_todo(title):
    create_todo = """
    mutation {
  createTodo(title: "%s"){
          id
          title
    }
  }
    """ % (title)
    return create_todo

def update_todo(id, title):
    update_todo = """
    mutation {
  updateTodo(id: %s, title: "%s"){
          id
          title
    }
  }
    """ % (id, title)
    return update_todo

def delete_todo(id):
    delete_todo = """
    mutation {
  deleteTodo(id: %s){
          ok
    }
  }
    """ % (id)
    return delete_todo

def tag_todo(id, tag):
    tag_todo = """
    mutation {
  tagTodo(id: %s, tag: "%s"){
          ok
    }
  }
    """ % (id, tag)
    return tag_todo
