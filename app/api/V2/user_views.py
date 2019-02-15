from flask_restful import Resource
from flask import request, make_response, jsonify

from .user_model import UserModel


class Auth(Resource):
    """docstring for Authentication"""

    def post(self):
        req = request.get_json()
        new = {
            "username": req['username'],
            "password": req['password']
        }

        if UserModel().check_exist('users', 'username', new['username']) == False:
            return make_response(jsonify({
                "msg": "No such user"
            }), 401)

        record = UserModel().get_user_by_username(new['username'])
        user_id, password = record
        if password != new['password']:
            return make_response(jsonify({
                "msg": "Username and password does not macth"
            }), 401)

        token = UserModel().ecnode_token(user_id)
        return make_response(jsonify({
            "msg": "Welcome {}".format(new['username']),
            "access-token": token
        }), 200)


class AuthLogOut(Resource):
    """docstring for Blogs"""

    def post(self):
        """creating a blog"""
        _auth = request.headers.get('Authorization')
        if not _auth:
            return make_response(jsonify({
                "msg": "No authorization header provided. This resource is secured."
            }), 403)

        auth_t_oken = _auth.split(" ")[1]
        response = UserModel().decode_token(auth_t_oken)
        if not isinstance(response, str):
            token = response
            logout = UserModel().logout(token)
            return make_response(jsonify({
                "msg": "Logged out successfully"
            }), 200)

        else:
            return make_response(jsonify({
                "msg": response
            }), 401)


class Registration(Resource):
    """docstring for Blogs"""

    def post(self):
        """creating a blog"""
        req = request.get_json()
        new = {
            "name": req['name'],
            "username": req['username'],
            "password": req['password'],
            "email": req['email']
        }

        reequest = UserModel(**new)
        res = reequest.save()

        if isinstance(res, int):
            token = UserModel().ecnode_token(res)
            return make_response(jsonify({
                "msg": "Registered successfully",
                "access-token": token
            }), 201)
        else:
            return make_response(jsonify({
                "msg": "user already exists"
            }), 409)
