from database import SQLite
from error import NotFound

class User(object):
    
    def __init__(self, email, username, password, address, phone, id = None):
        self.email = email
        self.username = username 
        self.password = password 
        self.address = address 
        self.phone = phone 
        self.id = id

    def to_dict(self):
        data = self.__dict__
        del data['password']
        return data

    def create(self):
        with SQLite() as db:
            args = (self.email, self.username, self.password, self.address, self.phone)
            cursor = db.execute('INSERT INTO user (email, username, password, address, phone) VALUES (?, ?, ?, ?, ?)',
                                args)
            self.id = cursor.lastrowid

        return self

    def update_user(self):
        user = User.get_user(self.id)
        
        with SQLite() as db:
            db.execute('UPDATE user SET email=?, username=?, address=?, phone=? WHERE id=?', (user.email, self.username, self.address, self.phone, self.id))

        return self

    def get_id(self):
        return self.id


    @staticmethod
    def delete(user_id):
        result = None
        with SQLite() as db:
            result = db.execute('DELETE FROM user WHERE id = ?',
                    (user_id,))
        if result.rowcount == 0:
            raise NotFound('No value present')

    @staticmethod
    def get_users():
        query = 'SELECT email, username, password, address, phone, id FROM user'
        
        with SQLite() as db:
            users = db.execute(query).fetchall()

        return [User(*row) for row in users]
            
    @staticmethod
    def get_user(user_id):
        user = None
        query = 'SELECT email, username, password, address, phone, id FROM user WHERE id = ?'
        
        with SQLite() as db:
            user = db.execute(query, user_id).fetchone()

        if user is None:
            raise NotFound('User does not exist')

        return User(*user)

    @staticmethod
    def find_by_username(username):
        with SQLite() as db:
            result = db.execute('SELECT email, username, password, address, phone, id FROM user WHERE username = ?', (username, ))

        user = result.fetchone()
        if user is None:
            raise NotFound('User({}) was not found'.format(username))

        return User(*user)