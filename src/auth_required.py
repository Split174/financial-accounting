"""
decorators module
"""
from functools import wraps
from flask import session


def auth_required(view_func):
    """
    decorator to check if the user is authorized
    :param view_func: view func
    :return: all that was accepted
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return {"answer": "Авторизуйтесь"}, 401
        return view_func(*args, **kwargs, user_id=user_id)
    return wrapper
