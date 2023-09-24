import PySimpleGUI as sg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Vietove, Regionas, Grybas
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


db_engine = create_engine("sqlite:///grybai.db")
Session = sessionmaker(db_engine)
session = Session()

def add_or_remove_region(session):
    regions = session.query(Regionas).all()
    region_names = [region.pavadinimas for region in regions]

    layout = [
        [
            sg.Text("Pasirinkite veiksmą:", size=(15, 1)),
            sg.Radio("Pridėti", "RADIO1", key="-ADD-", default=True, enable_events=True),
            sg.Radio("Ištrinti", "RADIO1", key="-REMOVE-", enable_events=True),
        ],
        [
            sg.Text("Regiono pavadinimas: ", size=(15, 1)),
            sg.InputText(key="-REGIONO-PAVADINIMAS-", disabled=False, size=(15,1)),
        ],
        [
            sg.Text("Pasirinkite regioną: ", size=(15, 1)),
            sg.Combo(region_names, key="-REGIONAI-", size=(15, 10), disabled=True),
        ],
        [sg.Button("Vykdyti", key="-VYKDYTI-")],
    ]
    window = sg.Window("Pridėti arba Ištrinti Regioną", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event in ("-ADD-", "-REMOVE-"):
            add_selected = values["-ADD-"]
            remove_selected = values["-REMOVE-"]

            if add_selected:
                window['-REGIONO-PAVADINIMAS-'].update(disabled=False)
                window['-REGIONAI-'].update(disabled=True)
            elif remove_selected:
                window['-REGIONO-PAVADINIMAS-'].update(disabled=True)
                window['-REGIONAI-'].update(disabled=False)

        if event == "-VYKDYTI-":
            add_selected = values["-ADD-"]
            remove_selected = values["-REMOVE-"]
            region_name = values["-REGIONO-PAVADINIMAS-"]
            selected_region_name = values["-REGIONAI-"]

            if add_selected:
                if region_name:
                    new_region = Regionas(pavadinimas=region_name)
                    session.add(new_region)
                    session.commit()
                    sg.popup(f"Regionas {region_name} pridėtas sėkmingai")
                    window["-REGIONO-PAVADINIMAS-"].update("")
                    regions = session.query(Regionas).all()
                    region_names = [region.pavadinimas for region in regions]
                    window["-REGIONAI-"].update(values=region_names)
                else:
                    sg.popup("Regiono pavadinimas negali būti tuščias")
            elif remove_selected:
                if selected_region_name:
                    region_to_delete = next(
                        (
                            region
                            for region in regions
                            if region.pavadinimas == selected_region_name
                        ),
                        None,
                    )
                    if region_to_delete:
                        session.delete(region_to_delete)
                        session.commit()
                        sg.popup(f"Regionas {selected_region_name} ištrintas sėkmingai")
                        regions = session.query(Regionas).all()
                        region_names = [region.pavadinimas for region in regions]
                        window["-REGIONAI-"].update(values=region_names)

    window.close()
# Lukas

def add_location(session):
    regionai = session.query(Regionas).all()

    layout = [
        [sg.Text('Pavadinima: ', size=(15, 1)), sg.Input(key='-VIETOVE-', size=(15, 1))],
        [sg.Text('Pasirinkite regiona: ', size=(15, 1)), sg.Combo(regionai, key='-REGIONAS-', size=(15, 1))],
        [sg.Button('Ivesti', key='-PRIDETI-')],
    ]
    window = sg.Window("Vietoves pridejimas", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "-PRIDETI-":
            if values["-REGIONAS-"] and len(values["-VIETOVE-"]) > 2:
                nauja_vietove = Vietove(pavadinimas=values["-VIETOVE-"], regionas=values["-REGIONAS-"])
                session.add(nauja_vietove)
                session.commit()
                sg.popup(f'Vietove {values["-VIETOVE-"]} sekmingai prideta')
                window['-VIETOVE-'].update('')
                window['-REGIONAS-'].update('')
            else:
                sg.popup("Pasirinktas regionas nerastas")

    window.close()


def vietoviu_perziura_trynimas(session):
    regionai = session.query(Regionas).all()
    layout = [
        [sg.Text('Pasirinkite regiona'), sg.Combo([regionas.pavadinimas for regionas in regionai], key='-REGIONAS-', enable_events=True)],
        [sg.Listbox(values=[], key='-VIETOVE-', size=(30, 10), enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
        [sg.Button('Prideti', key='-PRIDETI-'), sg.Button('Istrinti', key='-ISTRINTI-')]
    ]
    window = sg.Window("Vietoviu perziura", layout, finalize=False)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "-REGIONAS-":
            pasirinkto_regiono_pavadinimas = values["-REGIONAS-"]
            pasirinktas_regionas = None
            for region in regionai:
                if region.pavadinimas == pasirinkto_regiono_pavadinimas:
                    pasirinktas_regionas = region
                    break
            if pasirinktas_regionas:
                vietoves = [
                    vietove.pavadinimas for vietove in pasirinktas_regionas.vietoves
                ]
                window["-VIETOVE-"].update(values=vietoves)
            else:
                window["-VIETOVE-"].update(values=[])

        elif event == "-ISTRINTI-" and values["-VIETOVE-"]:
            selected_vietove = values["-VIETOVE-"]
            if selected_vietove:
                trinti_vietove = selected_vietove[0]
                pasirinkto_regiono_pavadinimas = values["-REGIONAS-"]
                pasirinktas_regionas = None
                for region in regionai:
                    if region.pavadinimas == pasirinkto_regiono_pavadinimas:
                        pasirinktas_regionas = region
                        break

                if pasirinktas_regionas:
                    for vietove in pasirinktas_regionas.vietoves:
                        if vietove.pavadinimas == trinti_vietove:
                            session.delete(vietove)
                            session.commit()
                            sg.popup(f'Vietove "{trinti_vietove}" sekmingai istrinta.')
                            vietoves = [
                                vietove.pavadinimas
                                for vietove in pasirinktas_regionas.vietoves
                            ]
                            window["-VIETOVE-"].update(values=vietoves)
                            break
        elif event == '-PRIDETI-':
            add_location(session)

def regionas_pagal_pavadinima(regionai, regiono_pavadinimas):
    for regionas in regionai:
        if regionas.pavadinimas == regiono_pavadinimas:
            return regionas
    return None

def vietove_pagal_pavadinima(vietoves, vietove_pavadinimas):
    for vietove in vietoves:
        if vietove.pavadinimas == vietove_pavadinimas:
            return vietove
    return None

def grybo_ivedimas(session):
    regionai = session.query(Regionas).all()
    regionu_pavadinimai = [region.pavadinimas for region in regionai]

    vietoves = [] 
    pasirinktas_regionas = None

    layout = [
        [sg.Text("Pasirinkite regioną:", size=(15, 1)), sg.Combo(regionu_pavadinimai, key="-REGIONAS-", size=(20, 1), enable_events=True)],
        [sg.Text("Pasirinkite vietovę:", size=(15, 1)), sg.Combo(vietoves, key="-VIETOVA-", size=(20, 1), enable_events=True)],
        [sg.Text("Pavadinimas:", size=(15, 1)), sg.InputText(key="-PAVADINIMAS-", size=(20, 1))],
        [sg.Text("Klasė:", size=(15, 1)), sg.InputText(key="-KLASE-", size=(20, 1))],
        [sg.Button("Pridėti", key="-PRIDETI-")],
    ]

    window = sg.Window("Pridėti Grybą", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "-REGIONAS-":
            pasirinktas_regionas = values["-REGIONAS-"]
            region = regionas_pagal_pavadinima(regionai, pasirinktas_regionas)
            if region:
                vietoves = [v.pavadinimas for v in region.vietoves]
                window["-VIETOVA-"].update(values=vietoves)
            else:
                vietoves = []
                window["-VIETOVA-"].update(values=[])

        if event == "-PRIDETI-":
            pavadinimas = values["-PAVADINIMAS-"]
            klase = values["-KLASE-"]
            pasirinkta_vietove = values["-VIETOVA-"]

            if pavadinimas and klase and pasirinkta_vietove:
                region = regionas_pagal_pavadinima(regionai, pasirinktas_regionas)
                if region:
                    vietove = vietove_pagal_pavadinima(region.vietoves, pasirinkta_vietove)
                    if vietove:
                        naujas_grybas = Grybas(pavadinimas=pavadinimas, klase=klase)
                        vietove.grybai.append(naujas_grybas)
                        session.commit()
                        sg.popup(f'Grybas "{pavadinimas}" pridėtas sėkmingai į vietovę "{vietove.pavadinimas}"')
                        window["-PAVADINIMAS-"].update("")
                        window["-KLASE-"].update("")
                    else:
                        sg.popup("Pasirinkta vietovė nerasta")
                else:
                    sg.popup("Pasirinktas regionas nerastas")
            else:
                sg.popup("Pavadinimas, klasė ir vietovė negali būti tušti")

    window.close()


def grybu_perziura(session):
    regionai = session.query(Regionas).all()
    layout = [
        [sg.Text('Regionas: '), sg.Combo(regionai, key='-REGIONAS-', enable_events=True, size=(15,1))], 
        [sg.Text('Vietovė: '), sg.Combo([], key='-VIETOVE-', enable_events=True, size=(17,1))],
        [sg.Table(values=[], headings=['Pavadinimas', 'Klasė'], auto_size_columns=False, justification='right', num_rows=10, key='-GRYBAS-', enable_events=True)],
        [sg.Button('Trinti', key='-TRINTI-'), sg.Button('Grybai', key='-GRYBO-IVEDIMAS-'), sg.Button('Regionai', key='-REGIONAI-'), sg.Button('Vietovės', key='-VIETOVES-')],
    ]
    window = sg.Window("Grybai", layout, finalize=False)
    pasirinktas_regionas = None
    pasirinkta_vietove = None
    pasirinktas_grybas = None
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-REGIONAS-":
            pasirinktas_regionas = values["-REGIONAS-"]
            if pasirinktas_regionas:
                vietoves = [vietove.pavadinimas for vietove in pasirinktas_regionas.vietoves]
                window["-VIETOVE-"].update(values=vietoves)
            else:
                window["-VIETOVE-"].update(values=[])

        elif event == "-VIETOVE-":
            pasirinkta_vietove = values["-VIETOVE-"]
            if pasirinkta_vietove and pasirinktas_regionas:
                pasirinkta = None
                for vietove in pasirinktas_regionas.vietoves:
                    if vietove.pavadinimas == pasirinkta_vietove:
                        pasirinkta = vietove
                        break
                if pasirinkta:
                    grybai_data = [(grybas.pavadinimas, grybas.klase) for grybas in pasirinkta.grybai]
                    window["-GRYBAS-"].update(values=grybai_data)
                else:
                    window['-GRYBAS-'].update(values=[])
        
        elif event == '-GRYBAS-':
            if values['-GRYBAS-']:
                pasirinktas_grybas = values['-GRYBAS-'][0]
        
        elif event == '-TRINTI-':
            if pasirinktas_grybas is not None:
                if pasirinkta_vietove and pasirinktas_regionas:
                    pasirinktas_indeksas = pasirinktas_grybas
                    if 0 <= pasirinktas_indeksas < len(grybai_data):
                        grybas = pasirinkta.grybai[pasirinktas_indeksas]
                        session.delete(grybas)
                        session.commit()
                        sg.popup(f'Grybas "{grybas.pavadinimas}" sekmingai istrintas.')
                    
                        grybai_data = [(grybas.pavadinimas, grybas.klase) for grybas in pasirinkta.grybai]
                        window['-GRYBAS-'].update(values=grybai_data)
                    
                    pasirinktas_grybas = None 

        elif event == '-REGIONAI-':
            add_or_remove_region(session)

        elif event == '-VIETOVES-':
            vietoviu_perziura_trynimas(session)
        elif event == '-GRYBO-IVEDIMAS-':
            grybo_ivedimas(session)

if __name__ == "__main__":
    Session = sessionmaker(db_engine)
    session = Session()
    grybu_perziura(session)