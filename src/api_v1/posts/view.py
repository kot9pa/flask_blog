from flask_openapi3 import APIBlueprint, Tag
from flask import current_app, jsonify, request
from pydantic import ValidationError

from src.config import settings
from src.api_v1.posts.models import Post, PostUpdate, PostPath, PostBody
from src.api_v1.users.view import auth_required
from src.api_v1.posts import api


posts_api_blueprint = APIBlueprint(
    '/post',
    __name__,
    url_prefix="/api/v1/posts", 
    abp_tags=[Tag(name="Post API")],
    abp_security=settings.security_basic,
)

@posts_api_blueprint.post('/create')
@auth_required
def create(body: PostBody):
    try:
        post_create = body.model_validate(request.json)
        post = api.create(post_create)
        return post.to_dict(), 201
    except ValidationError as err:
        return jsonify({'error': err.json()}), 400
    except Exception as err:
        raise err

@posts_api_blueprint.get('/')
@auth_required
def get_all():
    result = api.get_posts()
    if result is None:
        return jsonify({"error": f"Posts not found"}), 404
    return [post.to_dict() for post in result]

@posts_api_blueprint.get('/<id>')
@auth_required
def get_post(path: PostPath):
    result = api.get_posts(path.id)
    if result is None:
        return jsonify({"error": f"Posts not found"}), 404
    return result.to_dict()

@posts_api_blueprint.post('/find')
@auth_required
def find(body: PostBody):
    posts = api.find(body)
    if not posts:
        return jsonify({"error": f"Posts not found"}), 404
    return [post.to_dict() for post in posts]

@posts_api_blueprint.put('/<id>')
@posts_api_blueprint.patch('/<id>')
@auth_required
def update(path: PostPath, body: PostUpdate):  
    try:
        if request.method == 'PUT':
            post_update = PostBody.model_validate(request.json)
            partial = False
        else:
            post_update = PostUpdate.model_validate(request.json)
            partial = True

        post = api.get_posts(path.id)
        if not post:
            return jsonify({"error": f"Post id={path.id} not found"}), 404
        post_new = api.update(post, post_update, partial=partial)
        return post_new.to_dict()
    except ValidationError as err:
        return jsonify({'error': err.json()}), 400
    except Exception as err:
        raise err

@posts_api_blueprint.delete('/<id>')
@auth_required
def delete(path: PostPath):
    post = api.get_posts(path.id)
    if post is None:
        return jsonify({"error": f"Post id={path.id} not found"}), 404
    api.delete(post)
    return jsonify({"message": f"Post '{post.title}' was successfully deleted!"})
