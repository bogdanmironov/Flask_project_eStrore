from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from error import NotFound

users = {
    'john': generate_password_hash('hello'),
    'susan': generate_password_hash('bye')
}

def get_password_hash(password):
    return generate_password_hash(password)


def __verify_password(username, password):
    if username not in users.keys():
        return False
    
    return check_password_hash(users[username], password)
    

def init_auth():
    auth = HTTPBasicAuth()
    auth.verify_password(__verify_password)
    return auth