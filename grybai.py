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
    vietove_id = Column(Integer, ForeignKey('vietove_id'))
    vietoves = relationship('Vietoves', back_populates='grybai')

class Vietoves(Base):
    __tablename__ = 'vietoves'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vietoves_pavadinimas = Column(String(50))
    grybai = relationship('Grybai', back_populates='vietoves')

class Regionai(Base):
    __tablename__ = 'regionai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    regionas = Column(String(50))
    vietove_reg = Column(Integer, ForeignKey='vietoves.id')
    vietove = relationship('Vietoves', back_populates='regionai')

Base.metadata.create_all(db_engine)


def main_window():
    pass

def add_region():
    pass

def add_location():
    pass

def add_mushroom():
    pass
