import PyPDF2
import openpyxl
import docx2txt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from .date_cleaner import *
from .creation_date_os_meta import *

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


def creation_date_file_type(path_to_file):
    """
    Leest de datum van aanmaken van het bestand.
    :param path_to_file: Het bestand waarvan men de metadata wilt uitlezen.
    :return: De datum waarop het document voor het laatst is aangepast
    """
    # todo: datum uitlezen uit .xls bestanden

    if '.pdf' in path_to_file:
        try:
            pdf_bestand = open(path_to_file, 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_bestand)

            raw_creation_date = pdf_reader.getDocumentInfo()['/CreationDate']

            clean_creation_date = date_cleaner(raw_creation_date)
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
                        for key in maanden.keys():
                            if mm == key:
                                mm = maanden[key]

                    clean_creation_date = dd + '-' + mm + '-' + yyyy
                    return clean_creation_date

    else:
        clean_creation_date = 'Niet in staat de metadata te lezen.'
        return clean_creation_date