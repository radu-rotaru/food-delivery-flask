from flask import Blueprint, request, jsonify
from app.models import db, UserBalance, Promotions, Payments

routes = Blueprint("routes", __name__)

@routes.route('/payments/balance/<int:user_id>', methods=['GET'])
def get_user_balance(user_id):
    user_balance = UserBalance.query.filter_by(user_id=user_id).first()
    if user_balance:
        return jsonify({"user_id": user_id, "balance": user_balance.balance})
    return jsonify({"error": "User not found"}), 404

@routes.route('/payments/balance', methods=['POST'])
def add_balance():
    data = request.get_json()
    user_id = data.get('user_id')
    balance_to_add = data.get('balance_to_add')

    user_balance = UserBalance.query.filter_by(user_id=user_id).first()
    if user_balance:
        user_balance.balance += balance_to_add
    else:
        user_balance = UserBalance(user_id=user_id, balance=balance_to_add)
        db.session.add(user_balance)
    db.session.commit()
    return jsonify({"user_id": user_id, "new_balance": user_balance.balance})

@routes.route('/promotions/', methods=['GET'])
def get_promotions():
    promotions = Promotions.query.all()
    return jsonify([{ "id": p.id, "user_id": p.restaurant_id, "value": p.value } for p in promotions])

@routes.route('/promotions/<int:user_id>', methods=['POST'])
def add_promotion(user_id):
    data = request.get_json()
    value = data.get('value')
    promotion = Promotions(restaurant_id=user_id, value=value)
    db.session.add(promotion)
    db.session.commit()
    return jsonify({"id": promotion.id, "user_id": user_id, "value": value})

@routes.route('/payments', methods=['POST'])
def make_payment():
    data = request.get_json()
    user_id = data.get('user_id')
    total_amount = data.get('total_amount')
    order_id = data.get('order_id')

    user_balance = UserBalance.query.filter_by(user_id=user_id).first()
    if not user_balance:
        return jsonify({"error": "User not found"}), 404

    promotions = Promotions.query.filter_by(user_id=user_id).all()
    discount = sum(p.value for p in promotions)
    final_amount = total_amount - discount

    user_balance.balance -= final_amount
    status = "paid" if user_balance.balance >= 0 else "unpaid"

    payment = Payments(
        user_id=user_id,
        order_id=order_id,
        status=status,
        total_price=final_amount,
        promotion_applied_id=promotions[0].id if promotions else None
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "user_id": user_id,
        "order_id": order_id,
        "status": status,
        "final_amount": final_amount,
        "new_balance": user_balance.balance
    })

@routes.route('/payments/user/<int:user_id>', methods=['GET'])
def get_user_payments(user_id):
    payments = Payments.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": p.id,
            "order_id": p.order_id,
            "status": p.status,
            "total_price": p.total_price,
            "promotion_applied_id": p.promotion_applied_id
        } for p in payments
    ])
