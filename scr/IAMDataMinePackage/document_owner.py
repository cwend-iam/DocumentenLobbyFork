def document_owner(project_naam, referentie_doc):
    """
    Functie die aan de hand van een referentie CSV-bestand ('Overzicht_Eigenaarschap_documenten.csv') op basis van
    de projectnaam de eigenaar van de documenten toewijst.
    :param project_naam: De naam van het project waar het document onder valt.
    :param referentie_doc: Het referentiedocument van de document typen en bijbehorende documentklasse.
    :return: De naam van de eigenaar van het bestand.
    """

    for e in range(referentie_doc.shape[0]):
        row_series = referentie_doc.iloc[e]
        if row_series.values[0] == project_naam:
            eigenaar = row_series.values[1]
            return eigenaar
