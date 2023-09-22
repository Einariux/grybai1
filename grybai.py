import PySimpleGUI as sg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Grybai, Vietoves, Regionai


db_engine = create_engine("sqlite:///grybai.db")
Session = sessionmaker(db_engine)
session = Session()


def main_window():  # Einaras
    pass


def add_region(session):  # Deivida
    layout = [
        [
            sg.Text("Įveskite regiono pavadinimą: ", size=20),
            sg.InputText(key="-REGIONO-PAVADINIMAS-"),
        ],
        [sg.Button("Pridėti", key="-PRIDETI-")],
    ]
    window = sg.Window("Naujo regiono įvedimas", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-PRIDETI-":
            regiono_pavadinimas = values["-REGIONO-PAVADINIMAS-"]
            if regiono_pavadinimas:
                naujas_regionas = Regionai(pavadinimas=regiono_pavadinimas)
                session.add(naujas_regionas)
                session.commit()
                sg.popup(f"Regionas: {regiono_pavadinimas} sėkmingai pridėtas")
                break
            else:
                sg.popup("Regiono pavadinimas negali būti tuščias")
   
   
# Lukas
def perziureti_grybus(session):
    regions = session.query(Regionai).all()
    regionu_pavadinimai = [regionas.pavadinimas for regionas in regions]

    layout = [
        [sg.Text('Pasirinkite regiona: '), sg.Combo(regionu_pavadinimai, key='-REGIONAI-', size=(20, 1))],
        [sg.Text('Pasirinkite vietove: '), sg.Combo([], key='-VIETOVES-', size=(20, 1))],
        [sg.Multiline(key='-GRYBAI-', size=(40, 10))],
        [sg.Button('Uzdaryti', key='-UZDARYTI-')]
    ]
    window = sg.Window('Grybu perziura', layout, finalize=False)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == '-UZDARYTI-':
            break
        
        pasirinktas_regionas = values['-REGIONAI-']
        #debug
        print("pasirinktas regionas:", pasirinktas_regionas) 
        pasirinktas_regionas_objektas = next((region for region in regions if region.pavadinimas == pasirinktas_regionas), None)
        
        if pasirinktas_regionas_objektas:
            vietoves_pagal_regiona = [vietove.pavadinimas for vietove in pasirinktas_regionas_objektas.vietoves]
            #debug
            print("pasirinkto regiono vietoves:", vietoves_pagal_regiona)
            window['-VIETOVES-'].update(values=vietoves_pagal_regiona)
        else:
            window['-VIETOVES-'].update(values=[])
        #gaunam pasirinkta vietove
        pasirinkta_vietove = values['-VIETOVES-']

        if pasirinktas_regionas_objektas and pasirinkta_vietove:
            #grybai pagal pasirinkta regiona ir vietove
            grybai = session.query(Grybai).join(Vietoves).filter(
                Regionai.pavadinimas == pasirinktas_regionas,
                Vietoves.pavadinimas == pasirinkta_vietove
            ).all()
            #parodom visus grybus(multiline)
            visi_grybai = [f'{grybas.pavadinimas}, {grybas.klase}' for grybas in grybai]
            window['-GRYBAI-'].update('\n'.join(visi_grybai))
        else:
            window['-GRYBAI-'].update(values='')

def view_locations(session):
    regions = session.query(Regionai).all()
    regionu_pavadinimai = [regionas.pavadinimas for regionas in regions]

    layout = [
        [sg.Text('Pasirinkite regiona: '), sg.Combo(regionu_pavadinimai, key='-REGIONAI-', size=15)],
        [sg.Button('Rodyti', key='-RODYTI-')],
        [sg.Multiline(key='-VIETOVES-', size=(30,10))],
        [sg.Button('Uzdaryti', key='-UZDARYTI-')],
    ]
    window = sg.Window('Vietoviu perziura', layout, finalize=False)
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == '-UZDARYTI-':
            break
        if event == '-RODYTI-':

            pasirinktas_regionas = values['-REGIONAI-']
            pasirinktas_regionas_objektas = next((region for region in regions if region.pavadinimas == pasirinktas_regionas), None)
            
        if pasirinktas_regionas_objektas:
            visos_vietoves = [vietove.pavadinimas for vietove in pasirinktas_regionas_objektas.vietoves]
            window['-VIETOVES-'].update('\n'.join(visos_vietoves))
        else:
            window['-VIETOVES-'].update('') 

    window.close()


def add_location(session):
    # pasiimti regionus is db
    regions = session.query(Regionai).all()
    # regionu dropDown
    regionu_pavadinimai = [regionas.pavadinimas for regionas in regions]

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

            # pasiimti pasirinkta regiona (dropdown)
            pasirinktas_regionas = next((regionas for regionas in regions if regionas.pavadinimas == pasirinktas_regionas),None,)

        if pasirinktas_regionas:
            nauja_vietove = Vietoves(pavadinimas=vietoves_pavadinimas, regionai=pasirinktas_regionas)
            session.add(nauja_vietove)
            session.commit()
            sg.popup(f'Vietove: {vietoves_pavadinimas} Sekmingai prideta')
            break
        else:
            sg.popup('Pasirinktas regionas nerastas')


def remove_location(session):
    vietoves = session.query(Vietoves).all()
    layout = [
        [sg.Text('Pasirinkite vietove trynimui: ', size=20)],
        [sg.Listbox(values=[v.pavadinimas for v in vietoves], size=(15, 8), key='-VISOS-VIETOVES-', enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
        [sg.Button('Istrinti', key='-ISTRINTI-')],
    ]
    window = sg.Window('Vietoves pasalinimas', layout, finalize=False)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-ISTRINTI-':
           pasirinkta_vietove_pavadinimas = values['-VISOS-VIETOVES-'][0]
           if pasirinkta_vietove_pavadinimas is not None:
               pasirinkta_vietove = next((v for v in vietoves if v.pavadinimas == pasirinkta_vietove_pavadinimas), None)
               if pasirinkta_vietove:
                   session.delete(pasirinkta_vietove)
                   session.commit()
                   sg.popup(f'Vietove {pasirinkta_vietove.pavadinimas} sekmingai pasalinta')
                   vietoves = session.query(Vietoves).all()
                   window['-VISOS-VIETOVES-'].update(values=[v.pavadinimas for v in vietoves])

def add_mushroom(session):
    grybai = session.query(Grybai).all()
    grybu_names = [grybas.pavadinimas for grybas in grybai]
    vietoves = session.query(Vietoves).all()
    vietoviu_pavadinimai = [vietove.pavadinimas for vietove in vietoves]
    layout = [
        [
            sg.Text('Įveskite Grybo Pavadinimą: ', size=20),
            sg.InputText(key='-PAVADINIMAS-'),
        ],
        [
            sg.Text('Įveskite Grybo Klasę: ', size=20),
            sg.InputText(key='-KLASE-'),
        ],
        [
            sg.Text('Pasirinkite Vietovę: ', size=20),
            sg.Combo(vietoviu_pavadinimai, key='-VIETOVES-'),
        ],
        [sg.Button('Pridėti Grybą', key='-PRIDETI-')],
    ]
    window = sg.Window('Naujas Grybas', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '-PRIDETI-':
            grybo_name = values['-PAVADINIMAS-']
            grybo_class = values['-KLASE-']
            grybo_location_name = values['-VIETOVES-']
            
            grybo_location = next((vietove for vietove in vietoves if vietove.pavadinimas == grybo_location_name), None)

            if grybo_location:
                naujas_grybas = Grybai(pavadinimas=grybo_name, klase=grybo_class, vietove=grybo_location)
                session.add(naujas_grybas)
                session.commit()
                sg.popup(f'Grybas: {grybo_name} Sėkmingai Pridėtas')
                break
            else:
                sg.popup('Vietovė nerasta!')


if __name__ == "__main__":
    session = Session()
    add_mushroom(session)
    add_region(session)
    add_location(session)
    remove_location(session)
    view_locations(session)
    perziureti_grybus(session)
