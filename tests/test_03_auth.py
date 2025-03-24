import pytest
from sqlalchemy import select
from flask import session

from src.app import db
from src.api_v1.users.models import User


def test_login(client, app):
    assert client.get('/auth/').status_code == 200
    response = client.post(
        '/auth/', 
        data={
            'username': 'username', 
            'password': 'password',
        }
    )
    assert response.headers["Location"] == "/"

    with app.app_context():
        user = db.session.execute(select(User).where(User.username == 'username')).scalar()
        assert user is not None
        assert user.check_password('password') is True

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user' not in session