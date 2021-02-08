import IAMDataMinePackage as dmp
import bestand_locaties
import os
from openpyxl import load_workbook
import re
import pandas as pd
import xlrd
import PyPDF2

TBI_Holding_OneDrive = 'C:\\Users\\NBais\\TBI Holding'

# Pad voor de front-end (opslag van FMECAs, RAMS etc.)
# en de back-en (opslag main script, referentiebestanden en back-ups)
Front_End_Opslag = os.path.join(TBI_Holding_OneDrive, 'Document Management Systeem - General')
Back_End_Opslag = os.path.join(TBI_Holding_OneDrive, 'Document Management Systeem - Back-end - Back-end')

# Specificatie front-end mappen
Projecten_map = os.path.join(Front_End_Opslag, 'Centrale opslag')

project = 'Westerscheldetunnel'
bestand_map = 'FMECA'
bestand = 'DI23 VTI Dynamische openbare verlichting.xls'
bestand2 = 'DI61 VTI CCTV installatie.xlsx'

test_project = 'Rijnlandroute'
test_map = 'FMECA'
test_file = 'E430 - Dynamische Route Informatie Paneel, DRIP - 1803-0784.xlsx'
test_file2 = 'E601.021 - Verlichting verkeerstunnel - 1710-1349.xlsx'

test_path = os.path.join(Projecten_map, test_project, test_map, test_file)
test_path2 = os.path.join(Projecten_map, test_project, test_map, test_file2)

# unix_ctimestamp = os.path.getctime(test_path)
# print(f'unix timestamp = {unix_ctimestamp}')
# try:
#     pdf_bestand = open(test_path, 'rb')
#     pdf_reader = PyPDF2.PdfFileReader(pdf_bestand)
#
#     raw_creation_date = pdf_reader.getDocumentInfo()['/CreationDate']
#
#     clean_creation_date = dmp.datum_cleaner(raw_creation_date)
# except KeyError:
#     clean_creation_date = dmp.file_creation_date(test_path)
#
# print(f'clean date = {clean_creation_date}')
#

print('Script is gestart \n{}'.format("-" * 50))

documents = os.listdir(os.path.join(Projecten_map, test_project, test_map))

# Onderstaande telt het aantal documenten dat gescand moet/gaat worden.
doc_count = 0

total_doc_count = 0
for file in documents:
    total_doc_count += 1

print(f'Te behandelen documenten: {total_doc_count}')

for file in documents:
    # De vooruitgang printen
    doc_count += 1
    print(f'{doc_count} van de {total_doc_count}')

    # path_to_file definiëren
    path_to_file = os.path.join(Projecten_map, test_project, test_map, file)

    if '.xlsx' in path_to_file:
        # Geeft de titel uit de Documenten Lobby (dl)
        title_dl = str(file).lower()
        title_dl = title_dl.replace('.xlsx', '')
        print(f'title_dl = {title_dl}')

        if re.match(r'(?<=v.)\d', title_dl):
            print('deze shiii is riii')

        print(re.search(r'(?<=v.)\d', title_dl))

        # Zoeken naar 'v' gevolgd door digit in bestandsnaam
        if re.match(r'(?<=v)\d', title_dl):
            index_v = title_dl.find('v')
            # Controleren of de naam eindigd op digit. Als dit zo is, is het het laatste getal van versie nummer
            if not re.search(r'\d$', title_dl):
                print('geen digit aan eind string')
                # Achterwaards zoeken door de bestandsnaam
                reversed_title_dl = reversed(title_dl)
                print(f'reversed string = {reversed(title_dl)}')
                if re.search(r'(?<=.)\d', title_dl):
                    index_punt = title_dl.find('.')
                    versie_nummer = title_dl[index_v+1:index_punt+2]

                    print(f'versie nummer1 = {versie_nummer}')
            else:
                print(f'versie nummer2 = {title_dl[index_v + 1::]}')
        # Zoeken naar 'versie' gevolgd door spatie en digit
        elif re.search(r'(?<=versie )\d', title_dl):
            index_versie = title_dl.find('versie')
            print(f'versie nummer3 = {title_dl[index_versie+7::]}')
        # Zoeken naar 'v' gevolgd door '.' en een digit\
        elif re.search(r'(?<=v.)\d', title_dl):
            index_v = title_dl.find('v')
            print(f'versie nummer4 = {title_dl[index_v+1::]}')
        # Voor al het andere het onderstaande
        else:
            print('nu in else aka checking the properties....')
            # Definieren van een checklist
            check_list = {'versie': ['v', 'e', 'r', 's', 'i', 'e'],
                          'nummer': ['0', '1', '2', '.']}
            # Inladen van het document
            wb = load_workbook(path_to_file)
            # De DocumentProperties isoleren
            probs = wb.properties
            # Van de properties de titel van het document isoleren
            title = probs.title
            print(f'title = {title}')
            # Zoeken naar een 'v' gevolgd door een digit
            if re.search(r'(?<=v)\d', title):
                # Index van de letter bepalen
                index_v = title.find('v')
                # Itereren vanaf de index van de letter
                for i in range(index_v, len(title)):
                    # Notaties 'v2' of 'v2.0' eindigen beide op ' '(spatie)
                    if title[i] == ' ':
                        versie_nummer = title[index_v+1:i]  # 'v2' of 'v2.0' ==> '2' of '2.0'
                        print(f'versie nummer = {versie_nummer}')
                        break  # in module wordt dit 'return versie_nummer'
            else:
                versie_nummer = 'Geen versienummer bekend'
                print(f'versie nummer = {versie_nummer}')

    else:
        print('dit is geen .xlsx bestand')
