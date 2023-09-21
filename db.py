from sqlalchemy import create_engine, Column
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

    
class Grybai(Base):
    __tablename__ = 'grybai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(30))
    grybo_klase = Column(String(30))
    vietove_id = Column(Integer, ForeignKey('vietoves.id'))
    vietoves = relationship('Vietoves', back_populates='grybai')

    def __repr__(self):
        return f'{self.id}, {self.pavadinimas}, {self.grybo_klase}'
    

class Vietoves(Base):
    __tablename__ = 'vietoves'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vietoves_pavadinimas = Column(String(50))
    regionai = relationship('Regionai', back_populates='vietove')
    grybai = relationship('Grybai', back_populates='vietoves')

    def __repr__(self):
        return f'{self.vietoves_pavadinimas}'
    

class Regionai(Base):
    __tablename__ = 'regionai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    regionas = Column(String(50))
    vietove_reg = Column(Integer, ForeignKey('vietoves.id'))
    vietove = relationship('Vietoves', back_populates='regionai')

    def __repr__(self):
        return f'{self.regionas}'
    
    
Base.metadata.create_all(db_engine)
