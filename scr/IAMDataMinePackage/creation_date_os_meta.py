import os
from datetime import datetime

# todo: give_creation_date_meta aanpassen zodat pdfminer.six gebruikt wordt
def creation_date_os_meta(path_to_file):
    """
    Geeft de datum waarop het document is gecreëerd.
    :param path_to_file: Het pad naar het bestand dat men wilt uitlezen.
    :return: De datum van het aanmakenvan het document.

    DEZE FUNCTIE KAN WORDEN TOEGEVOEGD VOOR ALLE BESTANDTYPEN, MAAR ENKEL WANNEER HET
    HET CENTRALE OPSLAGPUNT WORDT GEBRUIKT.
    """
    unix_ctimestamp = os.path.getctime(path_to_file)
    utc_cts = datetime.utcfromtimestamp(unix_ctimestamp).strftime('%H:%M:%S %d-%m-%Y').split(" ")
    clean_date = utc_cts[1]
    return clean_date
