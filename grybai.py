import PySimpleGUI as sg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Vietove, Regionas, Grybas


db_engine = create_engine("sqlite:///grybai.db")
Session = sessionmaker(db_engine)
session = Session()


def add_or_remove_region(session):
    regions = session.query(Regionas).all()
    region_names = [region.pavadinimas for region in regions]

    layout = [
        [
            sg.Text("Pasirinkite veiksmą:", size=(20, 1)),
            sg.Radio("Pridėti", "RADIO1", key="-ADD-", default=True),
            sg.Radio("Ištrinti", "RADIO1", key="-REMOVE-"),
        ],
        [
            sg.Text("Regiono pavadinimas: ", size=(20, 1)),
            sg.InputText(key="-REGIONO-PAVADINIMAS-"),
        ],
        [
            sg.Text("Pasirinkite regioną: ", size=(20, 1)),
            sg.Combo(region_names, key="-REGIONAI-", size=(10, 10)),
        ],
        [sg.Button("Vykdyti", key="-VYKDYTI-")],
    ]
    window = sg.Window("Pridėti arba Ištrinti Regioną", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
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


# Lukas
def add_location(session):
    regionai = session.query(Regionas).all()

    layout = [
        [sg.Text("Pavadinima: ", size=(20, 1)), sg.Input(key="-VIETOVE-")],
        [
            sg.Text("Pasirinkite regiona: ", size=(20, 1)),
            sg.Combo(regionai, key="-REGIONAS-", size=(20, 1)),
        ],
        [sg.Button("Ivesti", key="-PRIDETI-")],
    ]
    window = sg.Window("Vietoves pridejimas", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "-PRIDETI-":
            if values["-REGIONAS-"] and len(values["-VIETOVE-"]) > 2:
                nauja_vietove = Vietove(
                    pavadinimas=values["-VIETOVE-"], regionas=values["-REGIONAS-"]
                )
                session.add(nauja_vietove)
                session.commit()
                sg.popup(f'Vietove {values["-VIETOVE-"]} sekmingai prideta')
            else:
                sg.popup("Pasirinktas regionas nerastas")

    window.close()


def vietoviu_perziura_trynimas(session):
    regionai = session.query(Regionas).all()
    layout = [
        [
            sg.Text("Pasirinkite regiona"),
            sg.Combo(
                [regionas.pavadinimas for regionas in regionai],
                key="-REGIONAS-",
                enable_events=True,
            ),
        ],
        [
            sg.Listbox(
                values=[],
                key="-VIETOVE-",
                size=(30, 10),
                enable_events=True,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
            )
        ],
        [sg.Button("Istrinti", key="-ISTRINTI-")],
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


def grybu_perziura(session):
    regionai = session.query(Regionas).all()
    layout = [
        [
            sg.Text("Regionas: "),
            sg.Combo(regionai, key="-REGIONAS-", enable_events=True),
            sg.Text("Vietove: "),
            sg.Combo([], key="-VIETOVE-", enable_events=True, size=(15, 1)),
        ],
        [
            sg.Listbox(
                values=[],
                key="-GRYBAS-",
                size=(50, 10),
                enable_events=True,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
            )
        ],
        [sg.Button("Trinti")],
    ]
    window = sg.Window("Grybai", layout, finalize=False)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-REGIONAS-":
            pasirinktas_regionas = values["-REGIONAS-"]
            if pasirinktas_regionas:
                vietoves = [
                    vietove.pavadinimas for vietove in pasirinktas_regionas.vietoves
                ]
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
                    grybai = [grybas.pavadinimas for grybas in pasirinkta.grybai]
                    window["-GRYBAS-"].update(values=grybai)
                else:
                    window["-GRYBAS-"].update(values=[])


Session = sessionmaker(db_engine)
session = Session()
# grybu_perziura(session)
# add_location(session)
# vietoviu_perziura_trynimas(session)
add_or_remove_region(session)
