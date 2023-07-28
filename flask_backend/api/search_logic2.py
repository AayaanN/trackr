import json
import urllib.request
#-----------------------------------------------------------------------------------------------------

def news_search(search):
    apikey = "4f2707d0900f3bb2f48391502b7652ff"
    url = f"https://gnews.io/api/v4/search?q={search}&lang=en&max=1&apikey={apikey}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        # print(articles)

        return articles

        # for i in range(len(articles)):
        #     # articles[i].title
        #     print(f"Title: {articles[i]['title']}")
        #     # articles[i].description
        #     print(f"Description: {articles[i]['description']}")
        #     print(f"Description: {articles[i]['url']}")
        #     break

# news(input())

print(news_search('aapl'))