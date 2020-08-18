lijst_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                 '1', '2', '3', '4', '5', '6', '7', '8', '9']


def document_status(versie_nummer):
    """
    Deze functie bepaalt aan de hand van het versie nummer de status van het document.
    :param versie_nummer: Versie nummer van het document verkregen door de functie 'give_versie'.
    :return: De status aanduiding van het document.
    """

    if '.' in versie_nummer:
        if '.0' in versie_nummer:
            status_aanduiding = 'DO/UO'
            return status_aanduiding
        else:
            status_aanduiding = 'Concept'
            return status_aanduiding

    elif versie_nummer in [f'{x}' for x in lijst_letters]:
        status_aanduiding = 'DO/UO'
        return status_aanduiding

    elif versie_nummer == 'Onbekend':
        status_aanduiding = 'Onbekend'
        return status_aanduiding
