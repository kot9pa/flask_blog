import os
import secrets
import sys
import click
from flask.cli import with_appcontext
from flask_session import Session
from flask_openapi3 import OpenAPI
from redis import Redis

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.database import db, migrate
from src.config import settings


def create_app(test_config=None):
    # Create and configure Application
    app = OpenAPI(__name__, security_schemes=settings.security_schemes)
    if test_config:
        # load the test config if passed in
        app.config.update(test_config)
    
    # if you are using client-side sessions ie. not Flask-Session
    # app.secret_key = secrets.token_hex()    
    # app.config['SESSION_USE_SIGNER'] = True

    # Configure Redis storage
    app.config['SESSION_TYPE'] = 'redis'
    # app.config['SESSION_PERMANENT'] = False    
    app.config['SESSION_REDIS'] = Redis.from_url(settings.get_redis_url())

    # Initialize Flask-Session
    Session(app)

    # Configure SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.get_db_url()

    # Initialize Flask-SQLAlchemy, Flask-Migrate and other commands
    db.init_app(app)
    migrate.init_app(app, db)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(create_db_command)

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
    db.drop_all()

@click.command("drop-db")
@with_appcontext
def drop_db_command():
    drop_db()

def create_db():
    db.create_all()

@click.command("create-db")
@with_appcontext
def create_db_command():
    create_db()

if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=True,
        host=settings.SERVER_HOST, 
        port=settings.SERVER_PORT,
    )
