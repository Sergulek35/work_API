import json
import pprint
from collections import Counter
import requests
from pycbrf import ExchangeRates

url = 'https://api.hh.ru/vacancies'
rate = ExchangeRates()

# Вводим вакансию
text = input('Введите вакансию : ')

params = {'text': text, 'area': 1}

information = requests.get(url, params=params).json()

pages = information['pages']

# Готовим переменные
total_vacancies = 0
salary = [[], []]
wages = {'from': 0, 'to': 0}
result = []
schedule = []

# итоговый вывод сюда
conclusion = {'keywords': text,
              'count': 0,
              'requirements': [],
              'salary': wages,
              'schedule': []
              }
print('Идёт загрузка', information['found'], 'вакансий в Москве....')
# Проходим по страницам
for page in range(pages):
    # if page > 10:
    #     break

    # Поиск только в Москве, для упрощения
    params = {'text': text, 'area': 1, 'page': page}
    information = requests.get(url, params=params).json()
    total_vacancies += len(information['items'])

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
for i in meter.most_common(7):
    conclusion['requirements'].append(i)

schedule_count = Counter(schedule)
for i in schedule_count.most_common():
    conclusion['schedule'].append(i)

pprint.pprint(conclusion)

# print(information['found'])
# сохраняем в файл
with open('conclusion.json', 'w') as f:
    json.dump(conclusion, f)
