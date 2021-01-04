"""
In dit bestand worden de locaties van de .csv referentiebestanden gedefinieerd en ingelezen als pandas.DataFrame
zodat deze locaties in de andere scripts geïmporteerd en gebruikt kunnen worden.
"""
import os
import pandas as pd

from find_storage_path import *
import getpass

find_storage_path()

# Definiëren van de mappen en documenten
while True:
    if os.getcwd().endswith('DocumentenLobby'):
        backend = os.getcwd()
        break
    else:
        os.chdir('..')

res_path = os.path.abspath('res')

os.chdir(res_path)
with open('centrale_opslag_path.txt', 'r') as file:
    text = file.read()
file.close()

centrale_opslag = text

# Front end Opslag (MS_teams map
user_path = os.path.join('C:\\Users', getpass.getuser())
tbi_path = os.path.join(user_path, 'TBI Holding')
Front_End_Opslag = os.path.join(tbi_path, 'Documenten Lobby - General')

# Specificatie back-end mappen/bestanden
sbs_path = os.path.join(res_path, 'sbs')

# Locatie en inlezen van de generieke SBS
Overzicht_SBS_Num_Generiek = os.path.join(sbs_path, 'Overzicht_SBS_num_Generiek.csv')
SBS_Generiek = pd.read_csv(Overzicht_SBS_Num_Generiek, sep=';')

# Locatie en inlezen van de referentie SBS van de Coentunnel
Overzicht_SBS_Num_Coentunnel = os.path.join(sbs_path, 'Overzicht_SBS_num_Coentunnel.csv')
SBS_Coentunnel = pd.read_csv(Overzicht_SBS_Num_Coentunnel, sep=';')

# Locatie en inlezen van de referentie SBS van de Maastunnel
Overzicht_SBS_Num_Maastunnel = os.path.join(sbs_path, 'Overzicht_SBS_num_Maastunnel.csv')
SBS_Maastunnel = pd.read_csv(Overzicht_SBS_Num_Maastunnel, sep=';')

# Locatie en inlezen van de referentie SBS van MaVa
Overzicht_SBS_Num_MaVa = os.path.join(sbs_path, 'Overzicht_SBS_num_MaVa.csv')
SBS_MaVa = pd.read_csv(Overzicht_SBS_Num_MaVa, sep=';')

# Locatie en inlezen van de referentie SBS van de Westerscheldetunnel
Overzicht_SBS_Num_Westerscheldetunnel = os.path.join(sbs_path,
                                                     'Overzicht_SBS_num_Westerscheldetunnel.csv')
SBS_Westerscheldetunnel = pd.read_csv(Overzicht_SBS_Num_Westerscheldetunnel, sep=';')
# Locatie en inlezen van de RAMS specifieke SBS van de Westerscheldetunnel
Overzicht_SBS_Num_Westerscheldetunnel_RAMS = os.path.join(sbs_path,
                                                          'Overzicht_SBS_num_Westerscheldetunnel_RAMS.csv')
SBS_Westerscheldetunnel_RAMS = pd.read_csv(Overzicht_SBS_Num_Westerscheldetunnel_RAMS, sep=';')

# Locatie en inlezen van de referentie SBS van de Rijnlandroute
Overzicht_SBS_Num_Rijnlandroute = os.path.join(sbs_path, 'Overzicht_SBS_num_Rijnlandroute.csv')
SBS_Rijnlandroute = pd.read_csv(Overzicht_SBS_Num_Rijnlandroute, sep=';')

# Locatie en inlezen van de referentie van de document typen en klassen
Overzicht_Document_Klasse_Type = os.path.join(res_path, 'Overzicht_Document_Klasse_Type.csv')
Document_Klasse_Type = pd.read_csv(Overzicht_Document_Klasse_Type, sep=';')

# Locatie en inlezen van de referentie van het eigenaarschap
Overzicht_Eigenaarschap_Documenten = os.path.join(res_path, 'Overzicht_Eigenaarschap_documenten.csv')
Referentietabel_Eigenaarschap = pd.read_csv(Overzicht_Eigenaarschap_Documenten, sep=';', encoding='latin1')

# Locatie en inlezen van het overzicht van de personen en de persoonsinformatie
Overzicht_Personen_Informatie = os.path.join(res_path, 'Overzicht_Personen_Informatie.csv')
Personen_Informatie = pd.read_csv(Overzicht_Personen_Informatie, sep=';')

# Locatie en inlezen van het overzicht van de status aanduidingen
Overzicht_Status_Aanduiding = os.path.join(res_path, 'Overzicht_Status_aanduiding.csv')
Status_Aanduiding = pd.read_csv(Overzicht_Status_Aanduiding, sep=';')

# Locatie en inlezen van het overzicht van de objecten van de projecten
Overzicht_Project_Informatie = os.path.join(res_path, 'Overzicht_Project_Informatie.csv')
Project_Informatie = pd.read_csv(Overzicht_Project_Informatie, sep=';')

# Locatie en inlezen van de definities van de object typen
Overzicht_Definities_Object_Typen = os.path.join(res_path, 'definitie_nat_droog_kunstwerk.csv')
Definities_Object_Typen = pd.read_csv(Overzicht_Definities_Object_Typen, sep=';')

# Standaard deel export url voor het makan van links naar de documenten
Standaard_url = "https://tbiholding.sharepoint.com/sites/DocumentManagementSysteem/Gedeelde%20documenten/" \
                "General/Centrale%20opslag"
