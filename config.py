import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'supersecretkey'
    POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
    if not POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY environment variable is not set")
