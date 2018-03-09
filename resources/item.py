from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('name', required="True", help="please input name")
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank loh!")
    parser.add_argument('store_id', type=int, required=True, help="This field cannot left blank")

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x : x['name'] == name, iter(items)), None)
        # old
        # item = next((item for item in items if item['name'] == name), None)
        item = ItemModel.find_by_name(name)

        # return next((item for item in items if item['name'] == name), ({'item':None}, 404))
        # old
        # return {'item':item}, 200 if item else 404
        if item:
            return item.json()
        return {'message' : 'Item not found.'}, 404



    def post(self, name):
        # old
        # if next((item for item in items if item['name'] == name), None) is not None:
        # # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message' : "An item with name '{}' already exists.".format(name)}
        #
        # #data = request.get_json() #force=True - means flask not look up the header
        # data = Item.parser.parse_args()
        # item = {'name' : name,
        #  'price' : data['price']}
        # items.append(item)
        # return item, 201
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exist.".format(name)}

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting data'}
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            message = 'Item has deleted'
        else:
            message = 'Item not found'

        return {'message' : message}


    def put(self, name):
        data = Item.parser.parse_args()

        # item = next((item for item in items if item['name'] == name), None)
        # if item is None:
        #     item = {'name' : name, 'price' : data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            Item.store_id = data['store_id']

        item.save_to_db()

        return item.json()



class ItemList(Resource):
    def get(self):
        # list comprehension
        return {'items' : [item.json() for item in ItemModel.query.all()]}

        # lambda
        # return {'items' : list(map(lambda item: item.json(), ItemModel.query.all()))}
