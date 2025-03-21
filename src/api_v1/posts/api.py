from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.app import db
from src.config import settings
from src.api_v1.posts.models import Post, PostQuery, PostUpdate, PostBody


def create(body: PostBody):
    try:
        post = Post(**body.model_dump(exclude_none=True))
        db.session.add(post)
        db.session.commit()
        return post
    except IntegrityError as err:
        raise err

def get_posts(post_id=None):
    if post_id is None:
        result = db.session.scalars(select(Post)).all()
        if not result:
            return
    else:
        result = db.session.scalar(select(Post).where(Post.id == post_id))
        if not result:
            return
    return result

def find(body: PostBody):
    if body.title and body.content:
        result = db.session.scalars(select(Post).where(Post.title.contains(body.title), 
                                                       Post.content.contains(body.content))).all()
    elif body.title:
        result = db.session.scalars(select(Post).where(Post.title.contains(body.title))).all()
    elif body.content:
        result = db.session.scalars(select(Post).where(Post.content.contains(body.content))).all()
    else:
        result = get_posts()
    return result

def update(post: Post, post_update: PostUpdate, partial=False):
    try:
        for key, value in post_update.model_dump(exclude_none=partial).items():
            setattr(post, key, value)
        db.session.commit()
        return post
    except IntegrityError as err:
        raise err

def delete(post: Post):
    db.session.delete(post)
    db.session.commit()
