#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc, asc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    if not bakeries:
        return {'Error': 'There are currenty no bakeries in database.'}, 404

    bakeries_data = [b.to_dict() for b in bakeries]

    return bakeries_data, 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return {'Error': f'Bakery with id {id} does not currently exist.'}, 404

    return bakery.to_dict(), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    if not sorted_baked_goods:
        return make_response(jsonify({'Error': 'There are no baked goods in the database.'}), 404)

    sbg_data = [s.to_dict() for s in sorted_baked_goods]

    return make_response(jsonify(sbg_data), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    sorted_baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).first()

    if not sorted_baked_goods:
        return make_response(jsonify({'Error': 'There are no baked goods in the database.'}), 404)

    return make_response(jsonify(sorted_baked_goods.to_dict()), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
