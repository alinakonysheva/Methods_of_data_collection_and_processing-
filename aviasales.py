# Задание 1.
#  Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города,
#  а не по IATA коду. Пункт отправления и пункт назначения должны передаваться в качестве параметров.
# Сделать форматированный вывод, который содержит в себе пункт отправления, пункт назначения, дату вылета,
# цену билета (можно добавить еще другие параметры по желанию)
import requests
import sys


def search_tickets(city_depart, city_arrive):
    # получим из городов iata
    req_get_locations = requests.get(
        f"https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{city_depart}%20в%20{city_arrive}")
    locations = req_get_locations.json()

    flight_params = {
        'origin': locations['origin']['iata'],
        'destination': locations['destination']['iata'],
        'one_way': 'true'
    }
    req = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
    data = req.json()

    tickets = data['best_prices']
    for ticket in tickets:
        print('--------------------------------------------------------------')
        print(f'Пункт отправки: {city_depart}. Пункт назначения: {city_arrive}')
        print('Цена билета:')
        print(ticket['value'])
        print('Дата вылета:')
        print(ticket['depart_date'])
        print('Количество пересадок')
        print(ticket['number_of_changes'])
        print('--------------------------------------------------------------')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Пример использования программы: python aviasales.py Москва Амстердам')
    else:
        search_tickets(sys.argv[1], sys.argv[2])

