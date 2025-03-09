# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration settings"""
    # A proper secret key for session security, CSRF protection, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'EQYtKyOoK8$tQkA&PTw9eBxZyK&P#z9KoQ7Qf%2c')
    
    # Get database URL from environment or use SQLite as fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False