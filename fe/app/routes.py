from flask import Blueprint, abort, render_template, request, redirect, url_for
import requests

USERS_SERVICE_URL = 'http://users-service:5000'
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
            return redirect(url_for('routes.dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials!")
    except requests.exceptions.RequestException as e:
        return render_template('login.html', error="Service is unavailable, please try again later.")

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
            return render_template('register.html', error="Registration failed!")
    except requests.exceptions.RequestException as e:
        return render_template('register.html', error="Service is unavailable, please try again later.")

@routes.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"
