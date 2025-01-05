from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configurare baza de date PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@postgres_db/restaurant_menu_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modele pentru restaurante și meniuri
class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    menus = db.relationship('MenuItem', backref='restaurant', lazy=True)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

# Creare baze de date
def create_tables():
    db.create_all()

@app.before_request
def initialize_once():
    if not hasattr(app, '_initialized'):
        app._initialized = True
        # Place your initialization code here
        create_tables()

@app.route('/')
def home():
    return render_template('index.html')

# Endpoint: Listă de restaurante
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        'id': r.id, 'name': r.name, 'location': r.location
    } for r in restaurants]), 200

# Endpoint: Detalii despre un restaurant
@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant_details(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    return jsonify({
        'id': restaurant.id,
        'name': restaurant.name,
        'location': restaurant.location
    }), 200

# Endpoint: Adaugă un restaurant (doar pentru admin)
@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    if 'name' not in data or 'location' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_restaurant = Restaurant(name=data['name'], location=data['location'])
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify({
        'id': new_restaurant.id,
        'name': new_restaurant.name,
        'location': new_restaurant.location
    }), 201

# Endpoint: Listă de produse din meniu
@app.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404

    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return jsonify([{
        'id': item.id, 'name': item.name, 'price': item.price
    } for item in menu_items]), 200

# Endpoint: Adaugă un produs în meniu
@app.route('/restaurants/<int:restaurant_id>/menu', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
