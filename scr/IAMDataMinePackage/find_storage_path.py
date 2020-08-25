import os
import getpass


def find_storage_path():
    # Definiëren van user en interne variabele
    user = getpass.getuser()
    _same_user = False
    _del_files = False
    # Zorgen dat de GitHub repo de wdir wordt
    while True:
        if os.getcwd().endswith('DocumentenLobby'):
            break
        else:
            os.chdir('..')

    # Definiëren van het pad naar de map 'res' (de map met de statische resources)
    res_path = os.path.abspath('res')

    # Controleren of eerder is bepaald wat het pad is naar de lokale locatie van het centrale opslagpunt
    # van de Documenten Lobby bij dezelfde gebruiker (m.a.w. of zelfde pad gebruikt kan worden).
    if 'laatst_gebruikte_account.txt' in [d for d in os.listdir(res_path)]:
        os.chdir(res_path)
        with open('laatst_gebruikte_account.txt', 'r') as u:
            text = u.read()
            if text == user:
                _same_user = True
            else:
                _del_files = True
        u.close()
        os.chdir('..')

    # Het verwijderen van de files (dit moet buiten 'with open():' om foutmelding te voorkomen
    if _del_files:
        try:
            os.remove(os.path.join(res_path, 'centrale_opslag_path.txt'))
            os.remove(os.path.join(res_path, 'laatst_gebruikte_account.txt'))
        except FileNotFoundError:
            pass

    # Het proces voor wanneer een nieuw pad gezocht moet worden.
    if not _same_user:
        print(f'Lokale pad naar de centrale opslag is onbekend.')
        print(f'Het bestand wordt gezocht. Sluit uw computer niet af..')

        # Definiëren van de namen van de mappen waar de opslag zich bevind na synch met lokale schijf
        tbi = 'TBI Holding'
        dl = 'Document Management Systeem - General'

        # Samenstellen van de paden
        user_path = os.path.join('C:\\Users', user)
        tbi_path = os.path.join(user_path, tbi)
        dl_path = os.path.join(tbi_path, dl)

        # Definiëren van de verschillende mappen in user_path
        dirpaths = [directory.path for directory in os.scandir(user_path) if directory.is_dir()]
        # Loop over paden in dirpaths
        for d in dirpaths:
            # Controleren of 'TBI Holding' in pad aanwezig is
            if tbi in d:  # Misschien laten zoeken a.h.v. regex i.p.v. deze statement
                # Definiëren van de verschillende mappen in tbi_path
                tbi_paths = [tbiholding.path for tbiholding in os.scandir(tbi_path) if tbiholding.is_dir()]
                # Loop over paden in tbi_paths
                for t in tbi_paths:
                    # Controleren of 'Document Management Systeem - General' in pad aanwezig is
                    if dl in t:
                        # Definiëren van de verschillende mappen in dl_path
                        dl_paths = [documentenlobby.path for documentenlobby in os.scandir(dl_path) if
                                    documentenlobby.is_dir()]
                        # Loop over paden in dl_paths
                        for dl_folder in dl_paths:
                            # Controleren of 'Centrale Opslag in pad aanwezig is
                            if 'Centrale opslag' in dl_folder:
                                path_to_write = dl_folder
                                break

        # Proberen het pad naar een .txt bestand te schrijven
        try:
            print('Oplaan van het pad.')
            # working dir veranderen naar ./res (hier moeten de docs opgeslagen worden
            os.chdir('res')

            # Schrijven van het pad naar .txt
            with open('centrale_opslag_path.txt', 'w', 5, 'utf-8') as file:
                file.write(path_to_write)
            file.close()  # Sluiten voor de netheid

            # Schrijven van de account naam naar .txt
            with open('laatst_gebruikte_account.txt', 'w', 5, 'utf-8') as file:
                file.write(user)
            file.close()  # Sluiten voor de netheid

            print('Pad is opgeslagen')
            return path_to_write

        # Bij error wordt het volgende teruggekoppeld
        except:
            message = """De lokale locatie van de centrale opslag is niet gevonden. Controleer of de MS Teams bestanden 
                         correct zijn gesynchroniseerd met de lokale harde schijf en probeer het vervolgens opnieuw."""
            print(message)
            return None
