import requests 
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/page/1/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("div", "quote")

for quote in quotes:
    text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text
    print(f"{text} - {author}")
