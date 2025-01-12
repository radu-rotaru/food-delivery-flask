from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
import requests

USERS_SERVICE_URL = 'http://users-service:5000'
RESTAURANTS_SERVICE_URL = 'http://restaurants-service:5000'
ORDERS_SERVICE_URL = 'http://order-service:5000'
PAYMENTS_SERVICE_URL = 'http://payment-methods-service:5000'

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

            if user_info.get('role') == 'customer':
                orders_response = requests.get(f'{ORDERS_SERVICE_URL}/user/{user_info.get("id")}', headers=headers)
                if orders_response.status_code == 200:
                    user_info['orders'] = orders_response.json()

                balance_response = requests.get(f'{PAYMENTS_SERVICE_URL}/payments/balance/{user_info.get("id")}', headers=headers)
                if balance_response.status_code == 200:
                    user_info['balance'] = balance_response.json().get('balance')

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
