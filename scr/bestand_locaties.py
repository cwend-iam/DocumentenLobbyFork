"""
In dit bestand worden de locaties van de .csv referentiebestanden gedefinieerd en ingelezen als pandas.DataFrame
zodat deze locaties in de andere scripts geïmporteerd en gebruikt kunnen worden.
"""
import os
import pandas as pd

# TODO: verander de adressen die worden gebruikt van lokaal naar cloud.
# Definiëren van de mappen en documenten
# Pad naar de algemene TBI One Drive Map (tijdenlijke centrale opslag)
TBI_Holding_OneDrive = 'C:\\Users\\NBais\\TBI Holding'

# Pad voor de front-end (opslag van FMECAs, RAMS etc.)
# en de back-en (opslag main script, referentiebestanden en back-ups)
Front_End_Opslag = os.path.join(TBI_Holding_OneDrive, 'Document Management Systeem - General')
Back_End_Opslag = os.path.join(TBI_Holding_OneDrive, 'Document Management Systeem - Back-end - Back-end')

# Specificatie front-end mappen
Projecten_map = os.path.join(Front_End_Opslag, 'Centrale opslag')

# Specificatie back-end mappen/bestanden
Map_Referentie_Documenten = os.path.join(Back_End_Opslag, 'Referentie documenten')

# Locatie en inlezen van de generieke SBS
Overzicht_SBS_Num_Generiek = os.path.join(Map_Referentie_Documenten, 'Overzicht_SBS_num_Generiek.csv')
SBS_Generiek = pd.read_csv(Overzicht_SBS_Num_Generiek, sep=';')

# Locatie en inlezen van de referentie SBS van de Coentunnel
Overzicht_SBS_Num_Coentunnel = os.path.join(Map_Referentie_Documenten, 'Overzicht_SBS_num_Coentunnel.csv')
SBS_Coentunnel = pd.read_csv(Overzicht_SBS_Num_Coentunnel, sep=';')

# Locatie en inlezen van de referentie SBS van de Maastunnel
Overzicht_SBS_Num_Maastunnel = os.path.join(Map_Referentie_Documenten, 'Overzicht_SBS_num_Maastunnel.csv')
SBS_Maastunnel = pd.read_csv(Overzicht_SBS_Num_Maastunnel, sep=';')

# Locatie en inlezen van de referentie SBS van MaVa
Overzicht_SBS_Num_MaVa = os.path.join(Map_Referentie_Documenten, 'Overzicht_SBS_num_MaVa.csv')
SBS_MaVa = pd.read_csv(Overzicht_SBS_Num_MaVa, sep=';')

# Locatie en inlezen van de referentie SBS van de Westerscheldetunnel
Overzicht_SBS_Num_Westerscheldetunnel = os.path.join(Map_Referentie_Documenten,
                                                     'Overzicht_SBS_num_Westerscheldetunnel.csv')
SBS_Westerscheldetunnel = pd.read_csv(Overzicht_SBS_Num_Westerscheldetunnel, sep=';')
# Locatie en inlezen van de RAMS specifieke SBS van de Westerscheldetunnel
Overzicht_SBS_Num_Westerscheldetunnel_RAMS = os.path.join(Map_Referentie_Documenten,
                                                          'Overzicht_SBS_num_Westerscheldetunnel_RAMS.csv')
SBS_Westerscheldetunnel_RAMS = pd.read_csv(Overzicht_SBS_Num_Westerscheldetunnel_RAMS, sep=';')

# Locatie en inlezen van de referentie SBS van de Rijnlandroute
Overzicht_SBS_Num_Rijnlandroute = os.path.join(Map_Referentie_Documenten, 'Overzicht_SBS_num_Rijnlandroute.csv')
SBS_Rijnlandroute = pd.read_csv(Overzicht_SBS_Num_Rijnlandroute, sep=';')

# Locatie en inlezen van de referentie van de document typen en klassen
Overzicht_Document_Klasse_Type = os.path.join(Map_Referentie_Documenten, 'Overzicht_Document_Klasse_Type.csv')
Document_Klasse_Type = pd.read_csv(Overzicht_Document_Klasse_Type, sep=';')

# Locatie en inlezen van de referentie van het eigenaarschap
Overzicht_Eigenaarschap_Documenten = os.path.join(Map_Referentie_Documenten, 'Overzicht_Eigenaarschap_documenten.csv')
Referentietabel_Eigenaarschap = pd.read_csv(Overzicht_Eigenaarschap_Documenten, sep=';', encoding='latin1')

# Locatie en inlezen van het overzicht van de personen en de persoonsinformatie
Overzicht_Personen_Informatie = os.path.join(Map_Referentie_Documenten, 'Overzicht_Personen_Informatie.csv')
Personen_Informatie = pd.read_csv(Overzicht_Personen_Informatie, sep=';')

# Locatie en inlezen van het overzicht van de status aanduidingen
Overzicht_Status_Aanduiding = os.path.join(Map_Referentie_Documenten, 'Overzicht_Status_aanduiding.csv')
Status_Aanduiding = pd.read_csv(Overzicht_Status_Aanduiding, sep=';')

# Standaard deel export url voor het makan van links naar de documenten
Standaard_url = "https://tbiholding.sharepoint.com/sites/DocumentManagementSysteem/Gedeelde%20documenten/" \
                "General/Centrale%20opslag"
