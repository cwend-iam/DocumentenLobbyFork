import pandas as pd
import os
from collections import Counter
from bestand_locaties import Project_Informatie

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


# Inlezen van de referentie documenten
definitie_nat_droog = pd.read_csv('res/definitie_nat_droog_kunstwerk.csv', sep=';')

# Uitvoeren van de gedefininieerde functie
dict_objecten_per_project = sort_objects_per_project()
