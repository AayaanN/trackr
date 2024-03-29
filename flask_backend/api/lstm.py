import tensorflow
from keras import Sequential
import keras
from keras.optimizers import Adam
from keras import layers
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from copy import deepcopy
import requests
import json

# df = pd.read_csv('/Users/ernest/Documents/GitHub/portfolio-predictions/flask_backend/api/amzn.csv')
# df = df[['Date', 'Close']]

def build_model():
  model = Sequential([layers.Input((3, 1)),
                      layers.LSTM(64),
                      layers.Dense(32, activation='relu'),
                      layers.Dense(32, activation='relu'),
                      layers.Dense(1)])

  model.compile(loss='mse', 
                optimizer=Adam(learning_rate=0.001),
                metrics=['mean_absolute_error'])

  return model


# print("input a stock symbol: ")
# x = input()

# model = build_model()

def train_model(x, loaded_model):
  url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+x+'&outputsize=full&apikey=DNWQMLFC43J1PHDI'
  r = requests.get(url)

  data = r.json()

  # for key in data['Time Series (Daily)']:
  #   print(key)
  # print(data)

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
          close.append(float(value["4. close"]))
          
      
      
      list_of_tuples = list(zip(dates, close))

      df = pd.DataFrame(list_of_tuples,
                    columns=['Date', 'Close']) 
      
      df= df.loc[::-1]
  # convert date from str to int
  def str_to_datetime(s):
    split = s.split('-')
    year = int(split[0])
    month = int(split[1])
    day = int(split[2])
    return datetime.datetime(year = year, month = month, day = day)

  def df_to_windowed_df(dataframe, first_date_str, last_date_str, n=3):
    first_date = str_to_datetime(first_date_str)
    last_date  = str_to_datetime(last_date_str)

    target_date = first_date
    
    dates = []
    X, Y = [], []

    last_time = False
    while True:
      df_subset = dataframe.loc[:target_date].tail(n+1)
      
      if len(df_subset) != n+1:
        print(f'Error: Window of size {n} is too large for date {target_date}')
        return

      values = df_subset['Close'].to_numpy()
      x, y = values[:-1], values[-1]

      dates.append(target_date)
      X.append(x)
      Y.append(y)

      next_week = dataframe.loc[target_date:target_date+datetime.timedelta(days=7)]
      next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
      next_date_str = next_datetime_str.split('T')[0]
      year_month_day = next_date_str.split('-')
      year, month, day = year_month_day
      next_date = datetime.datetime(day=int(day), month=int(month), year=int(year))
      
      if last_time:
        break
      
      target_date = next_date

      if target_date == last_date:
        last_time = True
      
    ret_df = pd.DataFrame({})
    ret_df['Target Date'] = dates
    
    X = np.array(X)
    for i in range(0, n):
      X[:, i]
      ret_df[f'Target-{n-i}'] = X[:, i]
    
    ret_df['Target'] = Y

    return ret_df 
  df['Date'] = df['Date'].apply(str_to_datetime)

  def windowed_df_to_date_X_y(windowed_dataframe):
    df_as_np = windowed_dataframe.to_numpy()

    dates = df_as_np[:, 0]

    middle_matrix = df_as_np[:, 1:-1]
    X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

    Y = df_as_np[:, -1]

    return dates, X.astype(np.float32), Y.astype(np.float32)

  df.index = df.pop('Date')

  plt.plot(df.index, df['Close'])


  windowed_df = df_to_windowed_df(df, '2022-03-3', '2023-04-05', n=3)

  dates, X, y = windowed_df_to_date_X_y(windowed_df)

  dates.shape, X.shape, y.shape

  q_80 = int(len(dates) * .8)
  q_90 = int(len(dates) * .9)

  dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]

  dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
  dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

  plt.plot(dates_train, y_train)
  plt.plot(dates_val, y_val)
  plt.plot(dates_test, y_test)

  plt.legend(['Train', 'Validation', 'Test'])


  # loaded_model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100)

  # print(loaded_model.evaluate(X_val, y_val))

  train_predictions = loaded_model.predict(X_train).flatten()


loaded_model = keras.models.load_model('trained_model.h5')
# famous_stocks = [
#     'FB',
#     'TSLA', 'NVDA', 'JPM']

print(train_model('AAPL', loaded_model))

def predict(input_data):
   predictions = loaded_model.predict(input_data)
   return predictions
   
# for stock_symbol in famous_stocks:
#     trained_model = train_model(stock_symbol, loaded_model)

# loaded_model.save('trained_model_after_further_training.h5')


# plt.plot(dates_train, train_predictions)
# plt.plot(dates_train, y_train)
# plt.legend(['Training Predictions', 'Training Observations'])

# val_predictions = model.predict(X_val).flatten()

# plt.plot(dates_val, val_predictions)
# plt.plot(dates_val, y_val)
# plt.legend(['Validation Predictions', 'Validation Observations'])

# test_predictions = model.predict(X_test).flatten()

# plt.plot(dates_test, test_predictions)
# plt.plot(dates_test, y_test)
# plt.legend(['Testing Predictions', 'Testing Observations'])

# recursive_predictions = []
# recursive_dates = np.concatenate([dates_val, dates_test])

# for target_date in recursive_dates:
#   last_window = deepcopy(X_train[-1])
#   next_prediction = model.predict(np.array([last_window])).flatten()
#   recursive_predictions.append(next_prediction)
#   last_window[-1] = next_prediction

# plt.plot(dates_train, train_predictions)
# plt.plot(dates_train, y_train)
# plt.plot(dates_val, val_predictions)
# plt.plot(dates_val, y_val)
# plt.plot(dates_test, test_predictions)
# plt.plot(dates_test, y_test)
# plt.plot(recursive_dates, recursive_predictions)
# plt.legend(['Training Predictions', 
#             'Training Observations',
#             'Validation Predictions', 
#             'Validation Observations',
#             'Testing Predictions', 
#             'Testing Observations',
#             'Recursive Predictions'])

# plt.show()