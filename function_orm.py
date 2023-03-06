from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///hh_orm.sql', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    city = Column(String, unique=True)

    def __init__(self, city):
        self.city = city


class Requirements(Base):
    __tablename__ = 'requirements'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    region_id = Column(Integer, ForeignKey('region.id'))

    def __init__(self, name, region_id):
        self.name = name
        self.region_id = region_id


class Vacancyrequirements(Base):
    __tablename__ = 'vacancyrequirements'
    id = Column(Integer, primary_key=True)
    vacancy_id = Column(Integer, ForeignKey('vacancy.id'))
    requirements_id = Column(Integer, ForeignKey('requirements.id'))

    def __init__(self, vacancy_id, requirements_id):
        self.vacancy_id = vacancy_id
        self.requirements_id = requirements_id


Base.metadata.create_all(engine)  # создать таблицы
