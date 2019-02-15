from flask_restful import Resource
from flask import request, make_response, jsonify

from .posts_model import PostModel


class Blogs(Resource):
    """docstring for Blogs"""

    def post(self):
        """creating a blog"""
        _auth = request.headers.get('Authorization')
        if not _auth:
            return make_response(jsonify({
                "msg": "No authorization header provided. This resource is secured."
            }), 403)

        auth_t_oken = _auth.split(" ")[1]
        response = PostModel().decode_token(auth_t_oken)
        if not isinstance(response, str):
            req = request.get_json()
            new = {
                "title": req['title'],
                "description": req['description'],
                "created_by": req['created_by']
            }

            reequest = PostModel(**new)
            res = reequest.save()

            if isinstance(res, int):
                return make_response(jsonify({
                    "msg": "Created",
                    "post_id": res
                }), 201)
            else:
                return make_response(jsonify({
                    "msg": "post already exists"
                }), 409)
        else:
            return make_response(jsonify({
                "msg": response
            }), 401)

    def get(self):
        """retrieving all blogs"""
        _auth = request.headers.get('Authorization')
        if not _auth:
            return make_response(jsonify({
                "msg": "No authorization header provided. This resource is secured."
            }), 403)

        auth_t_oken = _auth.split(" ")[1]
        response = Po().decode_token(auth_t_oken)
        if not isinstance(response, str):
            res = PostModel().get_posts()
            if not res:
                return make_response(jsonify({
                    "msg": "Database is empty"
                }), 200)
            else:
                return make_response(jsonify({
                    "msg": "Ok",
                    "posts": res
                }), 200)
        else:
            return make_response(jsonify({
                "msg": response
            }), 401)


class SingleBlog(Resource):
    """docstring for SingleBlog"""

    def get(self, id):
        """retrieving a single blog based on id"""
        _auth = request.headers.get('Authorization')
        if not _auth:
            return make_response(jsonify({
                "msg": "No authorization header provided. This resource is secured."
            }), 403)

        auth_t_oken = _auth.split(" ")[1]
        response = Po().decode_token(auth_t_oken)
        if not isinstance(response, str):

            res = PostModel().get_single_post(id)
            if isinstance(res, int):
                return make_response(jsonify({
                    "msg": "Not found"
                }), 404)
            else:
                return make_response(jsonify({
                    "msg": "Ok",
                    "post": res
                }), 200)
        else:
            return make_response(jsonify({
                "msg": response
            }), 401)

    def delete(self, id):
        """deleting a single blog based on id"""
        _auth = request.headers.get('Authorization')
        if not _auth:
            return make_response(jsonify({
                "msg": "No authorization header provided. This resource is secured."
            }), 403)

        auth_t_oken = _auth.split(" ")[1]
        response = Po().decode_token(auth_t_oken)
        if not isinstance(response, str):

            delete = PostModel()
            res = delete.delete_item("posts", "post_id", id)
            if isinstance(res, int):
                return make_response(jsonify({
                    "msg": "Deleted"
                }), 200)
            else:
                return make_response(jsonify({
                    "msg": "Not found"
                }), 404)
        else:
            return make_response(jsonify({
                "msg": response
            }), 401)

    def put(self, id):
        """editing a single blog based on id"""
        _auth = request.headers.get('Authorization')
        if not _auth:
            return make_response(jsonify({
                "msg": "No authorization header provided. This resource is secured."
            }), 403)

        auth_t_oken = _auth.split(" ")[1]
        response = Po().decode_token(auth_t_oken)
        if not isinstance(response, str):
            data = request.get_json()
            for key, value in data.items():
                res = PostModel().update_item("posts", key, value, "post_id", id)

                if isinstance(res, int):
                    return make_response(jsonify({
                        "msg": "{} Updated".format(key)
                    }), 200)
                else:
                    return make_response(jsonify({
                        "msg": "Not found"
                    }), 404)
        else:
            return make_response(jsonify({
                "msg": response
            }), 401)
