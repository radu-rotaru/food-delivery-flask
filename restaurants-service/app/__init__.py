from flask import Flask
from flask_migrate import Migrate
from app.config import Config
from app.models import db
from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(routes)
    return app
