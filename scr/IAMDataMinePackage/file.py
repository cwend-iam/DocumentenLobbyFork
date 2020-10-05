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
        Deze functie schoont de datum uit de metadata op tot de notatie 'dd-mm-jjjj'
        :param metadatum: de volledige string zoals verkregen uit de metadata 'D:20160722093347+02'00''
        :return: De opgeschoonde notatie 'dd-mm-jjjj'
        """
        yyyy = metadatum[2:6]
        mm = metadatum[6:8]
        dd = metadatum[8:10]
        clean_datum = dd + '-' + mm + '-' + yyyy

        return clean_datum

    def last_modification_file_type(self, path_to_file):
        """
        Leest de datum waarop het bestand voor het laatst is aangepast uit de metadata.
        :param path_to_file: Het bestand waarvan men de metadata wilt uitlezen.
        :return: De datum waarop het document voor het laatst is aangepast
        """

        if '.pdf' in path_to_file:
            try:
                pdf_bestand = open(path_to_file, 'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf_bestand)

                raw_modified_date = pdf_reader.getDocumentInfo()['/ModDate']

                clean_modified_date = self.date_cleaner(raw_modified_date)
                return clean_modified_date
            except KeyError:
                clean_modified_date = last_modification_os_meta(path_to_file)
                return clean_modified_date

        elif '.xlsx' in path_to_file:
            wb = openpyxl.load_workbook(path_to_file, read_only=True)

            raw_data = wb.properties.modified
            raw_data = str(raw_data).split(" ")

            r_data = raw_data[0]

            yyyy = r_data[:4]
            mm = r_data[5:7]
            dd = r_data[8:10]

            clean_modified_date = dd + '-' + mm + '-' + yyyy
            return clean_modified_date

        elif '.xls' in path_to_file and '.xlsx' not in path_to_file:
            clean_modified_date = last_modification_os_meta(path_to_file)
            return clean_modified_date

        elif '.docx' in path_to_file:
            text = docx2txt.process(path_to_file)

            tokens = word_tokenize(text)

            punctuations = ['(', ')', ';', ':', '[', ']', ',']
            stop_words = stopwords.words('dutch')
            keywords = [word for word in tokens if word not in stop_words and word not in punctuations]
            for i in range(len(keywords)):
                if keywords[i] == 'Datum':
                    n = i + 1
                    if keywords[n] != 'opgesteld' and len(keywords[n]) <= 2:
                        x = n
                        y = x + 1
                        z = y + 1

                        dd = keywords[x]
                        mm = keywords[y]
                        yyyy = keywords[z]
                        if len(mm) > 2:
                            for key in self.maanden.keys():
                                if mm == key:
                                    mm = self.maanden[key]
                        clean_modification_date = dd + '-' + mm + '-' + yyyy
                        return clean_modification_date

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

        if '.pdf' in path_to_file:
            try:
                pdf_bestand = open(path_to_file, 'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf_bestand)

                raw_creation_date = pdf_reader.getDocumentInfo()['/CreationDate']

                clean_creation_date = self.date_cleaner(raw_creation_date)
                return clean_creation_date
            except KeyError:
                clean_creation_date = creation_date_os_meta(path_to_file)
                return clean_creation_date

        elif '.xlsx' in path_to_file:
            wb = openpyxl.load_workbook(path_to_file, read_only=True)

            raw_data = wb.properties.created
            raw_data = str(raw_data).split(" ")

            r_data = raw_data[0]

            yyyy = r_data[:4]
            mm = r_data[5:7]
            dd = r_data[8:10]

            clean_creation_date = dd + '-' + mm + '-' + yyyy
            return clean_creation_date

        elif '.xls' in path_to_file and '.xlsx' not in path_to_file:
            clean_creation_date = creation_date_os_meta(path_to_file)
            return clean_creation_date

        elif '.docx' in path_to_file:
            text = docx2txt.process(path_to_file)

            tokens = word_tokenize(text)

            punctuations = ['(', ')', ';', ':', '[', ']', ',']
            stop_words = stopwords.words('dutch')
            keywords = [word for word in tokens if word not in stop_words and word not in punctuations]
            for i in range(len(keywords)):
                if keywords[i] == 'Datum':
                    n = i + 1
                    if keywords[n] == 'opgesteld':
                        x = n + 1
                        y = x + 1
                        z = y + 1

                        dd = keywords[x]
                        mm = keywords[y]
                        yyyy = keywords[z]
                        if len(mm) > 2:
                            for key in self.maanden.keys():
                                if mm == key:
                                    mm = self.maanden[key]

                        clean_creation_date = dd + '-' + mm + '-' + yyyy
                        return clean_creation_date

        else:
            clean_creation_date = 'Niet in staat de metadata te lezen.'
            return clean_creation_date
