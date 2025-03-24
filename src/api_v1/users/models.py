from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from src.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.username,
        }
    
    def __repr__(self):
        return f"<User username='{self.username}', password='{self.password_hash}'>"
    
    def set_password(self, value: str) -> None:
        """Store the password as a hash for security."""
        self.password_hash = generate_password_hash(value)

    # allow password = "..." to set a password
    password = property(fset=set_password)

    def check_password(self, value: str) -> bool:
        return check_password_hash(self.password_hash, value)

class UserPath(BaseModel):
    id: int

class UserQuery(BaseModel):
    pass

class UserBody(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)