import logging
import requests
import time 
from bs4 import BeautifulSoup
from config import BASE_URL

def fetch_with_retries(url:str, retries:int = 3, delay:int = 2):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Check if the request was successful
            return response
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            
            if attempt < retries - 1:
                sleep_time = delay * (2 ** attempt)  # Exponential backoff
                logging.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                logging.error(f"All {retries} attempts failed for {url}.")
                return None

def extract_quotes(page):
    url = BASE_URL.format(page)
    
    response = fetch_with_retries(url)
    if not response:
        return []   

    soup = BeautifulSoup(response.text, "html.parser")
    quote_blocks = soup.find_all("div", class_="quote")
    
    quotes = []
    
    for quote in quote_blocks:
        try:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        except AttributeError as e:
            logging.warning(f"Skip malformed quote from page {page}: {e}")
            continue

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
