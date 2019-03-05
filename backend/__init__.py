from flask import Flask, Blueprint
import backend.config as config
from backend.people import people_v1
from backend import db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        mongodb={},
    )

    if test_config is None:
        app.config.update(config.get())
    else:
        app.config.update(test_config)

    @app.route('/')
    def index():
        return "Welcome Paranuara Citizen API"

    # Register application commands
    db.init_app(app)

    app.register_blueprint(people_v1, url_prefix='/v1/people')
    return app