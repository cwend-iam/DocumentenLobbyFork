# DocumentenLobby
This repo contains the backend of the Documenten Lobby, developed for Croonwolter&dros Infra Asset Management.

# Toevoegen van nieuwe documenten
Het toevoegen van nieuwe documenten aan de centrale opslag is niet het obstakel waar men tegen aan loopt. Dit moet
echter wel op een wat gestandaardiseerde manier gebeuren om te zorgen dat het script `main.py`, verantwoordelijk voor 
het genereren van het navigatie document, zonder foutmeldingen doorlopen kan worden.

## Initialiseren
### Teams omgeving
Eén van de eerste dingen die gedaan moeten worden wanneer men voor de eerste keer een nieuw navigatie document wilt 
genereren, is het synchroniseren van de MS Team omgeving van de Documenten Lobby met de lokale harde schijf van het 
systeem waar het script op uitgevoerd gaat worden. 

Zorg dat het pad naar de Documenten Lobby op de lokale harde schijf is opgebouwd als volgt. 

`C:\Users\...\TBI Holding\Documenten Lobby - General`

### GitHub repository
De github repository moet volledig worden gekopieerd naar de lokale harde schijf. Dit kan door middel van een eigen
github account of door het downloaden van een ZIP-file met alle bestanden om deze vervolgens weer op de lokale harde 
schijf uit te pakken.

Zorg dat de map waarin alle bestanden staan de naam `DocumentenLobby` heeft (zonder spatie).

## Toevoegen
Wanneer de initialisatie afgerond is, kunnen de documenten toegevoegd worden. De rangschikking is per project, per 
document type. In het geval dat het benodigde type niet onder het project staat, moet er een map worden toegevoegd met
de naam van het document type. 

Vervolgens moet het document `res/document_type_class_overview.csv` (gezien vanaf root) worden gecontroleerd. Als het 
document type van de nieuw aangemaakte map niet aanwezig is in het bestand, dan moet deze worden toegevoegd.

## Checklist
    [ ] - MS Teams omgeving van de Documenten Lobby gesynchroniseerd met de lokale harde schijf.
    [ ] - Pad naar de Documenten Lobby op de lokale harde schijf klopt.
    [ ] - Kopie van de GitHub repository met de naam `DocumentenLobby`.
    [ ] - Staat het document type in `res/document_type_class_overview.csv`.

## Running main.py
Om `main.py` uit te kunnen voeren, moeten eerst de requirements geïnstalleerd worden. 
Open hiervoor de opdrachtprompt (te vinden door het systeem te doorzoeken op 'opdrachtprompt' of 'cmd'). Vervolgens 
de working directory te veranderen naar de map `DocumentenLobby\src` door middel van het command `cd` gevolgd door het
gehele pad naar de map (voorbeeld van het pad: `C:\Users\NBais\OneDrive - TBI Holding\Documenten\GitHub\DocumentenLobby\src`).

Voorbeeld van het command:
``
cd C:\Users\NBais\OneDrive - TBI Holding\Documenten\GitHub\DocumentenLobby\src
``

Wanneer de map veranderd is naar de map `DocumentenLobby\src` moet het onderstaande command gerund worden.

`pip3 install -r requirements.txt`

Dit command installeert de verschillende python-packages die worden gebruikt bij het uitvoeren van het script.

Zijn alle packages geïnstalleerd, dan is het tijd om het script uit te voeren door het volgende command te runnen in 
de opdrachtpromt. `python main.py`
