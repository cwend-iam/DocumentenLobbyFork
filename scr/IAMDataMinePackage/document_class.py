def document_class(documenttype, referentie_doc):
    """
    Geeft de klasse van het document type.
    :param documenttype: Te herleiden van de naam van de map waarin het document op het centrale punt is opgeslagen.
    :param referentie_doc: Het referentiedocument van de document typen en bijbehorende documentklasse.
    :return: De document klasse
    """
    for i in range(referentie_doc.shape[0]):
        row_series = referentie_doc.iloc[i]
        if row_series.values[0] == documenttype:
            documentklasse = row_series.values[1]
            return documentklasse
