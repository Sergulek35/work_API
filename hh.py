import pprint
from collections import Counter
import requests
from pycbrf import ExchangeRates
import time
from time import monotonic
import json


area_code = requests.get('https://api.hh.ru/areas/113').json()
area = {}

for dict in area_code['areas']:
    area[dict['name'].lower()] = dict['id']
    for i in dict['areas']:
        area[i['name'].lower()] = i['id']


def hh_parce(vykansiya, area_persons, time_persons):
    # Готовим переменные
    total_vacancies = 0
    salary = [[], []]
    wages = {'from': 0, 'to': 0}
    result = []
    schedule = []

    # поиск городов
    url = 'https://api.hh.ru/vacancies'
    rate = ExchangeRates()

    params = {'text': vykansiya, 'area': area[area_persons]}

    information = requests.get(url, params=params).json()

    pages = information['pages']

    # итоговый вывод сюда
    conclusion = {'keywords': vykansiya.capitalize(),
                  'count': 0,
                  'area': area_persons.capitalize(),
                  'requirements': [],
                  'salary': wages,
                  'schedule': []
                  }

    t = monotonic()
    for page in range(pages):

        if monotonic() - t > time_persons:  # Если загрузка больше введенных секунд
            break
        # if page > 5:
        #     break

        params = {'text': vykansiya, 'area': area[area_persons], 'page': page}
        information = requests.get(url, params=params).json()
        total_vacancies += len(information['items'])
        time.sleep(0.3)

        for inf in information['items']:
            # график работы
            schedule.append(inf['schedule']['name'])

            info = requests.get(inf['url']).json()
            # навыки
            for skill in info['key_skills']:
                result.append(skill['name'].lower())
            # зарплата
            if info['salary']:
                code = info['salary']['currency']
                if rate[code] is None:
                    code = 'RUR'
                k = 1 if code == 'RUR' else float(rate[code].value)  # С переводом валют, мне не очень понятно
                if info['salary']['from']:
                    salary[0].append(k * inf['salary']['from'])

                if info['salary']['to']:
                    salary[1].append(k * inf['salary']['to'])

    # print(result)
    wages['from'] = (int((sum(salary[0])) / len(salary[0])))
    wages['to'] = (int((sum(salary[1])) / len(salary[1])))
    conclusion['count'] = total_vacancies

    # pprint.pprint(information['items'])

    meter = Counter(result)
    for i in meter.most_common(5):
        conclusion['requirements'].append(i)

    schedule_count = Counter(schedule)
    for i in schedule_count.most_common(4):
        conclusion['schedule'].append(i)

    with open('conclusion.json', 'w') as f:
        json.dump(conclusion, f)


    return conclusion


if __name__ == '__main__':
    try:
        vykansiya = input('Введите вакансию : ')
        area_persons = input('Введите город для поиска: ').lower()
        time_persons = int(input('Введите максимальное время для загрузки в секундах: '))
        pprint.pprint(hh_parce(vykansiya, area_persons, time_persons))

    except ZeroDivisionError:
        print('Вакансий не найдено')
    except KeyError:
        print('Город не найден')
    except ValueError:
        print('Нужно ввести кол-во секунд!')
