from flask import Flask
from .routes import create_app

def create_app():
    app = create_app()
    return app