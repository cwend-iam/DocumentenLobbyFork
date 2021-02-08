import os
from IAMDataMinePackage import changing_document_properties

folder = 'C:\\Users\\NBais\\OneDrive - TBI Holding\\Documenten\\GitHub\\DocumentenLobby\\test\\Test_env\\doc'
list_doc = os.listdir(folder)

for file in list_doc:
    if file.endswith('.pdf'):
        changing_document_properties.change_properties(filename=os.path.join(folder, file),
                                                       title='test2',
                                                       subject='test2',
                                                       comments='This is a test2')
