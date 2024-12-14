# backend/app/routes/main.py

from flask_restx import Namespace, Resource
import logging

# Define the namespace for the main route
main_bp = Namespace('main', description='Main application route')

logger = logging.getLogger('app')

@main_bp.route("/")
class Main(Resource):
    def get(self):
        """Main welcome route"""
        try:
            logger.info("Processing request for Main route")
            return {"message": "Welcome to the Todo Management API!"}, 200
        except Exception as e:
            logger.error("Error in Main route: %s", e)
            return {"error": "An unexpected error occurred"}, 500
