import os
import bestand_locaties
from IAMDataMinePackage import Document

folder = 'C:\\Users\\NBais\\OneDrive - TBI Holding\\Documenten\\GitHub\\DocumentenLobby\\test'
filename = 'Differentiërende factoren.docx'

doc = Document(folder=folder, filename=filename)
print(doc.fileType)
print(doc.name)
