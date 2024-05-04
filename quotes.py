import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання даних про цитати зі сторінки
def scrape_quotes(page_url):
    quotes = []
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes.append({'text': text, 'author': author, 'tags': tags})
    return quotes

# Функція для скрапінгу всіх сторінок та збереження даних у файл quotes.json
def scrape_all_pages(base_url, num_pages):
    all_quotes = []
    for page_num in range(1, num_pages + 1):
        page_url = f"{base_url}/page/{page_num}/"
        all_quotes.extend(scrape_quotes(page_url))
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=4)

# Основна функція
def main():
    base_url = 'http://quotes.toscrape.com'
    num_pages = 10  # Загальна кількість сторінок для скрапінгу (10 сторінок на сайті)
    scrape_all_pages(base_url, num_pages)


if __name__ == "__main__":
    main()
