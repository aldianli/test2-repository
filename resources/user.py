import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

class UserInfo(Resource):
    @jwt_required()
    def get(self):
        user = current_identity
        return {'user' : {'user_id': user.id, 'username': user.username}}



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message' : 'User {0} already exist'.format(data['username'])}, 400

        try:
            user = UserModel(**data)
            user.save_to_db()
        except:
            return {'message' : 'Error register user'}

        return {'message' : 'User created successfully'}, 201
