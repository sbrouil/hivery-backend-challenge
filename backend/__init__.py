from flask import Flask, Blueprint, jsonify, request
import backend.config as config
from backend.people import people_v1
from backend import db
from backend.exceptions import BusinessException

def add_cors_headers(response):
    """ Enable CORS for any origin so that it can be requested for tools
        like swagger UI from any domain.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

def create_app(test_config=None):
    """ Flask application factory

        Load applicaiton configuration, creates Flask instance
        and attach some hook to it
        The method is called using 'flask' command line with FLASK_APP=backend as environmnt
        variable.
    """
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
    
    app.after_request(add_cors_headers)

    return app