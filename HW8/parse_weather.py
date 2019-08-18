#
# Final project for the course "Methods of parsing and crawling in the internet"
#
# Task of the project: to check some web site if it is expected to be rainy.
# If so, to send a notification to email,
# e.g. "don't forget to take an umbrella with you tomorrow"

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = 'https://www.gismeteo.com/weather-hove-14897/tomorrow/'
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


# to check internet connection
def request_to_site(page):
    session = requests.Session()
    try:
        request = session.get(page, headers=headers)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


# to get information about precipitation
def parse_page(page):
    html_doc = request_to_site(page)
    soup = BeautifulSoup(html_doc, 'html.parser')
    div = soup.find('div', attrs={'class': "tabs _center"})
    tomorrow = list(div.children)[1]
    precipitation = tomorrow.find_next_sibling()['data-text']
    return precipitation


def is_rainy(page):
    precipitation = parse_page(page)
    regex = re.compile(r"rain")
    return bool(regex.search(precipitation))


def send_letter():
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
    time.sleep(10)
    elem = driver.find_elements_by_class_name(
        'control button2 button2_view_classic button2_size_l button2_theme_normal button2_width_max passp-form-button')
    if len(elem) > 0:
        elem[0].click()
        time.sleep(5)

    elem = driver.find_elements_by_link_text('Лёгкая версия')
    elem = elem[len(elem) - 1]
    elem.click()
    time.sleep(5)
    elem = driver.find_element_by_css_selector(
        'div.b-page:nth-child(2) div.b-layout div.b-layout__right form.b-form div.b-toolbar.b-toolbar_type_messages:nth-child(1) div.b-toolbar__i span.b-toolbar__col:nth-child(1) > a.b-toolbar__but')
    elem.click()
    time.sleep(5)
    elem = driver.find_element_by_xpath("//input[@name='to']")
    elem.send_keys('konysheva.alina@gmail.com')
    elem = driver.find_element_by_xpath("//input[@name='subj']")
    elem.send_keys('It is going to be rain tomorrow')
    elem = driver.find_element_by_xpath("//textarea[@name='send']")
    elem.send_keys('Do not forget your umbrella!')
    elem = driver.find_element_by_xpath("//input[@name='doit']")
    elem.click()
    time.sleep(5)


if is_rainy(url):
    print('It\'s going to be rain tomorrow, we\'ll send a notification')
    send_letter()
else:
    print('There is no rain expected')
