"""
This file is configured as FLASK_APP environment variable.
"""
from src import create_app, cli

app = create_app()
cli.register(app)
