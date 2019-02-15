import datetime
import time

from flask_restful import Resource
from flask import request, make_response, jsonify

blog_list = []


class Blogs(Resource):
    """docstring for Blogs"""

    def post(self):
        """creating a blog"""
        req = request.get_json()
        new = {
            "id": len(blog_list) + 1,
            "title": req['title'],
            "description": req['description'],
            "date": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        }
        blog_list.append(new)
        return make_response(jsonify({
            "msg": "Created",
            "blog_id": new['id']
        }), 201)

    def get(self):
        """retrieving all blogs"""
        return make_response(jsonify({
            "msg": "ok",
            "blogs": blog_list
        }), 200)


class SingleBlog(Resource):
    """docstring for SingleBlog"""

    def get(self, id):
        """retrieving a single blog based on id"""
        for blog in blog_list:
            if blog['id'] == id:
                return make_response(jsonify({
                    "msg": "ok",
                    "blog": blog
                }), 200)

            return make_response(jsonify({
                "msg": "Not found"
            }), 404)

    def delete(self, id):
        """deleting a single blog based on id"""
        global blog_list
        blog_list = [blog for blog in blog_list if blog['id'] != id]
        return make_response(jsonify({
            "msg": "Blog with id {} id deleted".format(id)
        }), 200)

    def put(self, id):
        """editing a single blog based on id"""
        for blog in blog_list:
            if blog['id'] == id:
                req = request.get_json()
                blog['tittle'] = req['tittle']
                blog['description'] = req['description']
                blog['updated'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                return make_response(jsonify({
                    "msg": "ok",
                    "blog": blog
                }), 200)

            updated_blog = {
                "id": id,
                "tittle": req['tittle'],
                "description": req['description'],
                "updated": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            }
            blog_list.append(updated_blog)

            return make_response(jsonify({
                "msg": "ok",
                "blog": blog
            }), 201)
