from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserBalance(db.Model):
    __tablename__ = 'user_balances'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id = db.Column(db.Integer, nullable=False, unique=True)  # Unique user ID
    balance = db.Column(db.Float, nullable=False)  # Balance of the user

    def __repr__(self):
        return f"<UserBalance(user_id={self.user_id}, balance={self.balance})>"


class Promotions(db.Model):
    __tablename__ = 'promotions'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    restaurant_id = db.Column(db.Integer, nullable=False)  # ID of the restaurant
    value = db.Column(db.Float, nullable=False)  # Value of the promotion

    def __repr__(self):
        return f"<Promotions(restaurant_id={self.restaurant_id}, value={self.value})>"


class Payments(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id = db.Column(db.Integer, db.ForeignKey('user_balances.user_id'), nullable=False)  # Foreign Key to UserBalance
    order_id = db.Column(db.String(50), nullable=False)  # Unique identifier for the order
    status = db.Column(db.String(20), nullable=False)  # Payment status (e.g., pending, completed)
    total_price = db.Column(db.Float, nullable=False)  # Total price of the payment
    promotion_applied_id = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=True)  # FK to Promotions

    # Relationships for easier access
    user_balance = db.relationship('UserBalance', backref='payments')
    promotion = db.relationship('Promotions', backref='payments')

    def __repr__(self):
        return (
            f"<Payments(user_id={self.user_id}, order_id={self.order_id}, "
            f"status={self.status}, total_price={self.total_price}, promotion_applied_id={self.promotion_applied_id})>"
        )
