# from collections.abc import Mapping
import parser

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import jwt_required  # JWT=Jason Web Token

# for flask restful we don't need to jsonify

new_app = Flask(__name__)
# new_app.secret_key='secret101'
api = Api(new_app)
# jwt = JWT(new_app,security,identity) #checks and authenticate user --->/auth


items = []


class Item(Resource):
    parse = parser.RequestParser()
    parse.add_argument('price',
                       type=float,
                       required=True,
                       help='Field can\'t be left unfilled')

    # @jwt_required() #by adding this decorator we will going to have to authenticate before get method.
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404  # using the ryt status code is important

    def post(self, name):
        if (next(filter(lambda x: x['name'] == name, items), None)) is not None:
            return {'message': "An item with name '{}' already exist .".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}, 204

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1/item/item_name
api.add_resource(ItemList, '/items')
new_app.run(port=5000, debug=True)
