import bestand_locaties
import os

import docx2txt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

bestand = 'DI13 BTI Energievoorziening.docx'
bestand_map = 'RAMS'
project = 'MaVa'

path_to_file = os.path.join(bestand_locaties.Projecten_map, project, bestand_map, bestand)


text = docx2txt.process(path_to_file)

tokens = word_tokenize(text)

punctuations = ['(', ')', ';', ':', '[', ']', ',']
stop_words = stopwords.words('dutch')
keywords = [word for word in tokens if word not in stop_words and word not in punctuations]

with open('docx_tekst_test.txt', 'w', 5, 'utf-8') as text_file:
    text_file.write(text)

with open('docx_keywords_test.txt', 'w', 5, 'utf-8') as key_file:
    key_file.write(str(keywords))
