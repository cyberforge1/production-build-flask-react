# backend/app/__init__.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
import os

from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory for creating Flask app instances."""
    # Configure Flask to serve static files from 'static' directory
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config_class)

    # Validate configuration
    if hasattr(config_class, "validate"):
        config_class.validate()

    print("DEBUG (create_app): SQLALCHEMY_DATABASE_URI in config:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Import models here to ensure they're registered with SQLAlchemy before initializing migrations
    from .models import Todo  # Import all models here

    # Initialize migrations after models are imported
    migrate.init_app(app, db)

    # Initialize Flask-RESTx API
    api = Api(
        app,
        version='1.0',
        title='Todo Management API',
        description='API documentation for Todo Management System',
        doc='/api/docs',  # Swagger UI available at /api/docs
        strict_slashes=False  # Disable strict slash enforcement globally
    )

    # Import and register namespaces
    from .routes.main import main_bp
    from .routes.helloworld import helloworld_bp
    from .routes.todos import todos_bp

    # Register namespaces with specific paths
    api.add_namespace(main_bp, path='/api')          # Main route
    api.add_namespace(helloworld_bp, path='/api/helloworld')  # Hello World route
    api.add_namespace(todos_bp, path='/api/todos')   # Todos routes

    # Serve React Frontend for non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        """
        Serve React App for any non-API routes.
        """
        if path.startswith('api/'):
            # If the route starts with /api/, return 404 to let Flask-RESTx handle it
            return {"error": "Not found"}, 404
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            # If the requested path exists in the static folder, serve it
            return send_from_directory(app.static_folder, path)
        else:
            # For all other routes, serve index.html (for React Router)
            return send_from_directory(app.static_folder, 'index.html')

    return app
