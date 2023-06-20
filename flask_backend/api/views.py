from flask import Blueprint, jsonify, request
import random
from .models import Stock
from . import db
import string
# import finnhub

# finnhub_client = finnhub.Client(api_key="YOUR API KEY")

main = Blueprint('main', __name__)

@main.route('/add_data', methods=['POST'])

def add_data():

    price_data = random.randint(1, 500)

    name_data = request.json['query']

    new_stock = Stock(name = name_data.upper(), price = price_data)

    db.session.add(new_stock)

    db.session.commit()


    return 'added'

@main.route('/get_data', methods = ['GET'])

def get_data():

    # stocks = [{'name':'AAPL', 'price': 200}, {'name':'AMZN', 'price': 300}]

    stock_list = Stock.query.all()

    stocks = []

    for stock in stock_list:
        stocks.append({'name': stock.name, 'price': stock.price})

    return jsonify({'stocks':stocks})

