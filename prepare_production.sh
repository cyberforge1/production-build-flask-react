#!/usr/bin/env bash
# project_root/prepare_production.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Build the React frontend (located in frontend/)
cd frontend
npm install
npm run build
cd ..

# 2. Define the directory to store production-ready files
OUTPUT_DIR="production_build"

# 3. Remove any previous build artifacts
rm -rf "$OUTPUT_DIR"

# 4. Create the output directory
mkdir -p "$OUTPUT_DIR"

# 5. Copy the React build output into the production_build directory
# Vite outputs to 'dist' by default, so we copy that
cp -r frontend/dist "$OUTPUT_DIR/frontend_build"

# 6. Zip the Flask application and related files from backend/
# Ensure these files and directories exist in the project root
zip -r "$OUTPUT_DIR/flask_app.zip" backend/app backend/wsgi.py backend/requirements.txt backend/Procfile

echo "Production assets have been prepared in the '$OUTPUT_DIR' directory."
