# src/config.py
from dotenv import load_dotenv
import os

def load_config():
    # load the .env file
    load_dotenv(dotenv_path='keyword_generator_env/.env')  # Adjust the path to your .env file if needed
    
    # construct the DATABASE_URL from other environment variables
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    
    return {
        "DATABASE_URL": DATABASE_URL
    }