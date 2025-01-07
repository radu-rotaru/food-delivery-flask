from flask import Blueprint, request, jsonify
from app.models import db, Order

routes = Blueprint("routes", __name__)

@routes.route('/')
def hello_world():
    return "Hello, World with __init__.py and routes!"

# Helper function to serialize order object to dictionary
def order_to_dict(order):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "restaurant_id": order.restaurant_id,
        "menu_items_ids": order.menu_items_ids,
        "status": order.status,
    }

# Get orders by user ID
@routes.route('/user/<int:id>', methods=['GET'])
def get_orders_by_user(id):
    orders = Order.query.filter_by(user_id=id).all()
    if not orders:
        return jsonify({"message": "No orders found for this user"}), 404
    return jsonify([order_to_dict(order) for order in orders]), 200


# Get orders by restaurant ID
@routes.route('/restaurant/<int:id>', methods=['GET'])
def get_orders_by_restaurant(id):
    orders = Order.query.filter_by(restaurant_id=id).all()
    if not orders:
        return jsonify({"message": "No orders found for this restaurant"}), 404
    return jsonify([order_to_dict(order) for order in orders]), 200


# Create a new order
@routes.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        new_order = Order(
            user_id=data.get("user_id"),
            restaurant_id=data.get("restaurant_id"),
            menu_items_ids=data.get("menu_items_ids"),
            status=data.get("status", "processing"),
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(order_to_dict(new_order)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update the status of an order
@routes.route('/<int:id>/status', methods=['PUT'])
def update_order_status(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()
    new_status = data.get("status")
    if not new_status or new_status not in ['cancel', 'processing', 'done']:
        return jsonify({"error": "Invalid status"}), 400

    try:
        order.status = new_status
        db.session.commit()
        return jsonify(order_to_dict(order)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400