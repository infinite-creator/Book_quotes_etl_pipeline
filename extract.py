import requests 
from bs4 import BeautifulSoup

BASE_URL = 'https://quotes.toscrape.com/page/{}/'

def extract_quotes(page):
    url = BASE_URL.format(page)
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    
    soup = BeautifulSoup(response.text, "html.parser")
    quote_blocks = soup.find_all("div", class_="quote")
    
    quotes = []
    for quote in quote_blocks:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        
        quotes.append({
            "quote": text,
            "author": author,
            "tags": tags
        })
    return quotes   

def extract_all_quotes() -> list[dict]:
    all_quotes = []
    page = 1
    
    while True:
        quotes = extract_quotes(page)
        if not quotes:  # If no quotes are found, we've reached the end
            break
        all_quotes.extend(quotes)
        page += 1
    
    return all_quotes
