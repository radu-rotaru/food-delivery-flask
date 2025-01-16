import json
from flask import Blueprint, request, jsonify
from app.models import db, Order
from sqlalchemy import text


routes = Blueprint("routes", __name__)

# Helper function to serialize order object to dictionary
def order_to_dict(order):
    try:
        menu_items_ids = json.loads(order.menu_items_ids)  # Asigură-te că procesul de deserializare e corect
        menu_items_names = json.loads(order.menu_items_names)
    except json.JSONDecodeError as e:
        print(f"Error deserializing JSON: {e}")
        menu_items_ids = []
        menu_items_names = []
    return {
        "id": order.id,
        "user_id": order.user_id,
        "restaurant_id": order.restaurant_id,
        "menu_items_ids": order.menu_items_ids,
        "status": order.status,
        "menu_items_names": order.menu_items_names,
        "client_name": order.client_name,
        "restaurant_name": order.restaurant_name
    }

# Get orders by user ID
@routes.route('/user/<int:id>', methods=['GET'])
def get_orders_by_user(id):
    orders = Order.query.filter_by(user_id=id).all()
    if not orders:
        return jsonify({"message": "No orders found for this user"}), 404
    return jsonify([order_to_dict(order) for order in orders]), 200

# @routes.route('/orders', methods=['GET'])
# def get_all_orders():
#     orders = Order.query.all()  # Obține toate comenzile
#     orders = [order_to_dict(order) for order in orders]  # Serializează în JSON
#     return jsonify(orders)  # Returnează JSON-ul pentru frontend


# Get orders by restaurant ID
@routes.route('/orders', methods=['GET'])
def get_orders_by_restaurant():
    try:
        # Custom query to fetch only the necessary fields
        query = """
                SELECT id, restaurant_name, menu_items_names, status, client_name 
                FROM "order";
            """
        result = db.session.execute(text(query))
        orders = [
            {
                "id": row.id,
                "restaurant_name": row.restaurant_name,
                "menu_items_names": row.menu_items_names,
                "status": row.status,
                "client_name": row.client_name,
            }
            for row in result
        ]
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Create a new order
@routes.route('/createOrder', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        new_order = Order(
            user_id=data.get("user_id"),
            restaurant_id=data.get("restaurant_id"),
            menu_items_ids=data.get("menu_items_ids"),
            menu_items_names=data.get("menu_items_names"),
            client_name=data.get("client_name"),
            restaurant_name=data.get("restaurant_name"),
            status=data.get("status", "processing"),
        )
        db.session.add(new_order)
        db.session.commit()
        return  201
    except Exception as e:
        return 400

# Update the status of an order
@routes.route('/<int:id>/status', methods=['PUT'])
def update_order_status(id):
    try:
        # Parse the JSON body for the new status
        data = request.get_json()
        new_status = data.get("status")

        # Validate the status
        if not new_status or new_status not in ['cancel', 'processing', 'done']:
            return jsonify({"error": "Invalid status"}), 400

        # Update the status in the database
        update_query = text("""UPDATE "order" SET status = :status WHERE id = :id""")
        db.session.execute(update_query, {"status": new_status, "id": id})
        db.session.commit()

        # Return the updated order details
        updated_order_query = text("""
            SELECT id, restaurant_name, menu_items_names, status, client_name 
            FROM "order" WHERE id = :id
        """)
        updated_order = db.session.execute(updated_order_query, {"id": id}).fetchone()

        if updated_order:
            order_dict = {
                "id": updated_order.id,
                "restaurant_name": updated_order.restaurant_name,
                "menu_items_names": updated_order.menu_items_names,
                "status": updated_order.status,
                "client_name": updated_order.client_name,
            }
            return jsonify(order_dict), 200
        else:
            return jsonify({"error": "Failed to retrieve updated order"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 400