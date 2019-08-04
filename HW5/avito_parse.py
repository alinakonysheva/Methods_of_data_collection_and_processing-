# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные
# объявления с avito.ru в созданную БД (xpath/BS для парсинга на выбор)
# 2) Написать функцию, которая производит поиск и выводит на экран объявления с ценой меньше введенной суммы

import pymongo
import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/rossiya?q='


def request_to_site(url):
    try:
        request = requests.get(url)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


# to get lists of ads
def parse_page(search):
    list_doc_data = []
    html_doc = request_to_site(url + search)
    soup = BeautifulSoup(html_doc, 'html.parser')
    divs = soup.find_all('div', attrs={'data-marker': "item"})
    for div in divs:
        price = div.find('span', attrs={'class': "price"})['content']
        link = 'https://www.avito.ru/' + div.find('a', attrs={'class': "item-description-title-link"})['href']
        ad_id = div['data-item-id']
        doc_data = {'price': int(price), 'link': link, 'ad_id': int(ad_id)}
        list_doc_data.append(doc_data)
    return list_doc_data


# to add to db
def save_to_db(list_jsons):
    docs = get_db_collection()
    for adv in list_jsons:
        docs.update_one({'ad_id': adv['ad_id']}, {"$setOnInsert": adv}, True)


# to create db client  and return an object of a collection
def get_db_collection():
    client = pymongo.MongoClient(
        "mongodb://falja:123456123456@mflix-shard-00-00-kou0j.mongodb.net:27017,mflix-shard-00-01-kou0j.mongodb.net:27017,mflix-shard-00-02-kou0j.mongodb.net:27017/test?ssl=true&replicaSet=mflix-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client['ai']
    docs = db.docs
    return docs


# to look for objects with a price less than it was required

def db_search(max_price):
    docs = get_db_collection()
    for doc in docs.find({"price": {"$lt": max_price}}):
        print(doc['price'], doc['link'], doc['ad_id'])


if __name__ == '__main__':
    my_search = input('Please, enter your search here: ')
    my_price = int(input('Please, enter the highest price you can afford : '))
    save_to_db(parse_page(my_search))
    db_search(my_price)
