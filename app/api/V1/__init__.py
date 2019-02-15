from flask import Blueprint
from flask_restful import Api

from views import Blogs, SingleBlog

version1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version1)


api.add_resource(Blogs, '/blog')
api.add_resource(SingleBlog, '/blog/<int:id>')
