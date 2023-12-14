import requests
import json


def get_quote():
    r = requests.get("https://api.quotable.io/quotes/random?tags=motivational|failure")
    data = json.loads(r.content)
    quote_dict = data[0]
    return quote_dict["content"], quote_dict["author"]
