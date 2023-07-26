import json
import requests

def news_search(search):
    apikey = "4f2707d0900f3bb2f48391502b7652ff"
    url = f"https://gnews.io/api/v4/search?q={search}&lang=en&max=1&apikey={apikey}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP error status codes (4xx or 5xx)

        data = response.json()
        articles = data["articles"]
        return articles

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# print(news_search('AAPL'))