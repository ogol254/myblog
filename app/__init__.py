from flask import Flask


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    from .api.V1 import version1 as v1
    app.register_blueprint(v1)
    from .api.V2 import version2 as v2
    app.register_blueprint(v2)

    return app
