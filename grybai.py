import PySimpleGUI as sg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Grybai, Vietoves, Regionai


db_engine = create_engine("sqlite:///grybai.db")
Session = sessionmaker(db_engine)
session = Session()


def main_window():  # Einaras
    layout = [
        [sg.Text("Sveiki atvykę!")],
        [sg.Button("Pridėti/ ištrinti regioną")],
        [sg.Button("Peržiūrėti vietas")],
        [sg.Button("Pridėti vietą")],
        [sg.Button("Ištrinti vietą")],
        [sg.Button("Peržiūrėti Grybus")],
        [sg.Button("Išeiti")],
    ]

    window = sg.Window("Mushroom App", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Pridėti/ ištrinti regioną":
            add_or_remove_region(session)
        elif event == "Peržiūrėti vietas":
            view_locations(session)
        elif event == "Pridėti vietą":
            add_location(session)
        elif event == "Ištrinti vietą":
            remove_location(session)
        elif event == "Peržiūrėti Grybus":
            perziureti_grybus(session)

    window.close()


def add_or_remove_region(session):  # Deivida
    regions = session.query(Regionai).all()
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
                new_region = Regionai(pavadinimas=region_name)
                session.add(new_region)
                session.commit()
                sg.popup(f"Regionas {region_name} pridėtas sėkmingai")
                window["-REGIONO-PAVADINIMAS-"].update("")
                region_names.append(region_name)
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
                    region_names.remove(selected_region_name)
                    window["-REGIONAI-"].update(values=region_names)


# Lukas
def perziureti_grybus(session):
    regions = session.query(Regionai).all()
    regionu_pavadinimai = [regionas.pavadinimas for regionas in regions]

    layout = [
        [
            sg.Text("Pasirinkite regiona: "),
            sg.Combo(regionu_pavadinimai, key="-REGIONAI-", size=(20, 1)),
        ],
        [
            sg.Text("Pasirinkite vietove: "),
            sg.Combo([], key="-VIETOVES-", size=(20, 1)),
        ],
        [sg.Multiline(key="-GRYBAI-", size=(40, 10))],
        [sg.Button("Uzdaryti", key="-UZDARYTI-")],
    ]
    window = sg.Window("Grybu perziura", layout, finalize=False)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-UZDARYTI-":
            break

        pasirinktas_regionas = values["-REGIONAI-"]
        # debug
        print("pasirinktas regionas:", pasirinktas_regionas)
        pasirinktas_regionas_objektas = next(
            (
                region
                for region in regions
                if region.pavadinimas == pasirinktas_regionas
            ),
            None,
        )

        if pasirinktas_regionas_objektas:
            vietoves_pagal_regiona = [
                vietove.pavadinimas
                for vietove in pasirinktas_regionas_objektas.vietoves
            ]
            # debug
            print("pasirinkto regiono vietoves:", vietoves_pagal_regiona)
            window["-VIETOVES-"].update(values=vietoves_pagal_regiona)
        else:
            window["-VIETOVES-"].update(values=[])
        # gaunam pasirinkta vietove
        pasirinkta_vietove = values["-VIETOVES-"]

        if pasirinktas_regionas_objektas and pasirinkta_vietove:
            # grybai pagal pasirinkta regiona ir vietove
            grybai = (
                session.query(Grybai)
                .join(Vietoves)
                .filter(
                    Regionai.pavadinimas == pasirinktas_regionas,
                    Vietoves.pavadinimas == pasirinkta_vietove,
                )
                .all()
            )
            # parodom visus grybus(multiline)
            visi_grybai = [f"{grybas.pavadinimas}, {grybas.klase}" for grybas in grybai]
            window["-GRYBAI-"].update("\n".join(visi_grybai))
        else:
            window["-GRYBAI-"].update(values="")


def view_locations(session):
    regions = session.query(Regionai).all()
    regionu_pavadinimai = [regionas.pavadinimas for regionas in regions]

    layout = [
        [
            sg.Text("Pasirinkite regiona: "),
            sg.Combo(regionu_pavadinimai, key="-REGIONAI-", size=15),
        ],
        [sg.Multiline(key="-VIETOVES-", size=(30, 10))],
        [sg.Button("Uzdaryti", key="-UZDARYTI-")],
    ]
    window = sg.Window("Vietoviu perziura", layout, finalize=False)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or "-UZDARYTI-":
            break
    # pasirinktas regionas is dropDown
    pasirinktas_regionas = values["-REGIONAI-"]
    # pasirinkto regiono vieotves
    pasirinktas_regionas_objektas = next(
        (region for region in regions if region.pavadinimas == pasirinktas_regionas),
        None,
    )
    if pasirinktas_regionas_objektas:
        visos_vietoves = [
            vietove.pavadinimas for vietove in pasirinktas_regionas_objektas.vietoves
        ]
        window["-VIETOVES-"].update("\n".join(visos_vietoves))
    else:
        # nerodom vietoviu (multiline) jeigu nepasirinktas regionas
        window["-VIETOVES-"].update("")


def add_location(session):
    # pasiimti regionus is db
    regions = session.query(Regionai).all()
    # regionu dropDown
    regionu_pavadinimai = [regionas.pavadinimas for regionas in regions]

    layout = [
        [
            sg.Text("Iveskite vietoves pavadinima: ", size=20),
            sg.InputText(key="-PAVADINIMAS-"),
        ],
        [
            sg.Text("Pasirinkite regiona: ", size=20),
            sg.Combo(regionu_pavadinimai, key="-REGIONAI-"),
        ],
        [sg.Button("Prideti", key="-PRIDETI-")],
    ]
    window = sg.Window("Naujos Vietoves Ivedimas", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-PRIDETI-":
            vietoves_pavadinimas = values["-PAVADINIMAS-"]
            pasirinktas_regionas = values["-REGIONAI-"]

            # pasiimti pasirinkta regiona (dropdown)
            pasirinktas_regionas = next(
                (
                    regionas
                    for regionas in regions
                    if regionas.pavadinimas == pasirinktas_regionas
                ),
                None,
            )

        if pasirinktas_regionas:
            nauja_vietove = Vietoves(
                pavadinimas=vietoves_pavadinimas, regionai=pasirinktas_regionas
            )
            session.add(nauja_vietove)
            session.commit()
            sg.popup(f"Vietove: {vietoves_pavadinimas} Sekmingai prideta")
            break
        else:
            sg.popup("Pasirinktas regionas nerastas")


def remove_location(session):
    vietoves = session.query(Vietoves).all()
    # vietoves dropDown
    vietove = [vietove.pavadinimas for vietove in vietoves]

    layout = [
        [
            sg.Text("Pasirinkite vietove: ", size=20),
            sg.Combo(vietove, key="-VIETOVES-", size=(10, 10)),
        ],
        [
            sg.Listbox(
                values=vietoves,
                size=(15, 8),
                key="-VISOS-VIETOVES-",
                enable_events=True,
            )
        ],
        [sg.Button("Istrinti", key="-ISTRINTI-")],
    ]
    window = sg.Window("Vietoves pasalinimas", layout, finalize=False)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-ISTRINTI-":
            pasirinkta_vietove = values["-VIETOVES-"]
            if pasirinkta_vietove:
                pasirinkta_vietove_pavadinimas = pasirinkta_vietove
                trinti_vietove = next(
                    (
                        vietove
                        for vietove in vietoves
                        if vietove.pavadinimas == pasirinkta_vietove_pavadinimas
                    ),
                    None,
                )
                if trinti_vietove:
                    session.delete(trinti_vietove)
                    session.commit()
                    sg.popup(
                        f"Vietove {pasirinkta_vietove_pavadinimas} sekmingai istrinta"
                    )
                    vietove = [
                        v for v in vietove if v != pasirinkta_vietove_pavadinimas
                    ]
                    window["-VISOS-VIETOVES-"].update(values=vietove)


def add_mushroom():  # Vytautas
    pass


if __name__ == "__main__":
    session = Session()
    main_window()
    # add_or_remove_region(session)
    # add_location(session)
    # remove_location(session)
    # view_locations(session)
    # perziureti_grybus(session)
