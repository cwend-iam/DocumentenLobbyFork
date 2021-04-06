import PyPDF2
import docx2txt
import openpyxl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from creation_date_os_meta import *
from last_modification_os_meta import *


class File:
    name = ""
    path = ""
    folder = ""
    fileType = ""
    creationDate = ""
    lastModifiedDate = ""

    maanden = {'januari': '01',
               'februari': '02',
               'maart': '03',
               'april': '04',
               'mei': '05',
               'juni': '06',
               'juli': '07',
               'augustus': '08',
               'september': '09',
               'oktober': '10',
               'november': '11',
               'december': '12'}

    def __init__(self, folder, filename):
        opgedeelde_naam = filename.split('.')

        self.fileType = f'.{opgedeelde_naam[-1]}'
        opgedeelde_naam.pop(-1)

        self.name = ".".join(opgedeelde_naam)

        self.path = os.path.join(folder, filename)
        self.folder = folder

        self.lastModifiedDate = self.last_modification_file_type(folder + "\\" + filename)
        self.creationDate = self.creation_date_file_type(folder + "\\" + filename)

    def date_cleaner(self, metadatum):
        """
        Deze module vormt de notatie van de datum verkregen uit de metadata van het document, om tot de
        notatie 'dd-mm-jjjj'.
        :param metadatum: De datum string uit de metadata ==> 'D:20160722093347+02'00''
        :return: De opgeschoonde notatie 'dd-mm-jjjj'
        """
        yyyy = metadatum[2:6]
        mm = metadatum[6:8]
        dd = metadatum[8:10]
        clean_datum = dd + '-' + mm + '-' + yyyy

        return clean_datum

    def last_modification_file_type(self, path_to_file):
        """
        Deze module leest de datum waarop het bestand voor het laatst is aangepast uit de metadata.
        :param path_to_file: Het pad naar het bestand.
        :return: De datum waarop het document voor het laatst is aangepast.
        """
        # Bestansformat controleren
        if '.pdf' in path_to_file:
            # Proberen de datum uit de metadata van het document te lezen
            try:
                # Pdf object aanmaken
                pdf_bestand = open(path_to_file, 'rb')
                # Pdf reader object aanmaken
                pdf_reader = PyPDF2.PdfFileReader(pdf_bestand)
                # Datum uit de properties lezen
                raw_modified_date = pdf_reader.getDocumentInfo()['/ModDate']

                clean_modified_date = self.date_cleaner(raw_modified_date)
                return clean_modified_date
            # Als try statement een error geeft, wordt de datum uit de os metadata verkregen (minder accuraat)
            except KeyError:
                clean_modified_date = last_modification_os_meta(path_to_file)
                return clean_modified_date

        # Bestandsformat controleren
        elif '.xlsx' in path_to_file:
            # Proberen de datum uit de metadata van het document te lezen
            try:
                # Workbook object aanmaken
                wb = openpyxl.load_workbook(path_to_file, read_only=True)

                # Properties aan object toewijzen en opsplitsen
                raw_data = wb.properties.modified
                raw_data = str(raw_data).split(" ")
                # Datum uit de properties halen
                r_data = raw_data[0]
                # Dag, maand en jaar toewijzen uit de proertie notatie
                yyyy = r_data[:4]
                mm = r_data[5:7]
                dd = r_data[8:10]
                # Datum in de juiste notatie toewijzen
                clean_modified_date = dd + '-' + mm + '-' + yyyy
                return clean_modified_date
            # Als try statement een error geeft, wordt de datum uit de os metadata verkregen (minder accuraat)
            except:
                clean_creation_date = creation_date_os_meta(path_to_file)
                return clean_creation_date

        # Bestandsformat controleren
        elif '.xls' in path_to_file and '.xlsx' not in path_to_file:
            clean_modified_date = last_modification_os_meta(path_to_file)
            return clean_modified_date

        # Bestandsformat controleren
        elif '.docx' in path_to_file:
            # Tekst uitlezen
            text = docx2txt.process(path_to_file)

            # Tekst opsplitsen in tokens
            tokens = word_tokenize(text)

            # Lijst met leestekens en stopwoorden definiëren
            punctuations = ['(', ')', ';', ':', '[', ']', ',']
            stop_words = stopwords.words('dutch')
            # Leestekens en stopwoorden uit tokens filteren
            keywords = [word for word in tokens if word not in stop_words and word not in punctuations]

            for i in range(len(keywords)):
                # Gelezen woord controleren
                if keywords[i] == 'Datum':
                    n = i + 1
                    # Het opvolgende woord controleren
                    if keywords[n] != 'opgesteld' and len(keywords[n]) <= 2:
                        x = n
                        y = x + 1
                        z = y + 1

                        # Dag, maand en jaar toewijzen aan variabelen
                        dd = keywords[x]
                        mm = keywords[y]
                        yyyy = keywords[z]
                        # Controleren of de maand is uitgeschreven
                        if len(mm) > 2:
                            for key in self.maanden.keys():
                                if mm == key:
                                    # De getalnatie van de uitgeschreven maand toewijzen
                                    mm = self.maanden[key]

                        # Datum in de juiste notatie toewijzen
                        clean_modification_date = dd + '-' + mm + '-' + yyyy
                        return clean_modification_date

        # Terugkoppeling wanneer geen datum gelezen kan worden
        else:
            clean_modified_date = 'Niet in staat de metadata te lezen.'
            return clean_modified_date

    def creation_date_file_type(self, path_to_file):
        """
        Leest de datum van aanmaken van het bestand.
        :param path_to_file: Het bestand waarvan men de metadata wilt uitlezen.
        :return: De datum waarop het document voor het laatst is aangepast
        """
        # todo: datum uitlezen uit .xls bestanden
        # todo: give_creation_date_meta aanpassen zodat pdfminer.six gebruikt wordt
        # Bestansformat controleren
        if '.pdf' in path_to_file:
            # Proberen de datum uit de metadata van het document te lezen
            try:
                # Pdf object aanmaken
                pdf_bestand = open(path_to_file, 'rb')
                # Pdf reader object aanmaken
                pdf_reader = PyPDF2.PdfFileReader(pdf_bestand)
                # Datum uit de properties lezen
                raw_creation_date = pdf_reader.getDocumentInfo()['/CreationDate']

                clean_creation_date = self.date_cleaner(raw_creation_date)
                return clean_creation_date
            # Als try statement een error geeft, wordt de datum uit de os metadata verkregen (minder accuraat)
            except KeyError:
                clean_creation_date = creation_date_os_meta(path_to_file)
                return clean_creation_date

        # Bestandsformat controleren
        elif '.xlsx' in path_to_file:
            # Proberen de datum uit de metadata van het document te lezen
            try:
                # Workbook object aanmaken
                wb = openpyxl.load_workbook(path_to_file, read_only=True)
                # Properties aan object toewijzen en opsplitsen
                raw_data = wb.properties.created
                raw_data = str(raw_data).split(" ")
                # Datum uit de properties halen
                r_data = raw_data[0]
                # Dag, maand en jaar toewijzen uit de proertie notatie
                yyyy = r_data[:4]
                mm = r_data[5:7]
                dd = r_data[8:10]
                # Datum in de juiste notatie toewijzen
                clean_creation_date = dd + '-' + mm + '-' + yyyy
                return clean_creation_date
            # Als try statement een error geeft, wordt de datum uit de os metadata verkregen (minder accuraat)
            except:
                clean_creation_date = creation_date_os_meta(path_to_file)
                return clean_creation_date

        # Bestandsformat controleren
        elif '.xls' in path_to_file and '.xlsx' not in path_to_file:
            clean_creation_date = creation_date_os_meta(path_to_file)
            return clean_creation_date

        # Bestandsformat controleren
        elif '.docx' in path_to_file:
            # Tekst uitlezen
            text = docx2txt.process(path_to_file)

            # Tekst opsplitsen in tokens
            tokens = word_tokenize(text)

            # Lijst met leestekens en stopwoorden definiëren
            punctuations = ['(', ')', ';', ':', '[', ']', ',']
            stop_words = stopwords.words('dutch')
            # Leestekens en stopwoorden uit tokens filteren
            keywords = [word for word in tokens if word not in stop_words and word not in punctuations]

            for i in range(len(keywords)):
                # Gelezen woord controleren
                if keywords[i] == 'Datum':
                    n = i + 1
                    # Het opvolgende woord controleren
                    if keywords[n] == 'opgesteld':
                        x = n + 1
                        y = x + 1
                        z = y + 1

                        # Dag, maand en jaar toewijzen aan variabelen
                        dd = keywords[x]
                        mm = keywords[y]
                        yyyy = keywords[z]
                        if len(mm) > 2:
                            for key in self.maanden.keys():
                                if mm == key:
                                    # De getalnatie van de uitgeschreven maand toewijzen
                                    mm = self.maanden[key]

                        # Datum in de juiste notatie toewijzen
                        clean_creation_date = dd + '-' + mm + '-' + yyyy
                        return clean_creation_date

        # Terugkoppeling wanneer geen datum gelezen kan worden
        else:
            clean_creation_date = 'Niet in staat de metadata te lezen.'
            return clean_creation_date

