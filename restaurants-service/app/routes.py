from flask import Blueprint, request, jsonify
from app.models import db, Restaurant, MenuItem

routes = Blueprint("routes", __name__)

# Endpoint: Listă de restaurante
@routes.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        'id': r.id, 'name': r.name, 'location': r.location
    } for r in restaurants]), 200

# Endpoint: Detalii despre un restaurant
@routes.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant_details(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404

    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    menu_items_response =  [{
            'id': item.id, 'name': item.name, 'price': item.price
        } for item in menu_items]

    return jsonify({
        'id': restaurant.id,
        'name': restaurant.name,
        'location': restaurant.location,
        'menu': menu_items_response
    }), 200

# Endpoint: Adaugă un restaurant (doar pentru admin)
@routes.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    if 'name' not in data or 'location' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_restaurant = Restaurant(name=data['name'], location=data['location'], description=data['description'])
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify({
        'id': new_restaurant.id,
        'name': new_restaurant.name,
        'location': new_restaurant.location,
        'description': new_restaurant.description
    }), 201

# Endpoint: Listă de produse din meniu
@routes.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404

    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return jsonify([{
        'id': item.id, 'name': item.name, 'price': item.price
    } for item in menu_items]), 200

# Endpoint: Adaugă un produs în meniu
@routes.route('/restaurants/<int:restaurant_id>/menu', methods=['POST'])
def add_menu_item(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404

    data = request.get_json()
    if 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_item = MenuItem(name=data['name'], price=data['price'], restaurant_id=restaurant_id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({
        'id': new_item.id,
        'name': new_item.name,
        'price': new_item.price
    }), 201
