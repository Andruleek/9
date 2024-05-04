import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання даних про авторів
def scrape_authors():
    authors = {}
    page_num = 1
    while True:
        url = f'http://quotes.toscrape.com/page/{page_num}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        if not quotes:  # Якщо немає цитат, завершуємо цикл
            break
        for quote in quotes:
            author_name = quote.find('small', class_='author').text
            author_element = quote.find('span', class_='author')
            if author_element:  # Перевіряємо, чи є елемент автора
                author_url = author_element.find_next_sibling('a')
                if author_url:  # Перевіряємо, чи є посилання на автора
                    author_url = author_url['href']
                else:
                    author_url = None
                if author_name not in authors:
                    authors[author_name] = {'author_name': author_name, 'author_url': author_url}
        page_num += 1

    return list(authors.values())

# Отримання даних про авторів
authors_data = scrape_authors()

# Запис даних у файл authors.json
with open('authors.json', 'w') as file:
    json.dump(authors_data, file, indent=4)

print("Дані про авторів успішно записано у файл authors.json")
