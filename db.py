from sqlalchemy import create_engine, Column, Table
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import OperationalError

try:
    db_engine = create_engine('sqlite:///grybai.db')
    Base = declarative_base()
    Session = sessionmaker(db_engine)
except OperationalError as e:
    print('Nepavyko prisijungti prie db')
    print(e)


Base = declarative_base()

table_vietoves_grybai = Table(
    'vietoves_grybai',
    Base.metadata,
    Column('vietove_id', Integer, ForeignKey('vietove.id')),
    Column('grybas_id', Integer, ForeignKey('grybas.id')),
)

class Regionas(Base):
    __tablename__ = 'regionas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(50))
    vietoves = relationship('Vietove', back_populates='regionas')
    
    def __repr__(self):
        return f'{self.pavadinimas}'

class Grybas(Base):
    __tablename__ = 'grybas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(50))
    klase = Column(String(50))
    vietoves = relationship('Vietove', secondary=table_vietoves_grybai, back_populates='grybai') 
    
    def __repr__(self):
        return f'{self.id}, {self.pavadinimas}, {self.klase}'

class Vietove(Base):
    __tablename__ = 'vietove'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(50))
    regionas_id = Column(Integer, ForeignKey('regionas.id'))
    regionas = relationship('Regionas', back_populates='vietoves')
    grybai = relationship('Grybas', secondary=table_vietoves_grybai, back_populates='vietoves') 

    def __repr__(self):
        return f'{self.pavadinimas}'

Base.metadata.create_all(db_engine)

