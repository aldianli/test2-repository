import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(80))

    def __init__(self,username, password):
        self.username = username
        self.password = password

    # @jwt_required()
    # def get(self):
    #     user = current_identity
    #     return {'user' : {'user_id': user.id, 'username': user.username}}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    @classmethod
    def find_by_id(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        if user:
            return user
        else:
            return None
