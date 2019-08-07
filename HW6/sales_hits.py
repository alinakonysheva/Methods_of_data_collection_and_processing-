#  Написать программу, которая собирает «Хиты продаж» с сайтов техники mvideo, onlinetrade и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

import json
import pprint

import pymongo
from pymongo import UpdateOne
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time


def get_db_collection():
    client = pymongo.MongoClient(
        "mongodb://falja:123456123456@mflix-shard-00-00-kou0j.mongodb.net:27017,mflix-shard-00-01-kou0j.mongodb.net:27017,mflix-shard-00-02-kou0j.mongodb.net:27017/test?ssl=true&replicaSet=mflix-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client['ai']
    return db.hits


driver = webdriver.Chrome()
driver.get('https://www.mvideo.ru/')
assert 'М.Видео' in driver.title

time.sleep(2)

element = driver.find_element_by_xpath('/html/body/div/div/div[1]')
actions = ActionChains(driver)
actions.move_to_element(element).click().perform()

buttons = driver.find_elements_by_class_name('sel-hits-button-next')
driver.execute_script("arguments[0].scrollIntoView();", buttons[1])

time.sleep(2)

for _ in range(0, 5):
    driver.execute_script("arguments[0].click();", buttons[1])
    time.sleep(3)

elements = driver.find_elements_by_class_name('sel-product-tile-title')
keys_to_store = ['productCategoryName', 'productName', 'productPriceLocal', 'productVendorName', 'productId']
update_list = []
for element in elements[:19]:
    to_db = {key: value for key, value in json.loads(element.get_attribute('data-product-info')).items() if
             key in keys_to_store}

    update_list.append(UpdateOne({"id": to_db['productId']}, {"$set": to_db}, upsert=True))
hits = get_db_collection()
print(hits.bulk_write(update_list).bulk_api_result)
pprint.pprint(hits.find_one())
driver.quit()
