import pytest
from app import create_app, db

######################
## Session Fixtures ##
######################

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

@pytest.fixture(scope='session')
def site():
    return '/site/'

@pytest.fixture(scope='session')
def site_secure():
    return '/site/secure'
