# Commands

## Production Build Scripts

chmod +x prepare_production.sh

./prepare_production.sh


## Running Gunicorn (Flask API)

gunicorn --chdir backend --bind 0.0.0.0:5001 wsgi:app

## Running React App

serve -s production_build/frontend_build -l 3000


# Venv

source backend/venv/bin/activate


## Testing API Endpoints

curl http://localhost:5001/api/

curl http://localhost:5001/api/helloworld/

curl http://localhost:5001/api/todos/



# Deploy Production Build Locally

cd production_build && source backend/venv/bin/activate

PYTHONPATH=backend gunicorn backend.wsgi:app --bind 0.0.0.0:5001 --workers 4

lsof -i :5001


# Production Endpoints

curl http://127.0.0.1:5001/api/
curl http://127.0.0.1:5001/api/helloworld/
curl http://127.0.0.1:5001/api/todos/
curl -X POST -H "Content-Type: application/json" -d '{"title": "New Todo"}' http://127.0.0.1:5001/api/todos/



