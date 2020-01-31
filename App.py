import json

from flask import Flask
from flask import request

from model.user import User
from model.ad import Advert

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

@app.route("/ads", methods = ["POST"])
@auth.login_required
def post_ad():
    data = request.get_json(force=True, silent=True)

    if data == None:
        return "Bad request", 400

    user = User.find_by_username(auth.username())

    advert = Advert(data["title"], data["description"], data["price"], data["creation_date"], True, user.get_id(), buyer_id = None)
    advert.create()

    return json.dumps(advert.to_dict()), 201

@app.route("/ads", methods = ["GET"])
def get_ads():
    ads = {"advertisements": []}
    
    for ad in Advert.get_ads():
        ads["advertisements"].append(ad.to_dict())

    return json.dumps(ads)


@app.route("/ads/<id>", methods = ["GET"])
def get_ad(id):
    return json.dumps(Advert.get_ad(id).to_dict())

@app.route("/ads/<id>", methods = ["DELETE"])
@auth.login_required
def delete_ad(id):
    user = User.find_by_username(auth.username())

    Advert.delete(id, user.get_id())
    return 'Success', 200

@app.route("/ads/<id>", methods = ["PATCH"])
@auth.login_required
def update_ad(id):
    data = request.get_json(force=True, silent=True)
    user_id = User.find_by_username(auth.username()).get_id()

    Advert.update_advert(Advert(data["title"], data["description"], data["price"], data["creation_date"], True, user_id), id)

    return "Success", 200


@app.route("/ads/<id>/buy", methods = ["PATCH"])
@auth.login_required
def buy_ad(id):
    data = request.get_json(force=True, silent=True)
    user_id = User.find_by_username(auth.username()).get_id()

    Advert.update_advert(Advert(data["title"], data["description"], data["price"], data["creation_date"], False, user_id, user_id), id) #fisrt user_id is not used

    return "Success", 200

@app.route('/sold')
@auth.login_required
def check_sold():
    result = {'sold': []}
    user_id = User.find_by_username(auth.username()).get_id()

    for ad in User.get_sold_ads(user_id):
        result['sold'].append(ad.to_dict())

    return json.dumps(result)

if __name__ == '__main__':
    app.run()