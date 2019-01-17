from flask import Flask
from flask_restful import Api
from views import Blogs, SingleBlog

app = Flask(__name__)
api = Api(app)

api.add_resource(Blogs, '/blog')
api.add_resource(SingleBlog, '/blog/<int:id>')


if __name__ == '__main__':
    app.run()
