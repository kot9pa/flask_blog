from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.app import db
from src.config import settings
from src.api_v1.users.models import User, UserBody, UserPath


def create(body: UserBody):
    try:
        user = User(**body.model_dump(exclude_none=True))
        db.session.add(user)
        db.session.commit()
        return user
    except IntegrityError as err:
        raise err

def get_users():    
    return db.session.scalars(select(User)).all()

def get_user_by_id(user_id: int):
    return db.session.scalar(select(User).where(User.id == user_id))

def get_user_by_username(username: str):
    return db.session.scalar(select(User).where(User.username == username))

def delete(user: User):
    db.session.delete(user)
    db.session.commit()
