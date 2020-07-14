from tests import client, site, site_secure

# Test the endpoints we care about work

def test_client(client):
    """The client exists"""
    assert client is not None

def test_open(client, site):
    """The open endpoint delivers a response"""
    site = client.get(site)
    assert site._status_code == 200
    assert 'site' in str(site.data)

def test_closed(client, site_secure):
    """The closed endpoint delivers a 401 without any authorization"""
    secure = client.get(site_secure)
    assert secure._status_code == 401
