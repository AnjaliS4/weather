import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:ANJALI999@localhost:5432/mydb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'your_openweather_api_key')
    NEWSAPI_API_KEY = os.environ.get('NEWSAPI_API_KEY', 'your_newsapi_api_key')
