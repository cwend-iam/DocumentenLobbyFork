import re
import PyPDF2
import docx2txt

from openpyxl import load_workbook

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def document_version(path_to_file):
    """
    Functie die het versienummer van het document ophaalt. De functie kijkt welk van de documentformats in het pad
    aanwezig zijn. Op basis daarvan wordt het gepaste proces voor extractie van de versienummers toegapst.
    :param path_to_file: Het pad naar het bestand waarvan men het versienummer wilt uitlezen.
    :return: Het versienummer van het document.
    """
    # todo: .xls encryptie omzeilen (verken msoffcrypto-tool package) <== wachtwoorden zijn nodig (!!!)

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
