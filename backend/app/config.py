# backend/app/config.py

import os
from dotenv import load_dotenv

class Config:
    # Load environment variables from .env file if it exists
    load_dotenv()

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def validate(cls):
        print("DEBUG (Config): SQLALCHEMY_DATABASE_URI loaded:", cls.SQLALCHEMY_DATABASE_URI)
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise ValueError(
                "SQLALCHEMY_DATABASE_URI is not set. Ensure it's defined in the .env file "
                "or as an environment variable. Check the .env file's location and syntax."
            )

class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use in-memory SQLite database
    ENV = 'testing'

class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False
    ENV = 'production'
    
    # Additional production-specific configurations can be added here
    # For example, setting up logging, security headers, etc.

    @classmethod
    def validate(cls):
        super().validate()
        # Additional production-specific validations can be added here
