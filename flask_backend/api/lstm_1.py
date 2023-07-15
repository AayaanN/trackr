from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import pandas as pd
# import pandas_market_calendars as mcal
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from copy import deepcopy
import requests
import json
import array
import pytz
# import holidays


# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+x+'&outputsize=full&apikey=JU7L288S6R939NEC'

# returns df of last 300 valid days of the stock dataset
def file_parse(data):
    with open( "data_file.json" , "w" ) as write:
        json.dump( data["Time Series (Daily)"] , write )

    with open("data_file.json", "r") as read_content:
        stock_dict = json.load(read_content)
        dates = []
        dates_keys = stock_dict.keys()
        for key in dates_keys:
            dates.append(key)
        val = stock_dict.values()
        close = []

        for value in val:
            close.append(float(value["5. adjusted close"]))
            
        
        
        list_of_tuples = list(zip(dates, close))

        df = pd.DataFrame(list_of_tuples,
                    columns=['Date', 'Close']) 
    
        df= df.loc[::-1]

        for index in df.index:
            if index > 300:
                df.drop([index], inplace = True)

        return(df)
    
def file_parse_all(data):
    with open( "data_file.json" , "w" ) as write:
        json.dump( data["Time Series (Daily)"] , write )

    with open("data_file.json", "r") as read_content:
        stock_dict = json.load(read_content)
        dates = []
        dates_keys = stock_dict.keys()
        for key in dates_keys:
            dates.append(key)
        val = stock_dict.values()
        close = []

        for value in val:
            close.append(float(value["5. adjusted close"]))
            
        
        
        list_of_tuples = list(zip(dates, close))

        df = pd.DataFrame(list_of_tuples,
                    columns=['Date', 'Close']) 
    
        df= df.loc[::-1]


        return(df)

# converts string to datetime format
def str_to_datetime(s):
  split = s.split('-')
  year = int(split[0])
  month = int(split[1])
  day = int(split[2])
  return datetime(year = year, month = month, day = day)

# returns df that has 3 dates to be used to predicted using LSTM
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

    next_week = dataframe.loc[target_date:target_date+timedelta(days=7)]
    next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
    next_date_str = next_datetime_str.split('T')[0]
    year_month_day = next_date_str.split('-')
    year, month, day = year_month_day
    next_date = datetime(day=int(day), month=int(month), year=int(year))
    
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

def windowed_df_to_date_X_y(windowed_dataframe):
  df_as_np = windowed_dataframe.to_numpy()

  dates = df_as_np[:, 0]

  middle_matrix = df_as_np[:, 1:-1]
  X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

  Y = df_as_np[:, -1]

  return dates, X.astype(np.float32), Y.astype(np.float32)

def is_stock_opening_day(date):
    nyse = mcal.get_calendar('NYSE')
    schedule = nyse.schedule(start_date=date, end_date=date)
    return len(schedule) > 0

def find_next_day(today):
    tmr = today + timedelta(days = 1)
    is_opening_day = is_stock_opening_day(tmr)
    if is_opening_day == False:
      find_next_day(tmr)
    
    return tmr

    # tz = pytz.timezone('US/Eastern')
    # us_holidays = holidays.US()
    # if 


def number_of_days_display(days, df):
   if days == "Max" or "max":
      return df
   elif days == "5D":
      return df.tail(5)
   elif days =="1M":
      return df.tail(30)
   elif days =="1Y":
      return df.tail(365)
   elif days =="5Y":
      return df.tail(1,825)
      

def lstm_main():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AMZN&outputsize=full&apikey=JU7L288S6R939NEC'
    r = requests.get(url)

    data = r.json()
    df = file_parse(data)

    df_backup = file_parse_all(data)

    start = (df['Date'].iloc[3])
    end = (df['Date'].iloc[-1])

    df['Date'] = df['Date'].apply(str_to_datetime)
    df.index = df.pop('Date')

    windowed_df = df_to_windowed_df(df, start, end, n=3)

    dates, X, y = windowed_df_to_date_X_y(windowed_df)

    dates.shape, X.shape, y.shape

    q_80 = int(len(dates) * .8)
    q_90 = int(len(dates) * .9)

    dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]
    dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
    dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

    model = Sequential([layers.Input((3, 1)),
                    layers.LSTM(64),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(1)])
    
    model.compile(loss='mse', 
              optimizer=Adam(learning_rate=0.001),
              metrics=['mean_absolute_error'])

    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100)

    train_predictions = model.predict(X_train).flatten()
    val_predictions = model.predict(X_val).flatten()
    test_predictions = model.predict(X_test).flatten()

    add = X_test[-1][-3:-1]
    add = add.tolist()
    add.append([y_test[-1]])

    X_test = X_test.tolist()
    X_test.append(add)
    X_test = np.array(X_test)

    dates_test = dates_test.tolist()

    today = datetime.now().date()
    # next_day = find_next_day(today)
    next_day = today + timedelta(days = 1)
    next_day = next_day.strftime('%Y-%m-%dT00:00:00')
    dates_test.append(pd.Timestamp(next_day))
    dates_test= np.array(dates_test)

    test_predictions = model.predict(X_test).flatten()
    y_test = y_test.tolist()
    y_test.append(test_predictions[-1])
    y_test = np.array(y_test)

    dates_full = dates_train.tolist() + dates_val.tolist() + dates_test.tolist()

    value_full = y_train.tolist() + y_val.tolist() + y_test.tolist()

    full_graph = {}
    for i in dates_full:
       for j in value_full:
          full_graph[i] = j

    before = number_of_days_display("1M", df_backup)

    # before = before.tolist()
    # before.append(y_test[-1])
    # before = np.array(before)

    return y_test[-1]


    # print(full_graph)



lstm_main()