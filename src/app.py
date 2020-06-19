from flask import Flask
from database import db
from blueprint.category import bp as bp_category

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(bp_category, url_prefix='/category')
    db.init_app(app)
    return app

