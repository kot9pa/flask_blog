from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.config import settings
from src.base import Base


db = SQLAlchemy(
    model_class=Base, 
    engine_options={
        'echo': settings.DB_ECHO
    },
)
migrate = Migrate()