import json

class BadRequest(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def to_dict(self):
        return { "message": self.message }

class NotFound(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 404

    def to_dict(self):
        return { "message": self.message }

class Unauthorised(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 401

    def to_dict(self):
        return { "message": self.message }

class UserExists(Exception):
    def __init__(self):
        self.message = "User already exists"
        self.status_code = 409

    def to_dict(self):
        return { "message": self.message }


def __handle_error(error):
    return json.dumps(error.to_dict()), error.status_code

def register_error_handlers(app):
    app.register_error_handler(BadRequest, __handle_error)
    app.register_error_handler(NotFound, __handle_error)
    app.register_error_handler(Unauthorised, __handle_error)
    app.register_error_handler(UserExists, __handle_error)