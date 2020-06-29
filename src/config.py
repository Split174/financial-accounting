"""
module contains config
"""
import os


class Config:
    """
    Сonfig class for app_flask
    """
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'sqlite:///data_base.db')
    SECRET_KEY = os.getenv('SECRET_KEY').encode()
