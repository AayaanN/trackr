# from flask import Blueprint, jsonify, request
import random
import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import json
import matplotlib.pyplot as plt
from .models import Stock, Portfolio_Log
from . import db
import string
import requests
from sqlalchemy import desc
# import finnhub

# finnhub_client = finnhub.Client(api_key="YOUR API KEY")

api_key = 'DNWQMLFC43J1PHDI'


main = Blueprint('main', __name__)

@main.route('/add_data', methods=['POST'])

def add_data():

    data = request.json
    name_data = data['query'].upper()
    amount_data = int(data['amount'])

    portfolio = Portfolio_Log.query.order_by(desc(Portfolio_Log.id)).first()

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={name_data}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if data['Global Quote'] and amount_data is not None and portfolio:

        stock_data = data['Global Quote']

        current_price = float(stock_data['05. price']) + 0.00

        previous_close = float(stock_data['08. previous close'])

        change = current_price - previous_close

        percent_change = (change / previous_close) * 100

        price_bought_at = current_price

        average_price = current_price

        value = average_price * amount_data

        new_stock = Stock(name = name_data, price = current_price, prev_price=previous_close, change=change, percent_change=percent_change, amount=amount_data, price_bought_at=price_bought_at, average_price=average_price, value=value)
        
        #adding to portfolio db
        new_value = portfolio.value + value

        new_portfolio_log = Portfolio_Log(value=new_value, initial_value=new_value, change=portfolio.change, percent_change=portfolio.percent_change)

        db.session.add(new_stock)
        db.session.add(new_portfolio_log)
        db.session.commit()

        return jsonify({'ok'})




# def add_data():

#     name_data = request.json['query'].upper()
#     amount_data = request.json['amount']

#     url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={name_data}&apikey={api_key}'
#     response = requests.get(url)
#     data = response.json()

#     # portfolio = Stock.query.order_by(desc(Stock.id)).first()
#     # try:
#     if data['Global Quote'] and amount_data is not None:

#         # adding to stock_db
#         stock_data = data['Global Quote']

#         current_price = float(stock_data['05. price']) + 0.00

#         previous_close = float(stock_data['08. previous close'])

#         change = current_price - previous_close

#         percent_change = (change / previous_close) * 100

#         price_bought_at = current_price

#         average_price = current_price

#         value = average_price * amount_data

#         new_stock = Stock(name = name_data, price = current_price, prev_price=previous_close, change=change, percent_change=percent_change, amount=amount_data, price_bought_at=price_bought_at, average_price=average_price, value=value)
        
#         #adding to portfolio db
#         # new_value = portfolio.value + value

#         # new_portfolio_log = Portfolio_Log(value=new_value, initial_value=new_value, change=portfolio.change, percent_change=portfolio.percent_change)

#         db.session.add(new_stock)
#         # db.session.add(new_portfolio_log)
#         db.session.commit()

#         return 'ok'

#     # except Exception as e:
#     #     return ('ahhh')


#     return 'added'


url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AMZN&outputsize=full&apikey=JU7L288S6R939NEC'
r = requests.get(url)

data = r.json()

with open( "data_file.json" , "w" ) as write:
    json.dump( data["Time Series (Daily)"] , write )

with open("data_file.json", "r") as read_content:
    stock_dict = json.load(read_content)
    dates = []
    dates_keys = stock_dict.keys()
    for key in dates_keys:
        dates.append(key)
    # df = pd.DataFrame(dates, columns=["dates"])
    # print(df)
    val = stock_dict.values()
    close = []

    for value in val:
        close.append(float(value["5. adjusted close"]))
        
    
    
    list_of_tuples = list(zip(dates, close))

    df = pd.DataFrame(list_of_tuples,
                  columns=['Date', 'Close']) 
    
    df= df.loc[::-1]
    df.index = df.pop('Date')

    
    print(df)

    plt.plot(df.index, df['Close'])

    plt.show()

# print(data)
# data = r.json()
# with open(data) as country_json1:
#   country_dict = json.load(country_json1)
#   print(country_dict)
# json.load(data['Time Series (Daily)'])

