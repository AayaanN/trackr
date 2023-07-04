from flask import Blueprint, jsonify, request
import random
from .models import Stock
from . import db
import string
import requests
# import finnhub

# finnhub_client = finnhub.Client(api_key="YOUR API KEY")

api_key = 'DNWQMLFC43J1PHDI'


main = Blueprint('main', __name__)

@main.route('/add_data', methods=['POST'])

def add_data():



    name_data = request.json['query'].upper()

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={name_data}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['Global Quote']:
        stock_data = data['Global Quote']
        current_price = float(stock_data['05. price']) + 0.00

        previous_close = float(stock_data['08. previous close'])

        change = current_price - previous_close
        percent_change = (change / previous_close) * 100

        new_stock = Stock(name = name_data, price = current_price, prev_price=previous_close, change=change, percent_change=percent_change)
        db.session.add(new_stock)
        db.session.commit()
    else:
        return 'There was an error'


    return 'added'

@main.route('/get_data', methods = ['GET'])

def get_data():

    # stocks = [{'name':'AAPL', 'price': 200}, {'name':'AMZN', 'price': 300}]

    stock_list = Stock.query.all()

    stocks = []

    for stock in stock_list:
        stocks.append({'name': stock.name, 'price': stock.price, 'prev_price': stock.prev_price, 'change':stock.change, 'percent_change': stock.percent_change})

    return jsonify({'stocks':stocks})


@main.route('/check_stock', methods = ['POST'])

def check_stock():

    stock_add = request.json['query'].upper()

    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock_add}&apikey={api_key}'

    r = requests.get(url)
    data = r.json()

    # if (data['bestMatches'][0]['1. symbol'] == stock_add) or (data['bestMatches'][0]['2. name'].upper() == stock_add):
    #     return jsonify({'validity': True})
    #     # return 'yes'
    
    # else:
    #     return jsonify({'validity': False})
    #     # return 'no'

    if 'bestMatches' in data and len(data['bestMatches']) > 0:
        return jsonify({'validity': True})
    else:
        return jsonify({'validity': False})

    # return 'ok'

@main.route('/already_added', methods = ['POST'])

def already_added():

    stock_name = request.json['query'].upper()

    stock_list = Stock.query.all()

    for stock in stock_list:

        if stock.name == stock_name:
            return jsonify({'added': True})
    
    
    return jsonify({'added': False})
