from database import SQLite
from error import NotFound, Forbidden

class Advert(object):
    
    def __init__(self, title, description, price, creation_date, is_active, user_id, buyer_id = None , id = None):
        self.title = title
        self.description = description 
        self.price = price 
        self.creation_date = creation_date 
        self.is_active = is_active 
        self.buyer_id = buyer_id
        self.id = id
        self.user_id = user_id

    def to_dict(self):
        data = self.__dict__
        return data

    def create(self):
        with SQLite() as db:
            args = (self.title, self.description, self.price, self.creation_date, self.is_active, self.buyer_id, self.user_id)
            cursor = db.execute('INSERT INTO advert (title, description, price, creation_date, is_active, buyer_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                                args)
            self.id = cursor.lastrowid

        return self

    def update_advert(self, ad_id):
        ad = Advert.get_ad(ad_id)

        if self.user_id != ad.user_id:
            raise Forbidden("User doesnt own ad")


        with SQLite() as db:
            db.execute('UPDATE advert SET title=?, description=?, creation_date=?, is_active=?, buyer_id=? WHERE id=?', (self.title, self.description, self.creation_date, self.is_active, self.buyer_id, ad_id))

        return self


    @staticmethod
    def delete(ad_id, user_id):
        if Advert.get_ad(ad_id).user_id != user_id:
            raise Forbidden("User doesnt own ad")

        result = None
        with SQLite() as db:
            result = db.execute('DELETE FROM advert WHERE id = ?',
                    (ad_id,))
        if result.rowcount == 0:
            raise NotFound('No value present')

    @staticmethod
    def get_ads():
        query = 'SELECT title, description, price, creation_date, is_active, user_id, buyer_id, id FROM advert'
        
        with SQLite() as db:
            ads = db.execute(query).fetchall()

        return [Advert(*ad) for ad in ads]
            
    @staticmethod
    def get_ad(ad_id):
        query = 'SELECT title, description, price, creation_date, is_active, user_id, buyer_id, id FROM advert WHERE id = ?'
        
        with SQLite() as db:
            ad = db.execute(query, ad_id).fetchone()

        if ad is None:
            raise NotFound('Advert does not exist')

        return Advert(*ad)
