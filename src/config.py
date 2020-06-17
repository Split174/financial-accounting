import os


class Config:
    """
    Сonfig class for app_flask
    """
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'db.sqlite')
    SECRET_KEY = os.getenv('SECRET_KEY')