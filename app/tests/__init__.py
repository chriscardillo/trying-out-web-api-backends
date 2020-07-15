import pytest
from app import create_app, db

#####################
## Common Fixtures ##
#####################

@pytest.fixture(scope='module')
def client():
    app = create_app('testing')
    with app.app_context() as ctx:
        ctx.push()
        db.create_all()
    client=app.test_client()
    return client

@pytest.fixture(scope='module')
def graphql_endpoint():
    return '/api/graphql/'

@pytest.fixture(scope='module')
def site():
    return '/site/'

@pytest.fixture(scope='module')
def site_secure():
    return '/site/secure'
