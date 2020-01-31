from flask import Flask
from security.basicAuth import init_auth, get_password_hash
from error import register_error_handlers

app = Flask(__name__)
auth = init_auth()
register_error_handlers(app)

@app.route('/')
@auth.login_required
def index():
    return "Hello {}!".format(auth.username())

if __name__ == '__main__':
    app.run()