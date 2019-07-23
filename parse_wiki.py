# Задание 2.
# В приложении парсинга википедии получить первую ссылку на другую страницу и вывести все значимые слова из неё.
# Результат записать в файл в форматированном виде

import collections
import requests
import re


def return_wiki_html(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    return wiki_request.text


# возвратим первую ссылку со страницы (нулевая ссылка -- картинка)
def get_first_link(topic):
    wiki_html = return_wiki_html(topic)
    all_links = re.findall('(http\w+://.*)[\'\"]', wiki_html)
    return all_links[1]


def return_words(topic):
    first_link = get_first_link(topic)
    wiki_html = return_wiki_html(first_link)
    words = re.findall('[а-яА-Я]{3,}', wiki_html)
    words_counter = collections.Counter()
    f = open(f'content_first_link_from_page{topic}', 'w')
    for word in words:
        words_counter[word] += 1
    # Путь самыми значимыми словами будут первые 10 самых часто встречающихся слов
    for word in words_counter.most_common(10):
        f.write(f'Слово {word[0]} встречается {word[1]} раз' '\n')
    f.close()



print(return_words('сернистая кислота'))
