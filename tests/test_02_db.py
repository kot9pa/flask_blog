from flask_migrate import upgrade
from sqlalchemy import text

from src.app import db


def test_migrate_head(app):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM public.alembic_version;"))
        assert '51e954a19a51' in result.first()