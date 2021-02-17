import os
from IAMDataMinePackage import Document

folder = 'C:\\Users\\NBais\\OneDrive - TBI Holding\\Documenten\\GitHub\\DocumentenLobby\\test\\Test_env\\doc'
list_doc = os.listdir(folder)

for file in list_doc:
    doc = Document(folder=folder, filename=file)
    props = doc.GetProperties()
    print(doc.name)
    print(props)
