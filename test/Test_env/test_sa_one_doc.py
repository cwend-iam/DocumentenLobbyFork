import os
import pandas as pd
import bestand_locaties
import IAMDataMinePackage

from export_dataframe import Export_data


def get_quarter(file_name):
    quarter_set = ('Q1', 'Q2', 'Q3', 'Q4')
    found_quarter = [x for x in quarter_set if x in file_name]
    return found_quarter


test_cent_opslag = 'test/Test_env/doc'
project = 'Maastunnel'
folder = 'Storingsanalyse'
sa_map = bestand = '2019'
test_file = 'Bijlage grafiek Q4.docx'

pad_naar_folder = os.path.join(test_cent_opslag, project, folder)
pad_sa_map = os.path.join(pad_naar_folder, sa_map)

overzicht_project_typen = IAMDataMinePackage.get_types_summary()
project_type = overzicht_project_typen[project]

storingsanalyse = IAMDataMinePackage.Document(pad_sa_map, test_file)

document_type = storingsanalyse.documentType

deelsysteem_nummer = storingsanalyse.di_number_v2(file_name=storingsanalyse.name, projectnaam=project)

deelsysteem_naam = storingsanalyse.di_name_v2(di_num=deelsysteem_nummer)

discipline = storingsanalyse.discipline_v2(deelsysteem_nummer)

document_eigenaar = storingsanalyse.GetDocumentOwner(project)

# Definitie van de waarden voor de lege kolommen
project_fase = str()
opmerking = get_quarter(test_file)
link_doc = str()

volle_pad_naar_cloud = storingsanalyse.path_to_hyperlink(project)

new_record = pd.Series([storingsanalyse.name, storingsanalyse.documentType, storingsanalyse.documentClass, storingsanalyse.version,
                        storingsanalyse.status, storingsanalyse.creationDate, storingsanalyse.lastModifiedDate, project,
                        project_type, deelsysteem_nummer, deelsysteem_naam, discipline, project_fase,
                        document_eigenaar, storingsanalyse.fileType, link_doc, opmerking, bestand,
                        volle_pad_naar_cloud],
                       index=Export_data.columns)

# De nieuwe regel toevoegen aan het DataFrame
Export_data = Export_data.append(new_record, ignore_index=True)
