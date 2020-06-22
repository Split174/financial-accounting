"""
module with application entry point
"""
from flask import Flask
from database import db
from blueprint.category import bp as bp_category
from blueprint.user import bp as bp_user
from blueprint.auth import bp as bp_auth


def create_app():
    """
    entry point
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(bp_category, url_prefix='/categories')
    app.register_blueprint(bp_user, url_prefix='/user')
    app.register_blueprint(bp_auth, url_prefix='/auth')
    db.init_app(app)
    return app

