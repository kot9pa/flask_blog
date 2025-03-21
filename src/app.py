import os
import secrets
import sys
import click
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_openapi3 import OpenAPI

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.database import db, migrate
from src.config import settings


def create_app():
    # Basic Authentication
    basic = {
        "type": "http",
        "scheme": "basic"
    }
    security_schemes = {"basic": basic}

    # Create and configure Application
    app = OpenAPI(__name__, security_schemes=security_schemes)
    app.secret_key = secrets.token_hex()
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.get_db_url()

    # Initialize Flask-SQLAlchemy, Flask-Migrate and the init-db command
    db.init_app(app)
    migrate.init_app(app, db)
    app.cli.add_command(drop_db_command)

    # Register Blueprints
    from src.api_v1.posts.view import posts_api_blueprint
    from src.api_v1.users.view import users_api_blueprint
    from src.auth import auth_bp
    from src.blog import blog_bp
    app.register_api(posts_api_blueprint)
    app.register_api(users_api_blueprint)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    
    # Register a rule for routing incoming requests and building URLs
    app.add_url_rule('/', endpoint='index')
    
    return app

def drop_db():
    # Clear existing data
    db.drop_all()

@click.command("drop-db")
@with_appcontext
def drop_db_command():
    drop_db()

if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=True,
        host=settings.SERVER_HOST, 
        port=settings.SERVER_PORT,
    )
