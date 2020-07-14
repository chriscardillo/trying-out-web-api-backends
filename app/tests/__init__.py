import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app('testing')
    with app.app_context() as ctx:
        ctx.push()
        db.create_all()
    client=app.test_client()
    return client

@pytest.fixture
def site(client):
    site = client.get('/site/')
    return site

@pytest.fixture
def secure(client):
    secure = client.get('/site/secure')
    return secure
