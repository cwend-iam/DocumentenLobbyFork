#! usr/bin/env python3
import os

import pandas as pd

import IAMDataMinePackage
import bestand_locaties
from export_dataframe import Export_data

# todo: voor gehele project: comments toevoegen (dus ook in classes)

print('Script is gestart \n{}'.format("-"*50))

# Onderstaande telt het aantal documenten dat gescand moet/gaat worden.
# Dit stuk is voor de terugkoppeling in de terminal, zodat men de vooruitgang kan bijhouden
total_doc_count = 0
doc_count = 0
# Lijst met de verschillende projecten in de Centrale Opslag
lijst_projecten = os.listdir(bestand_locaties.centrale_opslag)
for project in lijst_projecten:
    # Lijst met de verschillende mappen (RAMS, FMECA enz.) in de projectmap
    folders_in_projectmap = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project))
    for folder in folders_in_projectmap:
        # Pad naar de onderliggende map (RAMS, FMECA enz.) van het project die verwerkt gaat worden
        pad_naar_folder = os.path.join(bestand_locaties.centrale_opslag, project, folder)
        # Lijst van de verschillende documenten en mappen in de map die verwerkt gaat worden
        documenten_in_folder = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project, folder))
        for bestand in documenten_in_folder:
            # Controle of het bestand een document of een onderliggende map is
            if os.path.isdir(os.path.join(pad_naar_folder, bestand)):
                pass
            else:
                total_doc_count += 1

print(f'Te behandelen documenten: {total_doc_count}')

# Onderstaande itereert over de bestanden in de mappen per project (Faaldefinities, FMECA en RAMS etc.)
lijst_projecten = os.listdir(bestand_locaties.centrale_opslag)
overzicht_project_typen = IAMDataMinePackage.get_types_summary()

for project in lijst_projecten:
    # Pad naar de project map
    project_map = os.path.join(bestand_locaties.centrale_opslag, project)
    # Lijst met de verschillende mappen (RAMS, FMECA enz.) in de projectmap
    folders_in_projectmap = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project))

    # Ophalen van project type (Nat / Droog / Combinatie)
    project_type = overzicht_project_typen[project]

    for folder in folders_in_projectmap:
        # Pad naar de onderliggende map (RAMS, FMECA enz.) van het project die verwerkt gaat worden
        pad_naar_folder = os.path.join(bestand_locaties.centrale_opslag, project, folder)
        # Lijst van de verschillende documenten en mappen in de map die verwerkt gaat worden
        documenten_in_folder = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project, folder))

        for bestand in documenten_in_folder:
            # Controle of het bestand een document of een onderliggende map is
            if os.path.isdir(os.path.join(pad_naar_folder, bestand)):
                pass  # Onderliggende mappen moeten niet worden verwerkt
            else:
                # De vooruitgang printen
                doc_count += 1
                print(f'{doc_count} van de {total_doc_count}')
                print('Loading...')

                # Instance van class Document aanmaken
                document = IAMDataMinePackage.Document(pad_naar_folder, bestand)

                # Definitie van document type (FMECA, Faalanalyse, RAMS etc.)
                document_type = folder

                # Het bepalen van de document klasse
                document.SetClass(document_type, referentie_doc=bestand_locaties.Document_Klasse_Type)

                # Ophalen van het deelsysteem nummer van het bestand
                deelsysteem_nummer = document.GetDINumber(project)

                # Ophalen van de deelsysteem naam van het bestand
                deelsysteem_naam = document.GetDIName(deelsysteem_nummer)

                # Ophalen van de discipline a.h.v. de deelsystemen
                discipline = document.GetDiscipline(deelsysteem_nummer)

                # Verwijzen van eigenaar aan documenten
                document_eigenaar = document.GetDocumentOwner(project)

                # Definitie van de waarden voor de lege kolommen
                project_fase = str()
                opmerking = str()
                link_doc = str()

                # Genereren van het volledige pad naar de documenten (pad naar de cloud, niet naar lokale schijf)
                volle_pad_naar_cloud = document.path_to_hyperlink(project)

                # Samenstellen van de regel die wordt toegevoegd aan het dataframe
                new_record = pd.Series([document.name, document_type, document.documentClass, document.version,
                                        document.status, document.creationDate, document.lastModifiedDate, project,
                                        project_type, deelsysteem_nummer, deelsysteem_naam, discipline, project_fase,
                                        document_eigenaar, document.fileType, link_doc, opmerking, bestand,
                                        volle_pad_naar_cloud],
                                       index=Export_data.columns)

                # De nieuwe regel toevoegen aan het DataFrame
                Export_data = Export_data.append(new_record, ignore_index=True)

print('Done..')
# Exporteren van het DataFrame
# IAMDataMinePackage.auto_export(Export_data)

# Onderstaande is de test export
IAMDataMinePackage.test_export(Export_data)
