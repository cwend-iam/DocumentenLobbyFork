def date_cleaner(metadatum):
    """
    Deze functie schoont de datum uit de metadata op tot de notatie 'dd-mm-jjjj'
    :param metadatum: de volledige string zoals verkregen uit de metadata 'D:20160722093347+02'00''
    :return: De opgeschoonde notatie 'dd-mm-jjjj'
    """
    yyyy = metadatum[2:6]
    mm = metadatum[6:8]
    dd = metadatum[8:10]
    clean_datum = dd + '-' + mm + '-' + yyyy

    return clean_datum
