def di_number(bestandsnaam, projectnaam, sbs):  # Bestandsnaam is de titel uit het DataFrame.
    """
    Vertaalt het deelsysteem nummer van de projecten naar het deelsysteemnummer uit de generieke SBS.
    (!!) Wanneer geen tweede deelsysteem wordt gevonden wordt een waarde '9009' meegegeven. Dit Indiceert dat er geen
    tweede deelsysteem van toepassing is.
    :param bestandsnaam: Dit is de Titel van de bestanden.
    :param projectnaam: De projectnaam
    :param sbs: Het referentiedocument van de project specifieke SBS vertaalt naar de generieke SBS
    :return: Het deelsysteem nummer uit de generieke SBS
    """

    raw_deelsysteem_nummer_1 = int()  # Deze was eerst als global gedefinieerd (enige verandering)
    raw_deelsysteem_nummer_2 = int()  # Deze was eerst als global gedefinieerd (enige verandering)
    lijst_deelsysteem_combinaties = []

    if sbs is not None:

        for i in range(sbs.shape[0]):
            row_series = sbs.iloc[i]

            if projectnaam == 'MaVa':
                statement_1 = (str(row_series.values[0]) and str(row_series.values[1]))
            else:
                statement_1 = str(row_series.values[0])

            if statement_1 in bestandsnaam:
                raw_deelsysteem_nummer_1 = row_series.values[2]

                for z in [x for x in range(sbs.shape[0]) if x != i]:
                    row_series_2 = sbs.iloc[z]

                    if projectnaam == 'MaVa':
                        statement_2 = (str(row_series_2.values[0]) and str(row_series_2.values[1]))
                    else:
                        statement_2 = str(row_series_2.values[0])

                    if statement_2 in bestandsnaam:
                        raw_deelsysteem_nummer_2 = row_series_2.values[2]

                        if raw_deelsysteem_nummer_1 == raw_deelsysteem_nummer_2:
                            deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                            return deelsysteem_nummer_1

                        elif ([raw_deelsysteem_nummer_1, raw_deelsysteem_nummer_2] or
                              [raw_deelsysteem_nummer_2, raw_deelsysteem_nummer_1]) \
                                not in lijst_deelsysteem_combinaties:
                            lijst_deelsysteem_combinaties.append([raw_deelsysteem_nummer_1, raw_deelsysteem_nummer_2])
                            lijst_deelsysteem_combinaties.append([raw_deelsysteem_nummer_2, raw_deelsysteem_nummer_1])
                            deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                            deelsysteem_nummer_2 = raw_deelsysteem_nummer_2

                            if deelsysteem_nummer_1 > deelsysteem_nummer_2:
                                return deelsysteem_nummer_2, deelsysteem_nummer_1
                            elif deelsysteem_nummer_1 < deelsysteem_nummer_2:
                                return deelsysteem_nummer_1, deelsysteem_nummer_2

                        elif ([raw_deelsysteem_nummer_1, raw_deelsysteem_nummer_2] or
                              [raw_deelsysteem_nummer_2, raw_deelsysteem_nummer_1]) \
                                in lijst_deelsysteem_combinaties:
                            pass

                        break

                    else:
                        deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
                        return deelsysteem_nummer_1

        if raw_deelsysteem_nummer_1 == 0:
            raw_deelsysteem_nummer_1 = 9009
            deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
            return deelsysteem_nummer_1

    elif sbs is None:
        """ 
        Overige projecten hebben geen referentie SBS of documenten die betrekking hebben op gehele objecten
        door '9009' te verwijzen, wordt er gespecificeerd dat de deelsystemen niet van toepassing zijn op
        die documenten.
        """
        raw_deelsysteem_nummer_1 = 9009
        deelsysteem_nummer_1 = raw_deelsysteem_nummer_1
        return deelsysteem_nummer_1
