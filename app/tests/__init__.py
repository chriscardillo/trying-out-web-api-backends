import pytest
from app import create_app, db

@pytest.fixture(scope='session')
def client():
    app = create_app('testing')
    with app.app_context() as ctx:
        ctx.push()
        db.create_all()
    client=app.test_client()
    return client

@pytest.fixture(scope='session')
def graphql_endpoint():
    return '/api/graphql/'

def registration(username, email, password):
    registration = """
    mutation {
      register(username: "%s", email: "%s", password: "%s"){
              token
        }
      }
    """ % (username, email, password)
    return registration

def login(username, password):
    login = """
    mutation {
  login(username: "%s", password: "%s"){
          token
    }
  }
    """ % (username, password)
    return login

# Fixture levels - function, module, session
# https://docs.pytest.org/en/stable/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session
