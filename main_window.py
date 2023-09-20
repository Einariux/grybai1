import PySimpleGUI as sg
from sqlalchemy import create_engine, Table, Column
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import OperationalError

# Duomenų bazės inicializacija
try:
    db_engine = create_engine('sqlite:///grybai.db')
    Base = declarative_base()
    session = sessionmaker(db_engine)()
except OperationalError as e:
    print('Nepavyko prisijungti prie db')
    print(e)

# Sukurkime Grybai, Vietoves ir Regionai klases
class Grybai(Base):
    __tablename__ = 'grybai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pavadinimas = Column(String(30))
    grybo_klase = Column(String(30))
    vietove_id = Column(Integer, ForeignKey('vietoves.id'))
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
    vietove_reg = Column(Integer, ForeignKey('vietoves.id'))
    vietove = relationship('Vietoves', back_populates='regionai')

Base.metadata.create_all(db_engine)

layout = [
    [sg.Text('Pavadinimas:'), sg.InputText(key='-PAVADINIMAS-')],
    [sg.Text('Grybo klasė:'), sg.InputText(key='-KLASE-')],
    [sg.Text('Vietovė ID:'), sg.InputText(key='-VIETOVE_ID-')],
    [sg.Button('Įterpti'), sg.Button('Atnaujinti'), sg.Button('Ištrinti')],
    [sg.Output(size=(50, 10))]
]

window = sg.Window('Grybai Duomenų Bazė', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Įterpti':
        try:
            pavadinimas = values['-PAVADINIMAS-']
            klase = values['-KLASE-']
            vietove_id = int(values['-VIETOVE_ID-'])

            # Sukurkite naują Grybai įrašą ir pridėkite jį į duomenų bazę
            grybas = Grybai(pavadinimas=pavadinimas, grybo_klase=klase, vietove_id=vietove_id)
            session.add(grybas)
            session.commit()
            print('Įterpimas sėkmingas!')
        except Exception as e:
            print('Klaida įterpiant įrašą:')
            print(e)

    elif event == 'Atnaujinti':
        try:
            pavadinimas = values['-PAVADINIMAS-']
            klase = values['-KLASE-']
            vietove_id = int(values['-VIETOVE_ID-'])

            # Atnaujinkite Grybai įrašą
            grybas = session.query(Grybai).filter_by(id=1).first()  # Pakeiskite filtravimo sąlygą pagal poreikį
            if grybas:
                grybas.pavadinimas = pavadinimas
                grybas.grybo_klase = klase
                grybas.vietove_id = vietove_id
                session.commit()
                print('Atnaujinimas sėkmingas!')
            else:
                print('Nerastas įrašas su nurodytu ID.')
        except Exception as e:
            print('Klaida atnaujinant įrašą:')
            print(e)

    elif event == 'Ištrinti':
        try:
            # Ištrinkite Grybai įrašą pagal ID
            grybas = session.query(Grybai).filter_by(id=1).first()  # Pakeiskite filtravimo sąlygą pagal poreikį
            if grybas:
                session.delete(grybas)
                session.commit()
                print('Ištrinimas sėkmingas!')
            else:
                print('Nerastas įrašas su nurodytu ID.')
        except Exception as e:
            print('Klaida ištrinant įrašą:')
            print(e)

window.close()
