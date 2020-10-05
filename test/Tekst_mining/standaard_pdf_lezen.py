import bestand_locaties
import os

import PyPDF2

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

bestand = 'RAMS analyse Di 61 - CCTV camerasysteem en DBOS Versie A.pdf'
bestand_map = 'RAMS'
project = 'Coentunnel-tracé'

path_to_file = os.path.join(bestand_locaties.Projecten_map, project, bestand_map, bestand)


pdf_file_obj = open(path_to_file, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
num_pages = pdf_reader.numPages

text = str()
count = 0
while count < num_pages:
    page_obj = pdf_reader.getPage(count)
    text += page_obj.extractText()
    count += 1


tokens = word_tokenize(text)

punctuations = ['(', ')', ';', ':', '[', ']', ',']
stop_words = stopwords.words('dutch')
keywords = [word for word in tokens if word not in stop_words and word not in punctuations]

with open('pdf_tekst_test.txt', 'w', 5, 'utf-8') as text_file:
    text_file.write(text)

with open('pdf_keywords_test.txt', 'w', 5, 'utf-8') as key_file:
    key_file.write(str(keywords))
