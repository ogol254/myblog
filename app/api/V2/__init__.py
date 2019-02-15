from flask import Blueprint
from flask_restful import Api

from posts_views import Blogs, SingleBlog
from user_views import Registration, Auth, AuthLogOut

version2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version2)


api.add_resource(Blogs, '/blog')
api.add_resource(SingleBlog, '/blog/<int:id>')
api.add_resource(Auth, '/auth/login')
api.add_resource(AuthLogOut, '/auth/logout')
api.add_resource(Registration, '/auth/register')
