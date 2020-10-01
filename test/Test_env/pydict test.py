import os
import pandas as pd
import PyPDF2
import re

from nltk.text import ConcordanceIndex, Text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.text import *

from pattern.text.nl import lemma

TBI_Holding_OneDrive = 'C:\\Users\\NBais\\TBI Holding'

# Pad voor de front-end (opslag van FMECAs, RAMS etc.)
# en de back-en (opslag main script, referentiebestanden en back-ups)
Front_End_Opslag = os.path.join(TBI_Holding_OneDrive, 'Document Management Systeem - General')
Back_End_Opslag = os.path.join(TBI_Holding_OneDrive, 'Document Management Systeem - Back-end - Back-end')

# Specificatie front-end mappen
Projecten_map = os.path.join(Front_End_Opslag, 'Centrale opslag')

project = 'Coentunnel-tracé'
bestand_map = 'RAMS'

desktop = 'C:\\Users\\NBais\\Desktop'

bestand = 'RAMS analyse Di 48 - Toeritdoseerinstallatie VTTI Versie A.pdf'
path_to_file = os.path.join(desktop, bestand)

pdf_file_obj = open(path_to_file, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
num_pages = pdf_reader.numPages

punctuations = ['(', ')', ';', ':', '[', ']', ',', '...']
stop_words = stopwords.words('dutch')

page_obj1 = pdf_reader.getPage(9)
text1 = page_obj1.extractText()
tokens1 = word_tokenize(text1)
keywords1 = [word.lower() for word in tokens1 if word not in stop_words and word not in punctuations]

for i in range(len(keywords1)):
    print(keywords1[i])
