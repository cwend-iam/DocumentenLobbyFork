#! usr/bin/env python3
import os

import pandas as pd

import bestand_locaties
import IAMDataMinePackage as dmp

from Export_dataframe import Export_data

if __name__ == '__main__':

    print('Script is gestart \n{}'.format("-"*50))

    # Onderstaande telt het aantal documenten dat gescand moet/gaat worden.
    total_doc_count = 0
    doc_count = 0
    lijst_projecten = os.listdir(bestand_locaties.Projecten_map)
    for project in lijst_projecten:
        if '(incompleet)' not in project:
            mappen = os.listdir(os.path.join(bestand_locaties.Projecten_map, project))
            for m in mappen:
                docs = os.listdir(os.path.join(bestand_locaties.Projecten_map, project, m))
                for bestand in docs:
                    total_doc_count += 1

    print(f'Te behandelen documenten: {total_doc_count}')

    # Onderstaande itereert over de bestanden in de mappen per project (Faaldefinities, FMECA en RAMS etc.)
    lijst_projecten = os.listdir(bestand_locaties.Projecten_map)

    for project in lijst_projecten:

        if '(incompleet)' not in project:

            project_map = os.path.join(bestand_locaties.Projecten_map, project)
            mappen = os.listdir(os.path.join(bestand_locaties.Projecten_map, project))

            for m in mappen:

                mappen_doctypes_per_map = os.path.join(bestand_locaties.Projecten_map, project, m)
                docs = os.listdir(os.path.join(bestand_locaties.Projecten_map, project, m))
                document_type = m  # Definitie van document type (FMECA, Faalanalyse, RAMS etc.)

                for bestand in docs:

                    # De vooruitgang printen
                    doc_count += 1
                    print(f'{doc_count} van de {total_doc_count}')
                    print('Loading...')

                    # path_to_file definiëren
                    path_to_file = os.path.join(mappen_doctypes_per_map, bestand)

                    # Het omvormen van de volledige bestandsnaam in de Titel en het documenttype/format (.pdf etc.)
                    opgedeelde_naam = bestand.split('.')
                    bestand_format = f'.{opgedeelde_naam[-1]}'
                    opgedeelde_naam.pop(-1)

                    # Controleren of er een punt in de titel staat en vervolgens daarop handelen
                    if len(opgedeelde_naam) > 1:
                        titel = f'{opgedeelde_naam[0]}.{opgedeelde_naam[1]}'
                    else:
                        titel = str(opgedeelde_naam[0])

                    # Het bepalen van de document klasse
                    document_klasse = dmp.give_document_klasse(document_type,
                                                               referentie_doc=bestand_locaties.Document_Klasse_Type)

                    # Bepalen van de deelsystemen van toepassing
                    if project == 'Coentunnel-tracé':
                        gebruik_sbs = bestand_locaties.SBS_Coentunnel
                    elif project == 'Maastunnel':
                        gebruik_sbs = bestand_locaties.SBS_Maastunnel
                    elif project == 'MaVa':
                        gebruik_sbs = bestand_locaties.SBS_MaVa
                    elif project == 'Rijnlandroute':
                        gebruik_sbs = bestand_locaties.SBS_Rijnlandroute
                    elif project == 'Westerscheldetunnel':
                        if document_type == 'RAMS':
                            gebruik_sbs = bestand_locaties.SBS_Westerscheldetunnel_RAMS
                        else:
                            gebruik_sbs = bestand_locaties.SBS_Westerscheldetunnel
                    else:
                        gebruik_sbs = None

                    deelsysteem_nummer = dmp.give_deelsysteem_nummer(bestandsnaam=bestand, projectnaam=project,
                                                                     sbs=gebruik_sbs)

                    # Ophalen van de deelsysteem naam van toepassing
                    deelsysteem_naam = dmp.give_deelsysteem_naam(deelsysteem_nummer, sbs=bestand_locaties.SBS_Generiek)

                    # Ophalen van de discipline a.h.v. de deelsystemen
                    discipline = dmp.give_discipline(deelsysteem_nummer, sbs=bestand_locaties.SBS_Generiek)
                    # todo: give-creation_date_meta aanpassen zodat pdfminer.six gebruikt wordt
                    # Ophalen van de datum waarop het document is aangemaakt
                    datum = dmp.give_creation_date_meta(path_to_file)

                    # Ophalen van de datum waarop het document voor het laatst is aangepast
                    laatst_aangepast_op = dmp.give_last_mod_date_meta(path_to_file)

                    # Ophalen van het versie nummer
                    versie_nummer = dmp.give_versie(path_to_file)

                    # Verwijzen van eigenaar aan documenten
                    document_eigenaar = dmp.give_document_eigenaar(project,
                                                                   referentie_doc=bestand_locaties.
                                                                   Referentietabel_Eigenaarschap)

                    # Ophalen van de status van de documenten
                    status = dmp.give_status(versie_nummer)

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
                    new_record = pd.Series([titel, document_type, document_klasse, versie_nummer, status, datum,
                                            laatst_aangepast_op, project, str(deelsysteem_nummer),
                                            str(deelsysteem_naam), str(discipline), project_fase, document_eigenaar,
                                            bestand_format, link_doc, opmerking, bestand, volle_pad],
                                           index=Export_data.columns)

                    # De nieuwe regel toevoegen aan het DataFrame
                    Export_data = Export_data.append(new_record, ignore_index=True)

    print('Done..')
    # Exporteren van het DataFrame
    # dmp.auto_export(Export_data)
    dmp.test_export(Export_data)
