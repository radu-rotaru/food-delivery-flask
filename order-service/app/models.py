from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    restaurant_id = db.Column(db.Integer, nullable=True)
    menu_items_ids = db.Column(db.String(1000), nullable=True)
    menu_items_names = db.Column(db.String(1000), nullable=True)
    client_name = db.Column(db.String(100), nullable=True)
    restaurant_name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='processing')
    price = db.Column(db.Float, nullable=False, default=0.0)


