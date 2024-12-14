# backend/app/routes/helloworld.py

from flask_restx import Namespace, Resource
import logging

# Define the namespace for Hello World routes
helloworld_bp = Namespace('helloworld', description='Hello World route')

logger = logging.getLogger('app')

@helloworld_bp.route("/")
class HelloWorld(Resource):
    def get(self):
        """Returns a simple 'Hello, World!' message."""
        try:
            logger.info("Processing request for Hello World route")
            return {"message": "Hello, World!"}, 200
        except Exception as e:
            logger.error("Error in Hello World route: %s", e)
            return {"error": "An unexpected error occurred"}, 500
