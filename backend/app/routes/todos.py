# backend/app/routes/todos.py

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app.models import Todo, db
import logging

todos_bp = Namespace('todos', description='Todo routes')

# API model for input validation
todo_model = todos_bp.model('Todo', {
    'title': fields.String(required=True, description='The title of the todo')
})

logger = logging.getLogger('app')

@todos_bp.route("/")  # Route explicitly ends with a trailing slash
class TodoList(Resource):
    def get(self):
        """Get all todos."""
        try:
            logger.info("Fetching all todos")
            todos = Todo.query.all()
            response = [{"id": todo.id, "title": todo.title} for todo in todos]
            logger.debug("Todos fetched: %s", response)
            return response, 200
        except Exception as e:
            logger.error("Error fetching todos: %s", e)
            return {"error": "An unexpected error occurred"}, 500

    @todos_bp.expect(todo_model)
    def post(self):
        """Create a new todo."""
        try:
            data = request.get_json()
            title = data.get("title")
            logger.info("Creating new todo with title: %s", title)
            if not title:
                logger.warning("Todo creation failed: 'title' is required")
                return {"error": "'title' is required"}, 400

            new_todo = Todo(title=title)
            db.session.add(new_todo)
            db.session.commit()
            logger.info("Todo created: %s", {"id": new_todo.id, "title": new_todo.title})
            return {"message": "Todo created", "todo": {"id": new_todo.id, "title": new_todo.title}}, 201
        except Exception as e:
            logger.error("Error creating todo: %s", e)
            return {"error": "An unexpected error occurred"}, 500


@todos_bp.route("/<int:id>/")  # Route explicitly ends with a trailing slash
class TodoResource(Resource):
    def get(self, id):
        """Get a todo by ID."""
        try:
            logger.info("Fetching todo with ID: %d", id)
            todo = db.session.get(Todo, id)
            if not todo:
                logger.warning("Todo not found with ID: %d", id)
                return {"error": "Todo not found"}, 404
            logger.debug("Todo fetched: %s", {"id": todo.id, "title": todo.title})
            return {"id": todo.id, "title": todo.title}, 200
        except Exception as e:
            logger.error("Error fetching todo with ID %d: %s", id, e)
            return {"error": "An unexpected error occurred"}, 500

    @todos_bp.expect(todo_model)
    def put(self, id):
        """Update a todo by ID."""
        try:
            logger.info("Updating todo with ID: %d", id)
            todo = db.session.get(Todo, id)
            if not todo:
                logger.warning("Todo not found for update with ID: %d", id)
                return {"error": "Todo not found"}, 404

            data = request.get_json()
            title = data.get("title", todo.title)
            logger.debug("Updating title to: %s", title)
            todo.title = title
            db.session.commit()
            logger.info("Todo updated: %s", {"id": todo.id, "title": todo.title})
            return {"message": "Todo updated", "todo": {"id": todo.id, "title": todo.title}}, 200
        except Exception as e:
            logger.error("Error updating todo with ID %d: %s", id, e)
            return {"error": "An unexpected error occurred"}, 500

    def delete(self, id):
        """Delete a todo by ID."""
        try:
            logger.info("Deleting todo with ID: %d", id)
            todo = db.session.get(Todo, id)
            if not todo:
                logger.warning("Todo not found for deletion with ID: %d", id)
                return {"error": "Todo not found"}, 404
            db.session.delete(todo)
            db.session.commit()
            logger.info("Todo deleted with ID: %d", id)
            return {"message": "Todo deleted"}, 200
        except Exception as e:
            logger.error("Error deleting todo with ID %d: %s", id, e)
            return {"error": "An unexpected error occurred"}, 500
