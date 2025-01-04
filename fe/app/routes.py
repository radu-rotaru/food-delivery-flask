from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
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
        response = requests.get(f'{USERS_SERVICE_URL}/me', headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return render_template('dashboard.html', user_info=user_info)
            # return f"Welcome to your dashboard! Logged in user #{user_info['email']}"
        else:
            flash(response.json().get('message'), "error")
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
