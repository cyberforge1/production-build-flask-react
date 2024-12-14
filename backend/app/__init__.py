# backend/app/__init__.py

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
import os
import logging

from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    """Application factory for creating Flask app instances."""
    # Configure Flask to serve static files from 'static' directory
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config_class)

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info("Application is starting...")

    # Disable strict slash enforcement globally to avoid conflicts
    app.url_map.strict_slashes = False

    # Validate configuration
    if hasattr(config_class, "validate"):
        try:
            config_class.validate()
        except ValueError as e:
            logger.critical(f"Configuration validation failed: {e}")
            raise

    logger.debug("SQLALCHEMY_DATABASE_URI in config: %s", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Import models to ensure they're registered with SQLAlchemy before initializing migrations
    from .models import Todo

    # Initialize migrations after models are imported
    migrate.init_app(app, db)

    # Initialize Flask-RESTx API
    api = Api(
        app,
        version='1.0',
        title='Todo Management API',
        description='API documentation for Todo Management System',
        doc='/api/docs',
        strict_slashes=False
    )

    # Import and register namespaces
    from .routes.main import main_bp
    from .routes.helloworld import helloworld_bp
    from .routes.todos import todos_bp

    logger.debug("Registering API namespaces...")
    api.add_namespace(main_bp, path='/api')
    api.add_namespace(helloworld_bp, path='/api/helloworld')
    api.add_namespace(todos_bp, path='/api/todos')

    # Serve React Frontend for non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        """
        Serve React App for any non-API routes.
        """
        logger.info("Received request for path: %s", path)

        # Log request details
        logger.debug("Request method: %s, headers: %s", request.method, request.headers)

        # Prevent conflicts with API routes
        if path.startswith('api/'):
            logger.warning("Path %s starts with /api/. Returning 404 for API handling.", path)
            return jsonify({"error": "Not found"}), 404

        # Serve static files if they exist
        static_file_path = os.path.join(app.static_folder, path)
        if path and os.path.exists(static_file_path):
            logger.info("Serving static file: %s", static_file_path)
            return send_from_directory(app.static_folder, path)

        # Serve React's index.html for all other routes
        logger.info("Serving index.html for non-static, non-API route.")
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except FileNotFoundError:
            logger.error("index.html not found in the static folder.")
            return jsonify({"error": "React frontend not built or index.html is missing"}), 500

    # Log registered routes
    logger.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.info("%s -> %s", rule.rule, rule.endpoint)

    return app
