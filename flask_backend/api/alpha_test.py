import requests

name_data = 'AAPL'

api_key = ["DNWQMLFC43J1PHDI", "K62KTSJBG30692AL", 'OTKHLLKZ9SXFZUHP']



url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={name_data}&interval=5min&outputsize=full&apikey={api_key[0]}'
url2 = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={name_data}&apikey={api_key}"

response = requests.get(url2)
data = response.json()

for key in data:
    print(key)

print(data['Time Series (Daily)'])
