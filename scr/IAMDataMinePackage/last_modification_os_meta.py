#! usr/bin/env python3
import os
from datetime import datetime


def last_modification_os_meta(path_to_file):
    """
    Geeft de datum waarop het document voor het laatst is aangepast.
    :param path_to_file: Het pad naar het bestand dat men wilt uitlezen.
    :return: De datum van de laatste aanpassing.

    DEZE FUNCTIE KAN WORDEN TOEGEVOEGD VOOR ALLE BESTANDTYPEN, MAAR ENKEL WANNEER HET
    HET CENTRALE OPSLAGPUNT WORDT GEBRUIKT.
    """
    unix_mtimestamp = os.path.getctime(path_to_file)
    utc_mts = datetime.utcfromtimestamp(unix_mtimestamp).strftime('%H:%M:%S %d-%m-%Y').split(" ")
    clean_date = utc_mts[1]
    return clean_date
