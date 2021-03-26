"""
script to test the new module implemented in the Document- class
MaVa is aan de start van het herschrijven van deze module het enige project dat niet is omgezet naar
de nieuwe opbouw van het sbs koppeldocument. De rest van de projecten zijn toegevoegd aan het ene
koppeldocument dat gebruikt moet gaan worden in de toekomst. Dit is voor het eventueel aanpassen van
verwijzingen gemakkelijker. Ook is het beter om zo min mogelijk verschillende documenten te moeten
importeren.
"""
import bestand_locaties
import os
import pandas as pd

# Making sure the working dir is the root of the repo
while True:
    if os.getcwd().endswith('DocumentenLobby'):
        break
    else:
        os.chdir('..')

# folder with docs in test_env
test_docs_folder = 'test/Test_env/doc'
file_name = 'Faalkansanalyse Di 25 en Di 26 - Evacuatie- en Verkeersgeleidingsverlichting Versie A.pdf'

sbs_overview = pd.read_excel('res/sbs' + '/' + 'sbs_koppeldoc_dl.xlsx')
projectnaam = 'Coentunnel-tracé'

"""
onderstaande code werkt voor het herkennen van di_nummers als 10, 22, en 46A (uit testset documenten in Test_env)
loopt spaak op documenten die meerdere di_nums in titel hebben (25 en 26).
De koppeling tussen found_project_numbers en de bijbehorende generieke nummers moet gemaakt worden. Hiervoor moet
waarschijnlijk per found_project_number gekeken worden of deze aanwezig is in de sbs_overview.
Kijk of er iets geregeld kan worden met behulp van any() (https://www.geeksforgeeks.org/python-check-if-any-list-element-is-present-in-tuple/)
waarschijnlijk moet er gekeken worden of een gevonden nummer aanwezig is in de project kolom ipv anders om (zoals nu nog het geval is)
Misschien niet, maar het is misschien nog goed om te kijken naar het verschil tussen de eigenschappen van een 
tuple en een set. het kan zijn dat een set eigenschappen heeft die deze aanpak wel werkbaar maakt.
https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s07.html
"""
## Module body


def string_to_tuple(string):
    """
    Transforms a tuple that was formed to a string in the extraction back to a tuple for further handling.
    :param string:
    :return:
    """
    string = string.split(', ')
    value_list = []
    for i in range(len(string)):
        value_list.append(string[i])

    values = tuple(value_list)
    return values


project_column = f'sbs nummer {projectnaam}'
known_project_numbers = list(sbs_overview[project_column])
known_project_numbers = [x for x in known_project_numbers if not isinstance(x, float)]

"""
found_project_numbers contains all the project specific sbs numbers that are found in the file name.
"""
found_project_numbers = []
for n in known_project_numbers:
    if str(n) in file_name:
        found_project_numbers.append(n)
    elif isinstance(n, str) and ',' in n:
        split_numbers = string_to_tuple(n)
        num2append = [num for num in split_numbers if num in file_name]
        if len(num2append) != 0:
            for num in num2append:
                found_project_numbers.append(num)
    else:
        pass

# Transforming data types of values to tuples in the sbs_overview to support the check to gather the result_list
for row_index, row in sbs_overview.iterrows():
    for col_index, value in row.items():
        if (col_index != 'sbs omschrijving') and (isinstance(value, str)) and (',' in value):
            new_value = string_to_tuple(value)
            sbs_overview[col_index][row_index] = new_value


gen_col = 'sbs nummer generiek'
result_list = [sbs_overview.at[index, gen_col]
               for index in range(sbs_overview.shape[0])
               if sbs_overview.at[index, project_column] in found_project_numbers]

print(sbs_overview.at[58, project_column])

## Return statement (print statement for now)
