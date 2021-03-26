import re

import PyPDF2
import docx2txt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from openpyxl import load_workbook

from changing_document_properties import get_docx_properties, get_pdf_properties, get_xlsx_properties
import bestand_locaties
from file import File


# todo: Naamgeving aanpassen zodat deze correct is (camelCase en de variatie deelinstallatie/deelsysteem)
class Document(File):
    documentClass = ""
    version = ""
    status = ""

    def __init__(self, folder, filename):
        File.__init__(self, folder, filename)

        self.version = self.GetVersion()
        self.status = self.GetStatus(self.version)

    lijst_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                     '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def GetProperties(self):
        if self.path.endswith('.xlsx'):
            return get_xlsx_properties(filename=self.path)

        elif self.path.endswith('.docx'):
            return get_docx_properties(filename=self.path)

        elif self.path.endswith('.pdf'):
            return get_pdf_properties(filename=self.path)

    def GetStatus(self, versie_nummer):
        """
        De module bepaalt de status van het document aan de hand van het versie nummer van het document.
        :param versie_nummer: Het versie nummer van het document.
        :return: De status aanduiding van het document
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

    def GetDocumentOwner(self, project):
        """
        Deze module geeft de eigenaar van documenten door het referentiedocument uit te lezen. In een referentie
        document ('Overzicht_Eigenaarschap_documenten.csv') staat welke eigenaar bij welk project hoort.
        :param project: De naam van het project waartoe het document behoort.
        :return: De naam van de eigenaar van de documenten.
        """

        referentie_doc = bestand_locaties.Referentietabel_Eigenaarschap

        for e in range(referentie_doc.shape[0]):
            row_series = referentie_doc.iloc[e]
            if row_series.values[0] == project:
                eigenaar = row_series.values[1]
                return eigenaar

    def GetDINumber(self, project):
        """
        Deze module bepaalt op basis van het project welke project specifieke sbs gebruikt moet worden. Vervolgens
        wordt de onderliggende module voor het ophalen van het deelsysteem nummer toegepast en wordt het verkregen
        resultaat omgevomrd tot een string datatype. Zo is het resultaat gelijk toepastbaar in combinatie met een
        pandas DataFrame of Series.
        :param project: De naam van het project
        :return: Het deelsysteem nummer(s)
        """
        gebruik_sbs = None

        # Het project van toepassing specificeren
        if project == 'Coentunnel-tracé':
            gebruik_sbs = bestand_locaties.SBS_Coentunnel
        elif project == 'Maastunnel':
            gebruik_sbs = bestand_locaties.SBS_Maastunnel
        elif project == 'MaVa':
            gebruik_sbs = bestand_locaties.SBS_MaVa
        elif project == 'Rijnlandroute':
            gebruik_sbs = bestand_locaties.SBS_Rijnlandroute
        elif project == 'Westerscheldetunnel':
            # Todo: Gebruik van fileType lijkt me hier incorrect. Controleren!
            if self.fileType == 'RAMS':
                gebruik_sbs = bestand_locaties.SBS_Westerscheldetunnel_RAMS
            else:
                gebruik_sbs = bestand_locaties.SBS_Westerscheldetunnel

        # Toepassen van de onderliggende module
        _di_number = self.di_number(self.name + "." + self.fileType, project, gebruik_sbs)

        # Controleren of resultaat een tuple is (zo ja, omvormen naar string)
        if isinstance(_di_number, tuple):
            di_number = f'{_di_number[0]}, {_di_number[1]}'
        else:
            di_number = _di_number

        return di_number

    def GetDIName(self, deelinstallatie_nummer):
        """
        Deze module bepaalt de deelsysteem naam op basis van het deelsysteem nummer door het toepassen van een
        onderliggende module. Vervolgens wordt het verkregen resultaat omgevomrd tot een string datatype. Zo is
        het resultaat gelijk toepastbaar in combinatie met een pandas DataFrame of Series.
        :param deelinstallatie_nummer: Het deelinstallatie nummer(s).
        :return: De deelinstallatie naam/namen.
        """
        # Toepassen van de onderliggende module
        _di_name = self.di_name(deelinstallatie_nummer, sbs=bestand_locaties.SBS_Generiek)

        # Controleren of resultaat een tuple is (zo ja, omvormen naar string)
        if isinstance(_di_name, tuple):
            di_name = f'{_di_name[0]}, {_di_name[1]}'
        else:
            di_name = _di_name

        return di_name

    def SetClass(self, documenttype, referentie_doc):
        """
        Deze module geeft de klasse van het document en wijst deze toe aan een class variabele.
        :param documenttype: De map waarin het document op het centrale punt is opgeslagen.
        :param referentie_doc: Het referentiedocument van de document typen en bijbehorende documentklasse.
        :return: De document klasse
        """
        for i in range(referentie_doc.shape[0]):
            row_series = referentie_doc.iloc[i]
            if row_series.values[0] == documenttype:
                documentklasse = row_series.values[1]
                self.documentClass = documentklasse

    def path_to_hyperlink(self, project):
        """
        Deze module genereerd de url die gebruikt kan worden voor het instellen van een hyperlink naar het document
        in de cloud opslag (sharepoint) van het Centrale Opslagpunt.
        :param project: De naam van het project.
        :return: De url voor de locatie in sharepoint
        """
        # Ophalen van het eerste deel van de url (standaard)
        standaard_deel_url = bestand_locaties.Standaard_url
        # Ophalen van de benodigde informatie voor het opbouwen van de url
        naam_split = f'{self.folder}'.split('\\')
        folder_naam = naam_split[-1]
        # Informatie 'aan elkaar plakken' om de url volgorde op te bouwen
        hyperlink = f'{standaard_deel_url}/{project}/{folder_naam}/{self.name + self.fileType}'
        # Spaties vervangen door '%20'
        hyperlink = hyperlink.replace(' ', '%20')

        return hyperlink

    def GetDiscipline(self, deelinstallatie_nummer):
        """
        Deze module bepaalt de discipline (E, W, C) op basis van het deelsysteem nummer door het toepassen van een
        onderliggende module. Vervolgens wordt het verkregen resultaat omgevomrd tot een string datatype. Zo is
        het resultaat gelijk toepastbaar in combinatie met een pandas DataFrame of Series.
        :param deelinstallatie_nummer: Het deelinstallatie nummer
        :return: De discipline
        """
        # Toepassen van de onderliggende module
        _discipline = self.discipline(deelinstallatie_nummer, sbs=bestand_locaties.SBS_Generiek)

        # Controleren of resultaat een tuple is (zo ja, omvormen naar string)
        if isinstance(_discipline, tuple):
            discipline = f'{_discipline[0]}, {_discipline[1]}'
        else:
            discipline = _discipline

        return discipline

    def GetVersion(self):
        """
        Module voor het ophalen van de versie van het document. Deze module wordt uitgevoerd na het aanmaken van
        een instance en het resultaat wordt toegewezen aan een class variabele.
        :return: Het versie nummer
        """

        # todo: .xls encryptie omzeilen (verken msoffcrypto-tool package) <== wachtwoorden zijn nodig (!!!)
        path_to_file = self.path
        versie_check = False
        text = str()
        versie = str()

        # Bestandsformat checken
        if '.pdf' in path_to_file or '.docx' in path_to_file:
            # Aanpak voor pdf documenten
            if '.pdf' in path_to_file:
                # Pdf document openen
                pdf_file_obj = open(path_to_file, 'rb')
                # Pdf reader object maken
                pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
                # Aantal pagina nummers ophalen
                num_pages = pdf_reader.numPages

                # Totaal aantal pagina nummers controleren en overgaan op de specifieke aanpak van verwerken
                if num_pages == 1:
                    print(f"het aantal pagina's van het document is {num_pages}.")
                    pass
                else:
                    count = 1
                    # Pagina object aanmaken
                    page_obj = pdf_reader.getPage(count)
                    # De tekst van de pagina lezen
                    text += page_obj.extractText()

                    # controle slag op de tekst uit het document
                    if text != "":
                        text = text
                    elif text == "" and num_pages > 2:
                        count = 2
                        text = ""
                        page_obj = pdf_reader.getPage(count)
                        text += page_obj.extractText()
                    else:
                        pass

            # Aanpak voor docx documenten
            elif '.docx' in path_to_file:
                # De tekst in het document lezen
                text = docx2txt.process(path_to_file)

            else:
                text = ""

            # Indien tekst gelezen is, de desbetreffende verwerking daarvan starten
            if text != "":
                # De tekst opdelen in tokens
                tokens = word_tokenize(text)
                # Lijst leestekens definiëren
                punctuations = ['(', ')', ';', ':', '[', ']', ',']
                # Lijst stopwoorden ophalen
                stop_words = stopwords.words('dutch')
                # De tokens filteren door de leestekens en stopwoorden buiten te sluiten
                keywords = [word for word in tokens if word not in stop_words and word not in punctuations]

                # Loop specifieke variabele definiëren
                versie = str()
                versie_check = False

                for i in range(len(keywords)):
                    if keywords[i] == 'Versie' or keywords[i] == 'Revisie':
                        x = i + 1
                        if len(keywords[x]) == 1 or len(keywords[x]) == 3:  # len = 1 (versie 1), len = 3 (versie 1.2)
                            versie = keywords[x]
                            versie_check = True
                        else:
                            pass
                    # Controleren van de voorwaarde voor het breken van loop
                    if versie_check:
                        break

            # Wanneer geen versie nummer is gevonden in het document
            if not versie_check and versie == "":
                versie = "Onbekend"

            return versie

        # Bestandsformat checken
        elif '.xlsx' in path_to_file:
            # Path to file opdelen zodat de file name geïsoleerd wordt/kan worden
            splitted_path_to_file = path_to_file.split('\\')
            file_name = splitted_path_to_file[-1]

            # Geeft de titel uit de Documenten Lobby (dl) zonder '.xlsx' en hoofdletters
            title_dl = str(file_name).lower()
            title_dl = title_dl.replace('.xlsx', '')

            # Zoeken naar 'v' gevolgd door een digit in de bestandsnaam
            if re.search(r'(?<=v)\d', title_dl):
                index_v = title_dl.find('v')
                # Controleren of de naam eindigd op digit. Als dit zo is, is het het laatste getal van versie nummer
                if not re.search(r'\d$', title_dl):
                    if re.search(r'(?<=[.])\d', title_dl):
                        index_punt = title_dl.find('.')
                        versie = title_dl[index_v + 1:index_punt + 2]  # 'v2' of 'v2.0' wordt '2' of '2.0'
                        return versie
                    else:
                        versie = title_dl[index_v + 1::]  # 'v2' of 'v2.0' wordt '2' of '2.0'
                        return versie
                else:
                    versie = title_dl[index_v + 1::]  # 'v2' of 'v2.0' wordt '2' of '2.0'
                    return versie

            # Zoeken naar 'versie' gevolgd door een spatie en een digit
            elif re.search(r'(?<=versie )\d', title_dl):
                index_versie = title_dl.find('versie')
                versie = title_dl[index_versie + 7::]  # 'v2' of 'v2.0' wordt '2' of '2.0'
                return versie

            # Zoeken naar 'v' gevolgd door '.' en een digit\
            elif re.search(r'(?<=v.)\d', title_dl):
                index_v = title_dl.find('v')
                versie = title_dl[index_v + 1::]  # 'v2' of 'v2.0' wordt '2' of '2.0'
                return versie

            # Voor al het andere andere het onderstaande
            else:
                # Inladen van het document
                wb = load_workbook(path_to_file)
                # De DocumentProperties isoleren
                probs = wb.properties
                # Van de properties de titel van het document isoleren
                title = probs.title
                # Controleren of title in de properties is gegeven
                if title is not None:
                    # Zoeken naar een 'v' gevolgd door een digit
                    if re.search(r'(?<=v)\d', title):
                        # Index van de letter bepalen
                        index_v = title.find('v')
                        # Itereren vanaf de index van de letter
                        for i in range(index_v, len(title)):
                            # Notaties 'v2' of 'v2.0' eindigen beide op ' '(spatie)
                            if title[i] == ' ':
                                versie = title[index_v + 1:i]  # 'v2' of 'v2.0' wordt '2' of '2.0'
                                return versie
                    # Geen enkele opdracht is gelukt, dus ga uit van geen versie nummer ==> versie = 'onbekend'
                    else:
                        versie = 'Geen versienummer bekend'
                        return versie
                # Als title is None
                else:
                    versie = 'Geen versienummer bekend'
                    return versie

        # Bestandsformat checken
        elif '.xls' in path_to_file:
            versie = 'Onbekend'
            return versie

    def di_number(self, bestandsnaam, projectnaam, sbs=None):
        """
        Deze module geeft het generieke deelsysteem nummer van een document. Er wordt altijd een Tuple van 2 elementen
        teruggekoppeld. Wanneer er echter maar één nummer van toepassing is, is het tweede nummer '9009' - 'n.v.t.'.
        :param bestandsnaam: De titel van het bestand.
        :param projectnaam: De naam van het project.
        :param sbs: De project specifieke SBS.
        :return: Het generieke deelsysteem nummer.
        """

        raw_deelsysteem_nummer_1 = int()  # Deze was eerst als global gedefinieerd (enige verandering)
        raw_deelsysteem_nummer_2 = int()  # Deze was eerst als global gedefinieerd (enige verandering)
        lijst_deelsysteem_combinaties = []

        # Controleren of een sbs is gegeven
        if sbs is not None:

            # Itereren over de verschillende project specifieke deelsysteem nummers
            for i in range(sbs.shape[0]):
                row_series = sbs.iloc[i]

                # Controleren of MaVa het project is. Ja? Dan vraagt dit om een specifieke aanpak
                if projectnaam == 'MaVa':
                    statement_1 = (str(row_series.values[0]) and str(row_series.values[1]))
                else:
                    statement_1 = str(row_series.values[0])

                # Controleren of het project specifieke nummer in de titel voor komt
                if statement_1 in bestandsnaam:
                    # Specifieke deelsysteem nummer aan variabele toewijzen
                    raw_deelsysteem_nummer_1 = row_series.values[2]

                    # Een tweede iteratie starten voor een mogelijk tweede deelsysteem nummer
                    for z in [x for x in range(sbs.shape[0]) if x != i]:
                        row_series_2 = sbs.iloc[z]

                        if projectnaam == 'MaVa':
                            statement_2 = (str(row_series_2.values[0]) and str(row_series_2.values[1]))
                        else:
                            statement_2 = str(row_series_2.values[0])

                        # Controleren of het tweede project specifieke nummer in de titel voor komt
                        if statement_2 in bestandsnaam:
                            # Tweede specifieke deelsysteem nummer aan variabele toewijzen
                            raw_deelsysteem_nummer_2 = row_series_2.values[2]

                            # Eerste en tweede nummer zijn gelijk
                            if raw_deelsysteem_nummer_1 == raw_deelsysteem_nummer_2:
                                deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                                return deelsysteem_nummer_1

                            # todo: controleren/testen of dit nog nut heeft/van belang is
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

                            # todo: controleren/testen of dit nog nut heeft/van belang is
                            elif ([raw_deelsysteem_nummer_1, raw_deelsysteem_nummer_2] or
                                [raw_deelsysteem_nummer_2, raw_deelsysteem_nummer_1]) \
                                    in lijst_deelsysteem_combinaties:
                                pass

                            break

                        # Als er geen tweede deelsysteem nummer is geconstateerd
                        else:
                            deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                            return deelsysteem_nummer_1

            # Als deelsysteem nummer 0 is (onbekend of geen deelsysteem)
            # In de generieke sbs geldt '0 - Algemeen'
            if raw_deelsysteem_nummer_1 == 0:
                raw_deelsysteem_nummer_1 = 9009
                deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                return deelsysteem_nummer_1

        # Als er geen specifieke SBS is opgegeven
        elif sbs is None:
            """ 
            Overige projecten hebben geen referentie SBS of documenten die betrekking hebben op gehele objecten.
            Door '9009' te verwijzen, wordt er gespecificeerd dat de deelsystemen niet van toepassing zijn op
            die documenten.
            """
            raw_deelsysteem_nummer_1 = 9009
            deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
            return deelsysteem_nummer_1

    def di_name(self, deelsysteem_num, sbs=None):
        """
        Module voor het ophalen van de deelsysteem naam aan de hand van het deelsysteem nummer uit de generieke SBS.
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

    def discipline(self, deelinstallatie_nummer, sbs):
        """
        De onderliggende module voor het bepalen van de discipline. In deze module wordt er eerst gecontroleerd of
        twee deelsysteem nummer van toepassing zijn op het document. Vervolgens wordt op basis van het
        deelsysteem nummer de bijbehorende discipline opgehaald.
        :param deelinstallatie_nummer: Het generieke SBS nummer van de deelsysteem
        :param sbs: De generieke SBS
        :return: De discipline
        """
        discipline_1 = str()
        discipline_2 = str()

        # Controleren of er 1 of meerder deelsysteem nummers van toepassing zijn
        if ',' in str(deelinstallatie_nummer):
            # De twee nummers scheiden en toewijzen aan een eigen variabele
            deelinstallatie_nummer_1 = deelinstallatie_nummer[0]
            deelinstallatie_nummer_2 = deelinstallatie_nummer[1]

            for i in range(sbs.shape[0]):
                row_series = sbs.iloc[i]
                # Controleren of het eerste deelsysteem nummer gelijk is aan die in het referentie document
                if deelinstallatie_nummer_1 == int(row_series.values[2]):
                    discipline_1 = row_series.values[0]

                # Controleren of er een tweede deelsysteem nummer ongelijk is aan 'n.v.t.' etc.
                if deelinstallatie_nummer_2 != 9999 and deelinstallatie_nummer_2 != 9009 and \
                        deelinstallatie_nummer_2 != 0:

                    for x in range(sbs.shape[0]):
                        row_series = sbs.iloc[x]
                        # Controleren of het eerste deelsysteem nummer gelijk is aan die in het referentie document
                        if deelinstallatie_nummer_2 == int(row_series.values[2]):
                            discipline_2 = row_series.values[0]
                            if discipline_2 == discipline_1:
                                return discipline_1
                            else:
                                return discipline_1, discipline_2
                else:
                    return discipline_1
        # Voor wanneer en maar 1 deelsysteem nummer is gegeven
        else:
            deelinstallatie_nummer_1 = deelinstallatie_nummer

            for i in range(sbs.shape[0]):
                row_series = sbs.iloc[i]
                # Controleren of het eerste deelsysteem nummer gelijk is aan die in het referentie document
                if deelinstallatie_nummer_1 == int(row_series.values[2]):
                    discipline_1 = row_series.values[0]
                    return discipline_1
