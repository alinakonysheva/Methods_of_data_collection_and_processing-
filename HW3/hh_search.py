import requests
from lxml import html
import lxml.etree as etree

url = 'https://hh.ru/search/vacancy'
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def search_to_site(vacancy, page_number):
    session = requests.Session()

    try:
        request = session.get(url, headers=headers,
                              params={'text': vacancy, 'page': page_number
                                      })
        root = html.fromstring(request.text)
        results_list = root.xpath(
            "//div[@class='vacancy-serp-item__row vacancy-serp-item__row_header']")

        if results_list:
            for i in results_list:
                vacancy_info = html.fromstring(etree.tostring(i))
                vacancy_link = vacancy_info.xpath("string(//div[1]/a/@href)")
                vacancy_name = vacancy_info.xpath("string(//div[1]/a)")
                vacancy_salary = vacancy_info.xpath("string(//div[@class='vacancy-serp-item__compensation'])")
                print(vacancy_link)
                print(vacancy_name)
                print(vacancy_salary)
                print('---')

        else:
            print("At your request no results were found. Please, check your request.")

    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)


if __name__ == '__main__':
    my_str = input('Please, enter your vacancy here: ')
    page_numbers = int(input('Please, enter how many pages you would like to fetch: '))
    for page_number in range(page_numbers):
        search_to_site(my_str, page_number)