# df = pd.json_normalize(data['Time Series (Daily)']) 

# df.drop("3. low")

# print(df)

# numpy_2d_arrays = np.array(dict["data"])

# print(numpy_2d_arrays)
    # stocks = [{'name':'AAPL', 'price': 200}, {'name':'AMZN', 'price': 300}]

    stock_list = Stock.query.order_by(Stock.id).all()

    stocks = []

    for stock in stock_list:
        stocks.append({'name': stock.name, 'price': stock.price, 'prev_price': stock.prev_price, 'change':stock.change, 'percent_change': stock.percent_change, 'amount': stock.amount, 'price_bought_at': stock.price_bought_at, 'average_price': stock.average_price, 'value':stock.value})

    return jsonify({'stocks':stocks})

@main.route('/get_portfolio', methods = ['GET'])

def get_portfolio():

    # stocks = [{'name':'AAPL', 'price': 200}, {'name':'AMZN', 'price': 300}]

    portfolio = Portfolio_Log.query.order_by(desc(Portfolio_Log.id)).first()

    return jsonify({'portfolio':[{'time': portfolio.time, 'change': portfolio.change, 'percent_change': portfolio.percent_change, 'initial_value': portfolio.initial_value, 'value': portfolio.value}]})


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



@main.route('/increase_amount', methods = ['PUT'])

def increase_amount():
    try:
        stock_name = request.json['selected_stock'].upper()
        # stock_name = 'AAPL'

        # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_name}&apikey={api_key}'

        # response = requests.get(url)
        # data = response.json()

        # stock_data = data['Global Quote']

        # current_price = float(stock_data['05. price']) + 0.00


        row = Stock.query.filter_by(name=stock_name).order_by(Stock.id).first()

        portfolio = Stock.query.order_by(desc(Stock.id)).first()


        if row is None:
            return 'row does not exist, error', 404


        # row.average_price = (row.average_price*row.amount + current_price)/(row.amount + 1)

        row.amount += 1

        new_value = portfolio.value + row.average_price

        new_portfolio_log = Portfolio_Log(value=new_value, initial_value=new_value, change=portfolio.change, percent_change=portfolio.percent_change)

        db.session.add(new_portfolio_log)

        db.session.commit()

        return "row updated successfully"
    
    except Exception as e:
        print(e, 'ahhhh help an error')

        return 'oopsy'


@main.route('/decrease_amount', methods=['PUT'])

def decrease_amount():
    try:
        stock_name = request.json['selected_stock'].upper()

        # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_name}&apikey={api_key}'

        # response = requests.get(url)
        # data = response.json()

        # stock_data = data['Global Quote']

        # current_price = float(stock_data['05. price']) + 0.00

        row = Stock.query.filter_by(name=stock_name).order_by(Stock.id).first()

        portfolio = Portfolio_Log.query.order_by(desc(Portfolio_Log.id)).first()


        if row is None:
            return 'row does not exist, error', 404

        if row.amount != 0:
            row.amount -= 1

            new_value = portfolio.value - row.average_price

            new_portfolio_log = Portfolio_Log(value=new_value, initial_value=new_value, change=portfolio.change, percent_change=portfolio.percent_change)

            db.session.add(new_portfolio_log)


        db.session.commit()

        return "row updated successfully"
    
    except Exception as e:
        print(e)

    return "error occurred"  # Add a return statement here

@main.route('/delete_stock', methods=['DELETE'])

def delete_stock():

    stock_name = request.json['selected_stock'].upper()

    row = Stock.query.filter_by(name=stock_name).order_by(Stock.id).first()

    portfolio = Portfolio_Log.query.order_by(desc(Portfolio_Log.id)).first()



    if row:

        new_value = portfolio.value - (row.average_price * row.amount)

        new_portfolio_log = Portfolio_Log(value=new_value, initial_value=new_value, change=portfolio.change, percent_change=portfolio.percent_change)

        db.session.add(new_portfolio_log)

        db.session.delete(row)

        db.session.commit()
        return jsonify({'message': 'Stock deleted successfully'})
    else:
        return jsonify({'error': 'Stock not found'})

   
