import pytest
from sqlalchemy import func, select

from src.api_v1.posts.models import Post
from src.app import db

def test_index(client, auth):
    response = client.get("/auth/")
    assert "Вход в систему" in response.text
    assert "Войти" in response.text

    auth.login()
    response = client.get("/")
    assert "FlaskBlog" in response.text
    assert "New Post" in response.text
    assert "Logout" in response.text
    assert "First Post" in response.text
    assert "Second Post" in response.text

@pytest.mark.parametrize("path", ("/create", "/1/edit", "/1/delete"))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/"

def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "Third Post", "content": "Content for the third post"})

    with app.app_context():
        count = db.session.execute(select(func.count(Post.id))).scalar()
        assert count == 3

def test_edit(client, auth, app):
    auth.login()
    assert client.get('/1/edit').status_code == 200
    client.post('/1/edit', data={'title': 'First Post updated', 'content': ''})

    with app.app_context():
        post = db.session.execute(select(Post).where(Post.id == 1)).scalar()
        assert post.title == 'First Post updated'

@pytest.mark.parametrize('path', (
    '/create',
    '/1/edit',
))
def test_create_edit_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'content': ''})
    assert 'String should have at least 3 characters' in response.text

def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        post = db.session.execute(select(Post).where(Post.id == 1)).scalar()
        assert post is None