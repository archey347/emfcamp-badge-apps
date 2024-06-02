import requests


def GetMessage():
    url = "https://archbar.me/scrapbook/badge/data.txt"

    response = requests.get(url)
    return response.text