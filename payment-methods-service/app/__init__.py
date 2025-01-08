from flask import Flask
from app.models import db
from flask_migrate import Migrate
from app.routes import routes
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(routes)
    return app
