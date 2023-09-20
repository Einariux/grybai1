from sqlalchemy import create_engine, Table, Column
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import OperationalError


try:
    db_engine = create_engine('sqlite:///grybai.db')
    Base = declarative_base()
    session = sessionmaker(db_engine)
except OperationalError as e:
    print('Nepavyko prisijungti prie db')
    print(e)

    
class Grybai(Base):
    __tablename__ = 'grybai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(30))
    grybo_klase = Column(String(30))

class Vietoves(Base):
    __tablename__ = 'vietoves'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vietoves_pavadinimas = Column(String(50))

class Regionai(Base):
    __tablename__ = 'regionai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    regionas = Column(String(50))

Base.metadata.create_all(db_engine)