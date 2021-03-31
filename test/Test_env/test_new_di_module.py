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
file = 'E601.072 - Beveiliging en bewaking - 2001-1194'

sbs_overview = pd.read_excel('res/sbs' + '/' + 'sbs_koppeldoc_dl.xlsx')
project = 'Rijnlandroute'

lijst_projecten = os.listdir(bestand_locaties.centrale_opslag)

"""
De workflow van de module is gebouwd op de faalkananalysen van de Countunnel. De workflow moet nog worden getest voor
de andere projecten.
"""
## Module body


def string_to_tuple(string):
    """
    Transforms a tuple that was formed to a string in the extraction-phase back to a tuple for further
    handling. "(25, 61)" => ("25", "61")
    :param string:
    :return:
    """
    string = string.split(', ')
    value_list = []
    for i in range(len(string)):
        value_list.append(string[i])

    values = tuple(value_list)
    return values


def contains_any(string, set_var):
    """
    Check whether sequence str contains ANY of the items in set.
    Function found at source: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s07.html
    """
    return 1 in [c in string for c in set_var]


"""
kijk voor onderstaande functie of de map functie iets kan betekeken. ook kijken of het nuttig is te kijken naar
de lengte van de gevonden_sbs_nummers (qua aanpak voor het controleren van de nummers.
zie info: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s07.html
"""
def check_numbers(project_sbs_number, found_sbs_numbers):
    """
    function to check whether a project specific number is in the collection of found numbers from the file title
    :param project_sbs_number:
    :param found_sbs_numbers:
    :return:
    """
    # Making set of the found numbers
    found_sbs_numbers_set = set(found_sbs_numbers)
    """
    The if statement bellow covers the case of multiple project specific numbers pointing to one generic sbs number.
    If any of the project specific numbers is found in the 'found numbers set', return True. If none is found,
    return False.
    """
    if ',' in project_sbs_number:
        project_sbs_nummer_set = string_to_tuple(project_sbs_number)
        return 1 in [c in found_sbs_numbers_set for c in project_sbs_nummer_set]
    else:  # check if project_sbs_number is in found_sbs_numbers_set
        return 1 if project_sbs_number in found_sbs_numbers_set else 0


def di_number_v2(file_name, projectnaam):

    project_column = f'sbs nummer {projectnaam}'
    known_project_numbers = list(sbs_overview[project_column])
    known_project_numbers = [x for x in known_project_numbers if not isinstance(x, float)]

    """
    found_project_numbers contains all the project specific sbs numbers that are found in the file name.
    """
    found_project_numbers = []
    for n in known_project_numbers:
        if str(n) in file_name:
            found_project_numbers.append(str(n))
            """
            n is added as a string to make it possible to apply the function 'contains_any()' in the list 
            comprehension for result_list.
            """
        elif isinstance(n, str) and ',' in n:
            split_numbers = string_to_tuple(n)
            num2append = [num for num in split_numbers if num in file_name]
            if len(num2append) != 0:
                for num in num2append:
                    found_project_numbers.append(num)
        else:
            pass

    # Filling the nan values to make the list comprehension for result_list possible
    sbs = sbs_overview.fillna(value=-1)

    gen_col = 'sbs nummer generiek'
    # result_list = [sbs_overview.at[index, gen_col] for index in range(sbs_overview.shape[0])
    #                if contains_any(str(sbs_overview.at[index, project_column]), found_project_numbers)]
    """
    De list comprehension voor de result_list in nog niet geheel correct. De IF statement van de comprehension 
    geeft ook een hit wanneer '0' (project_specefiek) met '30' (generiek) wordt vergeleken. kijk of dit met behulp
    van een statische functie is op te lossen (functie enkel verantwoordelijk voor de check tussen de verschillende
    project_speciefieke cijfers met het desbetreffende generieke nummer. if True => add to result_list.
    """
    result_list = [sbs.at[index, gen_col] for index in range(sbs.shape[0])
                   if check_numbers(project_sbs_number=str(sbs.at[index, project_column]),
                                    found_sbs_numbers=found_project_numbers)]

    # Return statement (print statement for now)
    return result_list


num = di_number_v2(file_name=file, projectnaam=project)
print(f'di num = {num}')


def di_name_v2(di_num):
    if di_num == (9009 or 9999):
        di_name = 'n.v.t.'
        return di_name

    di_num = set(list(di_num))
    sbs = sbs_overview
    gen_col = 'sbs nummer generiek'
    name_col = 'sbs omschrijving'
    di_name = [sbs.at[index, name_col] for index in range(sbs.shape[0]) if sbs.at[index, gen_col] in di_num]
    return di_name


print(di_name_v2(di_num=num))


def discipline_v2(di_num):
    if di_num == (9009 or 9999):
        di_name = 'n.v.t.'
        return di_name

    di_num = set(di_num)
    sbs = sbs_overview
    gen_col = 'sbs nummer generiek'
    discipline_col = 'discipline'
    discipline = [sbs.at[index, discipline_col] for index in range(sbs.shape[0]) if sbs.at[index, gen_col] in di_num]

    unique = set(discipline)
    print(f'unique = {unique}')

    return unique


print(discipline_v2(di_num=num))
