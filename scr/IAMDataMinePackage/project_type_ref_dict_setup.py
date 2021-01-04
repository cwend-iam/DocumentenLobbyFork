import pandas as pd
import os
from collections import Counter
from bestand_locaties import Project_Informatie, Definities_Object_Typen

# Current working directory aanpassen naar toplevel van de github repo
while True:
    if os.getcwd().endswith('DocumentenLobby'):
        backend = os.getcwd()
        break
    else:
        os.chdir('..')


def sort_objects_per_project():
    """
    Deze statische functie neemt de project informatie uit het referentiedocument 'Overzicht_Project_Informatie.csv'
    en sorteert hiervan de objecten per project.
    :return: Dict met de projecten en de bijbehorende objecten in de key:value opbouw project:[objecten van project]
    """
    # Inlezen van de referentie documenten
    project_informatie = Project_Informatie

    # Lijst met de verschillende projecten
    projecten = list(Counter(project_informatie['Project']))

    # Dict initialiseren om op te vullen
    objecten_per_project = dict()

    # Dict opvullen met key (project) en values (objecten per project)
    for project in projecten:
        regels_per_project = project_informatie.loc[project_informatie['Project'] == project]
        lijst_object_typen_per_project = [x for x in regels_per_project['Object_type']]
        objecten_per_project[project] = lijst_object_typen_per_project

    return objecten_per_project


def get_kunstwerk_type(object):
    """
    Deze functie neemt het object als input en geeft het type van dit object(kunstwerk) als output.
    :param object: De omschrijving van het object (sluis, tunnel, etc.)
    :return: Het type van het kunstwerk dat als input is gegeven.
    """
    # Inlezen van het referentiedocument
    # todo: deze kan misschien beter omgevormd worden naar global
    overzicht_objecten_typen = Definities_Object_Typen

    # Isoleren van de informatie m.b.t. het object
    try:
        object_info = overzicht_objecten_typen.loc[overzicht_objecten_typen['object_type'] == object.capitalize()]

    except AttributeError:
        """Wordt gegeven als het eerste teken van de string een cijfer is."""
        object_info = overzicht_objecten_typen.loc[overzicht_objecten_typen['object_type'] == object]

    # Output waarde gereedstellen
    try:
        output = object_info['kunstwerk_type'].iloc[0]
        return output

    except IndexError as e:
        """Wordt gegeven als de object_type van een object niet is ingevuld (nan)"""
        print(f'IndexError: \'{e}\' for object: {object}\nOutput type set as: n.v.t.')
        error_output = 'n.v.t.'
        return error_output


def change_objects_to_types(overzicht_objecten_per_project):
    """
    Deze functie neemt het overzicht(dtype: dict) van de objecten per project als input en geeft een dict terug
    waarvan de objecten per project zijn vervangen door de kunstwerk typen van de objecten van de projecten.
    :param overzicht_objecten_per_project: Overzicht van de verschillende objecten per project (dtype: dict)
    :return: Dict met de kunstwerk typen per project.
    """
    # lijst projecten
    projecten = list(overzicht_objecten_per_project.keys())

    # Dict initialiseren om op te vullen
    dict_type_object_per_project = dict()

    for _ in projecten:

        # lijst met object soorten per project
        lijst_objecten_per_project = overzicht_objecten_per_project[_]

        # lijst met de type kunstwerken per project
        lijst_kunstwerk_typen_per_project = [get_kunstwerk_type(a) for a in lijst_objecten_per_project]

        # key: val pair in nieuwe dict in de vorm project: type_kunstwerken
        dict_type_object_per_project[_] = lijst_kunstwerk_typen_per_project

    return dict_type_object_per_project


def type_per_project(overzicht_type_object_per_project):
    """
    Functie voor het samenvatten van de typen kunstwerken in 1 uitdrukking (nat/droog/combinatie) per project.
    :param overzicht_type_object_per_project: Het overzicht met de verschillende objecten per project (dtype: dict)
    :return: Dict met een sammenvattende uitdrukking van het type van het project in de vorm [project: type].
    """
    # lege dict om op te vullen
    project_types = dict()

    # lijst projecten
    projecten = list(overzicht_type_object_per_project.keys())

    # itereren over de verschillende projecten
    for project in projecten:
        # Kijken hoe vaak de verschillende waarden voorkomen
        count_of_object_types = list(Counter(overzicht_type_object_per_project[project]))

        # als meer dan 1, dan zijn er meer typen per project
        # todo: elif schijven voor (len > 1 en n.v.t. in count_of_object_types)
        if len(count_of_object_types) > 1 and ('n.v.t.' not in count_of_object_types):
            project_type = "Combinatie"
        else:
            project_type = count_of_object_types[0]  # verkrijgen van de

        # project en bijbehorende types toevoegen aan dict
        project_types[project] = project_type

    return project_types


def get_types_summary():
    """
    Deze statische functie voegt alle lokale functies samen in één functie. Zo kan het overzicht van de projecten
    met daarbij hun type met één statement verkregen worden.
    :return: Dict met een sammenvattende uitdrukking van het type van het project in de vorm [project: type].
    """
    # Uitvoeren van de gedefininieerde functie
    dict_objecten_per_project = sort_objects_per_project()

    # lijst met verschillende kunstwerk typen per project
    lijst = change_objects_to_types(dict_objecten_per_project)

    # De typen bekeken per project
    typen_per_project = type_per_project(lijst)

    return typen_per_project


if __name__ == '__main__':
    import time
    start = time.time()

    summary = get_types_summary()

    end = time.time()
    print(f'runtime {end-start} sec')
