from flask import Flask, Blueprint, jsonify
import backend.config as config
from backend.people import people_v1
from backend import db
from backend.exceptions import BusinessException

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

    @app.errorhandler(BusinessException)
    def handle_not_found(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Register application commands
    db.init_app(app)

    app.register_blueprint(people_v1, url_prefix='/v1/people')
    return app