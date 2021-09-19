import pytest

from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_top(client):
    """ test top page """

    rv = client.get('/')
    assert b'sort font' in rv.data
