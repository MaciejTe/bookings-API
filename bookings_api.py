"""
This file is configured as FLASK_APP environment variable.
"""
from src import create_app, cli, create_api
from src.api import register_endpoints

app = create_app()
cli.register(app)
api = create_api(app)
register_endpoints(api)
