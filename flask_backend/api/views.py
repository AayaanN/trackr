# from flask import Blueprint, jsonify, request
import random
import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import json
import matplotlib.pyplot as plt




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

