import PySimpleGUI as sg
from sqlalchemy import create_engine, Table, Column
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


def main_window(): # Einaras
    pass

def add_region(): # Deivida
    pass

# Lukas
def add_location(session): 
    #pasiimti regionus is db
    regions = session.query(Regionai).all()
    #regionu dropDown
    regionu_pavadinimai = [regionas.regionas for regionas in regions]

    layout = [
        [sg.Text('Iveskite vietoves pavadinima: ', size=20), sg.InputText(key='-PAVADINIMAS-')],
        [sg.Text('Pasirinkite regiona: ', size=20), sg.Combo(regionu_pavadinimai, key='-REGIONAI-')],
        [sg.Button('Prideti', key='-PRIDETI-')],
    ]
    window = sg.Window('Naujos Vietoves Ivedimas', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-PRIDETI-':
            vietoves_pavadinimas = values['-PAVADINIMAS-']
            pasirinktas_regionas = values['-REGIONAI-']

            #pasiimti pasirinkta regiona (dropdown)
            pasirinktas_regionas = next((regionas for regionas in regions if regionas.regionas == pasirinktas_regionas), None)
        
        if vietoves_pavadinimas:
            nauja_vietove = Vietoves(vietoves_pavadinimas=vietoves_pavadinimas)
            session.add(nauja_vietove)
            session.commit()
            sg.popup(f'Vietove: {vietoves_pavadinimas} Sekmingai prideta')
            break
        else:
            sg.popup('Visi laukai turi buti uzpildyti')

def remove_location(session):
    vietoves = session.query(Vietoves).all()
    #vietoves dropDown
    vietove = [vietove.vietoves for vietove in vietoves]
    
    layout = [
        [sg.Text('Pasirinkite vietove: ', size=20), sg.Combo(vietove, key='-VIETOVES-', size=(10,10))],
        [sg.Listbox(values=vietoves, size=(15,8), key='-VISOS-VIETOVES-', enable_events=True)],
        [sg.Button('Istrinti', key='-ISTRINTI-')],
    ]
    window = sg.Window('Vietoves pasalinimas', layout, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-ISTRINTI-':
            pasirinkta_vietove = values['-VIETOVES-']
            if pasirinkta_vietove:
                pasirinkta_vietove_pavadinimas = pasirinkta_vietove[0]
                trinti_vietove = next((vietove for vietove in vietoves if vietove.vietoves == pasirinkta_vietove_pavadinimas), None)
                session.delete(trinti_vietove)
                session.comit()
                sg.popup(f'Vietove {pasirinkta_vietove_pavadinimas} sekmingai istrinta')
        else:
            sg.popup('Pasirinkite vietove, kuria norite istrinti')


def add_mushroom(): # Vytautas 
    pass


if __name__ == '__main__':
    session = Session()
    add_location(session)
    remove_location(session)
    