import sqlite3
import json
import os


def add_history():
    number_id = []
    permit = bool
    # Подключение к базе данных
    conn = sqlite3.connect('hh.sql')

    # Создаем курсор
    cursor = conn.cursor()

    if os.path.exists('conclusion.json'):
        with open('conclusion.json', 'r') as f:
            story = json.load(f)

    # записываем город
    revise = cursor.execute('select * from region where city = ?', [story['area']])
    if not revise.fetchone():
        cursor.execute("insert into region (city) values (?)", [story['area']])

    # записываем вакансию
    kak_id = cursor.execute('select id from region where city = ?', [story['area']])

    for i in kak_id.fetchone():
        number_id.append(i)
        if not cursor.execute('select * from vacancy where name = ? and region_id = ?', [story['keywords'], i]).fetchone():
            cursor.execute("insert into vacancy (name, region_id) VALUES (?, ?)", [story['keywords'], i])
            permit = True
        else:
            permit = False
    # записываем навыки
    for req in story['requirements']:

        revise = cursor.execute('select * from requirements where name = ?', [req[0]])
        if not revise.fetchone():
            cursor.execute("insert into requirements (name) values (?)", [req[0]])

    # основная таблица
    if permit == True:
        vacancy_id = cursor.execute('select id from vacancy where name = ? and region_id = ?',
                                    [story['keywords'], number_id[0]])

        for id in vacancy_id.fetchone():
            for req in story['requirements']:
                vacancyrequirements_id = cursor.execute('select id from requirements where name = ?', [req[0]])
                for a in vacancyrequirements_id.fetchone():
                    cursor.execute("insert into vacancyrequirements (vacancy_id, requirements_id) VALUES (?, ?)", [id, a])

    number_id.clear()

    conn.commit()


def show_history():
    conn = sqlite3.connect('hh.sql')
    cursor = conn.cursor()
    illation = 'select vr.id, v.name, r.city, req.name from vacancy v, region r, requirements req, vacancyrequirements ' \
                'vr  where vr.vacancy_id = v.id and vr.requirements_id = req.id and v.region_id = r.id'

    res_history = cursor.execute(illation).fetchall()
    return res_history

def dell_history():
    conn = sqlite3.connect('hh.sql')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM vacancyrequirements')
    cursor.execute('DELETE FROM vacancy')
    cursor.execute('DELETE FROM requirements')
    cursor.execute('DELETE FROM region')
    conn.commit()