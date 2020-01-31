import json

from flask import Flask
from flask import request

from model.user import User

from security.basicAuth import init_auth, get_password_hash
from error import register_error_handlers

app = Flask(__name__)
auth = init_auth()
register_error_handlers(app)

@app.route('/')
@app.route('/home')
def index():
    return 'Go to /users to create your first user'

@app.route('/users', methods = ['POST'])
def post_user():
    data = request.get_json(force=True, silent=True)

    if data == None:
        return 'Bad request', 400

    hashed_password = get_password_hash(data['password'])
    user = User(data['email'], data['username'], hashed_password, data['address'], data['phone'])
    user.create()

    return json.dumps(user.to_dict()), 201

@app.route('/users', methods = ['GET'])
def get_users():
    result = {'users': []}
    
    for user in User.get_users():
        result['users'].append(user.to_dict())

    return json.dumps(result)

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    return json.dumps(User.get_user(id).to_dict())

@app.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    User.delete(id)
    return 'Success', 200

@app.route('/users/<id>', methods = ['PATCH'])
def update_user(id):
    data = request.get_json(force=True, silent=True)

    User.update_user(User(None, data['username'], None, data['address'], data['phone'], id))

    return 'Success', 200

@app.route('/login')
@auth.login_required
def login():
    return 'Hello, {}!'.format(auth.username())

if __name__ == '__main__':
    app.run()