import requests

api_key = 'DNWQMLFC43J1PHDI'

url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BBBB&apikey={api_key}'

r = requests.get(url)
data = r.json()

stock = 'BBBB'

print(data['bestMatches'][0]['1. symbol'] == stock)
print(data['bestMatches'][0]['2. name'] == stock)