from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from error import NotFound

from model.user import User

users = {
    'john': generate_password_hash('hello'),
    'susan': generate_password_hash('bye')
}

def get_password_hash(password):
    return generate_password_hash(password)


def __verify_password(username, password):
    try:
        user = User.find_by_username(username)
    except NotFound:
        return False

    return check_password_hash(user.password, password)
    

def init_auth():
    auth = HTTPBasicAuth()
    auth.verify_password(__verify_password)
    return auth