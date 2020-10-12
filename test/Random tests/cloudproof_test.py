import os
import re
import getpass


# Vast stellen van de working directory
current_dir = os.getcwd()
user = getpass.getuser()
_same_user = False

# Zorgen dat de GitHub repo de wdir wordt 
while True:
    os.chdir('..')
    if os.getcwd().endswith('DocumentenLobby'):
        break

# Definiëren van het pad naar de map 'res' (de map met de statische resources)
res_path = os.path.abspath('res')

# Controleren of eerder is bepaald wat het pad is naar de lokale locatie van het centrale opslagpunt
# van de Documenten Lobby

if 'laatst_gebruikte_account.txt' in [d for d in os.listdir(res_path)]:
    os.chdir(res_path)
    with open('laatst_gebruikte_account.txt', 'r') as u:
        text = u.read()
        if text == user:
            _same_user = True
        else:
            try:
                os.remove(os.path.join(res_path, 'centrale_opslag_path.txt'))
                os.remove(os.path.join(res_path, 'laatst_gebruikte_account.txt'))
            except FileNotFoundError as e:
                pass
    u.close()
    os.chdir('..')
    print(f'Het pad naar de centrale opslag is {res_path}')

if not _same_user:
    print(f'Lokale pad naar de centrale opslag is onbekend.')
    print(f'Het bestand wordt gezocht. Sluit uw computer niet af..')

    tbi = 'TBI Holding'
    dl = 'Document Management Systeem - General'

    user_path = os.path.join('C:\\Users', user)
    tbi_path = os.path.join(user_path, tbi)
    dl_path = os.path.join(tbi_path, dl)

    dirpaths = [directory.path for directory in os.scandir(user_path) if directory.is_dir()]

    for d in dirpaths:
        if tbi in d:  # Misschien laten zoeken a.h.v. regex i.p.v. deze statement
            print(d)
            tbi_paths = [tbiholding.path for tbiholding in os.scandir(tbi_path) if tbiholding.is_dir()]
            for t in tbi_paths:
                if dl in t:
                    print(tbi_path)
                    dl_paths = [documentenlobby.path for documentenlobby in os.scandir(dl_path) if documentenlobby.is_dir()]
                    for dl_folder in dl_paths:
                        if 'Centrale opslag' in dl_folder:
                            print(dl_folder)
                            path_to_write = dl_folder
                            break

    try:
        print('writing path to memory...')
        os.chdir('res')
        with open('centrale_opslag_path.txt', 'w', 5, 'utf-8') as file:
            file.write(path_to_write)

        with open('laatst_gebruikte_account.txt', 'w', 5, 'utf-8') as file:
            file.write(user)

    except:
        message = """De lokale locatie van de centrale opslag is niet gevonden. Controleer of de MS Teams bestanden 
                     correct zijn gesynchroniseerd met de lokale harde schijf en probeer het vervolgens opnieuw."""
        print(message)

