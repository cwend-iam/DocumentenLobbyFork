#! usr/bin/env python3
import os

import pandas as pd

import bestand_locaties
import IAMDataMinePackage as dmp

from export_dataframe import Export_data

print('Script is gestart \n{}'.format("-"*50))

# Onderstaande telt het aantal documenten dat gescand moet/gaat worden.
total_doc_count = 0
doc_count = 0
lijst_projecten = os.listdir(bestand_locaties.centrale_opslag)
for project in lijst_projecten:
    if '(incompleet)' not in project:
        mappen = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project))
        for m in mappen:
            docs = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project, m))
            for bestand in docs:
                total_doc_count += 1

print(f'Te behandelen documenten: {total_doc_count}')

# Onderstaande itereert over de bestanden in de mappen per project (Faaldefinities, FMECA en RAMS etc.)
lijst_projecten = os.listdir(bestand_locaties.centrale_opslag)

for project in lijst_projecten:

    if '(incompleet)' not in project:

        project_map = os.path.join(bestand_locaties.centrale_opslag, project)
        mappen = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project))

        for m in mappen:

            mappen_doctypes_per_map = os.path.join(bestand_locaties.centrale_opslag, project, m)
            docs = os.listdir(os.path.join(bestand_locaties.centrale_opslag, project, m))
            document_type = m  # Definitie van document type (FMECA, Faalanalyse, RAMS etc.)

            for bestand in docs:

                # De vooruitgang printen
                doc_count += 1
                print(f'{doc_count} van de {total_doc_count}')
                print('Loading...')

                # path_to_file definiëren
                
                document = dmp.Document(mappen_doctypes_per_map, bestand)
                
                # Het bepalen van de document klasse
                document.SetClass(document_type, referentie_doc=bestand_locaties.Document_Klasse_Type)

                deelsysteem_nummer = document.GetDI(project)
                
                # Ophalen van de deelsysteem naam van toepassing
                deelsysteem_naam = dmp.di_name(deelsysteem_nummer, sbs=bestand_locaties.SBS_Generiek)

                # Ophalen van de discipline a.h.v. de deelsystemen
                discipline = dmp.discipline(deelsysteem_nummer, sbs=bestand_locaties.SBS_Generiek)
                # todo: give-creation_date_meta aanpassen zodat pdfminer.six gebruikt wordt
                # Ophalen van de datum waarop het document is aangemaakt
                datum = dmp.creation_date_file_type(document.path)

                # Ophalen van de datum waarop het document voor het laatst is aangepast
                laatst_aangepast_op = dmp.last_modification_file_type(document.path)

                # Ophalen van het versie nummer
                versie_nummer = dmp.document_version(document.path)

                # Verwijzen van eigenaar aan documenten
                document_eigenaar = dmp.document_owner(project,
                                                       referentie_doc=bestand_locaties.Referentietabel_Eigenaarschap)

                # Ophalen van de status van de documenten
                status = dmp.document_status(versie_nummer)

                # Definitie van de waarden voor de lege kolommen
                project_fase = str()
                opmerking = str()
                link_doc = str()

                # Genereren van het volledige pad naar de documenten (pad naar de cloud, niet naar lokale schijf)
                volle_pad = dmp.make_hyperlink_url(project, document_type, bestand)

                # Controleren op deelsysteem of discipline een tuple is (zo ja, omvormen naar string)
                if isinstance(deelsysteem_nummer, tuple):
                    deelsysteem_nummer = f'{deelsysteem_nummer[0]}, {deelsysteem_nummer[1]}'
                else:
                    pass

                if isinstance(deelsysteem_naam, tuple):
                    deelsysteem_naam = f'{deelsysteem_naam[0]}, {deelsysteem_naam[1]}'
                else:
                    pass

                if isinstance(discipline, tuple):
                    discipline = f'{discipline[0]}, {discipline[1]}'
                else:
                    pass

                # Samenstellen van de regel die wordt toegevoegd aan het dataframe
                new_record = pd.Series([document.name, document_type, document.documentClass, versie_nummer, status, datum,
                                        laatst_aangepast_op, project, str(deelsysteem_nummer),
                                        str(deelsysteem_naam), str(discipline), project_fase, document_eigenaar,
                                        document.fileType, link_doc, opmerking, bestand, volle_pad],
                                       index=Export_data.columns)

                # De nieuwe regel toevoegen aan het DataFrame
                Export_data = Export_data.append(new_record, ignore_index=True)

print('Done..')
# Exporteren van het DataFrame
# dmp.auto_export(Export_data)
dmp.test_export(Export_data)
