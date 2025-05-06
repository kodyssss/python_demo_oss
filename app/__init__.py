from flask import Flask
from .config import Config
from .database import init_db

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register routes
    from .routes import init_routes
    init_routes(app)
    
    return app