from bestand_locaties import Standaard_url


def make_hyperlink_url(project_naam, map_naam, bestand_naam):
    """
    Functie die de naam van het project, de map, en het bestand combineert met een standaard stuk van de url
    waarmee de bestanden via de browser geopend kunnen worden. Voor communicatie met sharepoint moeten de spaties in de
    url gesubstitueerd worden door '%20'.
    :param project_naam: de naam van het project.
    :param map_naam: de naam van de map.
    :param bestand_naam: de naam van het bestand met daarbij ook het bestandformat (.xlsx/.pfd etc.).
    :return: het volledige pad naar het bestand en tevens de url van de hyperlink voor het openen in de browser.
    """
    standaard_deel_url = Standaard_url
    hyperlink = f'{standaard_deel_url}/{project_naam}/{map_naam}/{bestand_naam}'
    hyperlink = hyperlink.replace(' ', '%20')
    return hyperlink
