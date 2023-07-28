import requests

name_data = 'AAPL'

api_key = ["DNWQMLFC43J1PHDI", "K62KTSJBG30692AL", 'OTKHLLKZ9SXFZUHP']



url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={name_data}&apikey={api_key[1]}'

response = requests.get(url)
data = response.json()

print(data)
