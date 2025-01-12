from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
import requests

USERS_SERVICE_URL = 'http://users-service:5000'
RESTAURANTS_SERVICE_URL = 'http://restaurants-service:5000'
ORDER_SERVICE_URL = 'http://order-service:5000'
PAYMENT_SERVICE_URL = 'http://payment-methods-service:5000'
routes = Blueprint("routes", __name__)

@routes.route('/')
def home():
    return render_template('login.html')

@routes.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        response = requests.post(f'{USERS_SERVICE_URL}/login', json={
            'email': email,
            'password': password
        })
        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                resp = make_response(redirect(url_for('routes.dashboard')))
                resp.set_cookie('jwt', token)
                return resp
            else:
                flash("Failed to retrieve token!", "error")
                return render_template('login.html')
        else:
            flash("Invalid credentials!", "error")
            return render_template('login.html')
    except requests.exceptions.RequestException as e:
        flash("Service is unavailable, please try again later.", "error")
        return render_template('login.html')

@routes.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@routes.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    try:
        response = requests.post(f'{USERS_SERVICE_URL}/register', json={
            'email': email,
            'password': password
        })
        if response.status_code == 201:
            return redirect(url_for('routes.home'))
        else:
            flash("Registration failed!", "error")
            return render_template('register.html')
    except requests.exceptions.RequestException as e:
        flash("Service is unavailable, please try again later.", "error")
        return render_template('register.html')

@routes.route('/dashboard')
def dashboard():
    token = request.cookies.get('jwt')
    if not token:
        flash("You need to log in first.", "error")
        return redirect(url_for('routes.home'))

    headers = {'Authorization': f'Bearer {token}'}

    try:
        users_response = requests.get(f'{USERS_SERVICE_URL}/me', headers=headers)
        if users_response.status_code == 200:
            user_info = users_response.json()

            if user_info.get('role') == 'admin':
                return render_template('dashboard-admin.html', user_info=user_info)
            else:
                flash(restaurants_response.json().get('message'), "error")
                return render_template('dashboard.html', user_info=user_info)
        else:
            flash(users_response.json().get('message'), "error")
            return redirect(url_for('routes.home'))
    except requests.exceptions.RequestException:
        flash("Service is unavailable, please try again later.", "error")
        return redirect(url_for('routes.home'))

@routes.route('/logout')
def logout():
    resp = make_response(redirect(url_for('routes.home')))
    resp.set_cookie('jwt', '', expires=0)
    flash("You have been logged out.", "success")
    return resp

@routes.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants_response = requests.get(f'{RESTAURANTS_SERVICE_URL}/restaurants')
    if restaurants_response.status_code == 200:
        return render_template('restaurants.html', restaurants=restaurants_response.json())
    else:
        flash("Failed to retrieve restaurants!", "error")
        return render_template('home.html')

@routes.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def restaurant(restaurant_id):
    restaurant_response = requests.get(f'{RESTAURANTS_SERVICE_URL}/restaurants/{restaurant_id}')
    if restaurant_response.status_code == 200:
        return render_template('restaurant.html', restaurant=restaurant_response.json())
    else:
        flash("Failed to retrieve restaurant!", "error")
        return redirect(url_for('routes.restaurants'))

@routes.route('/admin_orders', methods=['GET'])
def admin_orders_page():
    # Fetch all orders from the database
    orders =requests.get(f'{ORDER_SERVICE_URL}/restaurants/1')
    return render_template('admin_orders.html', orders=orders)


@routes.route('/admin_orders/restaurant/<int:id>', methods=['GET'])
def restaurant_orders(id):
    # Fetch the orders from the API
    id=1
    response = requests.get(f'{ORDER_SERVICE_URL}/restaurant/{id}')
    response.raise_for_status()
    orders = response.json()

    return render_template('admin_orders.html', restaurant_id=id, orders=orders)


@routes.route('/orders/update', methods=['POST'])
def update_order_status():
    order_id = request.form.get('order_id')
    status = request.form.get('status')
    restaurant_id = request.form.get('restaurant_id')

    if not order_id or not status:
        flash("Order ID and status are required.", "error")
        return redirect(url_for('routes.restaurant_orders', id=restaurant_id))

    try:
        response = requests.put(f'{ORDER_SERVICE_URL}/{order_id}/status', json={'status': status})
        response.raise_for_status()
        flash(f"Order {order_id} updated to {status}.", "success")
    except requests.exceptions.RequestException as e:
        flash(f"Error updating order: {e}", "error")

    return redirect(url_for('routes.restaurant_orders', id=restaurant_id))

@routes.route('/promotions', methods=['GET'])
def list_promotions():
    try:
        # Fetch promotions from the backend
        response = requests.get(PAYMENT_SERVICE_URL + '/promotions/')
        response.raise_for_status()
        promotions = response.json()
        return render_template('admin_promotions.html', promotions=promotions)
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching promotions: {e}", "error")
        return render_template('admin_promotions.html', promotions=[])

@routes.route('/promotions', methods=['POST'])
def add_promotion():
    user_id = request.form.get('user_id')
    value = request.form.get('value')

    if not user_id or not value:
        flash("User ID and value are required.", "error")
        return redirect(url_for('routes.list_promotions'))

    try:
        # Send a POST request to the backend to add the promotion
        response = requests.post(f'{PAYMENT_SERVICE_URL}/promotions/{user_id}', json={'value': value})
        response.raise_for_status()
        flash("Promotion added successfully.", "success")
    except requests.exceptions.RequestException as e:
        flash(f"Error adding promotion: {e}", "error")

    return redirect(url_for('routes.list_promotions'))

 @app.route('/add_restaurant', methods=['GET', 'POST'])
 def add_restaurant():
     if request.method == 'POST':
         # Get data from the form
         name = request.form.get('name')
         location = request.form.get('location')
         description = request.form.get('description')

         # Create a new restaurant entry
         new_restaurant = Restaurant(name=name, location=location, description=description)

         # Add to the database
         db.session.add(new_restaurant)
         db.session.commit()

         # Redirect to the restaurants page
         return redirect(url_for('routes.restaurants'))

     # If the request method is GET, render the form to add a restaurant
     return render_template('add_restaurant.html')
