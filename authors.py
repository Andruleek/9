import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання посилань на всі сторінки з цитатами
def get_all_pages():
    base_url = "http://quotes.toscrape.com"
    pages = [base_url]
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    while True:
        next_page = soup.find("li", class_="next")
        if next_page:
            next_page_link = next_page.find("a")['href']
            next_page_url = base_url + next_page_link
            pages.append(next_page_url)
            response = requests.get(next_page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            break
    return pages

# Функція для отримання інформації про авторів цитат
def get_authors(pages):
    authors_info = {}
    for page in pages:
        response = requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all("div", class_="quote")
        for quote in quotes:
            author_name = quote.find("small", class_="author").text
            author_url = quote.find("a")['href']
            if author_name not in authors_info:
                authors_info[author_name] = author_url
    return authors_info

# Функція для збереження інформації про авторів у файл JSON
def save_authors_to_json(authors_info):
    with open('authors.json', 'w') as f:
        json.dump(authors_info, f, indent=4)

# Отримуємо посилання на всі сторінки з цитатами
pages = get_all_pages()

# Отримуємо інформацію про авторів
authors_info = get_authors(pages)

# Зберігаємо інформацію про авторів у файл JSON
save_authors_to_json(authors_info)
