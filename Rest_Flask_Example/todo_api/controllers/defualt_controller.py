from flask import Blueprint

default_api = Blueprint('default_api', __name__)

@default_api.route('/')
def index():
    return "Hello, World!"