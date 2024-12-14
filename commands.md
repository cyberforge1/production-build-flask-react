# Commands

## Production Build Scripts

chmod +x prepare_production.sh

./prepare_production.sh


## Running Gunicorn (Flask API)

gunicorn --chdir backend --bind 0.0.0.0:5001 wsgi:application



## Running React App

serve -s production_build/frontend_build -l 3000




## Testing API Endpoints

curl http://localhost:5001/api/

curl http://localhost:5001/api/helloworld/

curl http://localhost:5001/api/todos/



# Deploy Production Build Locally

cd production_build/backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

flask db upgrade

gunicorn wsgi:app --bind 0.0.0.0:5001 --workers 4
