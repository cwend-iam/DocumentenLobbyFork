import os

import pandas as pd

import IAMDataMinePackage
import bestand_locaties
from export_dataframe import Export_data

backend = os.path.join(bestand_locaties.tbi_path, "Documenten Lobby - Beheer")
folder_tendercalculaties = os.path.join(backend, "Tendercalculaties")


lijst_projecten = os.listdir(folder_tendercalculaties)

for project in lijst_projecten:
    pad_naar_project = os.path.join(folder_tendercalculaties, project)
    folders_in_projectmap = os.listdir(pad_naar_project)

    for folder in folders_in_projectmap:

        pad_naar_folder = os.path.join(pad_naar_project, folder)
        documenten_in_folder = os.listdir(pad_naar_folder)

        for doc in documenten_in_folder:
            pad_naar_document = os.path.join(pad_naar_folder, doc)
            if os.path.isdir(pad_naar_document):
                pass
            else:
                print("-"*60)
                print(pad_naar_document)
                document_type = folder
                document = IAMDataMinePackage.Document(pad_naar_folder, doc)
                document.SetClass(document_type, referentie_doc=bestand_locaties.Document_Klasse_Type)
                deelsysteem_nummer = document.GetDIName(project)
                deelsysteem_naam = document.GetDIName(deelsysteem_nummer)
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
