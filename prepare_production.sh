#!/usr/bin/env bash
# prepare_production.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Define directories to clean up and store production-ready files
OUTPUT_DIR="production_build"
STATIC_DIR="backend/static"

# 2. Cleanup previous build artifacts
echo "Cleaning up previous builds..."
rm -rf "$OUTPUT_DIR" "$STATIC_DIR"

# 3. Build the React frontend (located in frontend/)
echo "Building the React frontend..."
cd frontend
npm install
npm run build
cd ..

# 4. Create the output directory structure
echo "Creating production build directory..."
mkdir -p "$OUTPUT_DIR/backend/app/static"  # Ensure app's static directory exists
mkdir -p "$STATIC_DIR"  # Ensure backend/static directory exists

# 5. Copy the React build output into both the Flask app's static directory and backend/static
echo "Copying React build to production_build/backend/app/static and backend/static..."
cp -r frontend/dist/* "$OUTPUT_DIR/backend/app/static"
cp -r frontend/dist/* "$STATIC_DIR"

# 6. Copy the Flask application and related files from backend/
echo "Copying Flask backend..."
cp -r backend/app "$OUTPUT_DIR/backend"
cp backend/wsgi.py "$OUTPUT_DIR/backend"
cp backend/app/config.py "$OUTPUT_DIR/backend/app"       # Corrected path
cp backend/requirements.txt "$OUTPUT_DIR/backend"
cp backend/Procfile "$OUTPUT_DIR/backend"

# 7. Copy the .env file from backend/.env to production_build/backend/.env
echo "Copying .env file to production build..."
cp backend/.env "$OUTPUT_DIR/backend/.env"

# 8. Copy the migrations directory to the production build
echo "Copying migrations directory to production build..."
cp -r backend/migrations "$OUTPUT_DIR/backend/migrations"

# 9. Set up the production environment and run migrations
echo "Setting up the production environment and running migrations..."

# Change to the backend directory
cd "$OUTPUT_DIR/backend"

# 9.1. Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 9.2. Activate the virtual environment
source venv/bin/activate

# 9.3. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# 9.4. Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# 9.5. Install python-dotenv if not already installed
echo "Installing python-dotenv..."
pip install python-dotenv

# 9.6. Export environment variables from .env
echo "Exporting environment variables from .env..."
export $(grep -v '^#' .env | xargs)

# 9.7. Run database migrations
echo "Running database migrations..."
flask db upgrade

# 9.8. Deactivate the virtual environment
deactivate

# Navigate back to the project root
cd "$OLDPWD"

# 10. Create a zip archive inside the production_build directory
echo "Zipping the production_build directory..."
cd "$OUTPUT_DIR"  # Ensure we're in the correct directory
zip -r flask_app.zip ./*

echo "Production assets have been prepared in the '$OUTPUT_DIR/flask_app.zip' file."
