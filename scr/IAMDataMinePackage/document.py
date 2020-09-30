import os
import re
import PyPDF2
import docx2txt

import bestand_locaties

from openpyxl import load_workbook

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Document:
    name = ""
    path = ""
    folder = ""
    fileType = ""
    documentClass = ""

    def __init__(self, folder, filename):
        opgedeelde_naam = filename.split('.')

        self.fileType = f'.{opgedeelde_naam[-1]}'
        opgedeelde_naam.pop(-1)

        self.name = ".".join(opgedeelde_naam)

        self.path = os.path.join(folder, filename)
        self.folder = folder

    lijst_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                     '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def document_status(self, versie_nummer):
        """
        Deze functie bepaalt aan de hand van het versie nummer de status van het document.
        :param versie_nummer: Versie nummer van het document verkregen door de functie 'give_versie'.
        :return: De status aanduiding van het document.
        """

        if '.' in versie_nummer:
            if '.0' in versie_nummer:
                status_aanduiding = 'DO/UO'
                return status_aanduiding
            else:
                status_aanduiding = 'Concept'
                return status_aanduiding

        elif versie_nummer in [f'{x}' for x in self.lijst_letters]:
            status_aanduiding = 'DO/UO'
            return status_aanduiding

        elif versie_nummer == 'Onbekend':
            status_aanduiding = 'Onbekend'
            return status_aanduiding

    def document_owner(self, project_naam, referentie_doc):
        """
        Functie die aan de hand van een referentie CSV-bestand ('Overzicht_Eigenaarschap_documenten.csv') op basis van
        de projectnaam de eigenaar van de documenten toewijst.
        :param project_naam: De naam van het project waar het document onder valt.
        :param referentie_doc: Het referentiedocument van de document typen en bijbehorende documentklasse.
        :return: De naam van de eigenaar van het bestand.
        """

        for e in range(referentie_doc.shape[0]):
            row_series = referentie_doc.iloc[e]
            if row_series.values[0] == project_naam:
                eigenaar = row_series.values[1]
                return eigenaar

    def GetDI(self, project):
        gebruik_sbs = None

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
            if self.fileType == 'RAMS':
                gebruik_sbs = bestand_locaties.SBS_Westerscheldetunnel_RAMS
            else:
                gebruik_sbs = bestand_locaties.SBS_Westerscheldetunnel
        
        return self.di_number(self.name + "." + self.fileType, project, gebruik_sbs)

    def SetClass(self, documenttype, referentie_doc):
        """
        Geeft de klasse van het document type.
        :param documenttype: Te herleiden van de naam van de map waarin het document op het centrale punt is opgeslagen.
        :param referentie_doc: Het referentiedocument van de document typen en bijbehorende documentklasse.
        :return: De document klasse
        """
        for i in range(referentie_doc.shape[0]):
            row_series = referentie_doc.iloc[i]
            if row_series.values[0] == documenttype:
                documentklasse = row_series.values[1]
                self.documentClass = documentklasse

    def document_version(self):
        """
        Functie die het versienummer van het document ophaalt. De functie kijkt welk van de documentformats in het pad
        aanwezig zijn. Op basis daarvan wordt het gepaste proces voor extractie van de versienummers toegapst.
        :param path_to_file: Het pad naar het bestand waarvan men het versienummer wilt uitlezen.
        :return: Het versienummer van het document.
        """
        # todo: .xls encryptie omzeilen (verken msoffcrypto-tool package) <== wachtwoorden zijn nodig (!!!)
        path_to_file = self.path
        versie_check = False
        text = str()
        versie = str()

        if '.pdf' in path_to_file or '.docx' in path_to_file:
            if '.pdf' in path_to_file:
                pdf_file_obj = open(path_to_file, 'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
                num_pages = pdf_reader.numPages
                if num_pages == 1:
                    print(f"het aantal pagina's van het document is {num_pages}.")
                    pass
                else:
                    count = 1
                    page_obj = pdf_reader.getPage(count)
                    text += page_obj.extractText()

                    if text != "":
                        text = text
                    elif text == "" and num_pages > 2:
                        count = 2
                        text = ""
                        page_obj = pdf_reader.getPage(count)
                        text += page_obj.extractText()
                    else:
                        pass

            elif '.docx' in path_to_file:
                text = docx2txt.process(path_to_file)

            else:
                text = ""

            if text != "":

                tokens = word_tokenize(text)

                punctuations = ['(', ')', ';', ':', '[', ']', ',']
                stop_words = stopwords.words('dutch')
                keywords = [word for word in tokens if word not in stop_words and word not in punctuations]

                versie = str()
                versie_check = False
                for i in range(len(keywords)):
                    if keywords[i] == 'Versie' or keywords[i] == 'Revisie':
                        x = i + 1
                        if len(keywords[x]) == 1 or len(keywords[x]) == 3:
                            versie = keywords[x]
                            versie_check = True
                        else:
                            pass

                    if versie_check:
                        break

            if not versie_check and versie == "":
                versie = "Onbekend"

            return versie

        elif '.xlsx' in path_to_file:
            # Path to file opdelen zodat de file name geïsoleerd wordt/kan worden
            splitted_path_to_file = path_to_file.split('\\')
            file_name = splitted_path_to_file[-1]
            # Geeft de titel uit de Documenten Lobby (dl) zonder '.xlsx' en hoofdletters
            title_dl = str(file_name).lower()
            title_dl = title_dl.replace('.xlsx', '')

            # Zoeken naar 'v' gevolgd door digit in bestandsnaam
            if re.search(r'(?<=v)\d', title_dl):
                index_v = title_dl.find('v')
                # Controleren of de naam eindigd op digit. Als dit zo is, is het het laatste getal van versie nummer
                if not re.search(r'\d$', title_dl):
                    if re.search(r'(?<=.)\d', title_dl):
                        index_punt = title_dl.find('.')
                        versie = title_dl[index_v + 1:index_punt + 2]  # 'v2' of 'v2.0' ==> '2' of '2.0'
                        return versie
                else:
                    versie = title_dl[index_v + 1::]  # 'v2' of 'v2.0' ==> '2' of '2.0'
                    return versie
            # Zoeken naar 'versie' gevolgd door spatie en digit
            elif re.search(r'(?<=versie )\d', title_dl):
                index_versie = title_dl.find('versie')
                versie = title_dl[index_versie + 7::]  # 'v2' of 'v2.0' ==> '2' of '2.0'
                return versie
            # Zoeken naar 'v' gevolgd door '.' en een digit\
            elif re.search(r'(?<=v.)\d', title_dl):
                index_v = title_dl.find('v')
                versie = title_dl[index_v + 1::]  # 'v2' of 'v2.0' ==> '2' of '2.0'
                return versie
            # Voor al het andere het onderstaande
            else:
                # Inladen van het document
                wb = load_workbook(path_to_file)
                # De DocumentProperties isoleren
                probs = wb.properties
                # Van de properties de titel van het document isoleren
                title = probs.title
                # Zoeken naar een 'v' gevolgd door een digit
                if re.search(r'(?<=v)\d', title):
                    # Index van de letter bepalen
                    index_v = title.find('v')
                    # Itereren vanaf de index van de letter
                    for i in range(index_v, len(title)):
                        # Notaties 'v2' of 'v2.0' eindigen beide op ' '(spatie)
                        if title[i] == ' ':
                            versie = title[index_v + 1:i]  # 'v2' of 'v2.0' ==> '2' of '2.0'
                            return versie
                # Geen enkele opdracht is gelukt, dus ga uit van geen versie nummer ==> versie = 'onbekend'
                else:
                    versie = 'Geen versienummer bekend'
                    return versie

        elif '.xls' in path_to_file:
            versie = 'Onbekend'
            return versie

    def di_number(bestandsnaam, projectnaam, sbs):  # Bestandsnaam is de titel uit het DataFrame.
        """
        Vertaalt het deelsysteem nummer van de projecten naar het deelsysteemnummer uit de generieke SBS.
        (!!) Wanneer geen tweede deelsysteem wordt gevonden wordt een waarde '9009' meegegeven. Dit Indiceert dat er geen
        tweede deelsysteem van toepassing is.
        :param bestandsnaam: Dit is de Titel van de bestanden.
        :param projectnaam: De projectnaam
        :param sbs: Het referentiedocument van de project specifieke SBS vertaalt naar de generieke SBS
        :return: Het deelsysteem nummer uit de generieke SBS
        """

        raw_deelsysteem_nummer_1 = int()  # Deze was eerst als global gedefinieerd (enige verandering)
        raw_deelsysteem_nummer_2 = int()  # Deze was eerst als global gedefinieerd (enige verandering)
        lijst_deelsysteem_combinaties = []

        if sbs is not None:

            for i in range(sbs.shape[0]):
                row_series = sbs.iloc[i]

                if projectnaam == 'MaVa':
                    statement_1 = (str(row_series.values[0]) and str(row_series.values[1]))
                else:
                    statement_1 = str(row_series.values[0])

                if statement_1 in bestandsnaam:
                    raw_deelsysteem_nummer_1 = row_series.values[2]

                    for z in [x for x in range(sbs.shape[0]) if x != i]:
                        row_series_2 = sbs.iloc[z]

                        if projectnaam == 'MaVa':
                            statement_2 = (str(row_series_2.values[0]) and str(row_series_2.values[1]))
                        else:
                            statement_2 = str(row_series_2.values[0])

                        if statement_2 in bestandsnaam:
                            raw_deelsysteem_nummer_2 = row_series_2.values[2]

                            if raw_deelsysteem_nummer_1 == raw_deelsysteem_nummer_2:
                                deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                                return deelsysteem_nummer_1

                            elif ([raw_deelsysteem_nummer_1, raw_deelsysteem_nummer_2] or
                                [raw_deelsysteem_nummer_2, raw_deelsysteem_nummer_1]) \
                                    not in lijst_deelsysteem_combinaties:
                                lijst_deelsysteem_combinaties.append([raw_deelsysteem_nummer_1, raw_deelsysteem_nummer_2])
                                lijst_deelsysteem_combinaties.append([raw_deelsysteem_nummer_2, raw_deelsysteem_nummer_1])
                                deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                                deelsysteem_nummer_2 = raw_deelsysteem_nummer_2

                                if deelsysteem_nummer_1 > deelsysteem_nummer_2:
                                    return deelsysteem_nummer_2, deelsysteem_nummer_1
                                elif deelsysteem_nummer_1 < deelsysteem_nummer_2:
                                    return deelsysteem_nummer_1, deelsysteem_nummer_2

                            elif ([raw_deelsysteem_nummer_1, raw_deelsysteem_nummer_2] or
                                [raw_deelsysteem_nummer_2, raw_deelsysteem_nummer_1]) \
                                    in lijst_deelsysteem_combinaties:
                                pass

                            break

                        else:
                            deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                            return deelsysteem_nummer_1

            if raw_deelsysteem_nummer_1 == 0:
                raw_deelsysteem_nummer_1 = 9009
                deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                return deelsysteem_nummer_1

        elif sbs is None:
            """ 
            Overige projecten hebben geen referentie SBS of documenten die betrekking hebben op gehele objecten
            door '9009' te verwijzen, wordt er gespecificeerd dat de deelsystemen niet van toepassing zijn op
            die documenten.
            """
            raw_deelsysteem_nummer_1 = 9009
            deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
            return deelsysteem_nummer_1

    def di_name(deelsysteem_num, sbs):
        """
        Functie voor het ophalen van de naam van de deelsysteem aan de hand van het nummer uit de generieke SBS.
        :param deelsysteem_num: Het generieke SBS nummer van de desbetreffende deelsysteem
        :param sbs: De verwijzing naar de generieke sbs die wordt gehanteert
        :return: De naam van de deelsysteem uit de generieke SBS
        """

        if ',' in str(deelsysteem_num):
            deelsysteem_num_1 = deelsysteem_num[0]
            deelsysteem_num_2 = deelsysteem_num[1]

            for g in range(sbs.shape[0]):
                generiek_sbs_row_series = sbs.iloc[g]

                if deelsysteem_num_1 == generiek_sbs_row_series.values[2]:
                    deelsysteem_naam_1 = generiek_sbs_row_series.values[1]

                    for h in [x for x in range(sbs.shape[0]) if x != g]:
                        generiek_sbs_row_series_2 = sbs.iloc[h]

                        if deelsysteem_num_2 == generiek_sbs_row_series_2.values[2]:
                            deelsysteem_naam_2 = generiek_sbs_row_series_2.values[1]
                            return deelsysteem_naam_1, deelsysteem_naam_2

        else:
            for g in range(sbs.shape[0]):
                generiek_sbs_row_series = sbs.iloc[g]
                if deelsysteem_num == generiek_sbs_row_series.values[2]:
                    deelsysteem_naam_1 = generiek_sbs_row_series.values[1]
                    return deelsysteem_naam_1