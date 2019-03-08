"""
Enable Swagger API documentation

The swagger UI will read the YAML API specification and generate an interactive
API documentation
"""
from flask import current_app
from flask_swagger_ui import get_swaggerui_blueprint
import pkg_resources

SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://127.0.0.1:5000/api/spec.yml' # Our API url (can of course be a local resource)

def init_app(app):
    @app.route('/api/spec.yml')
    def api_spec():
        return app.send_static_file('openapi.yml')

    with app.app_context():
        prefix_uri = current_app.config['doc']['prefix_uri']
        spec_uri = current_app.config['doc']['spec_uri']

        swaggerui_blueprint = get_swaggerui_blueprint(
            prefix_uri,
            spec_uri
        )
        app.register_blueprint(swaggerui_blueprint, url_prefix=prefix_uri)