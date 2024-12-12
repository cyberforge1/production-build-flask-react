# backend/wsgi.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file located in the backend directory
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)

from app import create_app

application = create_app()
