from flask import Blueprint, request, jsonify

routes = Blueprint("routes", __name__)

@routes.route('/')
def hello_world():
    return "Hello, World with __init__.py and routes!"
