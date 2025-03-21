import functools
from base64 import b64decode
from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, request, session, current_app
from pydantic import ValidationError

from src.config import settings
from src.api_v1.users import api
from src.api_v1.users.models import User, UserBody, UserPath


users_api_blueprint = APIBlueprint(
    '/user',
    __name__,
    url_prefix="/api/v1/users", 
    abp_tags=[Tag(name="User API")],
)

def auth_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get('user'):
            return jsonify({'error': 'You are not authorized'}), 403
        return view(*args, **kwargs)
    return wrapped_view

@users_api_blueprint.post('/auth', security=settings.security_basic)
def auth():
    auth: str = request.headers.get('authorization')
    if not auth:
        return {'error': 'You are not authorized'}, 403
    current_app.logger.debug(f"Auth: {auth}")
    auth_decode = b64decode(auth.split(' ')[1]).decode()
    username, password = auth_decode.split(':')
    user = api.get_user_by_username(username)
    if not user:
        return {'error': 'User not found'}, 404
    elif not user.check_password(password):
        return {'error': "Incorrect password"}, 403
    session['user'] = user.id
    return {'message': 'Logged in successfully'}

@users_api_blueprint.post('/register')
def register(body: UserBody):
    try:
        user_create = body.model_validate(request.json)
        user = api.create(user_create)
        return jsonify({'password_hash': user.password_hash}), 201
    except ValidationError as err:
        return jsonify({'error': err.json()}), 400
    except Exception as err:
        raise err

@users_api_blueprint.get('/', security=settings.security_basic)
@auth_required
def get_all():
    result = api.get_users()
    if not result:
        return jsonify({'error': 'Users not found'}), 404
    return [user.to_dict() for user in result]

@users_api_blueprint.get('/<id>', security=settings.security_basic)
@auth_required
def get_user(path: UserPath):
    result = api.get_user_by_id(path.id)
    if not result:
        return jsonify({"error": f"User id={path.id} not found"}), 404
    return jsonify(result.to_dict())

@users_api_blueprint.delete('/delete/<id>', security=settings.security_basic)
@auth_required
def delete(path: UserPath):
    user = api.get_user_by_id(path.id)
    if not user:
        return jsonify({"error": f"User id={path.id} not found"}), 404
    api.delete(user)
    return jsonify({"message": f"User id={path.id} deleted successfully"})

@users_api_blueprint.get('/logout', security=settings.security_basic)
@auth_required
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})