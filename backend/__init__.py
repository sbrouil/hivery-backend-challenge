from flask import Flask, Blueprint
from backend.people import people_v1

def create_app(config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Welcome Paranuara Citizen API"

    app.register_blueprint(people_v1, url_prefix='/v1/people')
    return app