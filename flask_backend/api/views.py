from flask import Blueprint, jsonify, request
import random
# import finnhub

# finnhub_client = finnhub.Client(api_key="YOUR API KEY")

main = Blueprint('main', __name__)

@main.route('/add_data', methods=['POST'])

def add_data():


    return 'added'

@main.route('/get_data', methods = ['GET'])

def get_data():

    stocks = [{'name':'AAPL', 'price': 200}, {'name':'AMZN', 'price': 300}]

    return jsonify({'stocks':stocks})

