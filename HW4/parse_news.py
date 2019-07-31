#  1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
# *Заголовок
# *Краткое описание
# *Ссылка на новость

from bs4 import BeautifulSoup
import requests

url = 'https://news.yandex.ru/Moscow/index.html'


def request_to_site(page):
    try:
        request = requests.get(page)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def parse_page(page):
    html_doc = request_to_site(page)
    soup = BeautifulSoup(html_doc, 'html.parser')
    divs = soup.find_all('div', attrs={'class': "story"})

    for div in divs:
        section = div.find('a').text
        link = 'https://news.yandex.ru'+ div.findAll('a', attrs={'class': "link"})[1]['href']
        try:
            short_content = div.find('div', attrs={'class': "story__text"}).text
        except AttributeError:
            print('no preview')
        title = div.find('h2', attrs={'class': "story__title"}).text
        print(f'Cсылка на новость: {link}')
        print(f'Новостной раздел: {section}')
        print(f'Заголовок: {title}')
        print(f'Превью: {short_content}')
        print('-' * 100)


parse_page(url)
