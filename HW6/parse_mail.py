# Задание 1
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
#  о письмах в базу данных (от кого, дата отправки, тема письма, текст письма)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymongo


def get_db_collection():
    client = pymongo.MongoClient(
        "mongodb://falja:123456123456@mflix-shard-00-00-kou0j.mongodb.net:27017,mflix-shard-00-01-kou0j.mongodb.net:27017,mflix-shard-00-02-kou0j.mongodb.net:27017/test?ssl=true&replicaSet=mflix-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client['ai']
    return db.mail


driver = webdriver.Chrome()
driver.get(
    'https://passport.yandex.ru/auth?from=mail&origin=hostroot_homer_auth_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fmail.yandex.ru%3Fnoretpath%3D1')
assert 'Авторизация' == driver.title

elem = driver.find_element_by_id("passp-field-login")
elem.send_keys('al.konysheva@ya.ru')
elem.send_keys(Keys.RETURN)
time.sleep(2)
elem = driver.find_element_by_id('passp-field-passwd')
elem.send_keys('Orwellthebest')
elem.send_keys(Keys.RETURN)
time.sleep(5)
elem = driver.find_elements_by_class_name(
    'control button2 button2_view_classic button2_size_l button2_theme_normal button2_width_max passp-form-button')
if len(elem) > 0:
    elem[0].click()
    time.sleep(5)

elem = driver.find_elements_by_link_text('Лёгкая версия')
elem = elem[len(elem) - 1]
elem.click()
time.sleep(5)
base_xpath = "//a[@class='b-messages__message__link']"
update_list = []
elem = driver.find_elements_by_xpath(base_xpath)

mails = get_db_collection()

for link in range(len(elem)):
    url = elem[link].get_attribute('href')
    driver.get(url)
    time.sleep(2)
    from_whom = driver.find_elements_by_xpath("//span[@class='b-message-head__person']")[0].text
    sending_date = driver.find_elements_by_xpath("//span[@class='b-message-head__date']")[0].text
    subject = driver.find_elements_by_xpath("//span[@class='b-message-head__subject-text']")[0].text
    content = driver.find_elements_by_xpath("//div[@class='b-message-body__content']")[0].text
    mail_data = {'from_whom': from_whom, 'link': url, 'sending_date': sending_date, 'subject': subject,
                 'content': content}
    mails.update_one({'link': url}, {"$setOnInsert": mail_data}, True)

    print(mail_data)

    driver.back()
    time.sleep(2)
    elem = driver.find_elements_by_xpath(base_xpath)

driver.quit()
