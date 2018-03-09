# old
# from flask import Flask, request
# from flask_restful import Resource, Api, reqparse
# from flask_jwt import JWT, jwt_required
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from datetime import datetime, timedelta
from resources.user import UserRegister, UserInfo
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.secret_key = 'mysecret'

# create sql alchemy decorator so when first app running will execute the method
@app.before_first_request
def create_tables():
    db.create_all()

# change default url from /auth to /login
# app.config['JWT_AUTH_URL_RULE'] = '/login'

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of defult 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

jwt = JWT(app, authenticate, identity) # jwt will create end-point -> /auth

# customize jwt response header
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id,
                    'expired_time': datetime.now() + timedelta(seconds=1800)})

@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({'message': error.description,
                    'code': error.status_code}), error.status_code

# items = []

# class Student(Resource):
#     def get(self, name):
#         return {'student': name}
#
# api.add_resource(Student, '/student/<string:name>')



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserInfo, '/user')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
