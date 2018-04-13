from flask import Flask, Response

class MyResponse(Response):
    default_mimetype = 'application/json'

# http://flask.pocoo.org/docs/0.10/patterns/appfactories/
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.response_class = MyResponse

    from app.devices.models import db
    db.init_app(app)

    return app
