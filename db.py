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
    Column('vietoves_id', Integer, ForeignKey('vietoves.id')),
    Column('grybai_id', Integer, ForeignKey('grybai.id')),
)

class Regionai(Base):
    __tablename__ = 'regionai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(50))
    vietoves = relationship('Vietoves', back_populates='regionai')
    
    def __repr__(self):
        return f'{self.pavadinimas}'

class Grybai(Base):
    __tablename__ = 'grybai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(50))
    klase = Column(String(50))
    vietove_id = Column(Integer, ForeignKey('vietoves.id'))
    vietove = relationship('Vietoves', secondary=table_vietoves_grybai, back_populates='grybai') #many to many
    
    def __repr__(self):
        return f'{self.id}, {self.pavadinimas}, {self.klase}'

class Vietoves(Base):
    __tablename__ = 'vietoves'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(50))
    regionai_id = Column(Integer, ForeignKey('regionai.id'))
    regionai = relationship('Regionai', back_populates='vietoves') #one to many
    grybai_id = Column(Integer, ForeignKey('grybai.id'))
    grybai = relationship('Grybai', secondary=table_vietoves_grybai, back_populates='vietove') #many to many

    def __repr__(self):
        return f'{self.pavadinimas}'

Base.metadata.create_all(db_engine)

