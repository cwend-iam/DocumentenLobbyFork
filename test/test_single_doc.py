import os

import pandas as pd

import IAMDataMinePackage
import bestand_locaties
from export_dataframe import Export_data

# Back end pad naar de staging locatie van het specifieke document
project = 'MaVa'
folder = 'FMECA'
doc = 'COB FMEA DI36 Tunnelventilatie Novenco.pdf'
pad_naar_folder = 'C:\\Users\\NBais\\OneDrive - TBI Holding\\Bureaublad'


# Meta data ophalen/instellen van specifiek document
pad_naar_document = os.path.join(pad_naar_folder, doc)
if os.path.isdir(pad_naar_document):
    pass
else:
    print("-"*60)
    print(pad_naar_document)
    document_type = folder
    document = IAMDataMinePackage.Document(pad_naar_folder, doc)
    document.SetClass(document_type, referentie_doc=bestand_locaties.Document_Klasse_Type)

    _di_num = document.di_number(document.name + "." + document.fileType, project, bestand_locaties.SBS_MaVa)
    print(f'_di_num = {_di_num}')

    deelsysteem_nummer = document.GetDINumber(project)
    print(document.GetDIName(project))
    assert deelsysteem_nummer == 28

    deelsysteem_naam = document.GetDIName(deelsysteem_nummer)
    assert deelsysteem_naam == 'Tunnelventilatie'

    discipline = document.GetDiscipline(deelsysteem_nummer)
    document_eigenaar = document.GetDocumentOwner(project)
    project_fase = str()
    opmerking = str()
    link_doc = str()
    volle_pad_naar_cloud = document.path_to_hyperlink(project)

    new_record = pd.Series([document.name, document_type, document.documentClass, document.version,
                            document.status, document.creationDate, document.lastModifiedDate, project,
                            deelsysteem_nummer, deelsysteem_naam, discipline, project_fase,
                            document_eigenaar,
                            document.fileType, link_doc, opmerking, doc, volle_pad_naar_cloud],
                           index=Export_data.columns)

    print(new_record)
    print("*"*60)

