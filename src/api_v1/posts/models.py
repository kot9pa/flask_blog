from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column

from src.base import Base


class Post(Base):
    title: Mapped[str]
    content: Mapped[str] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
        }
    
    def __repr__(self):
        return f"<Post title='{self.title}', content='{self.content}'>"

class PostPath(BaseModel):
    id: int

class PostQuery(BaseModel):
    pass

class PostBody(BaseModel):
    title: str = Field(min_length=3)
    content: str | None = None

class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3)
    content: str | None = None