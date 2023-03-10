import json
import os
from function_orm import Session, Region, Requirements, Vacancy, Vacancyrequirements


def add_history():
    number_id = []
    permit = bool

    # Создаем курсор
    session = Session()

    if os.path.exists('conclusion.json'):
        with open('conclusion.json', 'r') as f:
            story = json.load(f)

    # записываем город
    revise = session.query(Region).filter(Region.city == story['area']).all()

    if not revise:
        session.add(Region(story['area']))

    # записываем вакансию
    kak_id = session.query(Region.id).filter(Region.city == story['area']).one_or_none()
    for i in kak_id:
        number_id.append(i)
        if not session.query(Vacancy).filter(Vacancy.name == story['keywords'], Vacancy.region_id == i).all():
            session.add(Vacancy(story['keywords'], i))
            permit = True
        else:
            permit = False

    for req in story['requirements']:
        check = session.query(Requirements).filter(Requirements.name == req[0]).all()
        if not check:
            session.add(Requirements(req[0]))

    # основная таблица
    if permit == True:
        vacancy_id = session.query(Vacancy.id).filter(Vacancy.name == story['keywords'],
                                                      Vacancy.region_id == number_id[0]).one_or_none()

        for id in vacancy_id:
            for req in story['requirements']:
                vacancyrequirements_id = session.query(Requirements.id).filter(
                    Requirements.name == req[0]).one_or_none()
                for a in vacancyrequirements_id:
                    session.add(Vacancyrequirements(id, a))

    number_id.clear()
    session.commit()


def show_history():
    session = Session()

    res_history = session.query(Region, Vacancy).filter(Region.id == Vacancy.region_id).all()
    return res_history


def dell_history():
    session = Session()

    session.query(Vacancyrequirements).delete()
    session.query(Vacancy).delete()
    session.query(Requirements).delete()
    session.query(Region).delete()

    session.commit()
