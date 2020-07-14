from tests import client, site, secure

def test_client(client):
    assert client is not None

def test_open(site):
    assert site._status_code == 200
    assert 'site' in str(site.data)

def test_closed(secure):
    assert secure._status_code == 401
