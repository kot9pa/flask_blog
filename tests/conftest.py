import os
import sys
import pytest
from flask_migrate import downgrade, upgrade

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.app import create_app


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='username', password='password'):
        return self._client.post(
            '/auth/',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        app.test_cli_runner().invoke(args=['drop-db'])
        upgrade(revision='head')
    
    yield app

    with app.app_context():
        downgrade(revision='base')

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
