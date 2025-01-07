from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    restaurant_id = db.Column(db.Integer, nullable=True)
    menu_items_ids = db.Column(db.PickleType, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='processing')


